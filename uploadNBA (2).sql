-- Databricks notebook source
-- MAGIC %py
-- MAGIC dbutils.fs.rm("dbfs:/user/hive/warehouse/college_delta/",True)
-- MAGIC dbutils.fs.rm("dbfs:/user/hive/warehouse/euro_delta/",True)
-- MAGIC dbutils.fs.rm("dbfs:/user/hive/warehouse/nba_delta/",True)

-- COMMAND ----------

-- MAGIC %py
-- MAGIC dbutils.fs.rm("dbfs:/user/hive/warehouse/dim_europlayer/",True)
-- MAGIC dbutils.fs.rm("dbfs:/user/hive/warehouse/dim_nbaplayer/",True)
-- MAGIC dbutils.fs.rm("dbfs:/user/hive/warehouse/dim_collegeplayer/",True)

-- COMMAND ----------

-- MAGIC %fs 
-- MAGIC 
-- MAGIC ls dbfs:/user/hive/warehouse/

-- COMMAND ----------

create database if not exists zaleskig8;

--Upload Euro Player and NBA Player CSVs

drop table if EXISTS nbaPlayers;
drop table if EXISTS euroPlayers;

create table IF NOT EXISTS nbaPlayers USING csv OPTIONS
(path "dbfs:/FileStore/shared_uploads/zaleskig8@students.rowan.edu/NBA_Players.csv", header "true", mode "permissive",inferSchema "true");

create table IF NOT EXISTS euroPlayers USING csv OPTIONS
(path "dbfs:/FileStore/shared_uploads/zaleskig8@students.rowan.edu/mergedEuro_CSV.csv", header "true", mode "permissive",inferSchema "true");

-- COMMAND ----------

describe nbaPlayers;

-- COMMAND ----------

select count(*) from nbaPlayers;

-- COMMAND ----------

select * from nbaPlayers limit 10;

-- COMMAND ----------

describe euroPlayers;

-- COMMAND ----------

select count(*) from euroPlayers;

-- COMMAND ----------

select * from euroPlayers limit 10; 

-- COMMAND ----------

---Upload College Players CSV from bz2 format

drop table IF EXISTS collegePlayers;

create table IF NOT EXISTS collegePlayers USING csv OPTIONS
(path "dbfs:/FileStore/shared_uploads/zaleskig8@students.rowan.edu/mergedCBB_Players_csv.bz2", header "true", mode "permissive",inferSchema "true");

-- COMMAND ----------

describe collegePlayers;

-- COMMAND ----------

select count(*) from collegePlayers;

-- COMMAND ----------

select * from collegePlayers limit 10;

-- COMMAND ----------

DROP TABLE IF EXISTS nba_delta;

--Create NBA Delta table
CREATE TABLE IF NOT EXISTS nba_delta USING delta as
select
*
from nbaPlayers;

-- COMMAND ----------

describe nba_delta;

-- COMMAND ----------

select count(*) from nba_delta;

-- COMMAND ----------

select * from nba_delta limit 10;

-- COMMAND ----------

DROP TABLE IF EXISTS euro_delta;

--Create Euro Delta table
CREATE TABLE IF NOT EXISTS euro_delta USING delta as
select
*
from euroPlayers;

-- COMMAND ----------

describe euro_delta;

-- COMMAND ----------

select count(*) from euro_delta;

-- COMMAND ----------

select * from euro_delta limit 10;

-- COMMAND ----------

DROP TABLE IF EXISTS college_delta;

--Create College Parquet table
CREATE TABLE IF NOT EXISTS college_delta USING delta as
select
*
from collegePlayers;

-- COMMAND ----------

describe college_delta;

-- COMMAND ----------

select count(*) from college_delta;

-- COMMAND ----------

select * from college_delta limit 10;

-- COMMAND ----------

--Create NBA Player Dimension Table
DROP TABLE IF EXISTS dim_nbaPlayer;

CREATE TABLE IF NOT EXISTS dim_nbaPlayer USING delta as
select
    ID,FIRST_NAME,LAST_NAME,BIRTHDATE,HEIGHT,WEIGHT,POSITION,TEAM_NAME,TEAM_CITY,FROM_YEAR,
    TO_YEAR,DRAFT_YEAR,PTS,REB,AST
from
    nba_delta;

-- COMMAND ----------

describe dim_nbaPlayer;

-- COMMAND ----------

select count(*) from dim_nbaPlayer;

-- COMMAND ----------

select * from dim_nbaPlayer limit 10;

-- COMMAND ----------

--Create Euro Player Dimension Table
DROP TABLE IF EXISTS dim_euroPlayer;

CREATE TABLE IF NOT EXISTS dim_euroPlayer USING delta as
select
    euro_id,player_name,Season,Team,G,Pts,Avg,2FG,3FG,FT,Reb,St,As,Bl
from
    euro_delta;

-- COMMAND ----------

describe dim_euroPlayer;

-- COMMAND ----------

select count(*) from dim_euroPlayer;

-- COMMAND ----------

select * from dim_euroPlayer limit 25;

-- COMMAND ----------

--Create NCAA College Player Dimension Table
DROP TABLE IF EXISTS dim_CollegePlayer;

CREATE TABLE IF NOT EXISTS dim_CollegePlayer USING delta as
select
   ncaa_id,player_id,Year,points,assists,steals,blocks,free_throws,height,weight,team_abbreviation,
   total_rebounds,games_played
from
    college_delta;

-- COMMAND ----------

describe dim_CollegePlayer;

-- COMMAND ----------

select count(*) from dim_CollegePlayer;

-- COMMAND ----------

select * from dim_CollegePlayer limit 25;

-- COMMAND ----------

--Create Star Fact Table 
--Player who played in any of the 3 leagues

DROP TABLE IF EXISTS fact_Player;

CREATE TABLE IF NOT EXISTS fact_Player USING delta as
    (select ncaa_id as ID, player_id AS NAME, Year as FROM_DATE, YEAR as TO_DATE, height as HEIGHT, weight as  WEIGHT, team_abbreviation as TEAM_NAME, points AS POINTS, total_rebounds AS REBOUNDS, assists AS ASSISTS, steals AS STEALS, blocks AS BLOCKS,  games_played AS GAMES, free_throws AS FT, null AS 2FG, null as 3FG FROM dim_collegePlayer 
   UNION

   select euro_id as ID, player_name as NAME, Season as FROM_DATE, Season AS TO_DATE, null as HEIGHT, null as WEIGHT, Team as TEAM_NAME, Avg As POINTS, Reb as REBOUNDS, As AS ASSISTS, St AS STEALS, Bl AS BLOCKS, null AS GAMES, FT, 2FG, 3FG from dim_euroPlayer 
   
   UNION 

   select ID, concat(FIRST_NAME," ",LAST_NAME) as NAME, FROM_YEAR as FROM_DATE, TO_YEAR AS TO_DATE, HEIGHT, WEIGHT, concat(TEAM_CITY," ",TEAM_NAME) AS TEAM_NAME,PTS AS POINTS,REB AS REBOUNDS,AST AS ASSISTS,null AS STEALS,null AS BLOCKS, null AS GAMES, null as FT, null as 2FG,null as 3FG from dim_nbaPlayer);


-- COMMAND ----------

describe fact_Player;

-- COMMAND ----------

select count(*) from fact_Player;

-- COMMAND ----------

select * from fact_Player LIMIT 50;

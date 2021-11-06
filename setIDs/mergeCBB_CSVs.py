import csv
import os
import pandas as pd
import numpy 

mergedCBB = "/home/zaleskig8/dataWarehousing/basketball/setIDs/mergedCBB_Players.csv"
mergedEuro = "/home/zaleskig8/dataWarehousing/basketball/setIDs/mergedEuro_Players.csv"

euroID = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID.csv"
cbbID  = "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaID.csv"

euroCBB = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID_cbb.csv" 
cbbEuroAndAll = "/home/zaleskig8/dataWarehousing/basketball/setIDs/cbbID_noNBA.csv" 

cbbpath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaCSVs/"
europath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroLeagueCSVs/"

euroOnly = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID_Only.csv"

datapath  = "/home/zaleskig8/dataWarehousing/basketball/setIDs/Player_Attributes.csv"
nba_players = pd.read_csv(datapath)
nba_playerIDs = nba_players.ID

cbbIDs = pd.read_csv(cbbID)
collegeIDs = cbbIDs['ncaaID']
collegePlayers = cbbIDs['FileName']

euroIDs = pd.read_csv(euroID)
eLeagueIDs = euroIDs['euroID']
euroPlayers = euroIDs['FileName']

cbbToEuroIDs = pd.read_csv(cbbEuroAndAll)
CEL_IDs = cbbToEuroIDs['ncaaID']
CEL_PLAYERS = cbbToEuroIDs['FileName']

EL_IDs = pd.read_csv(euroCBB)
EL_PIDs = EL_IDs['euroID']
EL_PLAYERS = EL_IDs['FileName']

ELO_IDs = pd.read_csv(euroOnly)
ELO_PIDs = ELO_IDs['euroID']
ELO_PLAYERS = ELO_IDs['FileName']

# Merge College Basketball Players
with open(mergedCBB,'w') as mergeCBBCSV:
    writeHeader = True
    mergeCBBCSV = csv.writer(mergeCBBCSV)
    for player in os.listdir(cbbpath):
        print(player)
        playerCSV = csv.reader(open(cbbpath + player,'r'))
        collegePlayer = list(filter(lambda x: player == x, collegePlayers))
        collegePlayer += list(filter(lambda x: player == x, CEL_PLAYERS))
    
        try:
            playerCollegeID = collegeIDs[collegePlayers == collegePlayer[0]].values.item(0)
        except IndexError:
            try:
                playerCollegeID = CEL_IDs[CEL_PLAYERS == collegePlayer[0]].values.item(0)
            except IndexError:
                print("College ID not found for: " + player + " - Skipping")
                continue
    
        try:
            playerEuroID = eLeagueIDs[eLeagueIDs == playerCollegeID].values.item(0)
        except IndexError:
            try:
                playerEuroID = EL_PIDs[EL_PIDs == playerCollegeID].values.item(0)
            except IndexError:
                try:
                    playerEuroID = ELO_PIDs[ELO_PIDs == playerCollegeID].values.item(0)
                except IndexError:
                    playerEuroID = -999
    
        try:
            playerNBAID = nba_playerIDs[nba_playerIDs == playerCollegeID].values.item(0)
        except IndexError:
            playerNBAID = -999
        
        header = 0
        for row in playerCSV:
            if writeHeader:
                row.append("nba_id")
                row.append("euro_id")
                row.append("ncaa_id")
                mergeCBBCSV.writerow(row)
                writeHeader = False
                continue
            elif header == 0:
                header += 1
                continue
            row.append(playerNBAID)
            row.append(playerEuroID)
            row.append(playerCollegeID)
            mergeCBBCSV.writerow(row)
mergeCBBCSV.close()


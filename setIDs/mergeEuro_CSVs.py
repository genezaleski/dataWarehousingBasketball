import csv
import os
import pandas as pd
import numpy 

mergedEuro = "/home/zaleskig8/dataWarehousing/basketball/setIDs/mergedEuro_Players.csv"

euroID = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID.csv"
cbbID  = "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaID.csv"

euroCBB = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID_cbb.csv" 
cbbEuroAndAll = "/home/zaleskig8/dataWarehousing/basketball/setIDs/cbbID_noNBA.csv" 

cbbpath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaCSVs/"
europath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroLeagueCSVs/"

euroOnly = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID_Only.csv"

euroWebIDs= "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/playerIDs.csv"

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
with open(mergedEuro,'w') as mergeEuroCSV:
    writeHeader = True
    mergeEuroCSV = csv.writer(mergeEuroCSV)

    webIDs = pd.read_csv(euroWebIDs,header=None)
    playerNameList = webIDs[1]
    webIDs = webIDs[0]

    for player in os.listdir(europath):
        print(player)
        playerCSV = csv.reader(open(europath + player,'r'))
        euroPlayer = list(filter(lambda x: player == x, euroPlayers))
        euroPlayer += list(filter(lambda x: player == x, EL_PLAYERS))
        euroPlayer += list(filter(lambda x: player == x, ELO_PLAYERS))
    
        try:
            playerEuroID = eLeagueIDs[euroPlayers == euroPlayer[0]].values.item(0)
        except IndexError:
            try:
                playerEuroID = EL_PIDs[EL_PLAYERS == euroPlayer[0]].values.item(0)
            except IndexError:
                try:
                    playerEuroID = ELO_PIDs[ELO_PLAYERS == euroPlayer[0]].values.item(0)
                except IndexError:
                    print("Euro ID not found for: " + player + " - Skipping")
                    continue

        try:
            playerCollegeID = collegeIDs[collegeIDs == playerEuroID].values.item(0)
        except IndexError:
            try:
                playerCollegeID = CEL_IDs[CEL_IDs == playerEuroID].values.item(0)
            except IndexError:
                playerCollegeID = -999

        try:
            playerNBAID = nba_playerIDs[nba_playerIDs == playerEuroID].values.item(0)
        except IndexError:
            playerNBAID = -999

        playerName = ""
        for ii in range(len(webIDs)):
            pid = webIDs[ii]
            if pid in player:
                playerNameStr = playerNameList[ii].replace(" ","_")
                if playerNameStr in player:
                    playerName = playerNameList[ii]
                    break

        header = 0
        for row in playerCSV:
            if writeHeader:
                row.append("nba_id")
                row.append("euro_id")
                row.append("ncaa_id")
                row.append("player_name")
                mergeEuroCSV.writerow(row)
                writeHeader = False
                continue
            elif header == 0:
                header += 1
                continue
            row.append(playerNBAID)
            row.append(playerEuroID)
            row.append(playerCollegeID)
            row.append(playerName)
            mergeEuroCSV.writerow(row)
mergeEuroCSV.close()


import csv
import os
import pandas as pd
import numpy 

euroID = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID.csv"
cbbID  = "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaID.csv"

euroCBB = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID_cbb.csv" 
cbbEuroAndAll = "/home/zaleskig8/dataWarehousing/basketball/setIDs/cbbID_noNBA.csv" 

cbbpath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaCSVs/"
europath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroLeagueCSVs/"

finalEuro = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID_Only.csv"

euroCSV = os.listdir(europath)
cbbCSV = os.listdir(cbbpath)

#Write college ID for all CBB

cbbIDs = pd.read_csv(cbbID)
collegeIDs = cbbIDs['ncaaID']

euroIDs = pd.read_csv(euroID)
eLeagueIDs = euroIDs['euroID']
euroPlayers = euroIDs['FileName']

CELIDs = pd.read_csv(cbbEuroAndAll)
CEL_ID = CELIDs['ncaaID']

EL_IDs = pd.read_csv(euroCBB)
EL_PIDs = EL_IDs['euroID']
EL_PLAYERS = EL_IDs['FileName']

newIDs = []

with open(finalEuro,'w') as euroOut:
    euroOut = csv.writer(euroOut)
    euroOut.writerow(['FileName','euroID'])
    for player in os.listdir(europath):
        euroPlayer_1 = list(filter(lambda x: player in x, euroPlayers))
        euroPlayer_2 =  list(filter(lambda x: player in x, EL_PLAYERS))
        #Euro Player already has an NBA id and College ID
        if len(euroPlayer_1) > 0 or len(euroPlayer_2) > 0:
            continue
    
        print(player)

        playerID = 0
        while playerID == 0:
            playerID = numpy.random.randint(1,10000000) 
            if playerID in collegeIDs or playerID in eLeagueIDs or playerID in CEL_ID or playerID in EL_PIDs or playerID in newIDs:
                playerID = 0
        newIDs.append(playerID)

        euroOut.writerow([player,playerID])

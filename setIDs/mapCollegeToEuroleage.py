import csv
import os
import pandas as pd
import numpy 

euroID = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID.csv"
cbbID  = "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaID.csv"

outEuro = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID_cbb.csv" 
outCBB = "/home/zaleskig8/dataWarehousing/basketball/setIDs/cbbID_noNBA.csv" 

cbbpath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaCSVs/"
europath= "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroLeagueCSVs/"

euroCSV = os.listdir(europath)
cbbCSV = os.listdir(cbbpath)

#Write college ID for all CBB

cbbIDs = pd.read_csv(cbbID)
collegeIDs = cbbIDs['ncaaID']
collegePlayers = cbbIDs['FileName']

euroIDs = pd.read_csv(euroID)
eLeagueIDs = euroIDs['euroID']
euroPlayers = euroIDs['FileName']

newIDs = []

with open(outEuro,'w') as euroOut, open(outCBB,'w') as cbbOut:
    euroOut = csv.writer(euroOut)
    euroOut.writerow(['FileName','euroID'])
    cbbOut = csv.writer(cbbOut)
    cbbOut.writerow(['FileName','ncaaID'])
    for player in os.listdir(cbbpath):
        print(player)
        collegePlayer = list(filter(lambda x: player in x, collegePlayers))
        #College Player already has an NBA id
        if len(collegePlayer) > 0:
            continue
        euroName = player.strip().split("-")
        euroName = euroName[1].upper() + "_" + euroName[0].upper()
        euroPlayer = list(filter(lambda x: euroName in x, euroPlayers))
        #Euro Player already has an NBA id
        if len(euroPlayer) > 0:
            continue
    
        collegeEuroMap = list(filter(lambda x: euroName in x, euroCSV))

        playerID = 0
        while playerID == 0:
            playerID = numpy.random.randint(1,10000000) 
            if playerID in collegeIDs or playerID in eLeagueIDs or playerID in newIDs:
                playerID = 0
        newIDs.append(playerID)

        if len(collegeEuroMap) > 0:
            if len(collegeEuroMap) > 1:
                cbbplayer = csv.reader(open(cbbpath + player,'r'))
                szn = []
                header = 0
                for rr in cbbplayer:
                    if header == 0:
                        header += 1
                        continue
                    year = rr[0].strip().replace("'","")
                    if year.isdigit():
                        szn.append(year[0] + year[1] + year[-2] + year[-1])
                matchFound = False
                for match in collegeEuroMap:
                    if matchFound:
                        break
                    header = 0
                    euroFile = csv.reader(open(europath + match,"r"))
                    euro_szn = []
                    for rr in euroFile:
                        if header == 0:
                            header += 1
                            continue
                        year = rr[0].strip().replace("'","")
                        if year.isdigit():
                            euro_szn.append(year[0] + year[1] + year[-2] + year[-1])
                    overlap = [value for value in szn if szn in euro_szn]
                    if len(overlap) > 0:
                        print("Mapped: " + player + " -> " + match)
                        print(szn)
                        print(euro_szn)
                        euroOut.writerow([match,playerID])
                        cbbOut.writerow([player,playerID])
                        matchFound = True 
                        break
            else:
                # Found one mapping, write ID 
                euroOut.writerow([collegeEuroMap[0],playerID])
                cbbOut.writerow([player,playerID])
        else:
            # No mapping, write college player ID 
            cbbOut.writerow([player,playerID])

#Try to find existing mapping then map that to any Euroleague Players

#Write euro ID for remaining unmapped euroleague players

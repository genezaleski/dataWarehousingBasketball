import csv
import pandas as pd
import os

datapath  = "/home/zaleskig8/dataWarehousing/basketball/setIDs/Player_Attributes.csv"

europath  = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroLeagueCSVs/"
cbbpath   = "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaCSVs/"

euroID    = "/home/zaleskig8/dataWarehousing/basketball/setIDs/euroID.csv"
collegeID = "/home/zaleskig8/dataWarehousing/basketball/setIDs/ncaaID.csv"

euroWebIDs= "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/playerIDs.csv"

euro_players = os.listdir(europath)
cbb_players = os.listdir(cbbpath)

with open(euroID,"w") as outEuro, open(collegeID,"w") as outNCAA:
    nba_players = pd.read_csv(datapath)
    EWIDs = pd.read_csv(euroWebIDs)
    nba_ids = nba_players.ID
    college_IDs = []
    euro_IDs = []
    euroID_FILE = csv.writer(outEuro)
    euroID_FILE.writerow(["FileName","euroID"])
    ncaaID_FILE = csv.writer(outNCAA)
    ncaaID_FILE.writerow(["FileName","ncaaID"])
    for index,row in nba_players.iterrows():
        collegeName = row['PLAYER_SLUG']
        euroName = row['LAST_NAME'].upper() + "_" + row['FIRST_NAME'].upper()
        nbaID = row['ID']
        collegeMatches = list(filter(lambda x: collegeName in x, cbb_players)) 
        euroMatches = list(filter(lambda x: euroName in x, euro_players)) 
        print(collegeName)
        if len(collegeMatches) > 1:
            draftYear = row['DRAFT_YEAR']
            matchFound = False
            for match in collegeMatches:
                if matchFound:
                    break
                dashes = match.rfind("-")
                truncatedMatch = match[0:dashes]
                if truncatedMatch == collegeName:
                    ncaaCSV = csv.reader(open(cbbpath + match,"r"))
                    header = 0
                    prev = ""
                    lastCollegeSeason = ""
                    for rr in ncaaCSV:
                        if header == 0:
                            header += 1
                            continue
                        year = rr[0].strip()
                        year = year[0] + year[1] + year[-2] + year[-1]
                        if not year.isdigit():
                            lastCollegeSeason = prev
                        prev = year
                    if draftYear == lastCollegeSeason:
                        print("Mapped: " + collegeName + " to " + match)
                        print("NBA: " + draftYear + " -> CBB: " + lastCollegeSeason)
                        college_IDs.append(nbaID)
                        ncaaID_FILE.writerow([match,nbaID])
                        matchFound = True
                        break
        elif len(collegeMatches) == 1:
            college_IDs.append(nbaID)
            ncaaID_FILE.writerow([collegeMatches[0],nbaID])

        # Find Euro League matching players
        if len(euroMatches) > 1: 
            draftYear = row['DRAFT_YEAR']
            matchFound = False
            for match in euroMatches:
                if matchFound:
                    break
                euroCSV = csv.reader(open(europath + match))
                header = 0
                year = ""
                years= []
                for rr in euroCSV:
                    if header == 0:
                        header += 1
                        continue
                    year = rr[0].strip().replace("'","")
                    year = year[0] + year[1] + year[-2] + year[-1]
                    years.append(int(year))
                if len(years) > 0:
                    nbaSeasons = range(row['FROM_YEAR'],row['TO_YEAR'])
                    overlap = [value for value in years if value in nbaSeasons]
                    if len(overlap) > 0:
                        euro_IDs.append(nbaID)
                        euroID_FILE.writerow([match,nbaID])
                        matchFound = True
                        print("EURO Mapped " + collegeName + " to " + match)
                        print(years)
                        print(nbaSeasons)
                        break

        elif len(euroMatches) == 1:
            euro_IDs.append(nbaID)
            euroID_FILE.writerow([euroMatches[0],nbaID])

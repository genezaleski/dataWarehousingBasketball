import re
import string
import requests
import csv
import os
from csv import reader
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

def pullPlayer(playerCode,headers):

    requestPath = 'https://www.euroleague.net/competition/players/showplayer?pcode=' + playerCode + '&#!careerstats'

    req = requests.get(requestPath)

    soup = BeautifulSoup(req.text, 'html5lib')

    #print(soup.prettify())

    playerIMG = soup.body.find('div',attrs={'class':'player-img'})

    euroleague = soup.body.findAll('div',attrs={'class':'PlayerPhaseStatisticsContainer table-responsive-container'})

    career = soup.body.find('div',attrs={'class':'FieldContainer careerFieldContainer'})

    
    euroleague = soup.body.findAll('tr',attrs={'class':'PlayerGridRow'})
    try:
        career = career.findAll('tr',attrs={'class':'negro'})
        noCareer = 0
    except AttributeError:
        noCareer = 1

    headers = list(filter(removeItem,headers))
    headers[6] = "2P%"
    headers[8] = "3P%"
    headers[10] = "FT%"

    allStats = {name: [] for name in headers}

    toSkip = 1
    for statRow in euroleague:
        if toSkip <= 2:
            toSkip += 1
            continue
        idx = 0
        for block in statRow:
            if isinstance(block,Tag):
                try:
                    entry = block.findAll("a")[0].string
                except IndexError:
                    entry = block.string
                if entry == None:
                    entry = "N/A"
                try:
                    allStats[headers[idx]].append(entry)
                except IndexError:
                    continue
                idx += 1

    if noCareer == 1:
        return allStats

    try:
        for statRow in career:
            idx = 0
            for block in statRow:
                if isinstance(block,Tag):
                    try:
                        entry = block.findAll("a")[0].string
                    except IndexError:
                        entry = block.string
                    if u'\xa0' in entry:
                        entry = entry.replace(u"\xa0",u"")
                    if entry == None:
                        entry = "N/A"
                    try:
                        allStats[headers[idx]].append(entry)
                    except IndexError:
                        continue
                    idx += 1
    except TypeError as e:
        return allStats

    return allStats


def createHeaders():
    playerCode = '009866'

    requestPath = 'https://www.euroleague.net/competition/players/showplayer?pcode=' + playerCode + '&#!careerstats'

    req = requests.get(requestPath)

    soup = BeautifulSoup(req.text, 'html5lib')

    #print(soup.prettify())

    #playerIMG = soup.body.find('div',attrs={'class':'player-img'})

    euroleague = soup.body.findAll('div',attrs={'class':'PlayerPhaseStatisticsContainer table-responsive-container'})

    career = soup.body.find('div',attrs={'class':'FieldContainer careerFieldContainer'})

    headers = career.findAll('tr',attrs={'class':'blanco'})

    for h in headers:
        csvHeaders = h.text.split('\n')

    for ii in range(1,len(csvHeaders)):
        csvHeaders[ii] = csvHeaders[ii].strip()

    csvHeaders = list(filter(None,csvHeaders))
    return csvHeaders


def writePlayerCSV(playerStats,playerString):
    outpath = "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/playerCSVs/" + playerString 
    outfile = open(outpath,"w")
    writer = csv.writer(outfile)
    for key, value in playerStats.items():
        writer.writerow([key,value])

    outfile.close()


def removeItem(obj):
    if obj == "M-A":
        return False 
    return True


if __name__ == "__main__":
    headers = createHeaders()
    with open("/home/zaleskig8/dataWarehousing/basketball/getEuroleague/playerIDs.csv","r") as playerIDs:
        csv_reader = reader(playerIDs)
        for row in csv_reader:
            playerID = row[0]
            playerName = row[1]
            print(playerName)
            savepath = playerName+str(playerID)+".csv"
            if os.path.isfile("/home/zaleskig8/dataWarehousing/basketball/getEuroleague/playerCSVs/" + savepath):
                print("Exists!")
                continue
            playerStats = pullPlayer(playerID,headers)
            writePlayerCSV(playerStats,savepath)

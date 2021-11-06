from sportsreference.ncaab import roster
from os.path import exists
import pandas as pd

#https://sportsipy.readthedocs.io/en/latest/ncaab.html#module-sportsipy.ncaab.player

#player = roster.Player('carsen-edwards-1')

playerIDList = open('/home/zaleskig8/dataWarehousing/basketball/getCBB/playerIDsSorted.txt','r')
playerIDs = playerIDList.readlines()
playerIDList.close()

for ID in playerIDs:
    requestString = ID.split('/')[-1].split('.html')[0]
    savePath = "/home/zaleskig8/dataWarehousing/basketball/getCBB/playerCSVs/" + requestString + ".csv"
    if exists(savePath):
        continue
    print(requestString)
    player = roster.Player(requestString)
    player = player.dataframe
    player.index.rename("Year",inplace=True)
    player.to_csv(savePath)

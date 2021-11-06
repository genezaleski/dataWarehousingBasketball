#This script changes the names of the separated sql scripts.
import os

datapath = '/home/zaleskig8/dataWarehousing/basketball/'

for filename in os.listdir(datapath):
    if "nba" in filename:
        newName = "nba" + filename[-2:] + ".sql"
        os.rename((datapath + filename),(datapath + newName))

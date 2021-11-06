import os

basepath = "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/playerCSVs/"
outpath = "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/cleanCSVs/"
scriptPath = "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/transposeCSV.py" 

for file in os.listdir(basepath):
    print(file)
    csv = basepath + file
    outCSV = outpath + file
    outCSV = outCSV.replace(" ","_")
    os.system('python ' + scriptPath + ' "' + csv + '" > ' + outCSV)
    os.system("sed -i 's/[][]//g' " + outCSV)
    os.system('sed -i "s/\\"//g" ' + outCSV)
    os.system("sed -i '/^$/d' " + outCSV)

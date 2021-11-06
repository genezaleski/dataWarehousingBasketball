import csv
import os

def formatAllData(datapath,outpath):
    columns = ["Season", "Team", "G", "Pts", "Avg", "2FG", "2P%", "3FG", "3P%", "FT", "FT%", "Reb", "St", "As", "Bl"]
    ints = ["G", "Pts","Reb", "St", "As", "Bl"]
    floats = ["Avg", "2P%", "3P%", "FT%"]

    header = 0
    with open(datapath,"r") as csv_file, open(outpath,"w") as outfile:
        csv_reader = csv.reader(csv_file,delimiter=",")
        writer = csv.writer(outfile)
        for row in csv_reader:
            if header == 0:
                writer.writerow(row)
                header += 1
                continue
            idx = 0
            toWrite = True
            for col in row:
                formattedCol = col.strip().replace("'","")
                try:
                    colName = columns[idx]
                    #print(colName + " " + formattedCol)
                except IndexError:
                    continue
                if idx == 0 and not any([char.isdigit() for char in formattedCol]):
                    #Removing rows with empty season field
                    toWrite = False
                    break
                elif colName in ints:
                    if not "/" in formattedCol:
                        try:
                            formattedCol = int(formattedCol)
                            row[idx] = formattedCol
                        except ValueError:
                            toWrite = False
                    else:
                        toWrite = False
                elif colName in floats:
                    if not "/" in formattedCol:
                        try:
                            formattedCol = float(formattedCol)
                            row[idx] = formattedCol
                        except ValueError:
                            toWrite = False
                    else:
                        toWrite = False
                idx += 1
            if toWrite:
                writer.writerow(row)

if __name__ == "__main__":

    csvpath = "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/cleanCSVs/"
    outdir = "/home/zaleskig8/dataWarehousing/basketball/getEuroleague/cleanFormattedCSV/"
    for cc in os.listdir(csvpath):
        print(cc)
        inpath = csvpath + cc
        outpath = outdir + cc
        formatAllData(inpath,outpath)

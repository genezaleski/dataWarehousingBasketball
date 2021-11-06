import numpy as np
import os
import sys

datapath = sys.argv[1]

with open(datapath) as file:
    lis = [x.replace('\n','').split(',') for x in file]

for x in zip(*lis):
    for y in x:
        if 'N/A' in y:
            break
        if "\\t" in y:
            y = y.replace("\\t","")
        print(y + ', ', end="")
    print('')

#sed 's/[][]//g' test.csv > test2.csv
#sed 's/\"//g' test2.csv > test3.csv


#!/usr/bin/env python
import time
import sqlite3
import csv

start = time.clock()

for inn in range(0, 1):
    f = open("t20MLPred"+`(inn+1)`+"LiveBase.csv","rb")
    reader = csv.reader(f, delimiter=',')
    sumWins = {0:0, 10:0, 20:0, 30:0, 40:0, 50:0, 60:0, 70:0, 80:0, 90:0, 100:0}
    countNum = {0:0, 10:0, 20:0, 30:0, 40:0, 50:0, 60:0, 70:0, 80:0, 90:0, 100:0}
    for row in reader:
        if row[0] == "Id": continue
        if row[3] == "None": continue
        if int(row[1]) == (inn + 1):
            odds = float(row[3])
            roundOdds = round(odds, -1)
            results = float(row[4])
            sumWins[int(roundOdds)] += results
            countNum[int(roundOdds)] += 1
    f.close()

    fd = open('oddCheckMLT20Live.csv','a')
    oddsDiffWeightedSum = 0
    countCases = 0
    for pct in sorted(sumWins):
        if countNum[pct] == 0: continue
        actualOdds = float(sumWins[pct])*100/float(countNum[pct])
        if pct == 0:
            oddsDiff = actualOdds - 2.5
        elif pct == 100:
            oddsDiff = actualOdds - 97.5
        else:
            oddsDiff = actualOdds - pct
        oddsDiffWeightedSum += abs(oddsDiff * countNum[pct])
        countCases += countNum[pct]
        print `(inn + 1)` + " " + `pct` + " " + `sumWins[pct]` + " " + `countNum[pct]` + " " + `actualOdds` + " " + `oddsDiff`
        fd.write(`(inn + 1)` + "," + `pct` + "," + `sumWins[pct]` + "," + `countNum[pct]` + "," + `actualOdds` + "," + `oddsDiff` + "\n")
    fd.write(`(inn + 1)` + ",,,,," + `(float(oddsDiffWeightedSum)/float(countCases))` + "\n")
    fd.write("\n")
    fd.close()

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

#!/usr/bin/env python
import time
import sqlite3
import csv

start = time.clock()

for inn in range(0, 4):
    f = open("testOdds2.csv","rb")
    reader = csv.reader(f, delimiter=',')
    sumWins = {0:0, 10:0, 20:0, 30:0, 40:0, 50:0, 60:0, 70:0, 80:0, 90:0, 100:0}
    winCountNum = {0:0, 10:0, 20:0, 30:0, 40:0, 50:0, 60:0, 70:0, 80:0, 90:0, 100:0}
    sumDraws = {0:0, 10:0, 20:0, 30:0, 40:0, 50:0, 60:0, 70:0, 80:0, 90:0, 100:0}
    drawCountNum = {0:0, 10:0, 20:0, 30:0, 40:0, 50:0, 60:0, 70:0, 80:0, 90:0, 100:0}
    for row in reader:
        if row[4] == "None" or row[5] == "None": continue
        if int(row[0]) < 1600: continue
        if int(row[1]) == (inn + 1):
            winOdds = float(row[4])
            drawOdds = float(row[5])
            roundWinOdds = round(winOdds, -1)
            roundDrawOdds = round(drawOdds, -1)
            winCount = float(row[6])/2 if int(row[6]) == 2 else 0.0
            drawCount = float(row[6]) if int(row[6]) == 1 else 0.0
            sumWins[int(roundWinOdds)] += winCount
            sumDraws[int(roundDrawOdds)] += drawCount
            winCountNum[int(roundWinOdds)] += 1
            drawCountNum[int(roundDrawOdds)] += 1
    f.close()

    fd = open('oddCheckTest2.csv','a')
    winOddsDiffWeightedSum = 0
    drawOddsDiffWeightedSum = 0
    winCountCases = 0
    drawCountCases = 0
    for pct in sorted(sumWins):
        if winCountNum[pct] == 0 or drawCountNum[pct] == 0: continue
        actualWinOdds = float(sumWins[pct])*100/float(winCountNum[pct])
        actualDrawOdds = float(sumDraws[pct])*100/float(drawCountNum[pct])
        if pct == 0:
            winOddsDiff = actualWinOdds - 2.5
            drawOddsDiff = actualDrawOdds - 2.5
        elif pct == 100:
            winOddsDiff = actualWinOdds - 97.5
            drawOddsDiff = actualDrawOdds - 97.5
        else:
            winOddsDiff = actualWinOdds - pct
            drawOddsDiff = actualDrawOdds - pct
        winOddsDiffWeightedSum += abs(winOddsDiff * winCountNum[pct])
        drawOddsDiffWeightedSum += abs(drawOddsDiff * drawCountNum[pct])
        winCountCases += winCountNum[pct]
        drawCountCases += drawCountNum[pct]
        print `(inn + 1)` + " " + `pct` + " " + `sumWins[pct]` + " " + `winCountNum[pct]` + " " + `actualWinOdds` + " " + `winOddsDiff` + " " + `sumDraws[pct]` + " " + `drawCountNum[pct]` + " " + `actualDrawOdds` + " " + `drawOddsDiff`
        fd.write(`(inn + 1)` + "," + `pct` + "," + `sumWins[pct]` + "," + `winCountNum[pct]` + "," + `actualWinOdds` + "," + `winOddsDiff` + "," + `sumDraws[pct]` + "," + `drawCountNum[pct]` + "," + `actualDrawOdds` + "," + `drawOddsDiff` + "\n")
    fd.write(`(inn + 1)` + ",,,,," + `(float(winOddsDiffWeightedSum)/float(winCountCases))` + "," + `(float(drawOddsDiffWeightedSum)/float(drawCountCases))` + "\n")
    fd.write("\n")
    fd.close()

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
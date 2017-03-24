#!/usr/bin/env python
import time
import sqlite3
import csv

start = time.clock()

oversRem = range(449, 0, -1)
for overRem in oversRem:
    accuracyRatio = []
    winOdds = []
    drawOdds = []
    winCount = []
    drawCount = []
    overs = []
    f = open("testMLPred.csv","rb")
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if row[5] == "None" or row[6] == "None": continue
        # if int(row[0]) < 2069: continue
        if int(row[2]) == overRem:
            winOdds.append(float(row[3]))
            drawOdds.append(float(row[4]))
            if int(row[5]) == 2:
                winCount.append(float(row[5])/2)
            else:
                winCount.append(0.0)
            if int(row[6]) == 1:
                drawCount.append(float(row[6]))
            else:
                drawCount.append(0.0)
    f.close()
    if len(winOdds) == 0 or len(drawOdds) == 0: continue

    descOrder = [i[0] for i in sorted(enumerate(winOdds), key=lambda x:x[1], reverse=True)]
    totWins = sum(winCount)
    randomWin = totWins / len(winOdds)
    cumWins = list(xrange(len(winOdds)))
    perfectModel = list(xrange(len(winOdds)))
    randomModel = list(xrange(len(winOdds)))
    r = 0
    perfModelDiff = 0.0
    curModelDiff = 0.0
    for dO in descOrder:
        if r == 0:
            cumWins[r] = winCount[dO]
            perfectModel[r] = 1
            randomModel[r] = randomWin
        else:
            cumWins[r] = cumWins[r - 1] + winCount[dO]
            randomModel[r] = randomModel[r - 1] + randomWin
            if (perfectModel[r - 1] + 1) <= totWins:
                perfectModel[r] += 1
            elif (perfectModel[r - 1] + 0.5) == totWins:
                perfectModel[r] += 0.5
            else:
                perfectModel[r] = totWins
        #print cumWins[r]
        perfModelDiff += perfectModel[r] - randomModel[r]
        curModelDiff += cumWins[r] - randomModel[r]
        r += 1
    if perfModelDiff == 0.0: continue
    accuracyRatio.append(curModelDiff / perfModelDiff)

    descOrder = [i[0] for i in sorted(enumerate(drawOdds), key=lambda x:x[1], reverse=True)]
    totWins = sum(drawCount)
    randomWin = totWins / len(drawOdds)
    cumWins = list(xrange(len(drawOdds)))
    perfectModel = list(xrange(len(drawOdds)))
    randomModel = list(xrange(len(drawOdds)))
    r = 0
    perfModelDiff = 0.0
    curModelDiff = 0.0
    for dO in descOrder:
        if r == 0:
            cumWins[r] = drawCount[dO]
            perfectModel[r] = 1
            randomModel[r] = randomWin
        else:
            cumWins[r] = cumWins[r - 1] + drawCount[dO]
            randomModel[r] = randomModel[r - 1] + randomWin
            if (perfectModel[r - 1] + 1) <= totWins:
                perfectModel[r] += 1
            elif (perfectModel[r - 1] + 0.5) == totWins:
                perfectModel[r] += 0.5
            else:
                perfectModel[r] = totWins
        #print cumWins[r]
        perfModelDiff += perfectModel[r] - randomModel[r]
        curModelDiff += cumWins[r] - randomModel[r]
        r += 1
    if perfModelDiff == 0.0: continue
    accuracyRatio.append(curModelDiff / perfModelDiff)

    fd = open('accuracyRatioMLTest.csv','a')
    print `overRem` + " " + `round(accuracyRatio[0] * 100, 2)` + " " + `round(accuracyRatio[1] * 100, 2)`
    fd.write(`overRem` + "," + `round(accuracyRatio[0] * 100, 2)` + "," + `round(accuracyRatio[1] * 100, 2)` + "\n")
    fd.close()

winOdds = []
drawOdds = []
winCount = []
drawCount = []
f = open("testMLPred.csv","rb")
reader = csv.reader(f, delimiter=',')
for row in reader:
    if row[5] == "None" or row[6] == "None": continue
    # if int(row[0]) < 2069: continue
    winOdds.append(float(row[3]))
    drawOdds.append(float(row[4]))
    if int(row[5]) == 2:
        winCount.append(float(row[5])/2)
    else:
        winCount.append(0.0)
    if int(row[6]) == 1:
        drawCount.append(float(row[6]))
    else:
        drawCount.append(0.0)
f.close()

overallAccuracyRatio = []
descOrder = [i[0] for i in sorted(enumerate(winOdds), key=lambda x:x[1], reverse=True)]
totWins = sum(winCount)
randomWin = totWins / len(winOdds)
cumWins = list(xrange(len(winOdds)))
perfectModel = list(xrange(len(winOdds)))
randomModel = list(xrange(len(winOdds)))
r = 0
perfModelDiff = 0.0
curModelDiff = 0.0
for dO in descOrder:
    if r == 0:
        cumWins[r] = winCount[dO]
        perfectModel[r] = 1
        randomModel[r] = randomWin
    else:
        cumWins[r] = cumWins[r - 1] + winCount[dO]
        randomModel[r] = randomModel[r - 1] + randomWin
        if (perfectModel[r - 1] + 1) <= totWins:
            perfectModel[r] += 1
        elif (perfectModel[r - 1] + 0.5) == totWins:
            perfectModel[r] += 0.5
        else:
            perfectModel[r] = totWins
    perfModelDiff += perfectModel[r] - randomModel[r]
    curModelDiff += cumWins[r] - randomModel[r]
    r += 1
overallAccuracyRatio.append(curModelDiff / perfModelDiff)

descOrder = [i[0] for i in sorted(enumerate(drawOdds), key=lambda x:x[1], reverse=True)]
totWins = sum(drawCount)
randomWin = totWins / len(drawOdds)
cumWins = list(xrange(len(drawOdds)))
perfectModel = list(xrange(len(drawOdds)))
randomModel = list(xrange(len(drawOdds)))
r = 0
perfModelDiff = 0.0
curModelDiff = 0.0
for dO in descOrder:
    if r == 0:
        cumWins[r] = drawCount[dO]
        perfectModel[r] = 1
        randomModel[r] = randomWin
    else:
        cumWins[r] = cumWins[r - 1] + drawCount[dO]
        randomModel[r] = randomModel[r - 1] + randomWin
        if (perfectModel[r - 1] + 1) <= totWins:
            perfectModel[r] += 1
        elif (perfectModel[r - 1] + 0.5) == totWins:
            perfectModel[r] += 0.5
        else:
            perfectModel[r] = totWins
    perfModelDiff += perfectModel[r] - randomModel[r]
    curModelDiff += cumWins[r] - randomModel[r]
    r += 1
overallAccuracyRatio.append(curModelDiff / perfModelDiff)

fd = open('accuracyRatioMLTest.csv','a')
print "Overall " + `round(overallAccuracyRatio[0] * 100, 2)` + " " + `round(overallAccuracyRatio[1] * 100, 2)`
fd.write("Overall," + `round(overallAccuracyRatio[0] * 100, 2)` + "," + `round(overallAccuracyRatio[1] * 100, 2)` + "\n")
fd.close()

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

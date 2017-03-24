#!/usr/bin/env python
import time
import sqlite3
import csv

start = time.clock()

overs = list(xrange(20))
for inn in range(0, 2):
    #if inn == 1: continue
    for over in overs:
        if inn == 1 and over == 19: continue
        t20Ids = []
        odds = []
        results = []
        f = open("t20MLPred"+`(inn+1)`+"UnqRRHMLT.csv","rb")
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == "Id": continue
            # if int(row[0]) < 3315: continue
            if int(row[1]) == (inn + 1) and int(row[2]) == (over + 1):
                t20Ids.append(int(row[0]))
                odds.append(float(row[3]))
                results.append(float(row[4]))
        f.close()

        descOrder = [i[0] for i in sorted(enumerate(odds), key=lambda x:x[1], reverse=True)]
        totWins = sum(results)
        randomWin = totWins / len(odds)
        cumWins = list(xrange(len(odds)))
        perfectModel = list(xrange(len(odds)))
        randomModel = list(xrange(len(odds)))
        r = 0
        perfModelDiff = 0.0
        curModelDiff = 0.0
        for dO in descOrder:
            if r == 0:
                cumWins[r] = results[dO]
                perfectModel[r] = 1
                randomModel[r] = randomWin
            else:
                cumWins[r] = cumWins[r - 1] + results[dO]
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
        accuracyRatio = curModelDiff / perfModelDiff
        fd = open('accuracyRatioMLT20.csv','a')
        print `(inn + 1)` + " " + `(over + 1)` + " " + `round(accuracyRatio * 100, 2)`
        fd.write(`(inn + 1)` + "," + `(over + 1)` + "," + `round(accuracyRatio * 100, 2)` + "\n")
        fd.close()

t20Ids = []
odds = []
results = []
f = open("t20MLPred"+`(inn+1)`+"UnqRRHMLT.csv","rb")
reader = csv.reader(f, delimiter=',')
for row in reader:
    if row[0] == "Id": continue
    #if int(row[0]) < 3315: continue
    t20Ids.append(int(row[0]))
    odds.append(float(row[3]))
    results.append(float(row[4]))
f.close()

descOrder = [i[0] for i in sorted(enumerate(odds), key=lambda x:x[1], reverse=True)]
totWins = sum(results)
randomWin = totWins / len(odds)
cumWins = list(xrange(len(odds)))
perfectModel = list(xrange(len(odds)))
randomModel = list(xrange(len(odds)))
r = 0
perfModelDiff = 0.0
curModelDiff = 0.0
for dO in descOrder:
    if r == 0:
        cumWins[r] = results[dO]
        perfectModel[r] = 1
        randomModel[r] = randomWin
    else:
        cumWins[r] = cumWins[r - 1] + results[dO]
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
overallAccuracyRatio = curModelDiff / perfModelDiff
fd = open('accuracyRatioMLT20.csv','a')
print "Overall " + `round(overallAccuracyRatio * 100, 2)`
fd.write("Overall,," + `round(overallAccuracyRatio * 100, 2)` + "\n")
fd.close()

elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

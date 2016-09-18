#!/usr/bin/env python
import time
import sqlite3
import math
start = time.clock()

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

# get tests info
c.execute('select * from testInfo')
testsInfo = c.fetchall()

def fixStrikeRate(inningsNum, totRuns, totBalls, totMins, batInnings):
    addBalls = 0
    remBalls = 0
    remRuns = 0
    addMin = 0
    for batInn in batInnings:
        batsmanId = batInn[1]
        runs = batInn[8]
        minutes = batInn[9]
        balls = batInn[10]
        if minutes == None or addMin == None:
            addMin = None
        else:
            addMin = addMin + minutes
        if balls == None or addBalls == None:
            addBalls = None
        else:
            addBalls = addBalls + balls                
    
    if addMin > 0 and addBalls == None:
        print '\nCalculating balls using minutes for innings #'+`inningsNum`
        for batInn in batInnings:
            batsmanId = batInn[1]
            batsmanName = batInn[2]
            runs = batInn[8]
            minutes = batInn[9]
            balls = batInn[10]
            if balls != None: continue
            inningsId = `int(testId)` + `inningsNum` + `batsmanId`
            calcBalls = round(float(totBalls) * minutes / addMin, 0)
            c.execute('update battingTestInnings set balls=? where inningsId=?', (int(calcBalls), inningsId))
            print `inningsId`+",",`batsmanName`+", runs: "+`runs`+', balls: '+`int(calcBalls)`+', mins: '+`minutes`
        print "Total Minutes: "+`addMin`
        print "Total Balls: "+`totBalls`
            
    if addMin == None and addBalls == None:
        print '\nCalculating balls using runs for innings #'+`inningsNum`
        for batInn in batInnings:
            batsmanId = batInn[1]
            runs = batInn[8]
            balls = batInn[10]
            if balls > 0:
                remBalls = remBalls + balls
                remRuns = remRuns + runs
        
        totRuns = totRuns - remRuns
        totBalls = totBalls - remBalls        
        for batInn in batInnings:
            batsmanId = batInn[1]
            batsmanName = batInn[2]
            notOut = batInn[7]
            runs = batInn[8]
            balls = batInn[10]
            inningsId = `int(testId)` + `inningsNum` + `batsmanId`
            if balls == None:
                calcBalls = round(float(totBalls) * runs / totRuns, 0)
                if notOut == 0 and calcBalls == 0: calcBalls = 1
                c.execute('update battingTestInnings set balls=? where inningsId=?', (int(calcBalls), inningsId))
                print `inningsId`+",",`batsmanName`+", runs: "+`runs`+', balls: '+`int(calcBalls)`
        print "Removed Runs:",`remRuns`+", Total Runs: "+`totRuns`
        print "Removed Balls:",`remBalls`+", Total Balls: "+`totBalls`
    conn.commit()
    
# loop through test matches
#for x in range(1999, 2000):
for x in range(0, len(testsInfo)):
    # load test info
    testId = int(testsInfo[x][0])
    print '\nChecking for missing ball data for test #'+`int(testId)`	
    inningsRuns = {}
    inningsBalls = {}
    inningsMins = {}    
    c.execute('select innings, runs, balls, minutes from detailsTestInnings where testId=?', (testId, ))
    for inn in c.fetchall():
        innings = inn[0]
        runs = inn[1]
        balls = inn[2]
        mins = inn[3]
        inningsRuns[innings] = runs
        inningsBalls[innings] = balls
        inningsMins[innings] = mins
      
    c.execute('select innings from detailsTestInnings where testId=?', (testId, ))    
    for inn in c.fetchall():
        innings = inn[0]               
        c.execute('select * from battingTestInnings where testId=? and innings=?', (testId, innings))        
        batInnings = c.fetchall()        
        fixStrikeRate(innings, inningsRuns[innings], inningsBalls[innings], inningsMins[innings], batInnings)   
    conn.commit()  
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
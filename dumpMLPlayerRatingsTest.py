#!/usr/bin/env python
import time
import sqlite3
import csv
import datetime
start = time.clock()

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

# get tests info
c.execute('select distinct testId from overComparisonTest order by testId asc')
result = c.fetchall()

# loop through test matches
fd1 = open('testML1PR.csv','a')
fd1.write("Id,Overs,BattingRating,BowlingRating\n")
fd1.close()

fd2 = open('testML2PR.csv','a')
fd2.write("Id,Overs,BattingRating,BowlingRating\n")
fd2.close()

fd3 = open('testML3PR.csv','a')
fd3.write("Id,Overs,BattingRating,BowlingRating\n")
fd3.close()

fd4 = open('testML4PR.csv','a')
fd4.write("Id,Overs,BattingRating,BowlingRating\n")
fd4.close()
for x in range(0, len(result)):
    testId = result[x][0]
    # if testId < 1952: continue
    print testId
    c.execute('select startDate from testInfo where testId=?',(testId,))
    testDate = c.fetchone()
    testDate = testDate[0]

    c.execute('select batTeam from detailsTestInnings where testId=? and innings=1',(testId,))
    team1 = c.fetchone()
    team1 = team1[0] if team1 != None else None

    c.execute('select batTeam from detailsTestInnings where testId=? and innings=2',(testId,))
    team2 = c.fetchone()
    team2 = team2[0] if team2 != None else None

    d = datetime.datetime(int(testDate[0:4]), int(testDate[4:-2]), int(testDate[6:]))
    date2yAgo = d + datetime.timedelta(days=-720)
    date2yAgo = date2yAgo.strftime('%Y%m%d')

    c.execute('select b.playerId, b.testId from battingTestLive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team1, date2yAgo, testDate))
    playerTests = c.fetchall()
    playerLastTest = {}
    for i in range(0, len(playerTests)):
        pid = playerTests[i][0]
        pTestId = playerTests[i][1]
        if pid in playerLastTest:
            if pTestId > playerLastTest[pid]:
                playerLastTest[pid] = pTestId
        else:
            playerLastTest[pid] = pTestId

    battingRating = []
    for pid in playerLastTest:
        c.execute('select player, rating from battingTestLive where playerId=? and testId=?', (pid, playerLastTest[pid]))
        pRating = c.fetchone()
        battingRating.append(pRating[1])
    battingRating = sorted(battingRating, reverse=True)

    team1BattingRating = 0.0
    if len(battingRating) >= 7:
        for b in range(0, 7):
            team1BattingRating += battingRating[b]
    else:
        for b in range(0, len(battingRating)):
            team1BattingRating += battingRating[b]
    team1BattingRating = team1BattingRating / 7 * 5
    print team1BattingRating

    c.execute('select b.playerId, b.testId from bowlingTestLive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team2, date2yAgo, testDate))
    playerTests = c.fetchall()
    playerLastTest = {}
    for i in range(0, len(playerTests)):
        pid = playerTests[i][0]
        pTestId = playerTests[i][1]
        if pid in playerLastTest:
            if pTestId > playerLastTest[pid]:
                playerLastTest[pid] = pTestId
        else:
            playerLastTest[pid] = pTestId

    bowlingRating = []
    for pid in playerLastTest:
        c.execute('select player, rating from bowlingTestLive where playerId=? and testId=?', (pid, playerLastTest[pid]))
        pRating = c.fetchone()
        bowlingRating.append(pRating[1])
    bowlingRating = sorted(bowlingRating, reverse=True)

    team2BowlingRating = 0.0
    if len(bowlingRating) >= 5:
        for b in range(0, 5):
            team2BowlingRating += bowlingRating[b]
    else:
        for b in range(0, len(bowlingRating)):
            team2BowlingRating += bowlingRating[b]
    print team2BowlingRating

    c.execute('select b.playerId, b.testId from battingTestLive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team2, date2yAgo, testDate))
    playerTests = c.fetchall()
    playerLastTest = {}
    for i in range(0, len(playerTests)):
        pid = playerTests[i][0]
        pTestId = playerTests[i][1]
        if pid in playerLastTest:
            if pTestId > playerLastTest[pid]:
                playerLastTest[pid] = pTestId
        else:
            playerLastTest[pid] = pTestId

    battingRating = []
    for pid in playerLastTest:
        c.execute('select player, rating from battingTestLive where playerId=? and testId=?', (pid, playerLastTest[pid]))
        pRating = c.fetchone()
        battingRating.append(pRating[1])
    battingRating = sorted(battingRating, reverse=True)

    team2BattingRating = 0.0
    if len(battingRating) >= 7:
        for b in range(0, 7):
            team2BattingRating += battingRating[b]
    else:
        for b in range(0, len(battingRating)):
            team2BattingRating += battingRating[b]
    team2BattingRating = team2BattingRating / 7 * 5
    print team2BattingRating

    c.execute('select b.playerId, b.testId from bowlingTestLive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team1, date2yAgo, testDate))
    playerTests = c.fetchall()
    playerLastTest = {}
    for i in range(0, len(playerTests)):
        pid = playerTests[i][0]
        pTestId = playerTests[i][1]
        if pid in playerLastTest:
            if pTestId > playerLastTest[pid]:
                playerLastTest[pid] = pTestId
        else:
            playerLastTest[pid] = pTestId

    bowlingRating = []
    for pid in playerLastTest:
        c.execute('select player, rating from bowlingTestLive where playerId=? and testId=?', (pid, playerLastTest[pid]))
        pRating = c.fetchone()
        bowlingRating.append(pRating[1])
    bowlingRating = sorted(bowlingRating, reverse=True)

    team1BowlingRating = 0.0
    if len(bowlingRating) >= 5:
        for b in range(0, 5):
            team1BowlingRating += bowlingRating[b]
    else:
        for b in range(0, len(bowlingRating)):
            team1BowlingRating += bowlingRating[b]
    print team1BowlingRating

    battingWktWeight = [0.15, 0.15, 0.15, 0.15, 0.125, 0.1, 0.075, 0.05, 0.025, 0.025]
    c.execute('select overs, wkts from overComparisonTest where testId=? and innings=1', (testId, ))
    overComp = c.fetchall()
    fd1 = open('testML1PR.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        wkts = overComp[i][1]
        battingRating = team1BattingRating * (300 - float(overs)) / 300
        if wkts > 0:
            for w in range(0, wkts):
                battingRating = battingRating - team1BattingRating * battingWktWeight[w]
        battingRating = 0 if battingRating < 0 else battingRating
        bowlingRating = team2BowlingRating * (50 - float(overs)) / 50
        fd1.write(`testId` + ","  + `overs` + "," + `battingRating` + "," + `bowlingRating` + "\n")
    fd1.close()

    c.execute('select overs, wkts from overComparisonTest where testId=? and innings=2', (testId, ))
    overComp = c.fetchall()
    fd2 = open('testML2PR.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        wkts = overComp[i][1]
        battingRating = team2BattingRating * (300 - float(overs)) / 300
        if wkts > 0:
            for w in range(0, wkts):
                battingRating = battingRating - team2BattingRating * battingWktWeight[w]
        battingRating = 0 if battingRating < 0 else battingRating
        bowlingRating = team1BowlingRating * (50 - float(overs)) / 50
        fd2.write(`testId` + ","  + `overs` + "," + `battingRating` + "," + `bowlingRating` + "\n")
    fd2.close()

    c.execute('select overs, wkts from overComparisonTest where testId=? and innings=3', (testId, ))
    overComp = c.fetchall()
    fd3 = open('testML3PR.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        wkts = overComp[i][1]
        battingRating = team2BattingRating * (300 - float(overs)) / 300
        if wkts > 0:
            for w in range(0, wkts):
                battingRating = battingRating - team2BattingRating * battingWktWeight[w]
        battingRating = 0 if battingRating < 0 else battingRating
        bowlingRating = team1BowlingRating * (50 - float(overs)) / 50
        fd3.write(`testId` + ","  + `overs` + "," + `battingRating` + "," + `bowlingRating` + "\n")
    fd3.close()

    c.execute('select overs, wkts from overComparisonTest where testId=? and innings=4', (testId, ))
    overComp = c.fetchall()
    fd4 = open('testML4PR.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        wkts = overComp[i][1]
        battingRating = team2BattingRating * (300 - float(overs)) / 300
        if wkts > 0:
            for w in range(0, wkts):
                battingRating = battingRating - team2BattingRating * battingWktWeight[w]
        battingRating = 0 if battingRating < 0 else battingRating
        bowlingRating = team1BowlingRating * (50 - float(overs)) / 50
        fd4.write(`testId` + ","  + `overs` + "," + `battingRating` + "," + `bowlingRating` + "\n")
    fd4.close()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

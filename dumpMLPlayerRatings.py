#!/usr/bin/env python
import time
import sqlite3
import csv
import datetime
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

# get odis info
c.execute('select distinct odiId from overComparisonODI order by odiId asc')
result = c.fetchall()

# loop through odi matches
# fd1 = open('odiML1PR.csv','a')
# fd1.write("Id,Overs,BattingRating,BowlingRating\n")
# fd1.close()
#
# fd2 = open('odiML2PR.csv','a')
# fd2.write("Id,Overs,BattingRating,BowlingRating\n")
# fd2.close()
for x in range(0, len(result)):
    odiId = result[x][0]
    if odiId < 1952: continue
    print odiId
    c.execute('select startDate from odiInfo where odiId=?',(odiId,))
    odiDate = c.fetchone()
    odiDate = odiDate[0]

    c.execute('select batTeam from detailsODIInnings where odiId=? and innings=1',(odiId,))
    team1 = c.fetchone()
    team1 = team1[0] if team1 != None else None

    c.execute('select batTeam from detailsODIInnings where odiId=? and innings=2',(odiId,))
    team2 = c.fetchone()
    team2 = team2[0] if team2 != None else None

    d = datetime.datetime(int(odiDate[0:4]), int(odiDate[4:-2]), int(odiDate[6:]))
    date2yAgo = d + datetime.timedelta(days=-720)
    date2yAgo = date2yAgo.strftime('%Y%m%d')

    c.execute('select b.playerId, b.odiId from battingODILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team1, date2yAgo, odiDate))
    playerODIs = c.fetchall()
    playerLastODI = {}
    for i in range(0, len(playerODIs)):
        pid = playerODIs[i][0]
        pODIId = playerODIs[i][1]
        if pid in playerLastODI:
            if pODIId > playerLastODI[pid]:
                playerLastODI[pid] = pODIId
        else:
            playerLastODI[pid] = pODIId

    battingRating = []
    for pid in playerLastODI:
        c.execute('select player, rating from battingODILive where playerId=? and odiId=?', (pid, playerLastODI[pid]))
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

    c.execute('select b.playerId, b.odiId from bowlingODILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team2, date2yAgo, odiDate))
    playerODIs = c.fetchall()
    playerLastODI = {}
    for i in range(0, len(playerODIs)):
        pid = playerODIs[i][0]
        pODIId = playerODIs[i][1]
        if pid in playerLastODI:
            if pODIId > playerLastODI[pid]:
                playerLastODI[pid] = pODIId
        else:
            playerLastODI[pid] = pODIId

    bowlingRating = []
    for pid in playerLastODI:
        c.execute('select player, rating from bowlingODILive where playerId=? and odiId=?', (pid, playerLastODI[pid]))
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

    c.execute('select b.playerId, b.odiId from battingODILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team2, date2yAgo, odiDate))
    playerODIs = c.fetchall()
    playerLastODI = {}
    for i in range(0, len(playerODIs)):
        pid = playerODIs[i][0]
        pODIId = playerODIs[i][1]
        if pid in playerLastODI:
            if pODIId > playerLastODI[pid]:
                playerLastODI[pid] = pODIId
        else:
            playerLastODI[pid] = pODIId

    battingRating = []
    for pid in playerLastODI:
        c.execute('select player, rating from battingODILive where playerId=? and odiId=?', (pid, playerLastODI[pid]))
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

    c.execute('select b.playerId, b.odiId from bowlingODILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team1, date2yAgo, odiDate))
    playerODIs = c.fetchall()
    playerLastODI = {}
    for i in range(0, len(playerODIs)):
        pid = playerODIs[i][0]
        pODIId = playerODIs[i][1]
        if pid in playerLastODI:
            if pODIId > playerLastODI[pid]:
                playerLastODI[pid] = pODIId
        else:
            playerLastODI[pid] = pODIId

    bowlingRating = []
    for pid in playerLastODI:
        c.execute('select player, rating from bowlingODILive where playerId=? and odiId=?', (pid, playerLastODI[pid]))
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
    c.execute('select overs, wkts from overComparisonODI where odiId=? and innings=1', (odiId, ))
    overComp = c.fetchall()
    fd1 = open('odiML1PR.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        wkts = overComp[i][1]
        battingRating = team1BattingRating * (300 - float(overs)) / 300
        if wkts > 0:
            for w in range(0, wkts):
                battingRating = battingRating - team1BattingRating * battingWktWeight[w]
        battingRating = 0 if battingRating < 0 else battingRating
        bowlingRating = team2BowlingRating * (50 - float(overs)) / 50
        fd1.write(`odiId` + ","  + `overs` + "," + `battingRating` + "," + `bowlingRating` + "\n")
    fd1.close()

    c.execute('select overs, wkts from overComparisonODI where odiId=? and innings=2', (odiId, ))
    overComp = c.fetchall()
    fd2 = open('odiML2PR.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        wkts = overComp[i][1]
        battingRating = team2BattingRating * (300 - float(overs)) / 300
        if wkts > 0:
            for w in range(0, wkts):
                battingRating = battingRating - team2BattingRating * battingWktWeight[w]
        battingRating = 0 if battingRating < 0 else battingRating
        bowlingRating = team1BowlingRating * (50 - float(overs)) / 50
        fd2.write(`odiId` + ","  + `overs` + "," + `battingRating` + "," + `bowlingRating` + "\n")
    fd2.close()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

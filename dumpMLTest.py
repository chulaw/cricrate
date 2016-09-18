#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import csv
start = time.clock()

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

# get tests info
c.execute('select distinct testId from overComparisonTest order by testId asc')
result = c.fetchall()
conn.close()

fd = open('testML1.csv','a')
fd.write("Id,Overs,Runs,Wkts,OversRem,Team1Rating,Team2Rating,HomeAway,WinOdds,DrawOdds,WinResult,DrawResult\n")
fd.close()

fd = open('testML2.csv','a')
fd.write("Id,Overs,Runs,Wkts,RunsReq,OversRem,Team1Rating,Team2Rating,HomeAway,WinOdds,DrawOdds,WinResult,DrawResult\n")
fd.close()

fd = open('testML3.csv','a')
fd.write("Id,Overs,Runs,Wkts,RunsReq,OversRem,Team1Rating,Team2Rating,HomeAway,WinOdds,DrawOdds,WinResult,DrawResult\n")
fd.close()

fd = open('testML4.csv','a')
fd.write("Id,Overs,Runs,Wkts,RunsReq,OversRem,Team1Rating,Team2Rating,HomeAway,WinOdds,DrawOdds,WinResult,DrawResult\n")
fd.close()



def inningsOdds(testId, innNum):
    conn = sqlite3.connect('ccr.db')
    c = conn.cursor()
    c.execute('select ocId, overs, runs, wkts, runsReq, ballsRem, result from overComparisonTest where testId=? and innings=?', (testId, innNum))
    conn.commit()
    overComp = c.fetchall();
    fd = open("testML"+`innNum`+".csv",'a')
    for i in range(0, len(overComp)):
        overs = overComp[i][1]
        runs = overComp[i][2]
        wkts = overComp[i][3]
        runsReq = overComp[i][4]
        ballsRem = overComp[i][5]
        matchResult = overComp[i][6]
        if innNum == 4:            
            if int(runsReq) < 0:            
                c.execute('''select runs, wkts, runsReq, ballsRem, result, testId from overComparisonTest where testId<? and innings=? and wkts>=? and wkts<=? and runsReq>=? and runsReq<? and ballsRem<=? and ballsRem>?''',
                        (testId, innNum, wkts-1, wkts+1, runsReq*1.1, runsReq*0.9, ballsRem*1.1, ballsRem*0.9))
            else:
                if ballsRem < 60:
                    c.execute('''select runs, wkts, runsReq, ballsRem, result, testId from overComparisonTest where testId<? and innings=? and wkts>=? and wkts<=? and runsReq>=? and runsReq<? and ballsRem<=? and ballsRem>?''',
                            (testId, innNum, wkts-1, wkts+1, runsReq*0.8, runsReq*1.2, ballsRem*1.2, ballsRem*0.8))
                else:
                    c.execute('''select runs, wkts, runsReq, ballsRem, result, testId from overComparisonTest where testId<? and innings=? and wkts>=? and wkts<=? and runsReq>=? and runsReq<? and ballsRem<=? and ballsRem>?''',
                            (testId, innNum, wkts-1, wkts+1, runsReq*0.9, runsReq*1.1, ballsRem*1.1, ballsRem*0.9))
        else:
            if int(runsReq) < 0:            
                c.execute('''select runs, wkts, runsReq, ballsRem, result, testId from overComparisonTest where testId<? and innings=? and ballsRem>? and ballsRem<=? and wkts>=? and wkts<=? and runsReq>=? and runsReq<?''',
                        (testId, innNum, ballsRem*0.9, ballsRem*1.1, wkts-1, wkts+1, runsReq*1.1, runsReq*0.9))
            else:
                c.execute('''select runs, wkts, runsReq, ballsRem, result, testId from overComparisonTest where testId<? and innings=? and ballsRem>? and ballsRem<=? and wkts>=? and wkts<=? and runsReq>=? and runsReq<?''',
                        (testId, innNum, ballsRem*0.9, ballsRem*1.1, wkts-1, wkts+1, runsReq*0.9, runsReq*1.1))
        comp = c.fetchall()
        similarCount = len(comp)        
        winCount = 0.0
        drawCount = 0.0
        for j in range(0, len(comp)):
            compResult = comp[j][4]
            #print `testId` + ' Innings: ' + `innNum` + ' SimilarScore: ' + `compRuns` + '/' + `compWkts` + ' SimilarResult: ' + `compResult`
            if int(compResult) == 2:
                winCount = winCount + int(compResult) / 2
            elif int(compResult) == 1:
                drawCount = drawCount + int(compResult)
        winOdds = 100 * winCount / similarCount if similarCount > 0 else None
        drawOdds = 100 * drawCount / similarCount if similarCount > 0 else None

        # team current ratings adjustment
        teamHome = 0.0
        if winOdds != None:
            lossOdds = 100 - winOdds - drawOdds
            winOdds = winOdds / 100.0
            drawOdds = drawOdds / 100.0
            lossOdds = lossOdds / 100.0
            oddsDiff = abs(winOdds - lossOdds)
            drawOddsAdj = drawOdds * (1 - oddsDiff)
            if innNum == 2:
                winOddsAdj = (1 - drawOddsAdj) * (winOdds * 0.4 + team1StartingOdds * 0.6)
                lossOddsAdj = (1 - drawOddsAdj) * (lossOdds * 0.4 + team1StartingOdds * 0.6)
                teamHome = team2Home
            if innNum == 3:
                if team1 == team3:
                    winOddsAdj = (1 - drawOddsAdj) * (winOdds * 0.6 + team1StartingOdds * 0.4)
                    lossOddsAdj = (1 - drawOddsAdj) * (lossOdds * 0.6 + team2StartingOdds * 0.4)
                else:
                    winOddsAdj = (1 - drawOddsAdj) * (winOdds * 0.6 + team2StartingOdds * 0.4)
                    lossOddsAdj = (1 - drawOddsAdj) * (lossOdds * 0.6 + team1StartingOdds * 0.4)
                teamHome = team3Home
            if innNum == 4:
                if team4 == team1:
                    winOddsAdj = (1 - drawOddsAdj) * (winOdds * 0.8 + team1StartingOdds * 0.2)
                    lossOddsAdj = (1 - drawOddsAdj) * (lossOdds * 0.8 + team2StartingOdds * 0.2)
                else:
                    winOddsAdj = (1 - drawOddsAdj) * (winOdds * 0.8 + team2StartingOdds * 0.2)
                    lossOddsAdj = (1 - drawOddsAdj) * (lossOdds * 0.8 + team1StartingOdds * 0.2)
                teamHome = team4Home
            adjSum = drawOddsAdj + winOddsAdj + lossOddsAdj
            winOdds = 100.0 * winOddsAdj / adjSum
            drawOdds = 100.0 * drawOddsAdj / adjSum

            # home/away adjustment
            winOdds = winOdds + min(winOdds * 0.1, 7.0) * teamHome
            drawOdds = drawOdds - min(drawOdds * 0.1, 3.75) * teamHome
            if winOdds > 100.0: winOdds = 100.0
            if winOdds < 0.0: winOdds = 0.0
            if drawOdds > 100.0: drawOdds = 100.0
            if drawOdds < 0.0: drawOdds = 0.0

        if innNum == 4:
            winOdds = 100.0 if runsReq == 0 else winOdds
            drawOdds = 0.0 if runsReq == 0 else drawOdds
            winOdds = 0.0 if ballsRem == 0 and runsReq != 0 else winOdds
            winOdds = 0.0 if int(wkts) == 10 and runsReq != 0 else winOdds
            drawOdds = 0.0 if int(wkts) == 10 and runsReq != 0 else drawOdds

        winResult = 1 if matchResult == 2 else 0
        drawResult = 1 if matchResult == 1 else 0

        if innNum == 2:
            fd.write(`testId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `(float(ballsRem) / 6)` + "," + `team2Rating` + "," + `team1Rating` + "," + `teamHome` + "," + `winOdds` + "," + `drawOdds` + "," + `winResult` + "," + `drawResult` + "\n")
        elif innNum == 3:
            if team1 == team3:
                fd.write(`testId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `(float(ballsRem) / 6)` + "," + `team1Rating` + "," + `team2Rating` + "," + `teamHome` + "," + `winOdds` + "," + `drawOdds` + "," + `winResult` + "," + `drawResult` + "\n")
            else:
                fd.write(`testId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `(float(ballsRem) / 6)` + "," + `team2Rating` + "," + `team1Rating` + "," + `teamHome` + "," + `winOdds` + "," + `drawOdds` + "," + `winResult` + "," + `drawResult` + "\n")
        elif innNum == 4:
            if team1 == team4:
                fd.write(`testId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `(float(ballsRem) / 6)` + "," + `team1Rating` + "," + `team2Rating` + "," + `teamHome` + "," + `winOdds` + "," + `drawOdds` + "," + `winResult` + "," + `drawResult` + "\n")
            else:
                fd.write(`testId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `(float(ballsRem) / 6)` + "," + `team2Rating` + "," + `team1Rating` + "," + `teamHome` + "," + `winOdds` + "," + `drawOdds` + "," + `winResult` + "," + `drawResult` + "\n")
    fd.close()

#print `len(result)`
# loop through test matches
#for x in range(0, 1):
for x in range(0, len(result)):
    testId = result[x][0]
    print testId
    conn = sqlite3.connect('ccr.db')
    c = conn.cursor()
    c.execute('select startDate from testInfo where testId=?',(testId,))
    testDate = c.fetchone()
    testDate = testDate[0]

    c.execute('select batTeam from detailsTestInnings where testId=? and innings=1',(testId,))
    team1 = c.fetchone()
    team1 = team1[0] if team1 != None else None

    c.execute('select batTeam, balls from detailsTestInnings where testId=? and innings=2',(testId,))
    team2 = c.fetchone()
    team2 = team2[0] if team2 != None else None

    c.execute('select batTeam from detailsTestInnings where testId=? and innings=3',(testId,))
    team3 = c.fetchone()
    team3 = team3[0] if team3 != None else None

    c.execute('select batTeam from detailsTestInnings where testId=? and innings=4',(testId,))
    team4 = c.fetchone()
    team4 = team4[0] if team4 != None else None

    team1StartingOdds = 0.3333
    team2StartingOdds = 0.3333
    if team1 != None and team2 != None:
        c.execute('select rating from teamTestLive where team=? and startDate<?',(team1, testDate))
        team1Rating = c.fetchall()
        if len(team1Rating) > 0:
            team1Rating = team1Rating[len(team1Rating)-1][0]
        else:
            team1Rating = 100.0

        c.execute('select rating from teamTestLive where team=? and startDate<?',(team2, testDate))
        team2Rating = c.fetchall()
        if len(team2Rating) > 0:
            team2Rating = team2Rating[len(team2Rating)-1][0]
        else:
            team2Rating = 100.0

        team1StartingOddsUnAdj = team1Rating / (team1Rating + team2Rating)
        team2StartingOddsUnAdj = 1 - team1StartingOddsUnAdj
        oddsDiff = abs(team1StartingOddsUnAdj - team2StartingOddsUnAdj)
        drawOdds = 0.3333 * (1 - oddsDiff)
        team1StartingOdds = (1 - drawOdds) * team1StartingOddsUnAdj
        team2StartingOdds = (1 - drawOdds) * team2StartingOddsUnAdj

        # Check if match is home/away/neutral
        c.execute('select location from testInfo where testId=?',(testId,))
        location = c.fetchone()
        location = location[0] if location != None else None

        team1Home = 0.0
        team2Home = 0.0
        team3Home = 0.0
        team4Home = 0.0
        if team1 == location:
            team1Home = 1.0
            team2Home = -1.0
            if team3 == team1:
                team3Home = 1.0
                team4Home = -1.0
            else:
                team3Home = -1.0
                team4Home = 1.0
        elif team2 == location:
            team1Home = -1.0
            team2Home = 1.0
            if team3 == team2:
                team3Home = 1.0
                team4Home = -1.0
            else:
                team3Home = 1.0
                team4Home = -1.0

    c.execute('select ocId, overs, runs, wkts, result, ballsRem from overComparisonTest where testId=? and innings=1', (testId, ))
    conn.commit()
    overComp = c.fetchall();
    fd = open('testML1.csv','a')
    for i in range(0, len(overComp)):
        ocId = overComp[i][0]
        overs = overComp[i][1]
        runs = overComp[i][2]
        wkts = overComp[i][3]        
        matchResult = overComp[i][4]
        ballsRem = overComp[i][5]
        if runs == 0:
            c.execute('''select runs, wkts, result, testId from overComparisonTest where testId<? and innings=1 and ballsRem>? and ballsRem<=? and runs<=1 and wkts>=? and wkts<=?''',
                      (testId, ballsRem*0.9, ballsRem*1.1, wkts-1, wkts+1))
        else:
            c.execute('''select runs, wkts, result, testId from overComparisonTest where testId<? and innings=1 and ballsRem>? and ballsRem<=? and runs<=? and runs>? and wkts>=? and wkts<=?''',
                      (testId, ballsRem*0.9, ballsRem*1.1, runs*1.1, runs*0.9, wkts-1, wkts+1))
        comp = c.fetchall()
        similarCount = len(comp)        
        winCount = 0.0
        drawCount = 0.0
        for j in range(0, len(comp)):
            compRuns = comp[j][0]
            compWkts = comp[j][1]
            compResult = comp[j][2]
            # print `testId` + ' Innings: 1 SimilarScore: ' + `compRuns` + '/' + `compWkts` + ' SimilarResult: ' + `compResult`
            if int(compResult) == 2:
                winCount = winCount + int(compResult) / 2
            elif int(compResult) == 1:
                drawCount = drawCount + int(compResult)
        winOdds = 100 * winCount / similarCount if similarCount > 0 else None
        drawOdds = 100 * drawCount / similarCount if similarCount > 0 else None

        # team current ratings adjustment
        winOddsAdj = winOdds
        if winOdds != None:
            lossOdds = 100.0 - winOdds - drawOdds
            winOdds = winOdds / 100.0
            drawOdds = drawOdds / 100.0
            lossOdds = lossOdds / 100.0
            oddsDiff = abs(winOdds - lossOdds)
            drawOddsAdj = drawOdds * (1 - oddsDiff)
            winOddsAdj = (1 - drawOddsAdj) * (winOdds * 0.2 + team1StartingOdds * 0.8)
            lossOddsAdj = (1 - drawOddsAdj) * (lossOdds * 0.2 + team2StartingOdds * 0.8)
            adjSum = drawOddsAdj + winOddsAdj + lossOddsAdj
            winOdds = 100.0 * winOddsAdj / adjSum
            drawOdds = 100.0 * drawOddsAdj / adjSum

            # home/away adjustment
            winOdds = winOdds + min(winOdds * 0.1, 7.0) * team1Home
            drawOdds = drawOdds - min(drawOdds * 0.1, 3.75) * team1Home
            if winOdds > 100.0: winOdds = 100.0
            if winOdds < 0.0: winOdds = 0.0
            if drawOdds > 100.0: drawOdds = 100.0
            if drawOdds < 0.0: drawOdds = 0.0

        winResult = 1 if matchResult == 2 else 0
        drawResult = 1 if matchResult == 1 else 0

        fd.write(`testId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `(ballsRem / 6)` + "," + `team1Rating` + "," + `team2Rating` + "," + `team1Home` + "," + `winOdds` + "," + `drawOdds` + "," + `winResult` + "," + `drawResult` + "\n")
    fd.close()
    conn.close()

    inningsOdds(testId, 2)
    conn.close()
    
    inningsOdds(testId, 3)
    conn.close()
    
    inningsOdds(testId, 4)
    conn.close()    
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
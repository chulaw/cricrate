#!/usr/bin/env python
import time
import re
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

# get tests info
c.execute('select * from testInfo')
testsInfo = c.fetchall()
ignoreError = (1560, 1571, 1573, 1615, 1625, 1664, 1678, 1705, 1718, 1719, 1725, 1738, 1742, 1758, 1771, 1777, 1808, 1812, 1814, 1827, 1872, 1873, 1901, 1907, 1912, 1959, 1960, 1972, 1988, 1991, 2005, 2007, 2018,
               2028, 2070, 2083, 2138)

# loop through test matches
for x in range(0, len(testsInfo)):
    testId = testsInfo[x][0]
    if testId < 2170: continue
    if testId in ignoreError:
        continue
    result = testsInfo[x][8]
    
    overComparisonURL = 'http://www.espncricinfo.com' + testsInfo[x][12] + '?view=comparison'
    overComparisonPage = requests.get(overComparisonURL)
    scoreTree = html.fromstring(overComparisonPage.text)
    
    # parse all relevant fields from overComparison
    rows = scoreTree.xpath('(//div[@id="stats-container"]/div/table/tbody/tr)')
    dataTable = scoreTree.xpath('(//div[@id="stats-container"]/div/table/tbody/tr/td/text())')

    scorecardComparisonURL = 'http://www.espncricinfo.com' + testsInfo[x][12]
    scorecardComparisonPage = requests.get(scorecardComparisonURL)
    scorecardTree = html.fromstring(scorecardComparisonPage.text)
    dayTable = scorecardTree.xpath('(//ul[@class="close-of-play"]/li/span[@class="normal"]/text())')
    oversTable = scorecardTree.xpath('(//ul[@class="close-of-play"]/li/span[@class="normal"]/span/text())')

    closeDay = []
    closeTeam = []
    closeTeamInn = []
    closeScore = []
    closeOvers = []
    noPlayDays = []
    for dayData in dayTable:
        if "day" in dayData and "rest day" not in dayData:
            day = int(dayData.split('-')[0][4:])
            innState = dayData.split('-')[1]
            if "no play" in innState or "rest day" in innState:
                team = None
                innings = None
                score = None
                noPlayDays.append(day)                
            else:
                numLoc = re.search("\d", innState)
                team = innState[:(numLoc.start()-1)].strip()
                innings = int(innState[(numLoc.start()-1):].strip()[:1])
                score = innState[(numLoc.start()+11):-2].strip()
            closeDay.append(day)
            closeTeam.append(team)
            closeTeamInn.append(innings)
            closeScore.append(score)

    overDay = 1    
    for oversData in oversTable:
        if overDay in noPlayDays:
            closeOvers.append(None)
        if "ov" in oversData:
            overBalls = oversData.split(' ')[0].split('.')
            overs = int(overBalls[0])
            balls = 0
            if len(overBalls) == 2: balls = int(overBalls[1])
            if balls > 0: overs = overs + 1
            closeOvers.append(overs)
        if testId == 2165 and "ov" not in oversData and overDay not in noPlayDays:
            closeOvers.append(104)
        if testId == 2168 and "ov" not in oversData and overDay not in noPlayDays:
            closeOvers.append(119)
        if testId == 2170 and "ov" not in oversData and overDay not in noPlayDays:
            closeOvers.append(71)
        overDay = overDay + 1
    
    print closeDay
    print closeTeam
    print closeTeamInn
    print closeScore
    print closeOvers

    c.execute('select innings, batTeam, bowlTeam, runs, balls, wickets from detailsTestInnings where testId=?', (testId,))
    teamBat1 = ""
    teamBat2 = ""
    teamBat3 = ""
    teamBat4 = ""
    for inningsData in c.fetchall():
        inningsNum = inningsData[0]
        if inningsNum == 1:
            teamBat1 = inningsData[1]
            teamBowl1 = inningsData[2]
            totalRuns1 = inningsData[3]
            totalBalls1 = inningsData[4]
            totalOvers1 = totalBalls1 / 6
            if totalBalls1 % 6 > 0 : totalOvers1 = totalOvers1 + 1
            totalWkts1 = inningsData[5]
        elif inningsNum == 2:
            teamBat2 = inningsData[1]
            teamBowl2 = inningsData[2]
            totalRuns2 = inningsData[3]
            totalBalls2 = inningsData[4]
            totalOvers2 = totalBalls2 / 6
            if totalBalls2 % 6 > 0 : totalOvers2 = totalOvers2 + 1
            totalWkts2 = inningsData[5]
        elif inningsNum == 3:
            teamBat3 = inningsData[1]
            teamBowl3 = inningsData[2]
            totalRuns3 = inningsData[3]
            totalBalls3 = inningsData[4]
            totalOvers3 = totalBalls3 / 6
            if totalBalls3 % 6 > 0 : totalOvers3 = totalOvers3 + 1
            totalWkts3 = inningsData[5]
        else:
            teamBat4 = inningsData[1]
            teamBowl4 = inningsData[2]
            totalRuns4 = inningsData[3]
            totalBalls4 = inningsData[4]
            totalOvers4 = totalBalls4 / 6;
            if totalBalls4 % 6 > 0 : totalOvers4 = totalOvers4 + 1
            totalWkts4 = inningsData[5]        
    result1 = 0
    result2 = 0
    result3 = 0
    result4 = 0
    if teamBat1 == result:
        result1 = 2
    if teamBat2 == result:
        result2 = 2
    if teamBat3 == result:
        result3 = 2
    if teamBat4 == result:
        result4 = 2
    if result == "Draw":
        result1 = 1
        result2 = 1
        result3 = 1
        result4 = 1
        
    allOutDec1 = 0
    allOutDec2 = 0
    allOutDec3 = 0
    allOutDec4 = 0
    i = 1
    j = 1
    for i in range(len(rows)-1):
        i = i + 1
        overs = i
        day = 0
        if allOutDec1 == 0:
            score1 = dataTable[j]
            if score1.find("/") == -1:
                j = j + 1
                continue
            runs1 = int(score1.split('/')[0])
            wkts1 = int(score1.split('/')[1])
            ballsRem1 = (450 - overs) * 6
            if overs == totalOvers1 and runs1 == totalRuns1 and wkts1 == totalWkts1 : allOutDec1 = 1
            j = j + 3
            ocId = `testId` + `1` + `int(overs)`
            
            for i in range(len(closeDay)):
                if teamBat1 == closeTeam[i]:
                    if closeTeamInn[i] == 1:
                        if closeOvers[i] >= overs:
                            day = closeDay[i]
                        else:
                            day = closeDay[i] + 1
            
            if day == 0: day = 1                
            dayBalls = (450 - 90*(day-1)) * 6
            if dayBalls < ballsRem1:
                ballsRem1 = dayBalls
            
            print `ocId` + ' ' + `testId` + ' ' +  teamBat1 + ' ' + `runs1` + '/' + `wkts1` + ' ' + `day` + ' ' + `result1`
            c.execute('''insert or ignore into overComparisonTest (ocId, testId, innings, teamBat, overs, runs, wkts, runsReq, ballsRem, day, winOdds, drawOdds, adjWinOdds, adjDrawOdds, result)
                      values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (ocId, testId, 1, teamBat1, overs, runs1, wkts1, None, ballsRem1, day, None, None, None, None, result1))
            if j >= len(dataTable) : continue
            if dataTable[j] == str(i+1):
                j = j + 1
                continue                
        if allOutDec2 == 0:
            score2 = dataTable[j]
            if score2.find("/") == -1:
                j = j + 1
                continue
            runs2 = int(score2.split('/')[0])
            wkts2 = int(score2.split('/')[1])
            runsReq2 = totalRuns1 - runs2
            ballsRem2 = 450 * 6 - totalBalls1 - 6 * overs
            if overs == totalOvers2 and runs2 == totalRuns2 and wkts2 == totalWkts2 : allOutDec2 = 1
            # error in test #1795 and #1913 2nd innings wkts
            if testId == 1795 and overs == totalOvers2 and runs2 == totalRuns2 : allOutDec2 = 1
            if testId == 1913 and overs == totalOvers2 and runs2 == totalRuns2 : allOutDec2 = 1
            j = j + 3
            ocId = `testId` + `2` + `int(overs)`
            
            for i in range(len(closeDay)):
                if teamBat2 == closeTeam[i]:
                    if closeTeamInn[i] == 1:
                        if closeOvers[i] >= overs:
                            day = closeDay[i]
                        else:
                            day = closeDay[i] + 1
            
            dayBalls = (450 - 90*(day-1)) * 6
            if dayBalls < ballsRem2:
                ballsRem2 = dayBalls
            
            print `ocId` + ' ' + `testId` + ' ' +  teamBat2 + ' ' + `runs2` + '/' + `wkts2` + ' ' + `day` + ' ' + `result2`
            c.execute('''insert or ignore into overComparisonTest (ocId, testId, innings, teamBat, overs, runs, wkts, runsReq, ballsRem, day, winOdds, drawOdds, adjWinOdds, adjDrawOdds, result)
                      values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (ocId, testId, 2, teamBat2, overs, runs2, wkts2, runsReq2, ballsRem2, day, None, None, None, None, result2))
            if j >= len(dataTable) : continue
            if dataTable[j] == str(i+1):
                j = j + 1                
                continue
        if allOutDec3 == 0:    
            score3 = dataTable[j]
            if score3.find("/") == -1:
                j = j + 1
                continue
            runs3 = int(score3.split('/')[0])
            wkts3 = int(score3.split('/')[1])
            if teamBat1 == teamBat3:
                runsReq3 = totalRuns2 - totalRuns1 - runs3
            else:
                runsReq3 = totalRuns1 - totalRuns2 - runs3
            ballsRem3 = 450 * 6 - totalBalls1 - totalBalls2 - 6 * overs
            if overs == totalOvers3 and runs3 == totalRuns3 and wkts3 == totalWkts3 : allOutDec3 = 1
            # error in test #1706 and #1743 3rd innings over comparison, #2067 3rd innings wkts
            if testId == 1706 and overs == totalOvers3 and wkts3 == totalWkts3 : allOutDec3 = 1
            if testId == 1743 and overs == totalOvers3 and wkts3 == totalWkts3 : allOutDec3 = 1
            if testId == 2067 and overs == totalOvers3 and runs3 == totalRuns3 : allOutDec3 = 1
            j = j + 3
            ocId = `testId` + `3` + `int(overs)`
            
            for i in range(len(closeDay)):
                if teamBat3 == closeTeam[i]:
                    if closeTeamInn[i] == 2:
                        if closeOvers[i] >= overs:
                            day = closeDay[i]
                        else:
                            day = closeDay[i] + 1
            
            dayBalls = (450 - 90*(day-1)) * 6
            if dayBalls < ballsRem3:
                ballsRem3 = dayBalls
            
            print `ocId` + ' ' + `testId` + ' ' +  teamBat3 + ' ' + `runs3` + '/' + `wkts3` + ' ' + `day` + ' ' + `result3`
            c.execute('''insert or ignore into overComparisonTest (ocId, testId, innings, teamBat, overs, runs, wkts, runsReq, ballsRem, day, winOdds, drawOdds, adjWinOdds, adjDrawOdds, result)
                      values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (ocId, testId, 3, teamBat3, overs, runs3, wkts3, runsReq3, ballsRem3, day, None, None, None, None, result3))            
            if j >= len(dataTable) : continue
            if dataTable[j] == str(i+1):
                j = j + 1
                continue
        if allOutDec4 == 0:
            score4 = dataTable[j]
            if score4.find("/") == -1:
                j = j + 1
                continue
            if teamBat4 == "":
                j = j + 1
                continue
            runs4 = int(score4.split('/')[0])
            wkts4 = int(score4.split('/')[1])
            if teamBat2 == teamBat4:
                runsReq4 = 1 + totalRuns1 - totalRuns2 + totalRuns3 - runs4
            else:
                runsReq4 = 1 + totalRuns2 - totalRuns1 + totalRuns3 - runs4
            ballsRem4 = 450 * 6 - (totalBalls1 + totalBalls2 + totalBalls3) - 6 * overs
            if overs == totalOvers4 and runs4 == totalRuns4 and wkts4 == totalWkts4 : allOutDec4 = 1
            j = j + 5
            ocId = `testId` + `4` + `int(overs)`
                        
            for i in range(len(closeDay)):
                if teamBat4 == closeTeam[i]:
                    if closeTeamInn[i] == 2:
                        if closeOvers[i] >= overs:
                            day = closeDay[i]
                        else:
                            day = closeDay[i] + 1

            dayBalls = (450 - 90*(day-1)) * 6
            if dayBalls < ballsRem4:
                ballsRem4 = dayBalls
            
            print `ocId` + ' ' + `testId` + ' ' +  teamBat4 + ' ' + `runs4` + '/' + `wkts4` + ' ' + `day` + ' ' + `result4`
            c.execute('''insert or ignore into overComparisonTest (ocId, testId, innings, teamBat, overs, runs, wkts, runsReq, ballsRem, day, winOdds, drawOdds, adjWinOdds, adjDrawOdds, result)
                      values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (ocId, testId, 4, teamBat4, overs, runs4, wkts4, runsReq4, ballsRem4, day, None, None, None, None, result4))
            if j >= len(dataTable) : continue
    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
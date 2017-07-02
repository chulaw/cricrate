#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import re
start = time.clock()

# get ft20s info
conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()
c.execute('select ft20Id, startDate from ft20Info')
ft20sInfo = c.fetchall()
ignoreFT20DL = (40, 41, 65, 66, 196, 226, 246, 267, 270, 271, 364, 484, 487, 497, 528, 601, 619, 644, 673, 683, 709, 716, 731, 804, 832, 854, 855, 873, 875)
t20Info = {}
startDates = {}
for x in range(0, len(ft20sInfo)):
    ft20Id = ft20sInfo[x][0]
    if ft20Id in ignoreFT20DL:
        continue
    startDate = ft20sInfo[x][1]
    t20Id = `ft20Id`+"F"+startDate
    t20Info[t20Id] = ft20Id
    startDates[startDate] = ft20Id
conn.close()

# get t20is info
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()
c.execute('select t20iId, startDate from t20iInfo')
t20isInfo = c.fetchall()
ignoreT20IDL = (11, 26, 70, 119, 124, 157, 159, 160, 231, 242, 247, 252, 260, 270, 273, 290, 300, 318, 335, 340, 373, 380, 398, 404, 422, 529, 530, 534, 563)
for x in range(0, len(t20isInfo)):
    t20iId = t20isInfo[x][0]
    if t20iId in ignoreT20IDL:
        continue
    startDate = t20isInfo[x][1]
    t20Id = `t20iId`+"I"+startDate
    t20Info[t20Id] = t20iId
    startDates[startDate] = t20iId
conn.close()

t20Info = sorted(t20Info, key=t20Info.get)
startDates = sorted(startDates, key=int)

t20NumId = 1502
# loop through matches
for startDate in startDates:
    print `startDate`
    if int(startDate) <= 20170501: continue
    matches = [i for i, item in enumerate(t20Info) if re.search(str(startDate), item)]
    for key in matches:
        t20Id = t20Info[key]
        if "F" in t20Id:
            matchId = t20Id[:t20Id.index("F")]
            matchType = "FT20"
            conn = sqlite3.connect('ccrFT20.db')
            c = conn.cursor()
            c.execute('select result, scoreLink from ft20Info where ft20Id=?',(matchId,))
            ft20sInfo = c.fetchone()
            result = ft20sInfo[0]
            scoreLink = ft20sInfo[1]
        else:
            matchId = t20Id[:t20Id.index("I")]
            print `matchId`
            matchType = "T20I"
            conn = sqlite3.connect('ccrT20I.db')
            c = conn.cursor()
            c.execute('select result, scoreLink from t20iInfo where t20iId=?',(matchId,))
            t20isInfo = c.fetchone()
            result = t20isInfo[0]
            scoreLink = t20isInfo[1]

        overComparisonURL = 'http://www.espncricinfo.com' + scoreLink + '?view=comparison'
        print overComparisonURL
        overComparisonPage = requests.get(overComparisonURL)
        scoreTree = html.fromstring(overComparisonPage.text)

        # parse all relevant fields from overComparison
        rows = scoreTree.xpath('(//div[@id="stats-container"]/div/table/tbody/tr)')
        dataTable = scoreTree.xpath('(//div[@id="stats-container"]/div/table/tbody/tr/td/text())')

        c.execute('select innings, batTeam, bowlTeam from details'+matchType+'Innings where '+matchType.lower()+'Id=?', (matchId,))
        for inningsData in c.fetchall():
            inningsNum = inningsData[0]
            if inningsNum == 1:
                teamBat1 = inningsData[1]
                teamBowl1 = inningsData[2]
            else:
                teamBat2 = inningsData[1]
                teamBowl2 = inningsData[2]

        if teamBat1 == result:
            result1 = 2
            result2 = 0
        elif teamBat2 == result:
            result1 = 0
            result2 = 2
        else:
            result1 = 1
            result2 = 1

        inn1Row = 0
        allOut1 = 0
        allOut2 = 0
        allOut1Row = 0
        chase2 = 0
        for i in range(len(rows)-1):
            if allOut1 == 0:
                #print `dataTable[12*i+1 - 7*inn1Row]`
                overs = dataTable[12*i - 7*inn1Row]
                score1 = dataTable[12*i+1 - 7*inn1Row]
                runs1 = int(score1.split('/')[0])
                wkts1 = int(score1.split('/')[1])
                overRuns1 = dataTable[12*i+2 - 7*inn1Row]
                runRate1 = dataTable[12*i+3 - 7*inn1Row]
                ocId = `t20Id` + `1` + `int(overs)`
                print `ocId` + ' ' + `t20NumId` + ' ' +  teamBat1 + ' ' + `runs1` + ' ' + `wkts1` + ' ' + `overRuns1` + ' ' + `runRate1` + ' ' + `result1`
                conn = sqlite3.connect('ccrFT20.db')
                c = conn.cursor()
                c.execute('''insert or ignore into overComparison (ocId, t20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                          values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (ocId, t20NumId, 1, teamBat1, overs, runs1, wkts1, overRuns1, runRate1, None, None, None, None, result1))
                conn.commit()
                conn.close()
                conn = sqlite3.connect('ccrT20I.db')
                c = conn.cursor()
                c.execute('''insert or ignore into overComparison (ocId, t20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                          values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (ocId, t20NumId, 1, teamBat1, overs, runs1, wkts1, overRuns1, runRate1, None, None, None, None, result1))
                conn.commit()
                conn.close()
            if (chase2 == 1 or allOut2 == 1) and (wkts1 != 10 and int(overs) != 20):
                inn1Row = inn1Row + 1
                continue
            elif (chase2 == 0 and allOut2 == 0):
                if allOut1 == 0:
                    #print `12*i+5`
                    #print `dataTable[12*i+5]`
                    score2 = dataTable[12*i+5]
                    runs2 = int(score2.split('/')[0])
                    wkts2 = int(score2.split('/')[1])
                    overRuns2 = dataTable[12*i+6]
                    runRate2 = dataTable[12*i+7]
                    reqRate2 = dataTable[12*i+9]
                    runsReq2 = dataTable[12*i+10]
                    if int(runsReq2) == 0:
                        chase2 = 1
                    ballsRem2 = dataTable[12*i+11]
                    ocId = `t20Id` + `2` + `int(overs)`
                    print `ocId` + ' ' + `t20NumId` + ' ' +  teamBat2 + ' ' + `runs2` + ' ' + `wkts2` + ' ' + `overRuns2` + ' ' + `runRate2` + ' ' + `reqRate2`  + ' ' + `runsReq2`  + ' ' + `ballsRem2` + ' ' + `result2`
                    conn = sqlite3.connect('ccrFT20.db')
                    c = conn.cursor()
                    c.execute('''insert or ignore into overComparison (ocId, t20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (ocId, t20NumId, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect('ccrT20I.db')
                    c = conn.cursor()
                    c.execute('''insert or ignore into overComparison (ocId, t20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (ocId, t20NumId, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
                    conn.commit()
                    conn.close()
                else:
                    if allOut1Row == 0:
                        allOut1Row = i
                    #print `dataTable[12*allOut1Row+8*(i-allOut1Row)+5]`
                    score2 = dataTable[12*allOut1Row+8*(i-allOut1Row)+1]
                    runs2 = int(score2.split('/')[0])
                    wkts2 = int(score2.split('/')[1])
                    overRuns2 = dataTable[12*allOut1Row+8*(i-allOut1Row)+2]
                    runRate2 = dataTable[12*allOut1Row+8*(i-allOut1Row)+3]
                    reqRate2 = dataTable[12*allOut1Row+8*(i-allOut1Row)+5]
                    runsReq2 = dataTable[12*allOut1Row+8*(i-allOut1Row)+6]
                    if int(runsReq2) == 0:
                        chase2 = 1
                    ballsRem2 = dataTable[12*allOut1Row+8*(i-allOut1Row)+7]
                    ocId = `t20Id` + `2` + `int(overs)`
                    print `ocId` + ' ' + `t20NumId` + ' ' +  teamBat2 + ' ' + `runs2` + ' ' + `wkts2` + ' ' + `overRuns2` + ' ' + `runRate2` + ' ' + `reqRate2`  + ' ' + `runsReq2`  + ' ' + `ballsRem2` + ' ' + `result2`
                    conn = sqlite3.connect('ccrFT20.db')
                    c = conn.cursor()
                    c.execute('''insert or ignore into overComparison (ocId, t20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (ocId, t20NumId, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
                    conn.commit()
                    conn.close()
                    conn = sqlite3.connect('ccrT20I.db')
                    c = conn.cursor()
                    c.execute('''insert or ignore into overComparison (ocId, t20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (ocId, t20NumId, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
                    conn.commit()
                    conn.close()
            if wkts1 == 10:
                allOut1 = 1
            if wkts2 == 10:
                allOut2 = 1;
        t20NumId = t20NumId + 1
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()

# get ft20s info
c.execute('select * from ft20Info')
ft20sInfo = c.fetchall()
ignoreDL = (40, 41, 65, 66, 196, 226, 246, 267, 270, 271, 364, 484, 487, 497, 528)
  
# loop through ft20 matches
#for x in range(0, 1):
for x in range(0, len(ft20sInfo)):    
    ft20Id = ft20sInfo[x][0]
    if ft20Id in ignoreDL:
        continue
    result = ft20sInfo[x][6]
    
    overComparisonURL = 'http://www.espncricinfo.com' + ft20sInfo[x][9] + '?view=comparison'
    overComparisonPage = requests.get(overComparisonURL)
    scoreTree = html.fromstring(overComparisonPage.text)
    
    # parse all relevant fields from overComparison
    rows = scoreTree.xpath('(//div[@id="statsContainer"]/div/table/tbody/tr[@class="data1"])')
    dataTable = scoreTree.xpath('(//div[@id="statsContainer"]/div/table/tbody/tr[@class="data1"]/td/text())')
    
    c.execute('select innings, batTeam, bowlTeam from detailsFT20Innings where ft20Id=?', (ft20Id,))        
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
    for i in range(len(rows)):
        if allOut1 == 0:
            #print `dataTable[12*i+1 - 7*inn1Row]`
            overs = dataTable[12*i - 7*inn1Row]        
            score1 = dataTable[12*i+1 - 7*inn1Row]
            runs1 = int(score1.split('/')[0])
            wkts1 = int(score1.split('/')[1])            
            overRuns1 = dataTable[12*i+2 - 7*inn1Row]
            runRate1 = dataTable[12*i+3 - 7*inn1Row]
            ocId = `ft20Id` + `1` + `int(overs)`
            print `ocId` + ' ' + `ft20Id` + ' ' +  teamBat1 + ' ' + `runs1` + ' ' + `wkts1` + ' ' + `overRuns1` + ' ' + `runRate1` + ' ' + `result1`
            c.execute('''insert or ignore into overComparisonFT20 (ocId, ft20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                      values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (ocId, ft20Id, 1, teamBat1, overs, runs1, wkts1, overRuns1, runRate1, None, None, None, None, result1))
            conn.commit()
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
                ocId = `ft20Id` + `2` + `int(overs)`
                print `ocId` + ' ' + `ft20Id` + ' ' +  teamBat2 + ' ' + `runs2` + ' ' + `wkts2` + ' ' + `overRuns2` + ' ' + `runRate2` + ' ' + `reqRate2`  + ' ' + `runsReq2`  + ' ' + `ballsRem2` + ' ' + `result2`
                c.execute('''insert or ignore into overComparisonFT20 (ocId, ft20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                          values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (ocId, ft20Id, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
                conn.commit()
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
                ocId = `ft20Id` + `2` + `int(overs)`
                print `ocId` + ' ' + `ft20Id` + ' ' +  teamBat2 + ' ' + `runs2` + ' ' + `wkts2` + ' ' + `overRuns2` + ' ' + `runRate2` + ' ' + `reqRate2`  + ' ' + `runsReq2`  + ' ' + `ballsRem2` + ' ' + `result2`
                c.execute('''insert or ignore into overComparisonFT20 (ocId, ft20Id, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                          values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (ocId, ft20Id, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
                conn.commit()
        if wkts1 == 10:
            allOut1 = 1
        if wkts2 == 10:
            allOut2 = 1;                  
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()

# get t20is info
c.execute('select distinct t20iId from overComparisonT20I order by t20iId asc')
result = c.fetchall()

print `len(result)`
# loop through t20i matches
#for x in range(0, 1):
for x in range(0, len(result)):
    t20iId = result[x][0]
    c.execute('select ocId, overs, runs, wkts, result from overComparisonT20I where t20iId=? and innings=1', (t20iId, ))
    conn.commit()
    overComp = c.fetchall();
    for i in range(0, len(overComp)):
        ocId = overComp[i][0]
        overs = overComp[i][1]
        runs = overComp[i][2]
        wkts = overComp[i][3]        
        matchResult = overComp[i][4]
        c.execute('''select runs, wkts, result, t20iId from overComparisonT20I where t20iId<? and innings=1 and overs>=? and overs<? and runs<=? and runs>? and wkts>=? and wkts<?''',
                  (t20iId, overs, overs+2, runs, runs*0.9, wkts, wkts+2))
        comp = c.fetchall()
        similarCount = len(comp)        
        #print `similarCount`
        winCount = 0.0        
        for j in range(0, len(comp)):
            compRuns = comp[j][0]
            compWkts = comp[j][1]
            compResult = comp[j][2]
            winCount = winCount + int(compResult) / 2
        matchOdds = 100 * winCount / similarCount if similarCount > 0 else None
        print `t20iId` + ' Overs: ' + `overs` + ' Score: ' + `runs` + '/' + `wkts` + ' Result: ' + `matchResult` + ' Odds: ' + `matchOdds`
        c.execute('update overComparisonT20I set matchOdds=? where ocId=?', (matchOdds, ocId))
        conn.commit()
        
    c.execute('select ocId, overs, runs, wkts, runsReq, ballsRem, result from overComparisonT20I where t20iId=? and innings=2', (t20iId, ))
    conn.commit()
    overComp = c.fetchall();
    for i in range(0, len(overComp)):
        ocId = overComp[i][0]
        overs = overComp[i][1]
        runs = overComp[i][2]
        wkts = overComp[i][3]
        runsReq = overComp[i][4]
        ballsRem = overComp[i][5]
        matchResult = overComp[i][6]
        c.execute('''select runs, wkts, runsReq, ballsRem, result, t20iId from overComparisonT20I where t20iId<? and innings=2 and overs>=? and overs<? and runs<=? and runs>? and wkts>=? and wkts<? and
                  runsReq>=? and runsReq<? and ballsRem<=? and ballsRem>?''',
                  (t20iId, overs, overs+2, runs, runs*0.9, wkts, wkts+2, runsReq, runsReq*1.1, ballsRem, ballsRem*0.9))
        comp = c.fetchall()
        similarCount = len(comp)        
        #print `similarCount`
        winCount = 0.0        
        for j in range(0, len(comp)):
            compRuns = comp[j][0]
            compWkts = comp[j][1]
            compRunsReq = comp[j][2]
            compBallsRem = comp[j][3]
            compResult = comp[j][4]
            #print comp[j][5]
            winCount = winCount + int(compResult) / 2
        matchOdds = 100 * winCount / similarCount if similarCount > 0 else None
        matchOdds = 100.0 if runsReq == 0 else matchOdds
        print `t20iId` + ' Overs: ' + `overs` + ' Score: ' + `runs` + '/' + `wkts` + ' RunsReq: ' + `runsReq` + ' BallsRem: ' + `ballsRem` + ' Result: ' + `matchResult` + ' Odds: ' + `matchOdds`
        c.execute('update overComparisonT20I set matchOdds=? where ocId=?', (matchOdds, ocId))
        conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
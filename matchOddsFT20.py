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
c.execute('select distinct ft20Id from overComparisonFT20 order by ft20Id asc')
result = c.fetchall()

print `len(result)`
# loop through ft20 matches
#for x in range(0, 1):
for x in range(548, len(result)):
    ft20Id = result[x][0]
    c.execute('select ocId, overs, runs, wkts, result from overComparisonFT20 where ft20Id=? and innings=1', (ft20Id, ))
    conn.commit()
    overComp = c.fetchall();
    for i in range(0, len(overComp)):
        ocId = overComp[i][0]
        overs = overComp[i][1]
        runs = overComp[i][2]
        wkts = overComp[i][3]        
        matchResult = overComp[i][4]
        c.execute('''select runs, wkts, result, ft20Id from overComparisonFT20 where ft20Id<? and innings=1 and overs>=? and overs<? and runs<=? and runs>? and wkts>=? and wkts<?''',
                  (ft20Id, overs, overs+2, runs, runs*0.9, wkts, wkts+2))
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
        print `ft20Id` + ' Overs: ' + `overs` + ' Score: ' + `runs` + '/' + `wkts` + ' Result: ' + `matchResult` + ' Odds: ' + `matchOdds`
        c.execute('update overComparisonFT20 set matchOdds=? where ocId=?', (matchOdds, ocId))
        conn.commit()
        
    c.execute('select ocId, overs, runs, wkts, runsReq, ballsRem, result from overComparisonFT20 where ft20Id=? and innings=2', (ft20Id, ))
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
        c.execute('''select runs, wkts, runsReq, ballsRem, result, ft20Id from overComparisonFT20 where ft20Id<? and innings=2 and overs>=? and overs<? and runs<=? and runs>? and wkts>=? and wkts<? and
                  runsReq>=? and runsReq<? and ballsRem<=? and ballsRem>?''',
                  (ft20Id, overs, overs+2, runs, runs*0.9, wkts, wkts+2, runsReq, runsReq*1.1, ballsRem, ballsRem*0.9))
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
        print `ft20Id` + ' Overs: ' + `overs` + ' Score: ' + `runs` + '/' + `wkts` + ' RunsReq: ' + `runsReq` + ' BallsRem: ' + `ballsRem` + ' Result: ' + `matchResult` + ' Odds: ' + `matchOdds`
        c.execute('update overComparisonFT20 set matchOdds=? where ocId=?', (matchOdds, ocId))
        conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
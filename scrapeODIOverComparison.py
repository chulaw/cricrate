#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

# get odis info
c.execute('select * from odiInfo')
odisInfo = c.fetchall()
ignoreDL = (1724, 1782, 1832, 1839, 1843, 1851, 1873, 1880, 1888, 1889, 1895, 1901, 1904, 1913, 1942, 1943, 1955, 1956, 1979, 1980, 1982, 1991, 2007, 2011, 2024, 2031, 2043, 2048, 2051, 2065, 2069, 2085, 2086,
            2091, 2092, 2107, 2119, 2121, 2132, 2134, 2141, 2159, 2177, 2205, 2208, 2216, 2225, 2230, 2242, 2256, 2271, 2272, 2292, 2293, 2324, 2351, 2372, 2401, 2405, 2408, 2414, 2416, 2472, 2497, 2514, 2517,
            2519, 2532, 2551, 2581, 2590, 2601, 2602, 2603, 2618, 2621, 2656, 2659, 2670, 2672, 2676, 2677, 2683, 2684, 2699, 2701, 2709, 2712, 2719, 2741, 2743, 2753, 2761, 2767, 2778, 2786, 2789, 2792, 2807,
            2820, 2821, 2822, 2824, 2826, 2828, 2831, 2835, 2855, 2860, 2861, 2877, 2878, 2880, 2893, 2897, 2901, 2908, 2936, 2954, 3009, 3020, 3037, 3041, 3051, 3084, 3088, 3092, 3119, 3155, 3185, 3186, 3191,
            3227, 3271, 3274, 3279, 3296, 3305, 3308, 3324, 3351, 3369, 3371, 3394, 3405, 3414, 3422, 3423, 3432, 3434, 3435, 3444, 3452, 3459, 3499, 3503, 3538, 3580, 3592, 3629, 3650, 3653, 3655, 3686,
            3718, 3732, 3750, 3755, 3759)
#2237, 2243, 2268 extra over (51)

# loop through odi matches
for x in range(3759, len(odisInfo)):
    odiId = odisInfo[x][0]
    if odiId in ignoreDL:
        continue
    print odiId
    result = odisInfo[x][8]

    overComparisonURL = 'http://www.espncricinfo.com' + odisInfo[x][12] + '?view=comparison'
    print overComparisonURL
    overComparisonPage = requests.get(overComparisonURL)
    scoreTree = html.fromstring(overComparisonPage.text)

    # parse all relevant fields from overComparison
    rows = scoreTree.xpath('(//div[@id="stats-container"]/div/table/tbody/tr)')
    dataTable = scoreTree.xpath('(//div[@id="stats-container"]/div/table/tbody/tr/td/text())')

    c.execute('select innings, batTeam, bowlTeam from detailsODIInnings where odiId=?', (odiId,))
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
            #print `inn1Row`
            #print `dataTable[12*i+1 - 7*inn1Row]`
            overs = dataTable[12*i - 7*inn1Row]
            score1 = dataTable[12*i+1 - 7*inn1Row]
            runs1 = int(score1.split('/')[0])
            wkts1 = int(score1.split('/')[1])
            overRuns1 = dataTable[12*i+2 - 7*inn1Row]
            runRate1 = dataTable[12*i+3 - 7*inn1Row]
            ocId = `odiId` + `1` + `int(overs)`
            print `ocId` + ' ' + `odiId` + ' ' +  teamBat1 + ' ' + `runs1` + ' ' + `wkts1` + ' ' + `overRuns1` + ' ' + `runRate1` + ' ' + `result1`
            c.execute('''insert or ignore into overComparisonODI (ocId, odiId, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                      values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (ocId, odiId, 1, teamBat1, overs, runs1, wkts1, overRuns1, runRate1, None, None, None, None, result1))
            conn.commit()
        if (chase2 == 1 or allOut2 == 1) and (wkts1 != 10 and int(overs) != 50):
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
                ocId = `odiId` + `2` + `int(overs)`
                print `ocId` + ' ' + `odiId` + ' ' +  teamBat2 + ' ' + `runs2` + ' ' + `wkts2` + ' ' + `overRuns2` + ' ' + `runRate2` + ' ' + `reqRate2`  + ' ' + `runsReq2`  + ' ' + `ballsRem2` + ' ' + `result2`
                c.execute('''insert or ignore into overComparisonODI (ocId, odiId, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                          values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (ocId, odiId, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
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
                print runsReq2
                if int(runsReq2) == 0:
                    chase2 = 1
                ballsRem2 = dataTable[12*allOut1Row+8*(i-allOut1Row)+7]
                ocId = `odiId` + `2` + `int(overs)`
                print `ocId` + ' ' + `odiId` + ' ' +  teamBat2 + ' ' + `runs2` + ' ' + `wkts2` + ' ' + `overRuns2` + ' ' + `runRate2` + ' ' + `reqRate2`  + ' ' + `runsReq2`  + ' ' + `ballsRem2` + ' ' + `result2`
                c.execute('''insert or ignore into overComparisonODI (ocId, odiId, innings, teamBat, overs, runs, wkts, overRuns, runRate, reqRate, runsReq, ballsRem, matchOdds, result)
                          values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (ocId, odiId, 2, teamBat2, overs, runs2, wkts2, overRuns2, runRate2, reqRate2, runsReq2, ballsRem2, None, result2))
                conn.commit()
        if wkts1 == 10:
            allOut1 = 1
        if wkts2 == 10:
            allOut2 = 1
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

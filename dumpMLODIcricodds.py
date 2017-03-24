#!/usr/bin/env python
import time
import sqlite3
import csv
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

# get odis info
c.execute('select distinct odiId from overComparisonODI order by odiId asc')
result = c.fetchall()

fd1 = open('odiML1cricodds.csv','a')
fd1.write("Id,Overs,SimilarCount,MatchOdds,MatchOddsAdj,Result\n")
fd1.close()

fd2 = open('odiML2cricodds.csv','a')
fd2.write("Id,Overs,SimilarCount,MatchOdds,MatchOddsAdj,Result\n")
fd2.close()

# loop through odi matches
for x in range(0, len(result)):
    odiId = result[x][0]
    #if odiId < 3315: continue
    print odiId
    c.execute('select startDate from odiInfo where odiId=?',(odiId,))
    odiDate = c.fetchone()
    odiDate = odiDate[0]

    c.execute('select batTeam from detailsODIInnings where odiId=? and innings=1',(odiId,))
    team1 = c.fetchone()
    team1 = team1[0] if team1 != None else None

    c.execute('select batTeam, balls from detailsODIInnings where odiId=? and innings=2',(odiId,))
    team2 = c.fetchone()
    team2 = team2[0] if team2 != None else None

    team1StartingOdds = 0.5
    team2StartingOdds = 0.5
    team1Rating = 100.0
    team2Rating = 100.0
    if team1 != None and team2 != None:
        c.execute('select rating from teamODILive where team=? and startDate<?',(team1, odiDate))
        team1Rating = c.fetchall()
        if len(team1Rating) > 0:
            team1Rating = team1Rating[len(team1Rating)-1][0]
        else:
            team1Rating = 100.0

        c.execute('select rating from teamODILive where team=? and startDate<?',(team2, odiDate))
        team2Rating = c.fetchall()
        if len(team2Rating) > 0:
            team2Rating = team2Rating[len(team2Rating)-1][0]
        else:
            team2Rating = 100.0

        team1StartingOdds = team1Rating / (team1Rating + team2Rating)
        team2StartingOdds = 1 - team1StartingOdds

    c.execute('select overs, runs, wkts, result from overComparisonODI where odiId=? and innings=1', (odiId, ))
    overComp = c.fetchall()
    fd1 = open('odiML1cricodds.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        runs = overComp[i][1]
        wkts = overComp[i][2]
        matchResult = overComp[i][3]/2
        if runs == 0:
            c.execute('select avg(result), odiId from overComparisonODI where odiId<'+`odiId`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runs<=1 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' group by odiId')
        else:
            c.execute('select avg(result), odiId from overComparisonODI where odiId<'+`odiId`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' group by odiId')

        comp = c.fetchall()
        similarCount = len(comp)
        winCount = 0.0
        for j in range(0, len(comp)):
            compOdiId = comp[j][1]
            compResult = comp[j][0]
            winCount = winCount + int(compResult) / 2
        matchOdds = 100 * winCount / similarCount if similarCount > 0 else None

        matchOddsAdj = None
        if matchOdds != None:
            matchOdds = matchOdds / 100.0
            oddsDiff = matchOdds - (1 - matchOdds)
            matchOddsAdj = matchOdds

            # team current ratings adjustment
            if team1StartingOdds >= 0.5:
                oddsAdj = team1StartingOdds - 0.5
                if matchOdds >= 0.5:
                    matchOddsAdj = matchOdds - oddsAdj * oddsDiff + oddsAdj
                else:
                    matchOddsAdj = matchOdds + oddsAdj * oddsDiff + oddsAdj
            elif team1StartingOdds < 0.5:
                oddsAdj = 0.5 - team1StartingOdds
                if matchOdds >= 0.5:
                    matchOddsAdj = matchOdds + oddsAdj * oddsDiff - oddsAdj
                else:
                    matchOddsAdj = matchOdds - oddsAdj * oddsDiff - oddsAdj
            matchOddsAdj = 100.0 * matchOddsAdj
            #print "team1: " + team1 + ", startOdds: " + `team1StartingOdds` + ", odds: " + `matchOdds` + ", oddsAdj: " + `matchOddsAdj`

            if matchOddsAdj > 100: matchOddsAdj = 100.0
            if matchOddsAdj < 0: matchOddsAdj = 0.0

        fd1.write(`odiId` + ","  + `overs` + "," + `similarCount` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult` + "\n")
    fd1.close()

    c.execute('select overs, runs, wkts, runsReq, ballsRem, result from overComparisonODI where odiId=? and innings=2', (odiId, ))
    overComp = c.fetchall()
    fd2 = open('odiML2cricodds.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        runs = overComp[i][1]
        wkts = overComp[i][2]
        runsReq = overComp[i][3]
        ballsRem = overComp[i][4]
        matchResult = overComp[i][5]/2
        c.execute('select avg(result), odiId from overComparisonODI where odiId<'+`odiId`+' and innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`+' group by odiId')

        comp = c.fetchall()
        similarCount = len(comp)

        if ballsRem < 60 and similarCount < 10:
            c.execute('select avg(result), odiId from overComparisonODI where odiId<'+`odiId`+' and innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`+' group by odiId')
            comp = c.fetchall()
            similarCount = len(comp)

        winCount = 0.0
        for j in range(0, len(comp)):
            compOdiId = comp[j][1]
            compResult = comp[j][0]
            winCount = winCount + int(compResult) / 2
        matchOdds = 100 * winCount / similarCount if similarCount > 0 else None
        matchOdds = 100.0 if runsReq == 0 else matchOdds
        matchOdds = 0.0 if int(overs) == 50 and runsReq != 0 else matchOdds
        matchOdds = 0.0 if int(wkts) == 10 and runsReq != 0 else matchOdds

        matchOddsAdj = None
        if matchOdds != None:
            matchOdds = matchOdds / 100.0
            oddsDiff = matchOdds - (1 - matchOdds)
            matchOddsAdj = matchOdds

            # team current ratings adjustment
            if team2StartingOdds >= 0.5:
                oddsAdj = team2StartingOdds - 0.5
                if matchOdds >= 0.5:
                    matchOddsAdj = matchOdds - oddsAdj * oddsDiff + oddsAdj
                else:
                    matchOddsAdj = matchOdds + oddsAdj * oddsDiff + oddsAdj
            elif team2StartingOdds < 0.5:
                oddsAdj = 0.5 - team2StartingOdds
                if matchOdds >= 0.5:
                    matchOddsAdj = matchOdds + oddsAdj * oddsDiff - oddsAdj
                else:
                    matchOddsAdj = matchOdds - oddsAdj * oddsDiff - oddsAdj
            matchOddsAdj = 100.0 * matchOddsAdj
            # print "team2: " + team2 + ", startOdds: " + `team2StartingOdds` + ", odds: " + `matchOdds` + ", oddsAdj: " + `matchOddsAdj`

            if matchOddsAdj > 100: matchOddsAdj = 100.0
            if matchOddsAdj < 0: matchOddsAdj = 0.0

        fd2.write(`odiId` + ","  + `overs` + "," + `similarCount` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult` + "\n")
    fd1.close()
    fd2.close()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

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

# loop through odi matches
#for x in range(0, 1):
#fd1 = open('odiML1.csv','a')
#fd1.write("Id,Overs,Runs,Wkts,Team1Rating,Team2Rating,ExpRuns1,ExpRuns2,RuleChg,HomeAway,Momentum,MatchOdds,MatchOddsAdj,Result\n")
#fd1.close()

#fd2 = open('odiML2.csv','a')
#fd2.write("Id,Overs,Runs,Wkts,RunsReq,BallsRem,Team1Rating,Team2Rating,ExpRuns1,ExpRuns2,RuleChg,HomeAway,Momentum,MatchOdds,MatchOddsAdj,Result\n")
#fd2.close()
for x in range(0, len(result)):
    odiId = result[x][0]
    if odiId < 3449: continue
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

    # Find weighted average expected runs scored at ground for 1st and 2nd innings
    c.execute('select ground from odiInfo where odiId=?',(odiId,))
    ground = c.fetchone()
    ground = ground[0] if ground != None else None

    if ground != None:
        c.execute('select odiId from odiInfo where ground=? and odiId<?',(ground, odiId))
        groundMatches = c.fetchall()
        groundMatches = groundMatches if groundMatches != None else None

    matchingOdis = ""
    for g in range(0, len(groundMatches)):
         matchingOdis = matchingOdis + `groundMatches[g][0]` + ", "
    matchingOdis = matchingOdis[:-2]

    c.execute('select odiId, runs from detailsODIInnings where innings=1 and runs>149 and odiId in (' + matchingOdis + ')')
    runs1st = c.fetchall()
    runs1st = runs1st if runs1st != None else None

    c.execute('select odiId, runs from detailsODIInnings where innings=2 and runs>149 and odiId in (' + matchingOdis + ')')
    runs2nd = c.fetchall()
    runs2nd = runs2nd if runs2nd != None else None

    expRuns1st = 0
    if runs1st != None:
        distSum = 0.0
        compDist = {}
        compRuns = {}
        compWeight = {}
        for r in range(0, len(runs1st)):
            compOdiId = runs1st[r][0]
            compRuns[compOdiId] = runs1st[r][1]
            compDist[compOdiId] = odiId - compOdiId
            distSum += compDist[compOdiId]

        weightSum = 0.0
        for d in compDist:
            compWeight[d] = distSum / compDist[d]
            weightSum += compWeight[d]

        for w in compWeight:
            expRuns1st += (compWeight[w] / weightSum) * compRuns[w]

    expRuns2nd = 0
    if runs2nd != None:
        distSum = 0.0
        compDist = {}
        compRuns = {}
        compWeight = {}
        for r in range(0, len(runs2nd)):
            compOdiId = runs2nd[r][0]
            compRuns[compOdiId] = runs2nd[r][1]
            compDist[compOdiId] = odiId - compOdiId
            distSum += compDist[compOdiId]

        weightSum = 0.0
        for d in compDist:
            compWeight[d] = distSum / compDist[d]
            weightSum += compWeight[d]

        for w in compWeight:
            expRuns2nd += (compWeight[w] / weightSum) * compRuns[w]

    # Check if match is home/away/neutral
    c.execute('select location from odiInfo where odiId=?',(odiId,))
    location = c.fetchone()
    location = location[0] if location != None else None

    team1Home = 0.0
    team2Home = 0.0
    if team1 == location:
        team1Home = 1.0
        team2Home = -1.0
    elif team2 == location:
        team1Home = -1.0
        team2Home = 1.0

    c.execute('select overs, runs, wkts, result from overComparisonODI where odiId=? and innings=1', (odiId, ))
    overComp = c.fetchall()
    last3OversOdds = []
    fd1 = open('odiML1.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        runs = overComp[i][1]
        wkts = overComp[i][2]
        matchResult = overComp[i][3]/2
        if runs == 0:
            c.execute('select result, odiId from overComparisonODI where odiId<'+`odiId`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runs<=1 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
        else:
            c.execute('select result, odiId from overComparisonODI where odiId<'+`odiId`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)

        comp = c.fetchall()
        similarCount = len(comp)
        winCount = 0.0
        for j in range(0, len(comp)):
            compOdiId = comp[j][1]
            compResult = comp[j][0]
            winCount = winCount + int(compResult) / 2
        matchOdds = 100 * winCount / similarCount if similarCount > 0 else None

        matchOddsAdj = None
        momentum = 0.0
        momentumAdj = 0.0
        ruleChg = 1.0
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

            # odi rule change adjustment
            if odiId >= 2203 and odiId <= 3309:
                ruleChg = 2.0
                matchOddsAdj = matchOddsAdj - min(matchOddsAdj * 0.075, 10.0)
            if odiId > 3309 and odiId <= 3361:
                ruleChg = 3.0
                matchOddsAdj = matchOddsAdj - min(matchOddsAdj * 0.15, 10.0)
            if odiId > 3661:
                ruleChg = 4.0
                matchOddsAdj = matchOddsAdj - min(matchOddsAdj * 0.1125, 10.0)
            if matchOddsAdj < 0.0: matchOddsAdj = 0.0

            # ground average runs adjustment
            if expRuns1st != 0 and expRuns2nd != 0 and overs < 44 and overs > 1:
                adjRuns1st = (0.0166 * overs - 0.0142) * expRuns1st if overs <= 35 else (0.0007 * overs**2 - 0.0315 * overs + 0.825) * expRuns1st
                matchOddsAdj = matchOddsAdj + 5.0 * float(adjRuns1st - runs) / float(adjRuns1st) * float(50 - overs) / 50.0
                if matchOddsAdj > 100.0: matchOddsAdj = 100.0
                if matchOddsAdj < 0.0: matchOddsAdj = 0.0

            # home/away adjustment
            matchOddsAdj = matchOddsAdj + min(matchOddsAdj * 0.1, 7.5) * team1Home
            if matchOddsAdj > 100.0: matchOddsAdj = 100.0
            if matchOddsAdj < 0.0: matchOddsAdj = 0.0

            # # momentum adjustment
            if len(last3OversOdds) < 3:
                last3OversOdds.append(matchOddsAdj)
            else:
                for o in range(0, len(last3OversOdds)):
                    if o == 0:
                        continue
                    else:
                        if last3OversOdds[o] != None and last3OversOdds[o-1] != None:
                            momentum += last3OversOdds[o] - last3OversOdds[o-1]

                last3OversOdds.pop(0)
                last3OversOdds.append(matchOddsAdj)

            if momentum >= 15:
                momentumAdj = 3.0
            elif momentum < -15:
                momentumAdj = -3.0
            else:
                momentumAdj = momentum / 5.0

            matchOddsAdj = matchOddsAdj + momentumAdj
            if matchOddsAdj > 100: matchOddsAdj = 100.0
            if matchOddsAdj < 0: matchOddsAdj = 0.0

        #print `odiId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `team1Rating` + "," + `team2Rating` + "," + `expRuns1st` + "," + `expRuns2nd` + "," + `ruleChg` + "," + `team1Home` + "," + `momentum` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult`
        fd1.write(`odiId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `team1Rating` + "," + `team2Rating` + "," + `expRuns1st` + "," + `expRuns2nd` + "," + `ruleChg` + "," + `team1Home` + "," + `momentum` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult` + "\n")
    fd1.close()

    c.execute('select overs, runs, wkts, runsReq, ballsRem, result from overComparisonODI where odiId=? and innings=2', (odiId, ))
    overComp = c.fetchall()
    last3OversOdds = []
    fd2 = open('odiML2.csv','a')
    for i in range(0, len(overComp)):
        overs = overComp[i][0]
        runs = overComp[i][1]
        wkts = overComp[i][2]
        runsReq = overComp[i][3]
        ballsRem = overComp[i][4]
        matchResult = overComp[i][5]/2
        c.execute('select result, odiId from overComparisonODI where odiId<'+`odiId`+' and innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`)

        comp = c.fetchall()
        similarCount = len(comp)

        if ballsRem < 60 and similarCount < 10:
            c.execute('select result, odiId from overComparisonODI where odiId<'+`odiId`+' and innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
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
        momentum = 0.0
        momentumAdj = 0.0
        ruleChg = 1.0
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

            # odi rule change adjustment
            if odiId >= 2203 and odiId <= 3309:
                ruleChg = 2.0
                matchOddsAdj = matchOddsAdj + min(matchOddsAdj * 0.075, 10.0)
            if odiId > 3309 and odiId <= 3361:
                ruleChg = 3.0
                matchOddsAdj = matchOddsAdj + min(matchOddsAdj * 0.15, 10.0)
            if odiId > 3661:
                ruleChg = 4.0
                matchOddsAdj = matchOddsAdj + min(matchOddsAdj * 0.1125, 10.0)
            if matchOddsAdj > 100.0: matchOddsAdj = 100.0

            runsToChase = runs + runsReq
            if expRuns1st != 0 and expRuns2nd != 0 and overs < 44:
                adjRuns2nd = expRuns2nd * float(runsToChase - 1) / float(expRuns1st)
                matchOddsAdj = matchOddsAdj + 5.0 * float(adjRuns2nd - runsToChase) / float(runsToChase) * float(50 - overs) / 50.0
                if matchOddsAdj > 100.0: matchOddsAdj = 100.0
                if matchOddsAdj < 0.0: matchOddsAdj = 0.0

            # home/away adjustment
            matchOddsAdj = matchOddsAdj + min(matchOddsAdj * 0.1, 5.0) * team2Home
            if matchOddsAdj > 100.0: matchOddsAdj = 100.0
            if matchOddsAdj < 0.0: matchOddsAdj = 0.0

            # # momentum adjustment
            if len(last3OversOdds) < 3:
                last3OversOdds.append(matchOddsAdj)
            else:
                for o in range(0, len(last3OversOdds)):
                    if o == 0:
                        continue
                    else:
                        if last3OversOdds[o] != None and last3OversOdds[o-1] != None:
                            momentum += last3OversOdds[o] - last3OversOdds[o-1]

                last3OversOdds.pop(0)
                last3OversOdds.append(matchOddsAdj)

            if momentum >= 15:
                momentumAdj = 3.0
            elif momentum < -15:
                momentumAdj = -3.0
            else:
                momentumAdj = momentum / 5.0

            matchOddsAdj = matchOddsAdj + momentumAdj
            if matchOddsAdj > 100: matchOddsAdj = 100.0
            if matchOddsAdj < 0: matchOddsAdj = 0.0

        #print `odiId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `ballsRem` + "," + `team1Rating` + "," + `team2Rating` + "," + `expRuns1st` + "," + `expRuns2nd` + "," + `ruleChg` + "," + `team1Home` + "," + `momentum` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult`
        fd2.write(`odiId` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `ballsRem` + "," + `team1Rating` + "," + `team2Rating` + "," + `expRuns1st` + "," + `expRuns2nd` + "," + `ruleChg` + "," + `team1Home` + "," + `momentum` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult` + "\n")
    fd1.close()
    fd2.close()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
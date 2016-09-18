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
ignoreFT20DL = (40, 41, 65, 66, 196, 226, 246, 267, 270, 271, 364, 484, 487, 497, 528, 601, 619, 644, 673, 683, 709, 716, 731)
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
ignoreT20IDL = (11, 26, 70, 119, 124, 157, 159, 160, 231, 242, 247, 252, 260, 270, 273, 290, 300, 318, 335, 340, 373, 380, 398, 404, 422)
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

t20NumId = 0
for startDate in startDates:
    matches = [i for i, item in enumerate(t20Info) if re.search(str(startDate), item)]
    for key in matches:
        oddsOvers = []
        oddsOdds = []
        oddsResult = []
        t20Id = t20Info[key]
        team1StartingOdds = 0.5
        team2StartingOdds = 0.5
        if "F" in t20Id:
            conn = sqlite3.connect('ccrFT20.db')
            c = conn.cursor()
            matchId = t20Id[:t20Id.index("F")]
            c.execute('select startDate from ft20Info where ft20Id=?',(matchId,))
            matchDate = c.fetchone()
            matchDate = matchDate[0]

            c.execute('select batTeam from detailsFT20Innings where ft20Id=? and innings=1',(matchId,))
            team1 = c.fetchone()
            team1 = team1[0] if team1 != None else None

            c.execute('select batTeam, balls from detailsFT20Innings where ft20Id=? and innings=2',(matchId,))
            team2 = c.fetchone()
            team2 = team2[0] if team2 != None else None

            if team1 != None and team2 != None:
                c.execute('select rating from teamFT20Live where team=? and startDate<?',(team1, matchDate))
                team1Rating = c.fetchall()
                if len(team1Rating) > 0:
                    team1Rating = team1Rating[len(team1Rating)-1][0]
                else:
                    team1Rating = 100.0

                c.execute('select rating from teamFT20Live where team=? and startDate<?',(team2, matchDate))
                team2Rating = c.fetchall()
                if len(team2Rating) > 0:
                    team2Rating = team2Rating[len(team2Rating)-1][0]
                else:
                    team2Rating = 100.0
            conn.close()
        else:
            conn = sqlite3.connect('ccrT20I.db')
            c = conn.cursor()
            matchId = t20Id[:t20Id.index("I")]
            c.execute('select startDate from t20iInfo where t20iId=?',(matchId,))
            matchDate = c.fetchone()
            matchDate = matchDate[0]

            c.execute('select batTeam from detailsT20IInnings where t20iId=? and innings=1',(matchId,))
            team1 = c.fetchone()
            team1 = team1[0] if team1 != None else None

            c.execute('select batTeam, balls from detailsT20IInnings where t20iId=? and innings=2',(matchId,))
            team2 = c.fetchone()
            team2 = team2[0] if team2 != None else None

            if team1 != None and team2 != None:
                c.execute('select rating from teamT20ILive where team=? and startDate<?',(team1, matchDate))
                team1Rating = c.fetchall()
                if len(team1Rating) > 0:
                    team1Rating = team1Rating[len(team1Rating)-1][0]
                else:
                    team1Rating = 100.0

                c.execute('select rating from teamT20ILive where team=? and startDate<?',(team2, matchDate))
                team2Rating = c.fetchall()
                if len(team2Rating) > 0:
                    team2Rating = team2Rating[len(team2Rating)-1][0]
                else:
                    team2Rating = 100.0
            conn.close()

        conn = sqlite3.connect('ccrFT20.db')
        c = conn.cursor()
        team1StartingOdds = team1Rating / (team1Rating + team2Rating)
        team2StartingOdds = 1 - team1StartingOdds

        c.execute('select ocId, overs, runs, wkts, result from overComparison where t20Id=? and innings=1', (t20NumId, ))
        conn.commit()
        overComp = c.fetchall();
        for i in range(0, len(overComp)):
            ocId = overComp[i][0]
            overs = overComp[i][1]
            runs = overComp[i][2]
            wkts = overComp[i][3]
            matchResult = overComp[i][4]

            if runs == 0:
                c.execute('select result from overComparison where t20Id<'+`t20NumId`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runs<=1 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
            else:
                c.execute('select result from overComparison where t20Id<'+`t20NumId`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)

            comp = c.fetchall()
            similarCount = len(comp)
            winCount = 0.0
            for j in range(0, len(comp)):
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

            oddsOvers.append(overs)
            oddsOdds.append(matchOddsAdj)
            oddsResult.append(matchResult)

            # print `t20Id` + ' Overs: ' + `overs` + ' Score: ' + `runs` + '/' + `wkts` + ' Result: ' + `matchResult` + ' Odds: ' + `matchOdds`
            # c.execute('update overComparison set matchOdds=? where ocId=?', (matchOdds, ocId))
            # conn.commit()

        fd = open('t20Odds.csv','a')
        for oo in range(len(oddsOvers)):
            print `t20NumId` + ",1,"  + `oddsOvers[oo]` + "," + `oddsOdds[oo]` + "," + `oddsResult[oo]`
            fd.write(`t20NumId` + ",1,"  + `oddsOvers[oo]` + "," + `oddsOdds[oo]` + "," + `oddsResult[oo]` + "\n")
        fd.close()

        oddsOvers = []
        oddsOdds = []
        oddsResult = []
        c.execute('select ocId, overs, runs, wkts, runsReq, ballsRem, result from overComparison where t20Id=? and innings=2', (t20NumId, ))
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

            if ballsRem < 30:
                c.execute('select result from overComparison where t20Id<'+`t20NumId`+' and innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
            else:
                c.execute('select result from overComparison where t20Id<'+`t20NumId`+' and innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`)

            comp = c.fetchall()
            similarCount = len(comp)
            winCount = 0.0
            for j in range(0, len(comp)):
                compResult = comp[j][0]
                winCount = winCount + int(compResult) / 2
            matchOdds = 100 * winCount / similarCount if similarCount > 0 else None
            matchOdds = 100.0 if runsReq == 0 else matchOdds
            matchOdds = 0.0 if int(overs) == 20 and runsReq != 0 else matchOdds
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

            # print `t20Id` + ' Overs: ' + `overs` + ' Score: ' + `runs` + '/' + `wkts` + ' RunsReq: ' + `runsReq` + ' BallsRem: ' + `ballsRem` + ' Result: ' + `matchResult` + ' Odds: ' + `matchOdds`
            # c.execute('update overComparison set matchOdds=? where ocId=?', (matchOdds, ocId))
            # conn.commit()

            oddsOvers.append(overs)
            oddsOdds.append(matchOddsAdj)
            oddsResult.append(matchResult)

        fd = open('t20Odds.csv','a')
        for oo in range(len(oddsOvers)):
            print `t20NumId` + ",2,"  + `oddsOvers[oo]` + "," + `oddsOdds[oo]` + "," + `oddsResult[oo]`
            fd.write(`t20NumId` + ",2,"  + `oddsOvers[oo]` + "," + `oddsOdds[oo]` + "," + `oddsResult[oo]` + "\n")
        fd.close()

        t20NumId += 1
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
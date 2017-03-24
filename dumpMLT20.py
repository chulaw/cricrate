#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import re
import datetime
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

fd1 = open('t20ML1UnqRRHMLT.csv','a')
fd1.write("Id,T20I,Overs,Runs,Wkts,Team1Rating,Team2Rating,BattingRating,BowlingRating,HomeAway,Momentum,MatchOdds,MatchOddsAdj,Result\n")
fd1.close()

fd2 = open('t20ML2UnqRRHMLT.csv','a')
fd2.write("Id,T20I,Overs,Runs,Wkts,RunsReq,BallsRem,Team1Rating,Team2Rating,BattingRating,BowlingRating,HomeAway,Momentum,MatchOdds,MatchOddsAdj,Result\n")
fd2.close()
t20NumId = 1
for startDate in startDates:
    matches = [i for i, item in enumerate(t20Info) if re.search(str(startDate), item)]
    for key in matches:
        t20Id = t20Info[key]
        print `t20NumId` + " " + `t20Id`
        team1StartingOdds = 0.5
        team2StartingOdds = 0.5
        team1Home = 0.0
        team2Home = 0.0
        team1BattingRating = 0.0
        team2BowlingRating = 0.0
        team2BattingRating = 0.0
        team1BowlingRating = 0.0
        battingWktWeight = [0.15, 0.15, 0.15, 0.15, 0.125, 0.1, 0.075, 0.05, 0.025, 0.025]
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
                    team1Rating = 500.0

                c.execute('select rating from teamFT20Live where team=? and startDate<?',(team2, matchDate))
                team2Rating = c.fetchall()
                if len(team2Rating) > 0:
                    team2Rating = team2Rating[len(team2Rating)-1][0]
                else:
                    team2Rating = 500.0

                d = datetime.datetime(int(matchDate[0:4]), int(matchDate[4:-2]), int(matchDate[6:]))
                date2yAgo = d + datetime.timedelta(days=-720)
                date2yAgo = date2yAgo.strftime('%Y%m%d')

                c.execute('select b.playerId, b.ft20Id from battingFT20Live b, playerInfo p where p.playerId=b.playerId and p.teams like ? and b.startDate>? and b.startDate<?', ('%'+team1+'%', date2yAgo, matchDate))
                playerFT20s = c.fetchall()
                playerLastFT20 = {}
                for i in range(0, len(playerFT20s)):
                    pid = playerFT20s[i][0]
                    pFT20Id = playerFT20s[i][1]
                    if pid in playerLastFT20:
                        if pFT20Id > playerLastFT20[pid]:
                            playerLastFT20[pid] = pFT20Id
                    else:
                        playerLastFT20[pid] = pFT20Id

                battingRating = []
                for pid in playerLastFT20:
                    c.execute('select player, rating from battingFT20Live where playerId=? and ft20Id=?', (pid, playerLastFT20[pid]))
                    pRating = c.fetchone()
                    battingRating.append(pRating[1])
                battingRating = sorted(battingRating, reverse=True)

                if len(battingRating) >= 7:
                    for b in range(0, 7):
                        team1BattingRating += battingRating[b]
                    team1BattingRating = team1BattingRating / 7 * 5

                c.execute('select b.playerId, b.ft20Id from bowlingFT20Live b, playerInfo p where p.playerId=b.playerId and p.teams like ? and b.startDate>? and b.startDate<?', ('%'+team2+'%', date2yAgo, matchDate))
                playerFT20s = c.fetchall()
                playerLastFT20 = {}
                for i in range(0, len(playerFT20s)):
                    pid = playerFT20s[i][0]
                    pFT20Id = playerFT20s[i][1]
                    if pid in playerLastFT20:
                        if pFT20Id > playerLastFT20[pid]:
                            playerLastFT20[pid] = pFT20Id
                    else:
                        playerLastFT20[pid] = pFT20Id

                bowlingRating = []
                for pid in playerLastFT20:
                    c.execute('select player, rating from bowlingFT20Live where playerId=? and ft20Id=?', (pid, playerLastFT20[pid]))
                    pRating = c.fetchone()
                    bowlingRating.append(pRating[1])
                bowlingRating = sorted(bowlingRating, reverse=True)

                if len(bowlingRating) >= 5:
                    for b in range(0, 5):
                        team2BowlingRating += bowlingRating[b]

                c.execute('select b.playerId, b.ft20Id from battingFT20Live b, playerInfo p where p.playerId=b.playerId and p.teams like ? and b.startDate>? and b.startDate<?', ('%'+team2+'%', date2yAgo, matchDate))
                playerFT20s = c.fetchall()
                playerLastFT20 = {}
                for i in range(0, len(playerFT20s)):
                    pid = playerFT20s[i][0]
                    pFT20Id = playerFT20s[i][1]
                    if pid in playerLastFT20:
                        if pFT20Id > playerLastFT20[pid]:
                            playerLastFT20[pid] = pFT20Id
                    else:
                        playerLastFT20[pid] = pFT20Id

                battingRating = []
                for pid in playerLastFT20:
                    c.execute('select player, rating from battingFT20Live where playerId=? and ft20Id=?', (pid, playerLastFT20[pid]))
                    pRating = c.fetchone()
                    battingRating.append(pRating[1])
                battingRating = sorted(battingRating, reverse=True)

                if len(battingRating) >= 7:
                    for b in range(0, 7):
                        team2BattingRating += battingRating[b]
                    team2BattingRating = team2BattingRating / 7 * 5

                c.execute('select b.playerId, b.ft20Id from bowlingFT20Live b, playerInfo p where p.playerId=b.playerId and p.teams like ? and b.startDate>? and b.startDate<?', ('%'+team1+'%', date2yAgo, matchDate))
                playerFT20s = c.fetchall()
                playerLastFT20 = {}
                for i in range(0, len(playerFT20s)):
                    pid = playerFT20s[i][0]
                    pFT20Id = playerFT20s[i][1]
                    if pid in playerLastFT20:
                        if pFT20Id > playerLastFT20[pid]:
                            playerLastFT20[pid] = pFT20Id
                    else:
                        playerLastFT20[pid] = pFT20Id

                bowlingRating = []
                for pid in playerLastFT20:
                    c.execute('select player, rating from bowlingFT20Live where playerId=? and ft20Id=?', (pid, playerLastFT20[pid]))
                    pRating = c.fetchone()
                    bowlingRating.append(pRating[1])
                bowlingRating = sorted(bowlingRating, reverse=True)

                if len(bowlingRating) >= 5:
                    for b in range(0, 5):
                        team1BowlingRating += bowlingRating[b]

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

                d = datetime.datetime(int(matchDate[0:4]), int(matchDate[4:-2]), int(matchDate[6:]))
                date2yAgo = d + datetime.timedelta(days=-720)
                date2yAgo = date2yAgo.strftime('%Y%m%d')

                c.execute('select b.playerId, b.t20iId from battingT20ILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team1, date2yAgo, matchDate))
                playerT20Is = c.fetchall()
                playerLastT20I = {}
                for i in range(0, len(playerT20Is)):
                    pid = playerT20Is[i][0]
                    pT20IId = playerT20Is[i][1]
                    if pid in playerLastT20I:
                        if pT20IId > playerLastT20I[pid]:
                            playerLastT20I[pid] = pT20IId
                    else:
                        playerLastT20I[pid] = pT20IId

                battingRating = []
                for pid in playerLastT20I:
                    c.execute('select player, rating from battingT20ILive where playerId=? and t20iId=?', (pid, playerLastT20I[pid]))
                    pRating = c.fetchone()
                    battingRating.append(pRating[1])
                battingRating = sorted(battingRating, reverse=True)

                if len(battingRating) >= 7:
                    for b in range(0, 7):
                        team1BattingRating += battingRating[b]
                    team1BattingRating = team1BattingRating / 7 * 5

                c.execute('select b.playerId, b.t20iId from bowlingT20ILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team2, date2yAgo, matchDate))
                playerT20Is = c.fetchall()
                playerLastT20I = {}
                for i in range(0, len(playerT20Is)):
                    pid = playerT20Is[i][0]
                    pT20IId = playerT20Is[i][1]
                    if pid in playerLastT20I:
                        if pT20IId > playerLastT20I[pid]:
                            playerLastT20I[pid] = pT20IId
                    else:
                        playerLastT20I[pid] = pT20IId

                bowlingRating = []
                for pid in playerLastT20I:
                    c.execute('select player, rating from bowlingT20ILive where playerId=? and t20iId=?', (pid, playerLastT20I[pid]))
                    pRating = c.fetchone()
                    bowlingRating.append(pRating[1])
                bowlingRating = sorted(bowlingRating, reverse=True)

                if len(bowlingRating) >= 5:
                    for b in range(0, 5):
                        team2BowlingRating += bowlingRating[b]

                c.execute('select b.playerId, b.t20iId from battingT20ILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team2, date2yAgo, matchDate))
                playerT20Is = c.fetchall()
                playerLastT20I = {}
                for i in range(0, len(playerT20Is)):
                    pid = playerT20Is[i][0]
                    pT20IId = playerT20Is[i][1]
                    if pid in playerLastT20I:
                        if pT20IId > playerLastT20I[pid]:
                            playerLastT20I[pid] = pT20IId
                    else:
                        playerLastT20I[pid] = pT20IId

                battingRating = []
                for pid in playerLastT20I:
                    c.execute('select player, rating from battingT20ILive where playerId=? and t20iId=?', (pid, playerLastT20I[pid]))
                    pRating = c.fetchone()
                    battingRating.append(pRating[1])
                battingRating = sorted(battingRating, reverse=True)

                if len(battingRating) >= 7:
                    for b in range(0, 7):
                        team2BattingRating += battingRating[b]
                    team2BattingRating = team2BattingRating / 7 * 5

                c.execute('select b.playerId, b.t20iId from bowlingT20ILive b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (team1, date2yAgo, matchDate))
                playerT20Is = c.fetchall()
                playerLastT20I = {}
                for i in range(0, len(playerT20Is)):
                    pid = playerT20Is[i][0]
                    pT20IId = playerT20Is[i][1]
                    if pid in playerLastT20I:
                        if pT20IId > playerLastT20I[pid]:
                            playerLastT20I[pid] = pT20IId
                    else:
                        playerLastT20I[pid] = pT20IId

                bowlingRating = []
                for pid in playerLastT20I:
                    c.execute('select player, rating from bowlingT20ILive where playerId=? and t20iId=?', (pid, playerLastT20I[pid]))
                    pRating = c.fetchone()
                    bowlingRating.append(pRating[1])
                bowlingRating = sorted(bowlingRating, reverse=True)

                if len(bowlingRating) >= 5:
                    for b in range(0, 5):
                        team1BowlingRating += bowlingRating[b]

            # Check if match is home/away/neutral
            c.execute('select location from t20iInfo where t20iId=?',(matchId,))
            location = c.fetchone()
            location = location[0] if location != None else None

            if team1 == location:
                team1Home = 1.0
                team2Home = -1.0
            elif team2 == location:
                team1Home = -1.0
                team2Home = 1.0
            conn.close()

        conn = sqlite3.connect('ccrFT20.db')
        c = conn.cursor()
        team1StartingOdds = team1Rating / (team1Rating + team2Rating)
        team2StartingOdds = 1 - team1StartingOdds

        c.execute('select ocId, overs, runs, wkts, result, runRate from overComparison where t20Id=? and innings=1', (t20NumId, ))
        conn.commit()
        overComp = c.fetchall();
        fd1 = open('t20ML1UnqRRHMLT.csv','a')
        last3OversOdds = []
        for i in range(0, len(overComp)):
            ocId = overComp[i][0]
            overs = overComp[i][1]
            runs = overComp[i][2]
            wkts = overComp[i][3]
            matchResult = overComp[i][4]
            runRate = overComp[i][5]
            try:
                float(runRate)
            except ValueError:
                runRate = float(runRate.replace("*",""))

            if runs == 0:
                c.execute('select avg(result), t20Id from overComparison where t20Id<'+`t20NumId`+' and t20Id>='+`(t20NumId - 600)`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runs<=1 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)` + ' group by t20Id ')
            else:
                c.execute('select avg(result), t20Id from overComparison where t20Id<'+`t20NumId`+' and t20Id>='+`(t20NumId - 600)`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runRate<='+`(runRate*1.1)`+' and runRate>'+`(runRate*0.9)`+' and wkts='+`wkts` + ' group by t20Id union '\
                'select avg(result), t20Id from overComparison where t20Id<'+`t20NumId`+' and t20Id>='+`(t20NumId - 600)`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runRate<='+`(runRate*1.05)`+' and runRate>'+`(runRate*0.85)`+' and wkts='+`(wkts+1)` + ' group by t20Id union '\
                'select avg(result), t20Id from overComparison where t20Id<'+`t20NumId`+' and t20Id>='+`(t20NumId - 600)`+' and innings=1 and overs>='+`(overs-1)`+' and overs<'+`(overs+1)`+' and runRate<='+`(runRate*1.15)`+' and runRate>'+`(runRate*0.95)`+' and wkts='+`(wkts-1)` + ' group by t20Id')

            comp = c.fetchall()
            similarCount = len(comp)
            winCount = 0.0
            for j in range(0, len(comp)):
                compResult = comp[j][0]
                winCount = winCount + int(compResult) / 2
            matchOdds = 100 * winCount / similarCount if similarCount > 0 else None

            matchOddsAdj = None
            momentum = 0.0
            momentumAdj = 0.0
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

                # momentum adjustment
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

            battingRating = team1BattingRating * (40 - float(overs)) / 40
            if wkts > 0:
                for w in range(0, wkts):
                    battingRating = battingRating - team1BattingRating * battingWktWeight[w]
            battingRating = 0 if battingRating < 0 else battingRating
            bowlingRating = team2BowlingRating * (20 - float(overs)) / 20

            # print `t20Id` + ' Overs: ' + `overs` + ' Score: ' + `runs` + '/' + `wkts` + ' Result: ' + `matchResult` + ' Odds: ' + `matchOdds`
            # c.execute('update overComparison set matchOdds=? where ocId=?', (matchOdds, ocId))
            # conn.commit()
            t20Type = 1 if "I" in t20Id else 0
            fd1.write(`t20NumId` + ","  + `t20Type` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `team1Rating` + "," + `team2Rating` + "," + `battingRating` + "," + `bowlingRating` + "," + `team1Home` + "," + `momentum` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult/2` + "\n")
        fd1.close()

        c.execute('select ocId, overs, runs, wkts, runsReq, ballsRem, result, reqRate from overComparison where t20Id=? and innings=2', (t20NumId, ))
        conn.commit()
        overComp = c.fetchall();
        fd2 = open('t20ML2UnqRRHMLT.csv','a')
        last3OversOdds = []
        for i in range(0, len(overComp)):
            ocId = overComp[i][0]
            overs = overComp[i][1]
            runs = overComp[i][2]
            wkts = overComp[i][3]
            runsReq = overComp[i][4]
            ballsRem = overComp[i][5]
            matchResult = overComp[i][6]
            reqRate = overComp[i][7]
            if runsReq == 0 or overs == 20 or reqRate == "-" or reqRate == "-*": continue
            try:
                float(reqRate)
            except ValueError:
                reqRate = float(reqRate.replace("*",""))

            c.execute('select avg(result), t20Id from overComparison where t20Id<'+`t20NumId`+' and t20Id>='+`(t20NumId - 600)`+' and innings=2 and wkts='+`wkts`+' and reqRate>='+`(reqRate*0.9)`+' and reqRate<'+`(reqRate*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id union '\
            'select avg(result), t20Id from overComparison where t20Id<'+`t20NumId`+' and t20Id>='+`(t20NumId - 600)`+' and innings=2 and wkts='+`(wkts-1)`+' and reqRate>='+`(reqRate*0.95)`+' and reqRate<'+`(reqRate*1.15)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id  union '\
            'select avg(result), t20Id from overComparison where t20Id<'+`t20NumId`+' and t20Id>='+`(t20NumId - 600)`+' and innings=2 and wkts='+`(wkts+1)`+' and reqRate>='+`(reqRate*0.85)`+' and reqRate<'+`(reqRate*1.05)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id')

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
            momentum = 0.0
            momentumAdj = 0.0
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

                # momentum adjustment
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

            battingRating = team2BattingRating * (40 - float(overs)) / 40
            if wkts > 0:
                for w in range(0, wkts):
                    battingRating = battingRating - team2BattingRating * battingWktWeight[w]
            battingRating = 0 if battingRating < 0 else battingRating
            bowlingRating = team1BowlingRating * (20 - float(overs)) / 20

            t20Type = 1 if "I" in t20Id else 0
            fd2.write(`t20NumId` + ","  + `t20Type` + ","  + `overs` + "," + `runs` + "," + `wkts` + "," + `runsReq` + "," + `ballsRem` + "," + `team1Rating` + "," + `team2Rating` + "," + `battingRating` + "," + `bowlingRating` + "," + `team1Home` + "," + `momentum` + "," + `matchOdds` + "," + `matchOddsAdj` + "," + `matchResult/2` + "\n")
        fd2.close()
        t20NumId += 1
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

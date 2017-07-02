#!/usr/bin/env python
# -*- cft20ng: utf-8 -*-

import time
from lxml import html
import requests
import sqlite3
start = time.clock()

startFT20 = int(input('Enter starting FT20 #: '))

#set PYTHONIOENCFT20NG=utf-8
conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()

# get ft20s info
c.execute('select ft20Id, startDate, scoreLink, result from ft20Info')
ft20sInfo = c.fetchall()
ignoreDL = (47, 66, 72, 198, 246, 315, 317, 497, 679, 683, 738, 854, 873, 940)
ft20Id2LastOverBowlerInn = {227:2, 575:2, 730:2, 731:2, 830:2, 943:2, 957:2}
ft20Id2LastOverBowler = {2272:"Kieron Pollard", 5752:"Mitchell Starc", 7302:"Kemar Roach", 7312:"Sohail Tanvir", 8302:"Piyush Chawla", 9432:"Kagiso Rabada", 9572:"Pawan Negi"}
rainedStops = {1:2, 40:2, 41:2, 226:2, 364:2, 644:2}
newPlayerPenaltyFactor = 0.0425
expSmoothFactor = 0.05

# loop through ft20 matches
for x in range(startFT20, len(ft20sInfo)):
    ft20Id = ft20sInfo[x][0]
    startDate = ft20sInfo[x][1]
    result =  ft20sInfo[x][3]
    if ft20Id in ignoreDL:
        continue
    print `ft20Id` + "\n"

    c.execute('select startDate from ft20Info where ft20Id=?',(ft20Id,))
    ft20Date = c.fetchone()
    ft20Date = ft20Date[0]

    c.execute('select batTeam, balls from detailsFT20Innings where ft20Id=? and innings=1',(ft20Id,))
    team1Balls = c.fetchone()
    team1 = team1Balls[0]
    inn1Balls = team1Balls[1]

    c.execute('select batTeam, balls from detailsFT20Innings where ft20Id=? and innings=2',(ft20Id,))
    team2Balls = c.fetchone()
    team2 = team2Balls[0]
    inn2Balls = team2Balls[1]

    c.execute('select rating from teamFT20Live where team=? and startDate<?',(team1, ft20Date))
    team1Rating = c.fetchall()
    if len(team1Rating) > 0:
        team1Rating = team1Rating[len(team1Rating)-1][0]
    else:
        team1Rating = 100.0

    c.execute('select rating from teamFT20Live where team=? and startDate<?',(team2, ft20Date))
    team2Rating = c.fetchall()
    if len(team2Rating) > 0:
        team2Rating = team2Rating[len(team2Rating)-1][0]
    else:
        team2Rating = 100.0

    team1StartingOdds = team1Rating / (team1Rating + team2Rating)
    team2StartingOdds = 1 - team1StartingOdds
    print team1
    print team2
    print team1StartingOdds
    print team2StartingOdds

    team2Win = 0.1
    if team2 == result:
        team2Win = 1.0
    elif result == "Tie/NR":
        team2Win = 0.5
    else:
        team2Win = 0.0

    c.execute('select runs from detailsFT20Innings where ft20Id=? and innings=2',(ft20Id,))
    team2TotRuns = c.fetchone()
    team2TotRuns = team2TotRuns[0]

    c.execute('select player, playerId from bowlingFT20Innings where ft20Id=? and innings=1',(ft20Id,))
    bowlers1 = c.fetchall()
    bowler1Names = []
    bowler2Id1 = {}

    for i in range(len(bowlers1)):
        bowler1Names.append(bowlers1[i][0])
        bowler2Id1[bowlers1[i][0]] = bowlers1[i][1]

    c.execute('select player, playerId, runs, balls from battingFT20Innings where ft20Id=? and innings=1',(ft20Id,))
    batsmen1 = c.fetchall()
    batsmen1Names = []
    batsman2Id1 = {}
    dismissedBatsman2Runs = {}
    dismissedBatsman2Balls = {}

    for i in range(len(batsmen1)):
        batsmen1Names.append(batsmen1[i][0])
        batsman2Id1[batsmen1[i][0]] = batsmen1[i][1]
        dismissedBatsman2Runs[batsmen1[i][1]] = int(batsmen1[i][2])
        dismissedBatsman2Balls[batsmen1[i][1]] = int(batsmen1[i][3])

    c.execute('select player, playerId from bowlingFT20Innings where ft20Id=? and innings=2',(ft20Id,))
    bowlers2 = c.fetchall()
    bowler2Names = []
    bowler2Id2 = {}

    for i in range(len(bowlers2)):
        bowler2Names.append(bowlers2[i][0])
        bowler2Id2[bowlers2[i][0]] = bowlers2[i][1]

    c.execute('select player, playerId, runs, balls from battingFT20Innings where ft20Id=? and innings=2',(ft20Id,))
    batsmen2 = c.fetchall()
    batsmen2Names = []
    batsman2Id2 = {}
    batsman2Runs2 = {}

    for i in range(len(batsmen2)):
        batsmen2Names.append(batsmen2[i][0])
        batsman2Id2[batsmen2[i][0]] = batsmen2[i][1]
        dismissedBatsman2Runs[batsmen2[i][1]] = int(batsmen2[i][2])
        dismissedBatsman2Balls[batsmen2[i][1]] = int(batsmen2[i][3])

    notOutBatsman2Runs = {}
    notOutBatsman2Balls = {}
    c.execute('select player, playerId, runs, balls from battingFT20Innings where ft20Id=? and notOut=1',(ft20Id,))
    notOutB = c.fetchall()

    for i in range(len(notOutB)):
        notOutBatsman2Runs[notOutB[i][0]] = int(notOutB[i][2])
        notOutBatsman2Balls[notOutB[i][0]] = int(notOutB[i][3])

    url = 'http://www.espncricinfo.com' + ft20sInfo[x][2]
    print url
    page = requests.get(url)
    tree = html.fromstring(page.text)
    fow1 = tree.xpath('(//div[@class="fow"])[1]/p/a[@class="fowLink"]/span/text()')
    fow2 = tree.xpath('(//div[@class="fow"])[2]/p/a[@class="fowLink"]/span/text()')

    # parse batsmen fall of wicket order
    wktOvers1 = []
    wktBalls1 = {}
    wktPlayer1 = {}
    for k in range(len(fow1)):
        batsmenFoW = fow1[k].split('(')[1].replace(')','')
        player = batsmenFoW.split(',')[0]
        overs = batsmenFoW.split(',')
        if len(overs) == 2:
            overs = overs[1].split()[0]
            if 'retired' in overs:
                balls = None
            else:
                if '.' in overs:
                    endOfOver = int(overs.split('.')[0]) + 1
                    balls = int(overs.split('.')[1])
                else:
                    balls = 0
        else: balls = None
        if balls == None: continue
        wicket = fow1[k].split('(')[0].strip().split('-')[0]
        runs = fow1[k].split('(')[0].strip().split('-')[1]
        wktOvers1.append(endOfOver)
        wktBalls1[overs] = balls
        wktPlayer1[overs] = player

    wktOvers2 = []
    wktBalls2 = {}
    wktPlayer2 = {}
    for k in range(len(fow2)):
        batsmenFoW = fow2[k].split('(')[1].replace(')','')
        player = batsmenFoW.split(',')[0]
        overs = batsmenFoW.split(',')
        if len(overs) == 2:
            overs = overs[1].split()[0]
            if 'retired' in overs:
                balls = None
            else:
                if '.' in overs:
                    endOfOver = int(overs.split('.')[0]) + 1
                    balls = int(overs.split('.')[1])
                else:
                    balls = 0
        else: balls = None
        if balls == None: continue
        wicket = fow2[k].split('(')[0].strip().split('-')[0]
        runs = fow2[k].split('(')[0].strip().split('-')[1]
        wktOvers2.append(endOfOver)
        wktBalls2[overs] = balls
        wktPlayer2[overs] = player

    battingWinShares1 = {}
    bowlingWinShares1 = {}
    battingWinShares2 = {}
    bowlingWinShares2 = {}
    fieldingWinShares1 = {}
    fieldingWinShares2 = {}
    totalWinShares = {}
    battingWinSharesAdj1 = {}
    bowlingWinSharesAdj1 = {}
    battingWinSharesAdj2 = {}
    bowlingWinSharesAdj2 = {}
    fieldingWinSharesAdj1 = {}
    fieldingWinSharesAdj2 = {}
    totalWinSharesAdj = {}
    lastTeam1Odds = 0.5
    lastTeam2Odds = 0.5
    lastTeam1OddsAdj = team1StartingOdds
    lastTeam2OddsAdj = team2StartingOdds
    onlyCurrentBowlerFiguresShown = 0
    for inn in range(1, 3):
        url = 'http://www.espncricinfo.com' + ft20sInfo[x][2] + '?innings=' + `inn` + ';view=commentary'
        page = requests.get(url)
        tree = html.fromstring(page.text)

        commentaryEvent = tree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"])')
        overBalls = tree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"]/div[@class="commentary-overs"]/text())')
        commentary = tree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"]/div[@class="commentary-text"])')
        endOfOverInfo = tree.xpath('(//div[@class="end-of-over-info"]/p/span/text())')
        endOfOverInfoDetail = tree.xpath('(//div[@class="end-of-over-info"]/p/text())')
        endOfOverInfoDetail = [z for z in endOfOverInfoDetail if "runs required" in z]
        endOfOverBatsmen = tree.xpath('(//div[@class="end-of-over-info"]/ul/li[@class="eov-stat-batsmen"]/ul/li/span/text())')
        endOfOverBowlers = tree.xpath('(//div[@class="end-of-over-info"]/ul/li[@class="eov-stat-bowlers"]/ul/li/span/text())')
        # sometimes  commentary only shows figures for one bowler and not both - this is a hack to figure out which
        if inn == 1:
            expBowlerFiguresMin = (inn1Balls / 6) * 4 * 0.7
        else:
            expBowlerFiguresMin = (inn2Balls / 6) * 4 * 0.7
        if len(endOfOverBowlers) < expBowlerFiguresMin: onlyCurrentBowlerFiguresShown = 1
        # print endOfOverInfo
        # print endOfOverInfoDetail
        # print endOfOverBatsmen
        # print endOfOverBowlers

        if ft20Id == 592:
            endOfOverBowlers.pop()
            endOfOverBowlers.pop()
            endOfOverBowlers.pop()
            endOfOverBowlers.pop()
            endOfOverBowlers.pop()
            endOfOverBowlers.pop()
            endOfOverBowlers.append('JE Taylor')
            endOfOverBowlers.append('4-0-43-0')
            endOfOverBowlers.append('AD Russell')
            endOfOverBowlers.append('3-0-23-2')
            endOfOverBowlers.append('J Theron')
            endOfOverBowlers.append('4-0-32-1')
            endOfOverBowlers.append('JE Taylor')
            endOfOverBowlers.append('4-0-43-0')
        over = 0
        batsman2Runs = {}
        batsman2Balls = {}
        bowler2Overs = {}
        bowler2NumWkts = {}
        lastRuns = 0
        lastRunsReq = 0
        lastWkts = 0
        lastBallOfOverWin = 0
        team1Odds = 0.0
        team2Odds = 0.0
        for i in range(len(endOfOverInfo)):
            dismissedPlayer = {}
            dismissedPlayerBall = {}
            lastBallDismissal = 0
            if "End of over " in endOfOverInfo[i]:
                over = float(endOfOverInfo[i][12:])
                # print `ft20Id` + ": " + `inn` + ": " + `int(over)`
            else:
                j = 0
                if inn == 1:
                    if int(over) in wktOvers1:
                        for b in range(0, 6):
                            overBall = `int(over-1)`+"."+`(b+1)`
                            if overBall in wktPlayer1:
                                dismissedPlayer[j] = wktPlayer1[overBall]
                                dismissedPlayerBall[j] = b+1
                                if b == 5: lastBallDismissal = 1
                                j += 1
                else:
                    if int(over) in wktOvers2:
                        for b in range(0, 6):
                            overBall = `int(over-1)`+"."+`(b+1)`
                            if overBall in wktPlayer2:
                                dismissedPlayer[j] = wktPlayer2[overBall]
                                dismissedPlayerBall[j] = b+1
                                if b == 5: lastBallDismissal = 1
                                j +=1

                runs = float(endOfOverInfo[i][(endOfOverInfo[i].rfind(" "))+1:(endOfOverInfo[i].index("/"))])
                wkts = float(endOfOverInfo[i][(endOfOverInfo[i].index("/"))+1:])

                runsReq = 0
                ballsRem = 0
                if (int(over)-1) >= len(endOfOverInfoDetail): lastBallOfOverWin = 1
                if inn == 2 and lastBallOfOverWin == 0:
                    detail = endOfOverInfoDetail[int(over)-1].replace("\n", "")
                    detail = detail.replace("(", "")
                    detail = detail.replace(")", "")
                    if " runs required from " not in detail:
                        detailSplit = detail.split(" runs required")
                        ballsRem = 0
                        lastBallOfOverWin = 1
                    else:
                        detailSplit = detail.split(" runs required from ")
                        if "balls" in detailSplit[1]:
                            ballsRem = int(detailSplit[1][0:detailSplit[1].index(" ")])
                        else:
                            overBalls = detailSplit[1][0:detailSplit[1].index(" ")]
                            if "." in overBalls:
                                overBallsSplit = overBalls.split(".")
                                ballsRem = int(overBallsSplit[0]) * 6 + int(overBallsSplit[1])
                            else:
                                ballsRem = int(overBalls) * 6
                    runsReq = int(detailSplit[0].strip())

                similarCount = 0
                winCount = 0
                if inn == 1:
                    if runs == 0:
		                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
                    else:
                        c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
                else:
                    lastRunsReq = runsReq
                    if ballsRem < 24:
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                    else:
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`)

                results = c.fetchall()

                for y in range(0, len(results)):
                    similarCount += 1
                    result = results[y][0]
                    winCount = winCount + result / 2

                if similarCount > 0:
                    if inn == 1:
                        team1Odds = float(winCount) / float(similarCount)
                        team2Odds = 1.0 - team1Odds
                    else:
                        team2Odds = float(winCount) / float(similarCount)
                        team1Odds = 1.0 - team2Odds

                if inn == 2:
                    similarCount2 = 0
                    winCount2 = 0
                    c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                    results = c.fetchall()

                    for z in range(0, len(results)):
                        similarCount2 += 1
                        result = results[z][0]
                        winCount2 = winCount2 + result / 2

                    if similarCount2 > 0:
                        team2Odds2 = float(winCount2) / float(similarCount2)
                        if team2Odds2 > team2Odds:
                            team2Odds = team2Odds2
                            team1Odds = 1.0 - team2Odds

                if runsReq == 0 and inn == 2:
                    team2Odds = 1.0

                if over == 20 and runsReq != 0 and inn == 2:
                    team2Odds = 0.0

                if wkts == 10 and runsReq != 0 and inn == 2:
                    team2Odds = 0.0

                team1Odds = 1.0 - team2Odds

                runsDiff = runs - lastRuns
                wktsDiff = wkts - lastWkts
                batsmanHasNotFaced = 0
                # print endOfOverBatsmen

                batsmanName1 = endOfOverBatsmen.pop(0)
                batsmanScoreBalls1 = endOfOverBatsmen.pop(0)
                batsmanScore1 = int(batsmanScoreBalls1[0:batsmanScoreBalls1.index(" ")])
                batsmanBalls1 = int(batsmanScoreBalls1[batsmanScoreBalls1.index("(")+1:batsmanScoreBalls1.index("b")])

                if ft20Id == 183 and inn == 1 and over == 6:
                     endOfOverBatsmen.insert(0, "R McLaren")
                     endOfOverBatsmen.insert(1, "0 (0b)")

                if ft20Id == 284 and inn == 2 and over == 9:
                     endOfOverBatsmen.insert(0, "JEC Franklin")
                     endOfOverBatsmen.insert(1, "0 (0b)")

                if len(endOfOverBatsmen) >= 1:
                    if endOfOverBatsmen[0] == "0 (0b)":
                        batsmanHasNotFaced = 1
                        endOfOverBatsmen.pop(0)

                if lastBallDismissal == 0 and batsmanHasNotFaced == 0 and not (ft20Id == 1 and inn == 2 and over == 16):
                    batsmanName2 = endOfOverBatsmen.pop(0)
                    batsmanScoreBalls2 = endOfOverBatsmen.pop(0)
                    batsmanScore2 = int(batsmanScoreBalls2[0:batsmanScoreBalls2.index(" ")])
                    batsmanBalls2 = int(batsmanScoreBalls2[batsmanScoreBalls2.index("(")+1:batsmanScoreBalls2.index("b")])

                if i == 1 or onlyCurrentBowlerFiguresShown == 1:
                    bowlerName1 = endOfOverBowlers.pop(0)
                    bowler1Figures = endOfOverBowlers.pop(0)
                else:
                    bowlerName1 = endOfOverBowlers[2*(i-3)]
                    bowler1Figures = endOfOverBowlers[2*(i-3)+1]
                    bowlerName2 = endOfOverBowlers[2*(i-3)+2]
                    bowler2Figures = endOfOverBowlers[2*(i-3)+3]
                    bowlerOvers2 = bowler2Figures[0:bowler2Figures.index("-")]
                    bowler2Wkts = bowler2Figures[(bowler2Figures.rfind("-")+1):]
                    bowler2FiguresMod = bowler2Figures[0:bowler2Figures.rfind("-")]
                    bowler2Runs = bowler2FiguresMod[(bowler2FiguresMod.rfind("-")+1):]
                bowlerOvers1 = bowler1Figures[0:bowler1Figures.index("-")]
                bowler1Wkts = bowler1Figures[(bowler1Figures.rfind("-")+1):]
                bowler1FiguresMod = bowler1Figures[0:bowler1Figures.rfind("-")]
                bowler1Runs = bowler1FiguresMod[(bowler1FiguresMod.rfind("-")+1):]

                if onlyCurrentBowlerFiguresShown == 0:
                    if bowlerName1 in bowler2Overs:
                        if i == 3:
                            bowlerName = bowlerName2
                            bowlerWkts = bowler2Wkts
                        else:
                            if bowler2Overs[bowlerName1] != bowlerOvers1:
                                bowlerName = bowlerName1
                                bowlerWkts = bowler1Wkts
                            else:
                                bowlerName = bowlerName2
                                bowlerWkts = bowler2Wkts
                    else:
                        if i == 1:
                            bowlerName = bowlerName1
                            bowlerWkts = bowler1Wkts
                        else:
                            if bowlerName2 in bowler2Overs:
                                if bowler2Overs[bowlerName2] != bowlerOvers2:
                                    bowlerName = bowlerName2
                                    bowlerWkts = bowler2Wkts
                                else:
                                    bowlerName = bowlerName1
                                    bowlerWkts = bowler1Wkts
                            bowler2Overs[bowlerName2] = bowlerOvers2
                    bowler2Overs[bowlerName1] = bowlerOvers1
                else:
                    bowlerName = bowlerName1
                    bowlerWkts = bowler1Wkts
                    bowler2Overs[bowlerName1] = bowlerOvers1

                if bowlerName in bowler2NumWkts:
                    bowlerWktDiff = int(bowlerWkts) - bowler2NumWkts[bowlerName]
                else:
                    bowlerWktDiff = int(bowlerWkts)
                bowler2NumWkts[bowlerName] = int(bowlerWkts)
                fielderWkts = wktsDiff - bowlerWktDiff

                batsman1 = ""
                batsman2 = ""
                batsmanName1FI = ""
                if " " in batsmanName1:
                    batsmanName1FI = batsmanName1.split(" ")[0]
                    batsmanName1FI = batsmanName1FI if batsmanName1FI.isupper() else ""
                    if batsmanName1FI != "": batsmanName1 = batsmanName1.split(" ")[1]

                if lastBallDismissal == 0 and batsmanHasNotFaced == 0:
                    batsmanName2FI = ""
                    if " " in batsmanName2:
                        batsmanName2FI = batsmanName2.split(" ")[0]
                        batsmanName2FI = batsmanName2FI if batsmanName2FI.isupper() else ""
                        if batsmanName2FI != "": batsmanName2 = batsmanName2.split(" ")[1]

                bowler = ""
                bowlerNameFI = ""
                if " " in bowlerName:
                    bowlerNameFI = bowlerName.split(" ")[0]
                    bowlerNameFI = bowlerNameFI if bowlerNameFI.isupper() else ""
                    if bowlerNameFI != "": bowlerName = bowlerName.split(" ")[1]

                dismissedBat = {}
                if inn == 1:
                    for bowlerN in bowler1Names:
                        if bowlerName in bowlerN and (bowlerNameFI == "" or bowlerN[0] in bowlerNameFI):
                            bowler = bowlerN

                    for batsmanName in batsmen1Names:
                        if batsmanName1 in batsmanName and (batsmanName1FI == "" or batsmanName[0] in batsmanName1FI):
                            batsman1 = batsmanName

                    if lastBallDismissal == 0 and batsmanHasNotFaced == 0:
                        for batsmanName in batsmen1Names:
                            if batsmanName2 in batsmanName and (batsmanName2FI == "" or batsmanName[0] in batsmanName2FI):
                                batsman2 = batsmanName

                    if len(dismissedPlayer) > 0:
                        for k in range(0, len(dismissedPlayer)):
                            dismissedPlayerFI = ""
                            if " " in dismissedPlayer[k]:
                                dismissedPlayerFI = dismissedPlayer[k].split(" ")[0]
                                dismissedPlayerFI = dismissedPlayerFI if dismissedPlayerFI.isupper() else ""
                                if dismissedPlayerFI != "": dismissedPlayer[k] = dismissedPlayer[k].split(" ")[1]

                            for batsmanName in batsmen1Names:
                                if dismissedPlayer[k] in batsmanName and (dismissedPlayerFI == "" or batsmanName[0] in dismissedPlayerFI):
                                    dismissedBat[k] = batsmanName

                            if dismissedPlayer[k] == "Scantlebury-Searles":
                                dismissedBat[k] = "Javon Searles"
                                batsman2Id1[dismissedBat[k]] = 461111

                            if dismissedPlayer[k] == "Matthew":
                                dismissedBat[k] = "Mervin Mathew"
                                batsman2Id1[dismissedBat[k]] = 105245
                else:
                    for bowlerN in bowler2Names:
                        if bowlerName in bowlerN and (bowlerNameFI == "" or bowlerN[0] in bowlerNameFI):
                            bowler = bowlerN

                    for batsmanName in batsmen2Names:
                        if batsmanName1 in batsmanName and (batsmanName1FI == "" or batsmanName[0] in batsmanName1FI):
                            batsman1 = batsmanName

                    if batsmanName1FI == "SPD" and batsmanName1 == "Smith":
                        batsman1 = "Steven Smith"
                        batsman2Id1[batsman1] = 534387

                    if batsmanName1FI == "DLR" and batsmanName1 == "Smith":
                        batsman1 = "Daniel Smith"
                        batsman2Id1[batsman1] = 15291

                    if lastBallDismissal == 0:
                        for batsmanName in batsmen2Names:
                            if batsmanName2 in batsmanName and (batsmanName2FI == "" or batsmanName[0] in batsmanName2FI):
                                batsman2 = batsmanName

                        if batsmanName2FI == "SPD" and batsmanName2 == "Smith":
                            batsman2 = "Steven Smith"
                            batsman2Id1[batsman2] = 534387

                        if batsmanName2FI == "DLR" and batsmanName2 == "Smith":
                            batsman2 = "Daniel Smith"
                            batsman2Id1[batsman2] = 15291

                    if len(dismissedPlayer) > 0:
                        for k in range(0, len(dismissedPlayer)):
                            dismissedPlayerFI = ""
                            if " " in dismissedPlayer[k]:
                                dismissedPlayerFI = dismissedPlayer[k].split(" ")[0]
                                dismissedPlayerFI = dismissedPlayerFI if dismissedPlayerFI.isupper() else ""
                                if dismissedPlayerFI != "": dismissedPlayer[k] = dismissedPlayer[k].split(" ")[1]

                            for batsmanName in batsmen2Names:
                                if dismissedPlayer[k] in batsmanName and (dismissedPlayerFI == "" or batsmanName[0] in dismissedPlayerFI):
                                    dismissedBat[k] = batsmanName

                if batsman1 in batsman2Runs:
                    batsmanScoreDiff1 = batsmanScore1 - batsman2Runs[batsman1]
                    batsmanBallDiff1 = batsmanBalls1 - batsman2Balls[batsman1]
                else:
                    batsmanScoreDiff1 = batsmanScore1
                    batsmanBallDiff1 = batsmanBalls1
                batsman2Runs[batsman1] = batsmanScore1
                batsman2Balls[batsman1] = batsmanBalls1

                if lastBallDismissal == 0 and batsmanHasNotFaced == 0:
                    if batsman2 in batsman2Runs:
                        batsmanScoreDiff2 = batsmanScore2 - batsman2Runs[batsman2]
                        batsmanBallDiff2 = batsmanBalls2 - batsman2Balls[batsman2]
                    else:
                        batsmanScoreDiff2 = batsmanScore2
                        batsmanBallDiff2 = batsmanBalls2
                    batsman2Runs[batsman2] = batsmanScore2
                    batsman2Balls[batsman2] = batsmanBalls2

                totDismissedBallFaced = 0
                # print dismissedPlayer
                # print dismissedBat
                if len(dismissedPlayer) > 0:
                    for k in range(0, len(dismissedBat)):
                        if inn == 1:
                            if dismissedBat[k] in batsman2Runs:
                                batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id1[dismissedBat[k]]] - batsman2Runs[dismissedBat[k]]
                                batsmanBallDiff = dismissedBatsman2Balls[batsman2Id1[dismissedBat[k]]] - batsman2Balls[dismissedBat[k]]
                            else:
                                batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id1[dismissedBat[k]]]
                                batsmanBallDiff = dismissedBatsman2Balls[batsman2Id1[dismissedBat[k]]]
                            batsman2Runs[dismissedBat[k]] = dismissedBatsman2Runs[batsman2Id1[dismissedBat[k]]]
                            batsman2Balls[dismissedBat[k]] = dismissedBatsman2Balls[batsman2Id1[dismissedBat[k]]]
                        else:
                            if dismissedBat[k] in batsman2Runs:
                                batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id2[dismissedBat[k]]] - batsman2Runs[dismissedBat[k]]
                                batsmanBallDiff = dismissedBatsman2Balls[batsman2Id2[dismissedBat[k]]] - batsman2Balls[dismissedBat[k]]
                            else:
                                batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id2[dismissedBat[k]]]
                                batsmanBallDiff = dismissedBatsman2Balls[batsman2Id2[dismissedBat[k]]]
                            batsman2Runs[dismissedBat[k]] = dismissedBatsman2Runs[batsman2Id2[dismissedBat[k]]]
                            batsman2Balls[dismissedBat[k]] = dismissedBatsman2Balls[batsman2Id2[dismissedBat[k]]]

                        totDismissedBallFaced += batsmanBallDiff
                        similarCount = 0
                        winCount = 0
                        dismissedTotalRuns = lastRuns + batsmanScoreDiff
                        lastRuns += batsmanScoreDiff
                        dismissedRunsReq = runsReq - batsmanScoreDiff
                        dismissedBallsRem = ballsRem - dismissedPlayerBall[k]
                        lastWkts += 1
                        if inn == 1:
                            if runs == 0:
        		                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(dismissedTotalRuns*1.1)`+' and runs>'+`(dismissedTotalRuns*0.9)`+' and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`+' and runsReq>='+`(dismissedRunsReq*0.75)`+' and runsReq<'+`(dismissedRunsReq*1.25)`+' and ballsRem<='+`(dismissedBallsRem*1.25)`+' and ballsRem>'+`(dismissedBallsRem*0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`+' and runsReq>='+`(dismissedRunsReq*0.9)`+' and runsReq<'+`(dismissedRunsReq*1.1)`+' and ballsRem<='+`(dismissedBallsRem*1.1)`+' and ballsRem>'+`(dismissedBallsRem*0.9)`);

                        results = c.fetchall()
                        dismissalTeam1Odds = 0.0
                        dismissalTeam2Odds = 0.0
                        dismissalTeam1OddsAdj = 0.0
                        dismissalTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                dismissalTeam1Odds = float(winCount) / float(similarCount)
                                dismissalTeam2Odds = 1.0 - dismissalTeam1Odds
                            else:
                                dismissalTeam2Odds = float(winCount) / float(similarCount)
                                dismissalTeam1Odds = 1.0 - dismissalTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`+' and runsReq>='+`(dismissedRunsReq*0.75)`+' and runsReq<'+`(dismissedRunsReq*1.25)`+' and ballsRem<='+`(dismissedBallsRem*1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                dismissalTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if dismissalTeam2Odds2 > dismissalTeam2Odds:
                                    dismissalTeam2Odds = dismissalTeam2Odds2
                                    dismissalTeam1Odds = 1.0 - dismissalTeam2Odds

                        if runsReq == 0 and inn == 2:
                            dismissalTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            dismissalTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            dismissalTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: dismissalTeam2Odds = lastTeam2Odds
                        dismissalTeam1Odds = 1.0 - dismissalTeam2Odds

                        disOddsAdjFact = 0.0
                        if inn == 1:
                            dismissedWinShares = dismissalTeam1Odds - lastTeam1Odds

                            if lastTeam1OddsAdj >= lastTeam1Odds and dismissedWinShares >= 0:
                                if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                    disOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        disOddsAdjFact = lastTeam2OddsAdj / lastTeam2Odds
                                    elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        disOddsAdjFact = lastTeam1Odds / lastTeam1OddsAdj
                                    else:
                                        disOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                            else:
                                if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                    disOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        disOddsAdjFact = lastTeam2Odds / lastTeam2OddsAdj
                                    elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        disOddsAdjFact = lastTeam1OddsAdj / lastTeam1Odds
                                    else:
                                        disOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                            dismissedWinSharesAdj = dismissedWinShares * disOddsAdjFact
                            dismissalTeam1OddsAdj = lastTeam1OddsAdj + dismissedWinSharesAdj

                            if dismissalTeam1OddsAdj > 1:
                                dismissedWinSharesAdj = dismissedWinSharesAdj - (dismissalTeam1OddsAdj - 1.0)
                                dismissalTeam1OddsAdj = 1.0
                            if dismissalTeam1OddsAdj < 0:
                                dismissedWinSharesAdj = dismissedWinSharesAdj - dismissalTeam1OddsAdj
                                dismissalTeam1OddsAdj = 0.0

                            lastTeam1Odds = dismissalTeam1Odds
                            lastTeam1OddsAdj = dismissalTeam1OddsAdj

                            if dismissedBat[k] in battingWinShares1:
                                battingWinShares1[dismissedBat[k]] = battingWinShares1[dismissedBat[k]] + dismissedWinShares
                                battingWinSharesAdj1[dismissedBat[k]] = battingWinSharesAdj1[dismissedBat[k]] + dismissedWinSharesAdj
                            else:
                                battingWinShares1[dismissedBat[k]] = dismissedWinShares
                                battingWinSharesAdj1[dismissedBat[k]] = dismissedWinSharesAdj
                        else:
                            dismissedWinShares = dismissalTeam2Odds - lastTeam2Odds

                            if lastTeam2OddsAdj >= lastTeam2Odds and dismissedWinShares >= 0:
                                if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                    disOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        disOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        disOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    else:
                                        disOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                            else:
                                if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                    disOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        disOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        disOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    else:
                                        disOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                            dismissedWinSharesAdj = dismissedWinShares * disOddsAdjFact
                            dismissalTeam2OddsAdj = lastTeam2OddsAdj + dismissedWinSharesAdj

                            if dismissalTeam2OddsAdj > 1:
                                dismissedWinSharesAdj = dismissedWinSharesAdj - (dismissalTeam2OddsAdj - 1.0)
                                dismissalTeam2OddsAdj = 1.0
                            if dismissalTeam2OddsAdj < 0:
                                dismissedWinSharesAdj = dismissedWinSharesAdj - dismissalTeam2OddsAdj
                                dismissalTeam2OddsAdj = 0.0

                            lastTeam2Odds = dismissalTeam2Odds
                            lastTeam2OddsAdj = dismissalTeam2OddsAdj

                            if dismissedBat[k] in battingWinShares2:
                                battingWinShares2[dismissedBat[k]] = battingWinShares2[dismissedBat[k]] + dismissedWinShares
                                battingWinSharesAdj2[dismissedBat[k]] = battingWinSharesAdj2[dismissedBat[k]] + dismissedWinSharesAdj
                            else:
                                battingWinShares2[dismissedBat[k]] = dismissedWinShares
                                battingWinSharesAdj2[dismissedBat[k]] = dismissedWinSharesAdj

                # print batsman1
                # print batsman2
                # print bowler
                team1WinShares = team1Odds - lastTeam1Odds
                team2WinShares = team2Odds - lastTeam2Odds

                oddsAdjFact = 0.0
                if lastTeam1OddsAdj >= lastTeam1Odds and team1WinShares >= 0:
                    if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                        oddsAdjFact = 1.0
                    else:
                        if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                            oddsAdjFact = lastTeam2OddsAdj / lastTeam2Odds
                        elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                            oddsAdjFact = lastTeam1Odds / lastTeam1OddsAdj
                        else:
                            oddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                else:
                    if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                        oddsAdjFact = 1.0
                    else:
                        if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                            oddsAdjFact = lastTeam2Odds / lastTeam2OddsAdj
                        elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                            oddsAdjFact = lastTeam1OddsAdj / lastTeam1Odds
                        else:
                            oddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2
                team1WinSharesAdj = team1WinShares * oddsAdjFact
                team2WinSharesAdj = team2WinShares * oddsAdjFact
                lastTeam1OddsAdj = lastTeam1OddsAdj + team1WinSharesAdj
                lastTeam2OddsAdj = 1 - lastTeam1OddsAdj
                if lastTeam1OddsAdj > 1:
                    team1WinSharesAdj = team1WinSharesAdj - (lastTeam1OddsAdj - 1.0)
                    lastTeam1OddsAdj = 1.0
                if lastTeam1OddsAdj < 0:
                    team1WinSharesAdj = team1WinSharesAdj - lastTeam1OddsAdj
                    lastTeam1OddsAdj = 0.0
                if lastTeam2OddsAdj > 1:
                    team2WinSharesAdj = team2WinSharesAdj - (lastTeam2OddsAdj - 1.0)
                    lastTeam2OddsAdj = 1.0
                if lastTeam2OddsAdj < 0:
                    team2WinSharesAdj = team2WinSharesAdj - lastTeam2OddsAdj
                    lastTeam2OddsAdj = 0.0

                lastTeam1Odds = team1Odds
                lastTeam2Odds = team2Odds

                # print similarCount
                # print winCount
                # print lastTeam1Odds
                # print lastTeam2Odds
                # print lastTeam1OddsAdj
                # print lastTeam2OddsAdj

                catch = {}
                stumping = {}
                droppedOrMissed = {}
                greatCatch = {}
                directHit = {}
                runsSaved = {}
                for b in range(0, 6):
                    ball = b + 1
                    eventId = `ft20Id` + `inn` + "'" + `(int(over)-1)` + "''" +`ball`+"'"
                    c.execute('select fielder, fielderId, droppedCatch, missedStumping, greatCatch, directHit, runsSaved, catch, stumping from fieldingEventFT20 where eventId=?', (eventId,));
                    results = c.fetchall()
                    for ff in range(0, len(results)):
                        fielder = results[ff][0]
                        if results[ff][2] != 0:
                            if fielder in droppedOrMissed:
                                droppedOrMissed[fielder] = droppedOrMissed[fielder] + results[ff][2]
                            else:
                                droppedOrMissed[fielder] = results[ff][2]
                        if results[ff][3] != 0:
                            if fielder in droppedOrMissed:
                                droppedOrMissed[fielder] = droppedOrMissed[fielder] + results[ff][3]
                            else:
                                droppedOrMissed[fielder] = results[ff][3]
                        if results[ff][4] != 0:
                            if fielder in greatCatch:
                                greatCatch[fielder] = greatCatch[fielder] + results[ff][4]
                            else:
                                greatCatch[fielder] = results[ff][4]
                        if results[ff][5] != 0:
                            if fielder in directHit:
                                directHit[fielder] = directHit[fielder] + results[ff][5]
                            else:
                                directHit[fielder] = results[ff][5]
                        if results[ff][6] != 0:
                            if fielder in runsSaved:
                                runsSaved[fielder] = runsSaved[fielder] + results[ff][6]
                            else:
                                runsSaved[fielder] = results[ff][6]
                        if results[ff][7] != 0:
                            if fielder in catch:
                                catch[fielder] = catch[fielder] + results[ff][7]
                            else:
                                catch[fielder] = results[ff][7]
                        if results[ff][8] != 0:
                            if fielder in stumping:
                                stumping[fielder] = stumping[fielder] + results[ff][8]
                            else:
                                stumping[fielder] = results[ff][8]

                for fielder in catch:
                    for ins in range(0, catch[fielder]):
                        beforeWkts = wkts - 1
                        if inn == 1:
                            if runs == 0:
                                c.execute('select result from overComparison where innings=1 and overs>=' + `(
                                over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=1 and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>=' + `(
                                over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=' + `(
                                runs * 1.1)` + ' and runs>' + `(runs * 0.9)` + ' and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                                runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(
                                ballsRem * 1.25)` + ' and ballsRem>' + `(ballsRem * 0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                                runsReq * 0.9)` + ' and runsReq<' + `(runsReq * 1.1)` + ' and ballsRem<=' + `(
                                ballsRem * 1.1)` + ' and ballsRem>' + `(ballsRem * 0.9)`);

                        results = c.fetchall()

                        similarCount = 0
                        winCount = 0
                        fieldingTeam1Odds = 0.0
                        fieldingTeam2Odds = 0.0
                        fieldingTeam1OddsAdj = 0.0
                        fieldingTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                fieldingTeam1Odds = float(winCount) / float(similarCount)
                                fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                            else:
                                fieldingTeam2Odds = float(winCount) / float(similarCount)
                                fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>=' + `(beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(ballsRem * 1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                    fieldingTeam2Odds = fieldingTeam2Odds2
                                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if runsReq == 0 and inn == 2:
                            fieldingTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                        fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        fieldOddsAdjFact = 0.0
                        if inn == 2:
                            fieldWinShares = (lastTeam1Odds - fieldingTeam1Odds) / 2

                            if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                                if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (
                                        lastTeam2OddsAdj / lastTeam2Odds)) / 2
                            else:
                                if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (
                                        lastTeam2Odds / lastTeam2OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                            if fieldingTeam1OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam1OddsAdj - 1.0)
                                fieldingTeam1OddsAdj = 1.0
                            if fieldingTeam1OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam1OddsAdj
                                fieldingTeam1OddsAdj = 0.0

                            lastTeam1Odds = fieldingTeam1Odds
                            lastTeam1OddsAdj = fieldingTeam1OddsAdj

                            if fielder in fieldingWinShares2:
                                fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                            else:
                                fieldingWinShares2[fielder] = fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                            if bowler in bowlingWinShares2:
                                bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                                bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                            else:
                                bowlingWinShares2[bowler] = -fieldWinShares
                                bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                        else:
                            fieldWinShares = (lastTeam2Odds - fieldingTeam2Odds) / 2

                            if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                                if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (
                                        lastTeam1OddsAdj / lastTeam1Odds)) / 2
                            else:
                                if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (
                                        lastTeam1Odds / lastTeam1OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                            if fieldingTeam2OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam2OddsAdj - 1.0)
                                fieldingTeam2OddsAdj = 1.0
                            if fieldingTeam2OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam2OddsAdj
                                fieldingTeam2OddsAdj = 0.0

                            lastTeam2Odds = fieldingTeam2Odds
                            lastTeam2OddsAdj = fieldingTeam2OddsAdj

                            if fielder in fieldingWinShares1:
                                fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares * 0.125
                                fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj * 0.125
                            else:
                                fieldingWinShares1[fielder] = fieldWinShares * 0.125
                                fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj * 0.125

                            if bowler in bowlingWinShares1:
                                bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares * 0.125
                                bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj * 0.125
                            else:
                                bowlingWinShares1[bowler] = -fieldWinShares * 0.125
                                bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj * 0.125

                for fielder in stumping:
                    for ins in range(0, stumping[fielder]):
                        beforeWkts = wkts - 1
                        if inn == 1:
                            if runs == 0:
                                c.execute('select result from overComparison where innings=1 and overs>=' + `(
                                    over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=1 and wkts>=' + `(
                                    beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>=' + `(
                                    over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=' + `(
                                    runs * 1.1)` + ' and runs>' + `(runs * 0.9)` + ' and wkts>=' + `(
                                    beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                                    beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                                    runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(
                                    ballsRem * 1.25)` + ' and ballsRem>' + `(ballsRem * 0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                                    beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                                    runsReq * 0.9)` + ' and runsReq<' + `(runsReq * 1.1)` + ' and ballsRem<=' + `(
                                    ballsRem * 1.1)` + ' and ballsRem>' + `(ballsRem * 0.9)`);

                        results = c.fetchall()

                        similarCount = 0
                        winCount = 0
                        fieldingTeam1Odds = 0.0
                        fieldingTeam2Odds = 0.0
                        fieldingTeam1OddsAdj = 0.0
                        fieldingTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                fieldingTeam1Odds = float(winCount) / float(similarCount)
                                fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                            else:
                                fieldingTeam2Odds = float(winCount) / float(similarCount)
                                fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                            beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                            runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(
                            ballsRem * 1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                    fieldingTeam2Odds = fieldingTeam2Odds2
                                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if runsReq == 0 and inn == 2:
                            fieldingTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                        fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        fieldOddsAdjFact = 0.0
                        if inn == 2:
                            fieldWinShares = (lastTeam1Odds - fieldingTeam1Odds) / 2

                            if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                                if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (
                                            lastTeam2OddsAdj / lastTeam2Odds)) / 2
                            else:
                                if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (
                                            lastTeam2Odds / lastTeam2OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                            if fieldingTeam1OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam1OddsAdj - 1.0)
                                fieldingTeam1OddsAdj = 1.0
                            if fieldingTeam1OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam1OddsAdj
                                fieldingTeam1OddsAdj = 0.0

                            lastTeam1Odds = fieldingTeam1Odds
                            lastTeam1OddsAdj = fieldingTeam1OddsAdj

                            if fielder in fieldingWinShares2:
                                fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                            else:
                                fieldingWinShares2[fielder] = fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                            if bowler in bowlingWinShares2:
                                bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                                bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                            else:
                                bowlingWinShares2[bowler] = -fieldWinShares
                                bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                        else:
                            fieldWinShares = (lastTeam2Odds - fieldingTeam2Odds) / 2

                            if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                                if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (
                                            lastTeam1OddsAdj / lastTeam1Odds)) / 2
                            else:
                                if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (
                                            lastTeam1Odds / lastTeam1OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                            if fieldingTeam2OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam2OddsAdj - 1.0)
                                fieldingTeam2OddsAdj = 1.0
                            if fieldingTeam2OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam2OddsAdj
                                fieldingTeam2OddsAdj = 0.0

                            lastTeam2Odds = fieldingTeam2Odds
                            lastTeam2OddsAdj = fieldingTeam2OddsAdj

                            if fielder in fieldingWinShares1:
                                fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares * 0.05
                                fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[
                                                                     fielder] + fieldWinSharesAdj * 0.05
                            else:
                                fieldingWinShares1[fielder] = fieldWinShares * 0.05
                                fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj * 0.05

                            if bowler in bowlingWinShares1:
                                bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares * 0.05
                                bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj * 0.05
                            else:
                                bowlingWinShares1[bowler] = -fieldWinShares * 0.05
                                bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj * 0.05

                for fielder in droppedOrMissed:
                    for ins in range(0,  droppedOrMissed[fielder]):
                        whatIfWkts = wkts + 1
                        if inn == 1:
                            if runs == 0:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                        results = c.fetchall()

                        similarCount = 0
                        winCount = 0
                        fieldingTeam1Odds = 0.0
                        fieldingTeam2Odds = 0.0
                        fieldingTeam1OddsAdj = 0.0
                        fieldingTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                fieldingTeam1Odds = float(winCount) / float(similarCount)
                                fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                            else:
                                fieldingTeam2Odds = float(winCount) / float(similarCount)
                                fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                    fieldingTeam2Odds = fieldingTeam2Odds2
                                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if runsReq == 0 and inn == 2:
                            fieldingTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                        fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        fieldOddsAdjFact = 0.0
                        if inn == 2:
                            fieldWinShares = lastTeam1Odds - fieldingTeam1Odds

                            if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                                if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                            else:
                                if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                            if fieldingTeam1OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam1OddsAdj - 1.0)
                                fieldingTeam1OddsAdj = 1.0
                            if fieldingTeam1OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam1OddsAdj
                                fieldingTeam1OddsAdj = 0.0

                            lastTeam1Odds = fieldingTeam1Odds
                            lastTeam1OddsAdj = fieldingTeam1OddsAdj

                            if fielder in fieldingWinShares2:
                                fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                            else:
                                fieldingWinShares2[fielder] = fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                            if bowler in bowlingWinShares2:
                                bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                                bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                            else:
                                bowlingWinShares2[bowler] = -fieldWinShares
                                bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                        else:
                            fieldWinShares = lastTeam2Odds - fieldingTeam2Odds

                            if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                                if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                            else:
                                if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                            if fieldingTeam2OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam2OddsAdj - 1.0)
                                fieldingTeam2OddsAdj = 1.0
                            if fieldingTeam2OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam2OddsAdj
                                fieldingTeam2OddsAdj = 0.0

                            lastTeam2Odds = fieldingTeam2Odds
                            lastTeam2OddsAdj = fieldingTeam2OddsAdj

                            if fielder in fieldingWinShares1:
                                fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares
                                fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj
                            else:
                                fieldingWinShares1[fielder] = fieldWinShares
                                fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj

                            if bowler in bowlingWinShares1:
                                bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares
                                bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj
                            else:
                                bowlingWinShares1[bowler] = -fieldWinShares
                                bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj

                directHitWkts = 0
                for fielder in directHit:
                    for ins in range(0,  directHit[fielder]):
                        directHitWkts = directHitWkts + 1
                        beforeWkts = wkts - 1
                        if inn == 1:
                            if runs == 0:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                        results = c.fetchall()

                        similarCount = 0
                        winCount = 0
                        fieldingTeam1Odds = 0.0
                        fieldingTeam2Odds = 0.0
                        fieldingTeam1OddsAdj = 0.0
                        fieldingTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                fieldingTeam1Odds = float(winCount) / float(similarCount)
                                fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                            else:
                                fieldingTeam2Odds = float(winCount) / float(similarCount)
                                fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                    fieldingTeam2Odds = fieldingTeam2Odds2
                                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if runsReq == 0 and inn == 2:
                            fieldingTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                        fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        fieldOddsAdjFact = 0.0
                        if inn == 2:
                            fieldWinShares = lastTeam1Odds - fieldingTeam1Odds

                            if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                                if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                            else:
                                if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                            if fieldingTeam1OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam1OddsAdj - 1.0)
                                fieldingTeam1OddsAdj = 1.0
                            if fieldingTeam1OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam1OddsAdj
                                fieldingTeam1OddsAdj = 0.0

                            lastTeam1Odds = fieldingTeam1Odds
                            lastTeam1OddsAdj = fieldingTeam1OddsAdj

                            if fielder in fieldingWinShares2:
                                fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                            else:
                                fieldingWinShares2[fielder] = fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                            if bowler in bowlingWinShares2:
                                bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                                bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                            else:
                                bowlingWinShares2[bowler] = -fieldWinShares
                                bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                        else:
                            fieldWinShares = lastTeam2Odds - fieldingTeam2Odds

                            if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                                if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                            else:
                                if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                            if fieldingTeam2OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam2OddsAdj - 1.0)
                                fieldingTeam2OddsAdj = 1.0
                            if fieldingTeam2OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam2OddsAdj
                                fieldingTeam2OddsAdj = 0.0

                            lastTeam2Odds = fieldingTeam2Odds
                            lastTeam2OddsAdj = fieldingTeam2OddsAdj

                            if fielder in fieldingWinShares1:
                                fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares
                                fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj
                            else:
                                fieldingWinShares1[fielder] = fieldWinShares
                                fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj

                            if bowler in bowlingWinShares1:
                                bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares
                                bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj
                            else:
                                bowlingWinShares1[bowler] = -fieldWinShares
                                bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj

                for fielder in greatCatch:
                    for ins in range(0,  greatCatch[fielder]):
                        beforeWkts = wkts - 1
                        if inn == 1:
                            if runs == 0:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                        results = c.fetchall()

                        similarCount = 0
                        winCount = 0
                        fieldingTeam1Odds = 0.0
                        fieldingTeam2Odds = 0.0
                        fieldingTeam1OddsAdj = 0.0
                        fieldingTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                fieldingTeam1Odds = float(winCount) / float(similarCount)
                                fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                            else:
                                fieldingTeam2Odds = float(winCount) / float(similarCount)
                                fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                    fieldingTeam2Odds = fieldingTeam2Odds2
                                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        if runsReq == 0 and inn == 2:
                            fieldingTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            fieldingTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                        fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                        fieldOddsAdjFact = 0.0
                        if inn == 2:
                            fieldWinShares = (lastTeam1Odds - fieldingTeam1Odds) / 2

                            if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                                if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                            else:
                                if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                            if fieldingTeam1OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam1OddsAdj - 1.0)
                                fieldingTeam1OddsAdj = 1.0
                            if fieldingTeam1OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam1OddsAdj
                                fieldingTeam1OddsAdj = 0.0

                            lastTeam1Odds = fieldingTeam1Odds
                            lastTeam1OddsAdj = fieldingTeam1OddsAdj

                            if fielder in fieldingWinShares2:
                                fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                            else:
                                fieldingWinShares2[fielder] = fieldWinShares
                                fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                            if bowler in bowlingWinShares2:
                                bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                                bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                            else:
                                bowlingWinShares2[bowler] = -fieldWinShares
                                bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                        else:
                            fieldWinShares = (lastTeam2Odds - fieldingTeam2Odds) / 2

                            if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                                if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                    elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                            else:
                                if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                    fieldOddsAdjFact = 1.0
                                else:
                                    if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                        fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                    elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                        fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                    else:
                                        fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                            fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                            fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                            if fieldingTeam2OddsAdj > 1:
                                fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam2OddsAdj - 1.0)
                                fieldingTeam2OddsAdj = 1.0
                            if fieldingTeam2OddsAdj < 0:
                                fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam2OddsAdj
                                fieldingTeam2OddsAdj = 0.0

                            lastTeam2Odds = fieldingTeam2Odds
                            lastTeam2OddsAdj = fieldingTeam2OddsAdj

                            if fielder in fieldingWinShares1:
                                fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares * 0.875
                                fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj * 0.875
                            else:
                                fieldingWinShares1[fielder] = fieldWinShares * 0.875
                                fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj * 0.875

                            if bowler in bowlingWinShares1:
                                bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares * 0.875
                                bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj * 0.875
                            else:
                                bowlingWinShares1[bowler] = -fieldWinShares * 0.875
                                bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj * 0.875

                for fielder in runsSaved:
                    if inn == 1:
                        whatIfRuns = runs + runsSaved[fielder]
                        if whatIfRuns == 0:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
                        else:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(whatIfRuns*1.1)`+' and runs>'+`(whatIfRuns*0.9)`+' and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
                    else:
                        whatIfRunsReq = runsReq - runsSaved[fielder]
                        if ballsRem < 24:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(whatIfRunsReq*0.75)`+' and runsReq<'+`(whatIfRunsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                        else:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(whatIfRunsReq*0.9)`+' and runsReq<'+`(whatIfRunsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                    results = c.fetchall()

                    similarCount = 0
                    winCount = 0
                    fieldingTeam1Odds = 0.0
                    fieldingTeam2Odds = 0.0
                    fieldingTeam1OddsAdj = 0.0
                    fieldingTeam2OddsAdj = 0.0
                    for y in range(0, len(results)):
                        similarCount += 1
                        result = results[y][0]
                        winCount = winCount + result / 2

                    if similarCount > 0:
                        if inn == 1:
                            fieldingTeam1Odds = float(winCount) / float(similarCount)
                            fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                        else:
                            fieldingTeam2Odds = float(winCount) / float(similarCount)
                            fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    if inn == 2:
                        similarCount2 = 0
                        winCount2 = 0
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(whatIfRunsReq*0.75)`+' and runsReq<'+`(whatIfRunsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                        results = c.fetchall()
                        for z in range(0, len(results)):
                            similarCount2 += 1
                            result = results[z][0]
                            winCount2 = winCount2 + result / 2

                        if similarCount2 > 0:
                            fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                            if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                fieldingTeam2Odds = fieldingTeam2Odds2
                                fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    if runsReq == 0 and inn == 2:
                        fieldingTeam2Odds = 1.0

                    if over == 20 and runsReq != 0 and inn == 2:
                        fieldingTeam2Odds = 0.0

                    if wkts == 10 and runsReq != 0 and inn == 2:
                        fieldingTeam2Odds = 0.0

                    if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    fieldOddsAdjFact = 0.0
                    if inn == 2:
                        fieldWinShares = lastTeam1Odds - fieldingTeam1Odds

                        if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                        if fieldingTeam1OddsAdj > 1:
                            fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam1OddsAdj - 1.0)
                            fieldingTeam1OddsAdj = 1.0
                        if fieldingTeam1OddsAdj < 0:
                            fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam1OddsAdj
                            fieldingTeam1OddsAdj = 0.0

                        lastTeam1Odds = fieldingTeam1Odds
                        lastTeam1OddsAdj = fieldingTeam1OddsAdj

                        if fielder in fieldingWinShares2:
                            fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares2[fielder] = fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = -fieldWinShares
                            bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                    else:
                        fieldWinShares = lastTeam2Odds - fieldingTeam2Odds

                        if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                        if fieldingTeam2OddsAdj > 1:
                            fieldWinSharesAdj = fieldWinSharesAdj - (fieldingTeam2OddsAdj - 1.0)
                            fieldingTeam2OddsAdj = 1.0
                        if fieldingTeam2OddsAdj < 0:
                            fieldWinSharesAdj = fieldWinSharesAdj - fieldingTeam2OddsAdj
                            fieldingTeam2OddsAdj = 0.0

                        lastTeam2Odds = fieldingTeam2Odds
                        lastTeam2OddsAdj = fieldingTeam2OddsAdj

                        if fielder in fieldingWinShares1:
                            fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares
                            fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares1[fielder] = fieldWinShares
                            fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares1[bowler] = -fieldWinShares
                            bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj

                fielderWkts = fielderWkts - directHitWkts # direct hit bowler win share adjustment already done
                if inn == 1:
                    if batsman1 in battingWinShares1:
                        if runsDiff > 0 and team1WinShares > 0:
                            battingWinShares1[batsman1] = battingWinShares1[batsman1] + team1WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj1[batsman1] = battingWinSharesAdj1[batsman1] + team1WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares1[batsman1] = battingWinShares1[batsman1] + team1WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj1[batsman1] = battingWinSharesAdj1[batsman1] + team1WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                    else:
                        if runsDiff > 0 and team1WinShares > 0:
                            battingWinShares1[batsman1] = team1WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj1[batsman1] = team1WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares1[batsman1] = team1WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj1[batsman1] = team1WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)

                    if lastBallDismissal == 0 and batsmanHasNotFaced == 0:
                        if batsman2 in battingWinShares1:
                            if runsDiff > 0 and team1WinShares > 0:
                                battingWinShares1[batsman2] = battingWinShares1[batsman2] + team1WinShares * float(batsmanScoreDiff2) / runsDiff
                                battingWinSharesAdj1[batsman2] = battingWinSharesAdj1[batsman2] + team1WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                            elif totDismissedBallFaced < 6:
                                battingWinShares1[batsman2] = battingWinShares1[batsman2] + team1WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                                battingWinSharesAdj1[batsman2] = battingWinSharesAdj1[batsman2] + team1WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                        else:
                            if runsDiff > 0 and team1WinShares > 0:
                                battingWinShares1[batsman2] = team1WinShares * float(batsmanScoreDiff2) / runsDiff
                                battingWinSharesAdj1[batsman2] = team1WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                            elif totDismissedBallFaced < 6:
                                battingWinShares1[batsman2] = team1WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                                battingWinSharesAdj1[batsman2] = team1WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)

                    if fielderWkts > 0:
                        wktsMod = wkts - fielderWkts
                        if inn == 1:
                            if runs == 0:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                        results = c.fetchall()

                        similarCount = 0
                        winCount = 0
                        noFieldWktsTeam1Odds = 0.0
                        noFieldWktsTeam2Odds = 0.0
                        noFieldWktsTeam1OddsAdj = 0.0
                        noFieldWktsTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                noFieldWktsTeam1Odds = float(winCount) / float(similarCount)
                                noFieldWktsTeam2Odds = 1.0 - noFieldWktsTeam1Odds
                            else:
                                noFieldWktsTeam2Odds = float(winCount) / float(similarCount)
                                noFieldWktsTeam1Odds = 1.0 - noFieldWktsTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                noFieldWktsTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if noFieldWktsTeam2Odds2 > noFieldWktsTeam2Odds:
                                    noFieldWktsTeam2Odds = noFieldWktsTeam2Odds2
                                    noFieldWktsTeam1Odds = 1.0 - noFieldWktsTeam2Odds

                        if runsReq == 0 and inn == 2:
                            noFieldWktsTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            noFieldWktsTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            noFieldWktsTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: noFieldWktsTeam2Odds = lastTeam2Odds
                        noFieldWktsTeam1Odds = 1.0 - noFieldWktsTeam2Odds

                        noFieldWktsOddsAdjFact = 0.0
                        noFieldWktsWinShares = lastTeam2Odds - noFieldWktsTeam2Odds

                        if lastTeam2OddsAdj >= lastTeam2Odds and noFieldWktsWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                noFieldWktsOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    noFieldWktsOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                noFieldWktsOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    noFieldWktsOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        noFieldWktsWinSharesAdj = noFieldWktsWinShares * noFieldWktsOddsAdjFact
                        noFieldWktsTeam2OddsAdj = lastTeam2OddsAdj + noFieldWktsWinSharesAdj

                        if noFieldWktsTeam2OddsAdj > 1:
                            noFieldWktsWinSharesAdj = noFieldWktsWinSharesAdj - (noFieldWktsTeam2OddsAdj - 1.0)
                            noFieldWktsTeam2OddsAdj = 1.0
                        if noFieldWktsTeam2OddsAdj < 0:
                            noFieldWktsWinSharesAdj = noFieldWktsWinSharesAdj - noFieldWktsTeam2OddsAdj
                            noFieldWktsTeam2OddsAdj = 0.0

                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] + team2WinShares - noFieldWktsWinShares
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] + team2WinSharesAdj - noFieldWktsWinSharesAdj
                        else:
                            bowlingWinShares1[bowler] = team2WinShares - noFieldWktsWinShares
                            bowlingWinSharesAdj1[bowler] = team2WinSharesAdj - noFieldWktsWinSharesAdj
                    else:
                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] + team2WinShares
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] + team2WinSharesAdj
                        else:
                            bowlingWinShares1[bowler] = team2WinShares
                            bowlingWinSharesAdj1[bowler] = team2WinSharesAdj
                    # print battingWinShares1
                    # print bowlingWinShares1
                    # print fieldingWinShares1
                    # print battingWinSharesAdj1
                    # print bowlingWinSharesAdj1
                    # print fieldingWinSharesAdj1
                else:
                    if batsman1 in battingWinShares2:
                        if runsDiff > 0 and team2WinShares > 0:
                            battingWinShares2[batsman1] = battingWinShares2[batsman1] + team2WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj2[batsman1] = battingWinSharesAdj2[batsman1] + team2WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares2[batsman1] = battingWinShares2[batsman1] + team2WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj2[batsman1] = battingWinSharesAdj2[batsman1] + team2WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                    else:
                        if runsDiff > 0 and team2WinShares > 0:
                            battingWinShares2[batsman1] = team2WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj2[batsman1] = team2WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares2[batsman1] = team2WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj2[batsman1] = team2WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)

                    if lastBallDismissal == 0 and batsmanHasNotFaced == 0:
                        if batsman2 in battingWinShares2:
                            if runsDiff > 0 and team2WinShares > 0:
                                battingWinShares2[batsman2] = battingWinShares2[batsman2] + team2WinShares * float(batsmanScoreDiff2) / runsDiff
                                battingWinSharesAdj2[batsman2] = battingWinSharesAdj2[batsman2] + team2WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                            elif totDismissedBallFaced < 6:
                                battingWinShares2[batsman2] = battingWinShares2[batsman2] + team2WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                                battingWinSharesAdj2[batsman2] = battingWinSharesAdj2[batsman2] + team2WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                        else:
                            if runsDiff > 0 and team2WinShares > 0:
                                battingWinShares2[batsman2] = team2WinShares * float(batsmanScoreDiff2) / runsDiff
                                battingWinSharesAdj2[batsman2] = team2WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                            elif totDismissedBallFaced < 6:
                                battingWinShares2[batsman2] = team2WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                                battingWinSharesAdj2[batsman2] = team2WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)

                    if fielderWkts > 0:
                        wktsMod = wkts - fielderWkts
                        if inn == 1:
                            if runs == 0:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`)
                            else:
                                c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`)
                        else:
                            if ballsRem < 24:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                            else:
                                c.execute('select result from overComparison where innings=2 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                        results = c.fetchall()

                        similarCount = 0
                        winCount = 0
                        noFieldWktsTeam1Odds = 0.0
                        noFieldWktsTeam2Odds = 0.0
                        noFieldWktsTeam1OddsAdj = 0.0
                        noFieldWktsTeam2OddsAdj = 0.0
                        for y in range(0, len(results)):
                            similarCount += 1
                            result = results[y][0]
                            winCount = winCount + result / 2

                        if similarCount > 0:
                            if inn == 1:
                                noFieldWktsTeam1Odds = float(winCount) / float(similarCount)
                                noFieldWktsTeam2Odds = 1.0 - noFieldWktsTeam1Odds
                            else:
                                noFieldWktsTeam2Odds = float(winCount) / float(similarCount)
                                noFieldWktsTeam1Odds = 1.0 - noFieldWktsTeam2Odds

                        if inn == 2:
                            similarCount2 = 0
                            winCount2 = 0
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(wktsMod-1)`+' and wkts<='+`(wktsMod+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                            results = c.fetchall()
                            for z in range(0, len(results)):
                                similarCount2 += 1
                                result = results[z][0]
                                winCount2 = winCount2 + result / 2

                            if similarCount2 > 0:
                                noFieldWktsTeam2Odds2 = float(winCount2) / float(similarCount2)
                                if noFieldWktsTeam2Odds2 > noFieldWktsTeam2Odds:
                                    noFieldWktsTeam2Odds = noFieldWktsTeam2Odds2
                                    noFieldWktsTeam1Odds = 1.0 - noFieldWktsTeam2Odds

                        if runsReq == 0 and inn == 2:
                            noFieldWktsTeam2Odds = 1.0

                        if over == 20 and runsReq != 0 and inn == 2:
                            noFieldWktsTeam2Odds = 0.0

                        if wkts == 10 and runsReq != 0 and inn == 2:
                            noFieldWktsTeam2Odds = 0.0

                        if similarCount == 0 and winCount == 0: noFieldWktsTeam2Odds = lastTeam2Odds
                        noFieldWktsTeam1Odds = 1.0 - noFieldWktsTeam2Odds

                        noFieldWktsOddsAdjFact = 0.0
                        noFieldWktsWinShares = lastTeam1Odds - noFieldWktsTeam1Odds

                        if lastTeam1OddsAdj >= lastTeam1Odds and noFieldWktsWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                noFieldWktsOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                else:
                                    noFieldWktsOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                noFieldWktsOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    noFieldWktsOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                else:
                                    noFieldWktsOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        noFieldWktsWinSharesAdj = noFieldWktsWinShares * noFieldWktsOddsAdjFact
                        noFieldWktsTeam1OddsAdj = lastTeam1OddsAdj + noFieldWktsWinSharesAdj

                        if noFieldWktsTeam1OddsAdj > 1:
                            noFieldWktsWinSharesAdj = noFieldWktsWinSharesAdj - (noFieldWktsTeam1OddsAdj - 1.0)
                            noFieldWktsTeam1OddsAdj = 1.0
                        if noFieldWktsTeam1OddsAdj < 0:
                            noFieldWktsWinSharesAdj = noFieldWktsWinSharesAdj - noFieldWktsTeam1OddsAdj
                            noFieldWktsTeam1OddsAdj = 0.0

                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] + team1WinShares - noFieldWktsWinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] + team1WinSharesAdj - noFieldWktsWinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = team1WinShares - noFieldWktsWinShares
                            bowlingWinSharesAdj2[bowler] = team1WinSharesAdj - noFieldWktsWinSharesAdj
                    else:
                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] + team1WinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] + team1WinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = team1WinShares
                            bowlingWinSharesAdj2[bowler] = team1WinSharesAdj
                    # print battingWinShares2
                    # print bowlingWinShares2
                    # print fieldingWinShares2
                    # print battingWinSharesAdj2
                    # print bowlingWinSharesAdj2
                    # print fieldingWinSharesAdj2
                lastRuns = runs
                lastWkts = wkts
                # if (int(over) == 20 and inn == 2): sads
        dismissedPlayer = {}
        dismissedPlayerBall = {}
        dismissedBat = {}
        totDismissedBallFaced = 0
        j = 0
        if ft20Id in rainedStops:
            if inn == rainedStops[ft20Id]: continue

        if over != 20 and lastBallDismissal == 0 and lastBallOfOverWin == 0 and batsmanHasNotFaced == 0:
            over += 1
            if inn == 1:
                if int(over) in wktOvers1:
                    for b in range(0, 6):
                        overBall = `int(over-1)`+"."+`(b+1)`
                        if overBall in wktPlayer1:
                            dismissedPlayer[j] = wktPlayer1[overBall]
                            dismissedPlayerBall[j] = b+1
                            if b == 5: lastBallDismissal = 1
                            j +=1
            else:
                if int(over) in wktOvers2:
                    for b in range(0, 6):
                        overBall = `int(over-1)`+"."+`(b+1)`
                        if overBall in wktPlayer2:
                            dismissedPlayer[j] = wktPlayer2[overBall]
                            dismissedPlayerBall[j] = b+1
                            if b == 5: lastBallDismissal = 1
                            j +=1

            if len(dismissedPlayer) > 0:
                for k in range(0, len(dismissedPlayer)):
                    dismissedPlayerFI = ""
                    if " " in dismissedPlayer[k]:
                        dismissedPlayerFI = dismissedPlayer[k].split(" ")[0]
                        dismissedPlayerFI = dismissedPlayerFI if dismissedPlayerFI.isupper() else ""
                        if dismissedPlayerFI != "": dismissedPlayer[k] = dismissedPlayer[k].split(" ")[1]

                    if inn == 1:
                        for batsmanName in batsmen1Names:
                            if dismissedPlayer[k] in batsmanName and (dismissedPlayerFI == "" or batsmanName[0] in dismissedPlayerFI):
                                dismissedBat[k] = batsmanName
                    else:
                        for batsmanName in batsmen2Names:
                            if dismissedPlayer[k] in batsmanName and (dismissedPlayerFI == "" or batsmanName[0] in dismissedPlayerFI):
                                dismissedBat[k] = batsmanName

                    if dismissedPlayer[k] == "Singh" and ft20Id == 154:
                        dismissedBat[k] = "RP Singh"
                        batsman2Id1[dismissedBat[k]] = 70563

            lastOverDismissed = []
            if len(dismissedPlayer) > 0:
                for k in range(0, len(dismissedBat)):
                    lastOverDismissed.append(dismissedBat[k])

                    if inn == 1:
                        if dismissedBat[k] in batsman2Runs:
                            batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id1[dismissedBat[k]]] - batsman2Runs[dismissedBat[k]]
                            batsmanBallDiff = dismissedBatsman2Balls[batsman2Id1[dismissedBat[k]]] - batsman2Balls[dismissedBat[k]]
                        else:
                            batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id1[dismissedBat[k]]]
                            batsmanBallDiff = dismissedBatsman2Balls[batsman2Id1[dismissedBat[k]]]
                        batsman2Runs[dismissedBat[k]] = dismissedBatsman2Runs[batsman2Id1[dismissedBat[k]]]
                        batsman2Balls[dismissedBat[k]] = dismissedBatsman2Balls[batsman2Id1[dismissedBat[k]]]
                    else:
                        if dismissedBat[k] in batsman2Runs:
                            batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id2[dismissedBat[k]]] - batsman2Runs[dismissedBat[k]]
                            batsmanBallDiff = dismissedBatsman2Balls[batsman2Id2[dismissedBat[k]]] - batsman2Balls[dismissedBat[k]]
                        else:
                            batsmanScoreDiff = dismissedBatsman2Runs[batsman2Id2[dismissedBat[k]]]
                            batsmanBallDiff = dismissedBatsman2Balls[batsman2Id2[dismissedBat[k]]]
                        batsman2Runs[dismissedBat[k]] = dismissedBatsman2Runs[batsman2Id2[dismissedBat[k]]]
                        batsman2Balls[dismissedBat[k]] = dismissedBatsman2Balls[batsman2Id2[dismissedBat[k]]]

                    similarCount = 0
                    winCount = 0
                    dismissedTotalRuns = lastRuns + batsmanScoreDiff
                    totDismissedBallFaced += batsmanBallDiff
                    lastRuns += batsmanScoreDiff
                    dismissedRunsReq = runsReq - batsmanScoreDiff
                    dismissedBallsRem = ballsRem - dismissedPlayerBall[k]
                    lastWkts += 1

                    if inn == 1:
                        if runs == 0:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`)
                        else:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(dismissedTotalRuns*1.1)`+' and runs>'+`(dismissedTotalRuns*0.9)`+' and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`)
                    else:
                        if ballsRem < 24:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`+' and runsReq>='+`(dismissedRunsReq*0.75)`+' and runsReq<'+`(dismissedRunsReq*1.25)`+' and ballsRem<='+`(dismissedBallsRem*1.25)`+' and ballsRem>'+`(dismissedBallsRem*0.75)`)
                        else:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`+' and runsReq>='+`(dismissedRunsReq*0.9)`+' and runsReq<'+`(dismissedRunsReq*1.1)`+' and ballsRem<='+`(dismissedBallsRem*1.1)`+' and ballsRem>'+`(dismissedBallsRem*0.9)`);

                    results = c.fetchall()
                    dismissalTeam1Odds = 0.0
                    dismissalTeam2Odds = 0.0
                    dismissalTeam1OddsAdj = 0.0
                    dismissalTeam2OddsAdj = 0.0
                    for y in range(0, len(results)):
                        similarCount += 1
                        result = results[y][0]
                        winCount = winCount + result / 2

                    if similarCount > 0:
                        dismissalTeam2Odds = float(winCount) / float(similarCount)
                        dismissalTeam1Odds = 1.0 - dismissalTeam2Odds

                    if inn == 2:
                        similarCount2 = 0
                        winCount2 = 0
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(lastWkts-1)`+' and wkts<='+`(lastWkts+1)`+' and runsReq>='+`(dismissedRunsReq*0.75)`+' and runsReq<'+`(dismissedRunsReq*1.25)`+' and ballsRem<='+`(dismissedBallsRem*1.25)`)

                        results = c.fetchall()
                        for z in range(0, len(results)):
                            similarCount2 += 1
                            result = results[z][0]
                            winCount2 = winCount2 + result / 2

                        if similarCount2 > 0:
                            dismissalTeam2Odds2 = float(winCount2) / float(similarCount2)
                            if dismissalTeam2Odds2 > dismissalTeam2Odds:
                                dismissalTeam2Odds = dismissalTeam2Odds2
                                dismissalTeam1Odds = 1.0 - dismissalTeam1Odds

                    if runsReq == 0 and inn == 2:
                        dismissalTeam2Odds = 1.0

                    if wkts == 10 and runsReq != 0 and inn == 2:
                        dismissalTeam2Odds = 0.0

                    if similarCount == 0 and winCount == 0: dismissalTeam2Odds = lastTeam2Odds
                    dismissalTeam1Odds = 1.0 - dismissalTeam2Odds

                    if inn == 1:
                        dismissedWinShares = dismissalTeam1Odds - lastTeam1Odds

                        if lastTeam1OddsAdj >= lastTeam1Odds and dismissedWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                disOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    disOddsAdjFact = lastTeam2OddsAdj / lastTeam2Odds
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    disOddsAdjFact = lastTeam1Odds / lastTeam1OddsAdj
                                else:
                                    disOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                disOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    disOddsAdjFact = lastTeam2Odds / lastTeam2OddsAdj
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    disOddsAdjFact = lastTeam1OddsAdj / lastTeam1Odds
                                else:
                                    disOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        dismissedWinSharesAdj = dismissedWinShares * disOddsAdjFact
                        dismissalTeam1OddsAdj = lastTeam1OddsAdj + dismissedWinSharesAdj

                        if dismissalTeam1OddsAdj > 1:
                            dismissalTeam1OddsAdj = 1.0
                        if dismissalTeam1OddsAdj < 0:
                            dismissalTeam1OddsAdj = 0.0

                        lastTeam1Odds = dismissalTeam1Odds
                        lastTeam1OddsAdj = dismissalTeam1OddsAdj

                        if dismissedBat[k] in battingWinShares1:
                            battingWinShares1[dismissedBat[k]] = battingWinShares1[dismissedBat[k]] + dismissedWinShares
                            battingWinSharesAdj1[dismissedBat[k]] = battingWinSharesAdj1[dismissedBat[k]] + dismissedWinSharesAdj
                        else:
                            battingWinShares1[dismissedBat[k]] = dismissedWinShares
                            battingWinSharesAdj1[dismissedBat[k]] = dismissedWinSharesAdj
                    else:
                        dismissedWinShares = dismissalTeam2Odds - lastTeam2Odds

                        if lastTeam2OddsAdj >= lastTeam2Odds and dismissedWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                disOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    disOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    disOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    disOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                disOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    disOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    disOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    disOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        dismissedWinSharesAdj = dismissedWinShares * disOddsAdjFact
                        dismissalTeam2OddsAdj = lastTeam2OddsAdj + dismissedWinSharesAdj

                        if dismissalTeam2OddsAdj > 1:
                            dismissalTeam2OddsAdj = 1.0
                        if dismissalTeam2OddsAdj < 0:
                            dismissalTeam2OddsAdj = 0.0

                        lastTeam2Odds = dismissalTeam2Odds
                        lastTeam2OddsAdj = dismissalTeam2OddsAdj

                        if dismissedBat[k] in battingWinShares2:
                            battingWinShares2[dismissedBat[k]] = battingWinShares2[dismissedBat[k]] + dismissedWinShares
                            battingWinSharesAdj2[dismissedBat[k]] = battingWinSharesAdj2[dismissedBat[k]] + dismissedWinSharesAdj
                        else:
                            battingWinShares2[dismissedBat[k]] = dismissedWinShares
                            battingWinSharesAdj2[dismissedBat[k]] = dismissedWinSharesAdj

            team2Odds = team2Win
            team1Odds = 1 - team2Odds
            team1WinShares = team1Odds - lastTeam1Odds
            team2WinShares = team2Odds - lastTeam2Odds

            if lastTeam1OddsAdj >= lastTeam1Odds and team1WinShares >= 0:
                if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                    oddsAdjFact = 1.0
                else:
                    if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                        oddsAdjFact = lastTeam2OddsAdj / lastTeam2Odds
                    elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                        oddsAdjFact = lastTeam1Odds / lastTeam1OddsAdj
                    else:
                        oddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
            else:
                if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                    oddsAdjFact = 1.0
                else:
                    if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                        oddsAdjFact = lastTeam2Odds / lastTeam2OddsAdj
                    elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                        oddsAdjFact = lastTeam1OddsAdj / lastTeam1Odds
                    else:
                        oddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

            team1WinSharesAdj = team1WinShares * oddsAdjFact
            team2WinSharesAdj = team2WinShares * oddsAdjFact
            lastTeam1OddsAdj = lastTeam1OddsAdj + team1WinSharesAdj
            lastTeam2OddsAdj = lastTeam2OddsAdj + team2WinSharesAdj
            if lastTeam1OddsAdj > 1:
                team1WinSharesAdj = team1WinSharesAdj - (lastTeam1OddsAdj - 1.0)
                lastTeam1OddsAdj = 1.0
            if lastTeam1OddsAdj < 0:
                team1WinSharesAdj = team1WinSharesAdj - lastTeam1OddsAdj
                lastTeam1OddsAdj = 0.0
            if lastTeam2OddsAdj > 1:
                team2WinSharesAdj = team2WinSharesAdj - (lastTeam2OddsAdj - 1.0)
                lastTeam2OddsAdj = 1.0
            if lastTeam2OddsAdj < 0:
                team2WinSharesAdj = team2WinSharesAdj - lastTeam2OddsAdj
                lastTeam2OddsAdj = 0.0

            # last over fielding events
            catch = {}
            stumping = {}
            droppedOrMissed = {}
            greatCatch = {}
            directHit = {}
            runsSaved = {}
            for b in range(0, 6):
                ball = b + 1
                eventId = `ft20Id` + `inn` + "'" + `(int(over)-1)` + "''" +`ball`+"'"
                c.execute('select fielder, fielderId, droppedCatch, missedStumping, greatCatch, directHit, runsSaved, catch, stumping from fieldingEventFT20 where eventId=?', (eventId,));
                results = c.fetchall()
                for ff in range(0, len(results)):
                    fielder = results[ff][0]
                    if results[ff][2] != 0:
                        if fielder in droppedOrMissed:
                            droppedOrMissed[fielder] = droppedOrMissed[fielder] + results[ff][2]
                        else:
                            droppedOrMissed[fielder] = results[ff][2]
                    if results[ff][3] != 0:
                        if fielder in droppedOrMissed:
                            droppedOrMissed[fielder] = droppedOrMissed[fielder] + results[ff][3]
                        else:
                            droppedOrMissed[fielder] = results[ff][3]
                    if results[ff][4] != 0:
                        if fielder in greatCatch:
                            greatCatch[fielder] = greatCatch[fielder] + results[ff][4]
                        else:
                            greatCatch[fielder] = results[ff][4]
                    if results[ff][5] != 0:
                        if fielder in directHit:
                            directHit[fielder] = directHit[fielder] + results[ff][5]
                        else:
                            directHit[fielder] = results[ff][5]
                    if results[ff][6] != 0:
                        if fielder in runsSaved:
                            runsSaved[fielder] = runsSaved[fielder] + results[ff][6]
                        else:
                            runsSaved[fielder] = results[ff][6]
                    if results[ff][7] != 0:
                        if fielder in catch:
                            catch[fielder] = catch[fielder] + results[ff][7]
                        else:
                            catch[fielder] = results[ff][7]
                    if results[ff][8] != 0:
                        if fielder in stumping:
                            stumping[fielder] = stumping[fielder] + results[ff][8]
                        else:
                            stumping[fielder] = results[ff][8]

            for fielder in catch:
                for ins in range(0, catch[fielder]):
                    beforeWkts = wkts - 1
                    if inn == 1:
                        if runs == 0:
                            c.execute('select result from overComparison where innings=1 and overs>=' + `(
                            over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=1 and wkts>=' + `(
                            beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                        else:
                            c.execute('select result from overComparison where innings=1 and overs>=' + `(
                            over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=' + `(
                            runs * 1.1)` + ' and runs>' + `(runs * 0.9)` + ' and wkts>=' + `(
                            beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                    else:
                        if ballsRem < 24:
                            c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                            beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                            runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(
                            ballsRem * 1.25)` + ' and ballsRem>' + `(ballsRem * 0.75)`)
                        else:
                            c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                            beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                            runsReq * 0.9)` + ' and runsReq<' + `(runsReq * 1.1)` + ' and ballsRem<=' + `(
                            ballsRem * 1.1)` + ' and ballsRem>' + `(ballsRem * 0.9)`);

                    results = c.fetchall()

                    similarCount = 0
                    winCount = 0
                    fieldingTeam1Odds = 0.0
                    fieldingTeam2Odds = 0.0
                    fieldingTeam1OddsAdj = 0.0
                    fieldingTeam2OddsAdj = 0.0
                    for y in range(0, len(results)):
                        similarCount += 1
                        result = results[y][0]
                        winCount = winCount + result / 2

                    if similarCount > 0:
                        if inn == 1:
                            fieldingTeam1Odds = float(winCount) / float(similarCount)
                            fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                        else:
                            fieldingTeam2Odds = float(winCount) / float(similarCount)
                            fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    if inn == 2:
                        similarCount2 = 0
                        winCount2 = 0
                        c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                        beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                        runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(
                        ballsRem * 1.25)`)

                        results = c.fetchall()
                        for z in range(0, len(results)):
                            similarCount2 += 1
                            result = results[z][0]
                            winCount2 = winCount2 + result / 2

                        if similarCount2 > 0:
                            fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                            if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                fieldingTeam2Odds = fieldingTeam2Odds2
                                fieldingTeam1Odds = 1.0 - fieldingTeam1Odds

                    if runsReq == 0 and inn == 2:
                        fieldingTeam2Odds = 1.0

                    if wkts == 10 and runsReq != 0 and inn == 2:
                        fieldingTeam2Odds = 0.0

                    if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    fieldOddsAdjFact = 0.0
                    if inn == 2:
                        fieldWinShares = (lastTeam1Odds - fieldingTeam1Odds) / 2

                        if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (
                                    lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (
                                    lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                        if fieldingTeam1OddsAdj > 1:
                            fieldingTeam1OddsAdj = 1.0
                        elif fieldingTeam1OddsAdj < 0:
                            fieldingTeam1OddsAdj = 0.0

                        lastTeam1Odds = fieldingTeam1Odds
                        lastTeam1OddsAdj = fieldingTeam1OddsAdj

                        if fielder in fieldingWinShares2:
                            fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares2[fielder] = fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = -fieldWinShares
                            bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                    else:
                        fieldWinShares = (lastTeam2Odds - fieldingTeam2Odds) / 2

                        if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (
                                    lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (
                                    lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                        if fieldingTeam2OddsAdj > 1:
                            fieldingTeam2OddsAdj = 1.0
                        elif fieldingTeam2OddsAdj < 0:
                            fieldingTeam2OddsAdj = 0.0

                        lastTeam2Odds = fieldingTeam2Odds
                        lastTeam2OddsAdj = fieldingTeam2OddsAdj

                        if fielder in fieldingWinShares1:
                            fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares * 0.125
                            fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj * 0.125
                        else:
                            fieldingWinShares1[fielder] = fieldWinShares * 0.125
                            fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj * 0.125

                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares * 0.125
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj * 0.125
                        else:
                            bowlingWinShares1[bowler] = -fieldWinShares * 0.125
                            bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj * 0.125

            for fielder in stumping:
                for ins in range(0, stumping[fielder]):
                    beforeWkts = wkts - 1
                    if inn == 1:
                        if runs == 0:
                            c.execute('select result from overComparison where innings=1 and overs>=' + `(
                                over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=1 and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                        else:
                            c.execute('select result from overComparison where innings=1 and overs>=' + `(
                                over - 1)` + ' and overs<' + `(over + 1)` + ' and runs<=' + `(
                                runs * 1.1)` + ' and runs>' + `(runs * 0.9)` + ' and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)`)
                    else:
                        if ballsRem < 24:
                            c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                                runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(
                                ballsRem * 1.25)` + ' and ballsRem>' + `(ballsRem * 0.75)`)
                        else:
                            c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                                beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                                runsReq * 0.9)` + ' and runsReq<' + `(runsReq * 1.1)` + ' and ballsRem<=' + `(
                                ballsRem * 1.1)` + ' and ballsRem>' + `(ballsRem * 0.9)`);

                    results = c.fetchall()

                    similarCount = 0
                    winCount = 0
                    fieldingTeam1Odds = 0.0
                    fieldingTeam2Odds = 0.0
                    fieldingTeam1OddsAdj = 0.0
                    fieldingTeam2OddsAdj = 0.0
                    for y in range(0, len(results)):
                        similarCount += 1
                        result = results[y][0]
                        winCount = winCount + result / 2

                    if similarCount > 0:
                        if inn == 1:
                            fieldingTeam1Odds = float(winCount) / float(similarCount)
                            fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                        else:
                            fieldingTeam2Odds = float(winCount) / float(similarCount)
                            fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    if inn == 2:
                        similarCount2 = 0
                        winCount2 = 0
                        c.execute('select result from overComparison where innings=2 and wkts>=' + `(
                            beforeWkts - 1)` + ' and wkts<=' + `(beforeWkts + 1)` + ' and runsReq>=' + `(
                            runsReq * 0.75)` + ' and runsReq<' + `(runsReq * 1.25)` + ' and ballsRem<=' + `(
                            ballsRem * 1.25)`)

                        results = c.fetchall()
                        for z in range(0, len(results)):
                            similarCount2 += 1
                            result = results[z][0]
                            winCount2 = winCount2 + result / 2

                        if similarCount2 > 0:
                            fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                            if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                fieldingTeam2Odds = fieldingTeam2Odds2
                                fieldingTeam1Odds = 1.0 - fieldingTeam1Odds

                    if runsReq == 0 and inn == 2:
                        fieldingTeam2Odds = 1.0

                    if wkts == 10 and runsReq != 0 and inn == 2:
                        fieldingTeam2Odds = 0.0

                    if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    fieldOddsAdjFact = 0.0
                    if inn == 2:
                        fieldWinShares = (lastTeam1Odds - fieldingTeam1Odds) / 2

                        if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (
                                        lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (
                                        lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                        if fieldingTeam1OddsAdj > 1:
                            fieldingTeam1OddsAdj = 1.0
                        elif fieldingTeam1OddsAdj < 0:
                            fieldingTeam1OddsAdj = 0.0

                        lastTeam1Odds = fieldingTeam1Odds
                        lastTeam1OddsAdj = fieldingTeam1OddsAdj

                        if fielder in fieldingWinShares2:
                            fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares2[fielder] = fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = -fieldWinShares
                            bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                    else:
                        fieldWinShares = (lastTeam2Odds - fieldingTeam2Odds) / 2

                        if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (
                                        lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (
                                        lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                        if fieldingTeam2OddsAdj > 1:
                            fieldingTeam2OddsAdj = 1.0
                        elif fieldingTeam2OddsAdj < 0:
                            fieldingTeam2OddsAdj = 0.0

                        lastTeam2Odds = fieldingTeam2Odds
                        lastTeam2OddsAdj = fieldingTeam2OddsAdj

                        if fielder in fieldingWinShares1:
                            fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares * 0.05
                            fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj * 0.05
                        else:
                            fieldingWinShares1[fielder] = fieldWinShares * 0.05
                            fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj * 0.05

                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares * 0.05
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj * 0.05
                        else:
                            bowlingWinShares1[bowler] = -fieldWinShares * 0.05
                            bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj * 0.05

            for fielder in droppedOrMissed:
                for ins in range(0,  droppedOrMissed[fielder]):
                    whatIfWkts = wkts + 1
                    if inn == 1:
                        if runs == 0:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`)
                        else:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`)
                    else:
                        if ballsRem < 24:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                        else:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                    results = c.fetchall()

                    similarCount = 0
                    winCount = 0
                    fieldingTeam1Odds = 0.0
                    fieldingTeam2Odds = 0.0
                    fieldingTeam1OddsAdj = 0.0
                    fieldingTeam2OddsAdj = 0.0
                    for y in range(0, len(results)):
                        similarCount += 1
                        result = results[y][0]
                        winCount = winCount + result / 2

                    if similarCount > 0:
                        if inn == 1:
                            fieldingTeam1Odds = float(winCount) / float(similarCount)
                            fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                        else:
                            fieldingTeam2Odds = float(winCount) / float(similarCount)
                            fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    if inn == 2:
                        similarCount2 = 0
                        winCount2 = 0
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(whatIfWkts-1)`+' and wkts<='+`(whatIfWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                        results = c.fetchall()
                        for z in range(0, len(results)):
                            similarCount2 += 1
                            result = results[z][0]
                            winCount2 = winCount2 + result / 2

                        if similarCount2 > 0:
                            fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                            if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                fieldingTeam2Odds = fieldingTeam2Odds2
                                fieldingTeam1Odds = 1.0 - fieldingTeam1Odds

                    if runsReq == 0 and inn == 2:
                        fieldingTeam2Odds = 1.0

                    if wkts == 10 and runsReq != 0 and inn == 2:
                        fieldingTeam2Odds = 0.0

                    if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    fieldOddsAdjFact = 0.0
                    if inn == 2:
                        fieldWinShares = lastTeam1Odds - fieldingTeam1Odds

                        if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                        if fieldingTeam1OddsAdj > 1:
                            fieldingTeam1OddsAdj = 1.0
                        elif fieldingTeam1OddsAdj < 0:
                            fieldingTeam1OddsAdj = 0.0

                        lastTeam1Odds = fieldingTeam1Odds
                        lastTeam1OddsAdj = fieldingTeam1OddsAdj

                        if fielder in fieldingWinShares2:
                            fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares2[fielder] = fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = -fieldWinShares
                            bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                    else:
                        fieldWinShares = lastTeam2Odds - fieldingTeam2Odds

                        if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                        if fieldingTeam2OddsAdj > 1:
                            fieldingTeam2OddsAdj = 1.0
                        elif fieldingTeam2OddsAdj < 0:
                            fieldingTeam2OddsAdj = 0.0

                        lastTeam2Odds = fieldingTeam2Odds
                        lastTeam2OddsAdj = fieldingTeam2OddsAdj

                        if fielder in fieldingWinShares1:
                            fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares
                            fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares1[fielder] = fieldWinShares
                            fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares1[bowler] = -fieldWinShares
                            bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj

            for fielder in directHit:
                for ins in range(0,  directHit[fielder]):
                    beforeWkts = wkts - 1
                    if inn == 1:
                        if runs == 0:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                        else:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                    else:
                        if ballsRem < 24:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                        else:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                    results = c.fetchall()

                    similarCount = 0
                    winCount = 0
                    fieldingTeam1Odds = 0.0
                    fieldingTeam2Odds = 0.0
                    fieldingTeam1OddsAdj = 0.0
                    fieldingTeam2OddsAdj = 0.0
                    for y in range(0, len(results)):
                        similarCount += 1
                        result = results[y][0]
                        winCount = winCount + result / 2

                    if similarCount > 0:
                        if inn == 1:
                            fieldingTeam1Odds = float(winCount) / float(similarCount)
                            fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                        else:
                            fieldingTeam2Odds = float(winCount) / float(similarCount)
                            fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    if inn == 2:
                        similarCount2 = 0
                        winCount2 = 0
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                        results = c.fetchall()
                        for z in range(0, len(results)):
                            similarCount2 += 1
                            result = results[z][0]
                            winCount2 = winCount2 + result / 2

                        if similarCount2 > 0:
                            fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                            if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                fieldingTeam2Odds = fieldingTeam2Odds2
                                fieldingTeam1Odds = 1.0 - fieldingTeam1Odds

                    if runsReq == 0 and inn == 2:
                        fieldingTeam2Odds = 1.0

                    if wkts == 10 and runsReq != 0 and inn == 2:
                        fieldingTeam2Odds = 0.0

                    if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    fieldOddsAdjFact = 0.0
                    if inn == 2:
                        fieldWinShares = lastTeam1Odds - fieldingTeam1Odds

                        if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                        if fieldingTeam1OddsAdj > 1:
                            fieldingTeam1OddsAdj = 1.0
                        elif fieldingTeam1OddsAdj < 0:
                            fieldingTeam1OddsAdj = 0.0

                        lastTeam1Odds = fieldingTeam1Odds
                        lastTeam1OddsAdj = fieldingTeam1OddsAdj

                        if fielder in fieldingWinShares2:
                            fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares2[fielder] = fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = -fieldWinShares
                            bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                    else:
                        fieldWinShares = lastTeam2Odds - fieldingTeam2Odds

                        if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                        if fieldingTeam2OddsAdj > 1:
                            fieldingTeam2OddsAdj = 1.0
                        elif fieldingTeam2OddsAdj < 0:
                            fieldingTeam2OddsAdj = 0.0

                        lastTeam2Odds = fieldingTeam2Odds
                        lastTeam2OddsAdj = fieldingTeam2OddsAdj

                        if fielder in fieldingWinShares1:
                            fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares
                            fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares1[fielder] = fieldWinShares
                            fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares1[bowler] = -fieldWinShares
                            bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj

            for fielder in greatCatch:
                for ins in range(0,  greatCatch[fielder]):
                    beforeWkts = wkts - 1
                    if inn == 1:
                        if runs == 0:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                        else:
                            c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(runs*1.1)`+' and runs>'+`(runs*0.9)`+' and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`)
                    else:
                        if ballsRem < 24:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                        else:
                            c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                    results = c.fetchall()

                    similarCount = 0
                    winCount = 0
                    fieldingTeam1Odds = 0.0
                    fieldingTeam2Odds = 0.0
                    fieldingTeam1OddsAdj = 0.0
                    fieldingTeam2OddsAdj = 0.0
                    for y in range(0, len(results)):
                        similarCount += 1
                        result = results[y][0]
                        winCount = winCount + result / 2

                    if similarCount > 0:
                        if inn == 1:
                            fieldingTeam1Odds = float(winCount) / float(similarCount)
                            fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                        else:
                            fieldingTeam2Odds = float(winCount) / float(similarCount)
                            fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    if inn == 2:
                        similarCount2 = 0
                        winCount2 = 0
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(beforeWkts-1)`+' and wkts<='+`(beforeWkts+1)`+' and runsReq>='+`(runsReq*0.75)`+' and runsReq<'+`(runsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                        results = c.fetchall()
                        for z in range(0, len(results)):
                            similarCount2 += 1
                            result = results[z][0]
                            winCount2 = winCount2 + result / 2

                        if similarCount2 > 0:
                            fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                            if fieldingTeam2Odds2 > fieldingTeam2Odds:
                                fieldingTeam2Odds = fieldingTeam2Odds2
                                fieldingTeam1Odds = 1.0 - fieldingTeam1Odds

                    if runsReq == 0 and inn == 2:
                        fieldingTeam2Odds = 1.0

                    if wkts == 10 and runsReq != 0 and inn == 2:
                        fieldingTeam2Odds = 0.0

                    if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                    fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                    fieldOddsAdjFact = 0.0
                    if inn == 2:
                        fieldWinShares = (lastTeam1Odds - fieldingTeam1Odds) / 2

                        if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                            if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                        else:
                            if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                        if fieldingTeam1OddsAdj > 1:
                            fieldingTeam1OddsAdj = 1.0
                        elif fieldingTeam1OddsAdj < 0:
                            fieldingTeam1OddsAdj = 0.0

                        lastTeam1Odds = fieldingTeam1Odds
                        lastTeam1OddsAdj = fieldingTeam1OddsAdj

                        if fielder in fieldingWinShares2:
                            fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                        else:
                            fieldingWinShares2[fielder] = fieldWinShares
                            fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                        if bowler in bowlingWinShares2:
                            bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                            bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                        else:
                            bowlingWinShares2[bowler] = -fieldWinShares
                            bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                    else:
                        fieldWinShares = (lastTeam2Odds - fieldingTeam2Odds) / 2

                        if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                            if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                                elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                        else:
                            if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                                fieldOddsAdjFact = 1.0
                            else:
                                if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                    fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                                elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                    fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                                else:
                                    fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                        fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                        fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                        if fieldingTeam2OddsAdj > 1:
                            fieldingTeam2OddsAdj = 1.0
                        elif fieldingTeam2OddsAdj < 0:
                            fieldingTeam2OddsAdj = 0.0

                        lastTeam2Odds = fieldingTeam2Odds
                        lastTeam2OddsAdj = fieldingTeam2OddsAdj

                        if fielder in fieldingWinShares1:
                            fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares * 0.875
                            fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj * 0.875
                        else:
                            fieldingWinShares1[fielder] = fieldWinShares * 0.875
                            fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj * 0.875

                        if bowler in bowlingWinShares1:
                            bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares * 0.875
                            bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj * 0.875
                        else:
                            bowlingWinShares1[bowler] = -fieldWinShares * 0.875
                            bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj * 0.875

            for fielder in runsSaved:
                if inn == 1:
                    whatIfRuns = runs + runsSaved[fielder]
                    if whatIfRuns == 0:
                        c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<=1 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
                    else:
                        c.execute('select result from overComparison where innings=1 and overs>='+`(over-1)`+' and overs<'+`(over+1)`+' and runs<='+`(whatIfRuns*1.1)`+' and runs>'+`(whatIfRuns*0.9)`+' and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`)
                else:
                    whatIfRunsReq = runsReq - runsSaved[fielder]
                    if ballsRem < 24:
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(whatIfRunsReq*0.75)`+' and runsReq<'+`(whatIfRunsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`+' and ballsRem>'+`(ballsRem*0.75)`)
                    else:
                        c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(whatIfRunsReq*0.9)`+' and runsReq<'+`(whatIfRunsReq*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)`);

                results = c.fetchall()

                similarCount = 0
                winCount = 0
                fieldingTeam1Odds = 0.0
                fieldingTeam2Odds = 0.0
                fieldingTeam1OddsAdj = 0.0
                fieldingTeam2OddsAdj = 0.0
                for y in range(0, len(results)):
                    similarCount += 1
                    result = results[y][0]
                    winCount = winCount + result / 2

                if similarCount > 0:
                    if inn == 1:
                        fieldingTeam1Odds = float(winCount) / float(similarCount)
                        fieldingTeam2Odds = 1.0 - fieldingTeam1Odds
                    else:
                        fieldingTeam2Odds = float(winCount) / float(similarCount)
                        fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                if inn == 2:
                    similarCount2 = 0
                    winCount2 = 0
                    c.execute('select result from overComparison where innings=2 and wkts>='+`(wkts-1)`+' and wkts<='+`(wkts+1)`+' and runsReq>='+`(whatIfRunsReq*0.75)`+' and runsReq<'+`(whatIfRunsReq*1.25)`+' and ballsRem<='+`(ballsRem*1.25)`)

                    results = c.fetchall()
                    for z in range(0, len(results)):
                        similarCount2 += 1
                        result = results[z][0]
                        winCount2 = winCount2 + result / 2

                    if similarCount2 > 0:
                        fieldingTeam2Odds2 = float(winCount2) / float(similarCount2)
                        if fieldingTeam2Odds2 > fieldingTeam2Odds:
                            fieldingTeam2Odds = fieldingTeam2Odds2
                            fieldingTeam1Odds = 1.0 - fieldingTeam1Odds

                if runsReq == 0 and inn == 2:
                    fieldingTeam2Odds = 1.0

                if wkts == 10 and runsReq != 0 and inn == 2:
                    fieldingTeam2Odds = 0.0

                if similarCount == 0 and winCount == 0: fieldingTeam2Odds = lastTeam2Odds
                fieldingTeam1Odds = 1.0 - fieldingTeam2Odds

                fieldOddsAdjFact = 0.0
                if inn == 2:
                    fieldWinShares = lastTeam1Odds - fieldingTeam1Odds

                    if lastTeam1OddsAdj >= lastTeam1Odds and fieldWinShares >= 0:
                        if lastTeam1OddsAdj == 0.0 or lastTeam2Odds == 0.0:
                            fieldOddsAdjFact = 1.0
                        else:
                            if (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                            elif (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                            else:
                                fieldOddsAdjFact = ((lastTeam1Odds / lastTeam1OddsAdj) + (lastTeam2OddsAdj / lastTeam2Odds)) / 2
                    else:
                        if lastTeam1Odds == 0.0 or lastTeam2OddsAdj == 0.0:
                            fieldOddsAdjFact = 1.0
                        else:
                            if (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                            elif (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                            else:
                                fieldOddsAdjFact = ((lastTeam1OddsAdj / lastTeam1Odds) + (lastTeam2Odds / lastTeam2OddsAdj)) / 2

                    fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                    fieldingTeam1OddsAdj = lastTeam1OddsAdj + fieldWinSharesAdj

                    if fieldingTeam1OddsAdj > 1:
                        fieldingTeam1OddsAdj = 1.0
                    elif fieldingTeam1OddsAdj < 0:
                        fieldingTeam1OddsAdj = 0.0

                    lastTeam1Odds = fieldingTeam1Odds
                    lastTeam1OddsAdj = fieldingTeam1OddsAdj

                    if fielder in fieldingWinShares2:
                        fieldingWinShares2[fielder] = fieldingWinShares2[fielder] + fieldWinShares
                        fieldingWinSharesAdj2[fielder] = fieldingWinSharesAdj2[fielder] + fieldWinSharesAdj
                    else:
                        fieldingWinShares2[fielder] = fieldWinShares
                        fieldingWinSharesAdj2[fielder] = fieldWinSharesAdj

                    if bowler in bowlingWinShares2:
                        bowlingWinShares2[bowler] = bowlingWinShares2[bowler] - fieldWinShares
                        bowlingWinSharesAdj2[bowler] = bowlingWinSharesAdj2[bowler] - fieldWinSharesAdj
                    else:
                        bowlingWinShares2[bowler] = -fieldWinShares
                        bowlingWinSharesAdj2[bowler] = -fieldWinSharesAdj
                else:
                    fieldWinShares = lastTeam2Odds - fieldingTeam2Odds

                    if lastTeam2OddsAdj >= lastTeam2Odds and fieldWinShares >= 0:
                        if lastTeam2OddsAdj == 0.0 or lastTeam1Odds == 0.0:
                            fieldOddsAdjFact = 1.0
                        else:
                            if (lastTeam2Odds / lastTeam2OddsAdj) > 10:
                                fieldOddsAdjFact = (lastTeam1OddsAdj / lastTeam1Odds)
                            elif (lastTeam1OddsAdj / lastTeam1Odds) > 10:
                                fieldOddsAdjFact = (lastTeam2Odds / lastTeam2OddsAdj)
                            else:
                                fieldOddsAdjFact = ((lastTeam2Odds / lastTeam2OddsAdj) + (lastTeam1OddsAdj / lastTeam1Odds)) / 2
                    else:
                        if lastTeam2Odds == 0.0 or lastTeam1OddsAdj == 0.0:
                            fieldOddsAdjFact = 1.0
                        else:
                            if (lastTeam2OddsAdj / lastTeam2Odds) > 10:
                                fieldOddsAdjFact = (lastTeam1Odds / lastTeam1OddsAdj)
                            elif (lastTeam1Odds / lastTeam1OddsAdj) > 10:
                                fieldOddsAdjFact = (lastTeam2OddsAdj / lastTeam2Odds)
                            else:
                                fieldOddsAdjFact = ((lastTeam2OddsAdj / lastTeam2Odds) + (lastTeam1Odds / lastTeam1OddsAdj)) / 2

                    fieldWinSharesAdj = fieldWinShares * fieldOddsAdjFact
                    fieldingTeam2OddsAdj = lastTeam2OddsAdj + fieldWinSharesAdj

                    if fieldingTeam2OddsAdj > 1:
                        fieldingTeam2OddsAdj = 1.0
                    elif fieldingTeam2OddsAdj < 0:
                        fieldingTeam2OddsAdj = 0.0

                    lastTeam2Odds = fieldingTeam2Odds
                    lastTeam2OddsAdj = fieldingTeam2OddsAdj

                    if fielder in fieldingWinShares1:
                        fieldingWinShares1[fielder] = fieldingWinShares1[fielder] + fieldWinShares
                        fieldingWinSharesAdj1[fielder] = fieldingWinSharesAdj1[fielder] + fieldWinSharesAdj
                    else:
                        fieldingWinShares1[fielder] = fieldWinShares
                        fieldingWinSharesAdj1[fielder] = fieldWinSharesAdj

                    if bowler in bowlingWinShares1:
                        bowlingWinShares1[bowler] = bowlingWinShares1[bowler] - fieldWinShares
                        bowlingWinSharesAdj1[bowler] = bowlingWinSharesAdj1[bowler] - fieldWinSharesAdj
                    else:
                        bowlingWinShares1[bowler] = -fieldWinShares
                        bowlingWinSharesAdj1[bowler] = -fieldWinSharesAdj

            c.execute('select player from bowlingFT20Innings where ft20Id=? and innings=? and balls % 6 <> 0',(ft20Id, inn))
            lastOverB = c.fetchall()
            if len(lastOverB) == 1:
                lastOverBowlerName = lastOverB[0][0]
            elif ft20Id in ft20Id2LastOverBowlerInn:
                if ft20Id2LastOverBowlerInn[ft20Id] == inn:
                    lastOverBowlerName = ft20Id2LastOverBowler[int(`ft20Id` + `inn`)]

            runsDiff = team2TotRuns - lastRuns
            if batsman1 not in lastOverDismissed and batsman1 != "":
                if batsman1 in batsman2Runs:
                    batsmanScoreDiff1 = notOutBatsman2Runs[batsman1] - batsman2Runs[batsman1]
                    batsmanBallDiff1 = notOutBatsman2Balls[batsman1] - batsman2Balls[batsman1]
                else:
                    batsmanScoreDiff1 = notOutBatsman2Runs[batsman1]
                    batsmanBallDiff1 = notOutBatsman2Balls[batsman1]

            if batsman2 not in lastOverDismissed and batsman2 != "":
                if batsman2 in batsman2Runs:
                    batsmanScoreDiff2 = notOutBatsman2Runs[batsman2] - batsman2Runs[batsman2]
                    batsmanBallDiff2 = notOutBatsman2Balls[batsman2] - batsman2Balls[batsman2]
                else:
                    batsmanScoreDiff2 = notOutBatsman2Runs[batsman2]
                    batsmanBallDiff2 = notOutBatsman2Balls[batsman2]

            if inn == 1:
                if batsman1 not in lastOverDismissed:
                    if batsman1 in battingWinShares1:
                        if runsDiff > 0 and team1WinShares > 0:
                            battingWinShares1[batsman1] = battingWinShares1[batsman1] + team1WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj1[batsman1] = battingWinSharesAdj1[batsman1] + team1WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares1[batsman1] = battingWinShares1[batsman1] + team1WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj1[batsman1] = battingWinSharesAdj1[batsman1] + team1WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                    else:
                        if runsDiff > 0 and team1WinShares > 0:
                            battingWinShares1[batsman1] = team1WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj1[batsman1] = team1WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares1[batsman1] = team1WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj1[batsman1] = team1WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)

                if batsman2 not in lastOverDismissed:
                    if batsman2 in battingWinShares1:
                        if runsDiff > 0 and team1WinShares > 0:
                            battingWinShares1[batsman2] = battingWinShares1[batsman2] + team1WinShares * float(batsmanScoreDiff2) / runsDiff
                            battingWinSharesAdj1[batsman2] = battingWinSharesAdj1[batsman2] + team1WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares1[batsman2] = battingWinShares1[batsman2] + team1WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj1[batsman2] = battingWinSharesAdj1[batsman2] + team1WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                    else:
                        if runsDiff > 0 and team1WinShares > 0:
                            battingWinShares1[batsman2] = team1WinShares * float(batsmanScoreDiff2) / runsDiff
                            battingWinSharesAdj1[batsman2] = team1WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares1[batsman2] = team1WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj1[batsman2] = team1WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)

                if lastOverBowlerName in bowlingWinShares1:
                    bowlingWinShares1[lastOverBowlerName] = bowlingWinShares1[lastOverBowlerName] + team2WinShares
                    bowlingWinSharesAdj1[lastOverBowlerName] = bowlingWinSharesAdj1[lastOverBowlerName] + team2WinSharesAdj
                else:
                    bowlingWinShares1[lastOverBowlerName] = team2WinShares
                    bowlingWinSharesAdj1[lastOverBowlerName] = team2WinSharesAdj
            else:
                if batsman1 not in lastOverDismissed:
                    if batsman1 in battingWinShares2:
                        if runsDiff > 0 and team2WinShares > 0:
                            battingWinShares2[batsman1] = battingWinShares2[batsman1] + team2WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj2[batsman1] = battingWinSharesAdj2[batsman1] + team2WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares2[batsman1] = battingWinShares2[batsman1] + team2WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj2[batsman1] = battingWinSharesAdj2[batsman1] + team2WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                    else:
                        if runsDiff > 0 and team2WinShares > 0:
                            battingWinShares2[batsman1] = team2WinShares * float(batsmanScoreDiff1) / runsDiff
                            battingWinSharesAdj2[batsman1] = team2WinSharesAdj * float(batsmanScoreDiff1) / runsDiff
                        else:
                            battingWinShares2[batsman1] = team2WinShares * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj2[batsman1] = team2WinSharesAdj * float(batsmanBallDiff1) / (6 - totDismissedBallFaced)

                if batsman2 not in lastOverDismissed:
                    if batsman2 in battingWinShares2:
                        if runsDiff > 0 and team2WinShares > 0:
                            battingWinShares2[batsman2] = battingWinShares2[batsman2] + team2WinShares * float(batsmanScoreDiff2) / runsDiff
                            battingWinSharesAdj2[batsman2] = battingWinSharesAdj2[batsman2] + team2WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares2[batsman2] = battingWinShares2[batsman2] + team2WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj2[batsman2] = battingWinSharesAdj2[batsman2] + team2WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                    else:
                        if runsDiff > 0 and team2WinShares > 0:
                            battingWinShares2[batsman2] = team2WinShares * float(batsmanScoreDiff2) / runsDiff
                            battingWinSharesAdj2[batsman2] = team2WinSharesAdj * float(batsmanScoreDiff2) / runsDiff
                        elif totDismissedBallFaced < 6:
                            battingWinShares2[batsman2] = team2WinShares * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)
                            battingWinSharesAdj2[batsman2] = team2WinSharesAdj * float(batsmanBallDiff2) / (6 - totDismissedBallFaced)

                if lastOverBowlerName in bowlingWinShares2:
                    bowlingWinShares2[lastOverBowlerName] = bowlingWinShares2[lastOverBowlerName] + team1WinShares
                    bowlingWinSharesAdj2[lastOverBowlerName] = bowlingWinSharesAdj2[lastOverBowlerName] + team1WinSharesAdj
                else:
                    bowlingWinShares2[lastOverBowlerName] = team1WinShares
                    bowlingWinSharesAdj2[lastOverBowlerName] = team1WinSharesAdj

    battingRating = {}
    bowlingRating = {}
    fieldingRating = {}
    totalRating = {}
    numCareerMatches = {}

    for batsman in battingWinShares1:
        if batsman == "": continue
        battingWS = 0
        bowlingWS = 0
        fieldingWS = 0
        battingWSAdj = 0
        bowlingWSAdj = 0
        fieldingWSAdj = 0
        batsmanId = batsman2Id1[batsman]
        battingWS = battingWinShares1[batsman]
        battingWSAdj = battingWinSharesAdj1[batsman]
        if batsman in bowlingWinShares2:
            bowlingWS = bowlingWinShares2[batsman]
            bowlingWSAdj = bowlingWinSharesAdj2[batsman]
        if batsman in fieldingWinShares2:
            fieldingWS = fieldingWinShares2[batsman]
            fieldingWSAdj = fieldingWinSharesAdj2[batsman]
        totalWS = battingWS + bowlingWS + fieldingWS
        totalWSAdj = battingWSAdj + bowlingWSAdj + fieldingWSAdj
        matchId = repr(int(ft20Id)) + repr(batsmanId)
        print batsman + ": " + `totalWS` + ": " + `totalWSAdj`
        c.execute('insert or ignore into winSharesFT20Match (matchId, playerId, player, ft20Id, battingWS, bowlingWS, fieldingWS, totalWS, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, batsmanId, batsman, ft20Id, battingWS, bowlingWS, fieldingWS, totalWS, battingWSAdj, bowlingWSAdj, fieldingWSAdj, totalWSAdj))

        c.execute('select matchId, battingRating, bowlingRating, fieldingRating, totalRating from winSharesFT20Live where playerId=? order by matchId desc', (batsmanId, ))
        liveRating = c.fetchone()
        if liveRating is None:
            battingRating[batsmanId] = 0
            bowlingRating[batsmanId] = 0
            fieldingRating[batsmanId] = 0
            totalRating[batsmanId] = 0
            numCareerMatches[batsmanId] = 0
        else:
            battingRating[batsmanId] = liveRating[1]
            bowlingRating[batsmanId] = liveRating[2]
            fieldingRating[batsmanId] = liveRating[3]
            totalRating[batsmanId] = liveRating[4]
            numCareerMatches[batsmanId] = len(c.fetchall())+1

        battingLiveRating = 0
        bowlingLiveRating = 0
        fieldingLiveRating = 0
        totalLiveRating = 0
        if numCareerMatches[batsmanId] == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            battingLiveRating = battingWSAdj * 0.15
            bowlingLiveRating = bowlingWSAdj * 0.15
            fieldingLiveRating = fieldingWSAdj * 0.15
            totalLiveRating = totalWSAdj * 0.15
        elif numCareerMatches[batsmanId] < 20:
            battingLiveRating = expSmoothFactor * battingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * battingRating[batsmanId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * bowlingRating[batsmanId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * fieldingRating[batsmanId]
            totalLiveRating = expSmoothFactor * totalWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * totalRating[batsmanId]
        else:
            battingLiveRating = expSmoothFactor * battingWSAdj + (1 - expSmoothFactor) * battingRating[batsmanId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj + (1 - expSmoothFactor) * bowlingRating[batsmanId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj + (1 - expSmoothFactor) * fieldingRating[batsmanId]
            totalLiveRating = expSmoothFactor * totalWSAdj + (1 - expSmoothFactor) * totalRating[batsmanId]

        c.execute('insert or ignore into winSharesFT20Live(matchId, startDate, playerId, ft20Id, battingRating, bowlingRating, fieldingRating, totalRating) values ' '(?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, startDate, batsmanId, ft20Id, battingLiveRating, bowlingLiveRating, fieldingLiveRating, totalLiveRating))

    for bowler in bowlingWinShares2:
        if bowler == "": continue
        bowlingWS = 0
        bowlingWSAdj = 0
        fieldingWS = 0
        fieldingWSAdj = 0
        bowlerId = bowler2Id2[bowler]
        bowlingWS = bowlingWinShares2[bowler]
        bowlingWSAdj = bowlingWinSharesAdj2[bowler]
        if bowler not in battingWinShares1:
            if bowler in fieldingWinShares2:
                fieldingWS = fieldingWinShares2[bowler]
                fieldingWSAdj = fieldingWinSharesAdj2[bowler]
            totalWS = bowlingWS + fieldingWS
            totalWSAdj =  bowlingWSAdj + fieldingWSAdj
            matchId = repr(int(ft20Id)) + repr(bowlerId)
            print bowler + ": " + `bowlingWS` + ": " + `bowlingWSAdj`
            c.execute('insert or ignore into winSharesFT20Match (matchId, playerId, player, ft20Id, battingWS, bowlingWS, fieldingWS, totalWS, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, bowlerId, bowler, ft20Id, 0, bowlingWS, fieldingWS, totalWS, 0, bowlingWSAdj, fieldingWSAdj, totalWSAdj))

        c.execute('select matchId, battingRating, bowlingRating, fieldingRating, totalRating from winSharesFT20Live where playerId=? order by matchId desc', (bowlerId, ))
        liveRating = c.fetchone()
        if liveRating is None:
            battingRating[bowlerId] = 0
            bowlingRating[bowlerId] = 0
            fieldingRating[bowlerId] = 0
            totalRating[bowlerId] = 0
            numCareerMatches[bowlerId] = 0
        else:
            battingRating[bowlerId] = liveRating[1]
            bowlingRating[bowlerId] = liveRating[2]
            fieldingRating[bowlerId] = liveRating[3]
            totalRating[bowlerId] = liveRating[4]
            numCareerMatches[bowlerId] = len(c.fetchall())+1

        battingLiveRating = 0
        bowlingLiveRating = 0
        fieldingLiveRating = 0
        totalLiveRating = 0
        if numCareerMatches[bowlerId] == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            battingLiveRating = battingWSAdj * 0.15
            bowlingLiveRating = bowlingWSAdj * 0.15
            fieldingLiveRating = fieldingWSAdj * 0.15
            totalLiveRating = totalWSAdj * 0.15
        elif numCareerMatches[bowlerId] < 20:
            battingLiveRating = expSmoothFactor * battingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * battingRating[bowlerId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * bowlingRating[bowlerId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * fieldingRating[bowlerId]
            totalLiveRating = expSmoothFactor * totalWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * totalRating[bowlerId]
        else:
            battingLiveRating = expSmoothFactor * battingWSAdj + (1 - expSmoothFactor) * battingRating[bowlerId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj + (1 - expSmoothFactor) * bowlingRating[bowlerId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj + (1 - expSmoothFactor) * fieldingRating[bowlerId]
            totalLiveRating = expSmoothFactor * totalWSAdj + (1 - expSmoothFactor) * totalRating[bowlerId]

        c.execute('insert or ignore into winSharesFT20Live(matchId, startDate, playerId, ft20Id, battingRating, bowlingRating, fieldingRating, totalRating) values ' '(?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, startDate, bowlerId, ft20Id, battingLiveRating, bowlingLiveRating, fieldingLiveRating, totalLiveRating))


    for batsman in battingWinShares2:
        if batsman == "": continue
        battingWS = 0
        bowlingWS = 0
        fieldingWS = 0
        battingWSAdj = 0
        bowlingWSAdj = 0
        fieldingWSAdj = 0
        batsmanId = batsman2Id2[batsman]
        battingWS = battingWinShares2[batsman]
        battingWSAdj = battingWinSharesAdj2[batsman]
        if batsman in bowlingWinShares1:
            bowlingWS = bowlingWinShares1[batsman]
            bowlingWSAdj = bowlingWinSharesAdj1[batsman]
        if batsman in fieldingWinShares1:
            fieldingWS = fieldingWinShares1[batsman]
            fieldingWSAdj = fieldingWinSharesAdj1[batsman]
        totalWS = battingWS + bowlingWS + fieldingWS
        totalWSAdj = battingWSAdj + bowlingWSAdj + fieldingWSAdj
        matchId = repr(int(ft20Id)) + repr(batsmanId)
        print batsman + ": " + `totalWS` + ": " + `totalWSAdj`
        c.execute('insert or ignore into winSharesFT20Match (matchId, playerId, player, ft20Id, battingWS, bowlingWS, fieldingWS, totalWS, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, batsmanId, batsman, ft20Id, battingWS, bowlingWS, fieldingWS, totalWS, battingWSAdj, bowlingWSAdj, fieldingWSAdj, totalWSAdj))

        c.execute('select matchId, battingRating, bowlingRating, fieldingRating, totalRating from winSharesFT20Live where playerId=? order by matchId desc', (batsmanId, ))
        liveRating = c.fetchone()
        if liveRating is None:
            battingRating[batsmanId] = 0
            bowlingRating[batsmanId] = 0
            fieldingRating[batsmanId] = 0
            totalRating[batsmanId] = 0
            numCareerMatches[batsmanId] = 0
        else:
            battingRating[batsmanId] = liveRating[1]
            bowlingRating[batsmanId] = liveRating[2]
            fieldingRating[batsmanId] = liveRating[3]
            totalRating[batsmanId] = liveRating[4]
            numCareerMatches[batsmanId] = len(c.fetchall())+1

        battingLiveRating = 0
        bowlingLiveRating = 0
        fieldingLiveRating = 0
        totalLiveRating = 0
        if numCareerMatches[batsmanId] == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            battingLiveRating = battingWSAdj * 0.15
            bowlingLiveRating = bowlingWSAdj * 0.15
            fieldingLiveRating = fieldingWSAdj * 0.15
            totalLiveRating = totalWSAdj * 0.15
        elif numCareerMatches[batsmanId] < 20:
            battingLiveRating = expSmoothFactor * battingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * battingRating[batsmanId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * bowlingRating[batsmanId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * fieldingRating[batsmanId]
            totalLiveRating = expSmoothFactor * totalWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[batsmanId]-1)) + (1 - expSmoothFactor) * totalRating[batsmanId]
        else:
            battingLiveRating = expSmoothFactor * battingWSAdj + (1 - expSmoothFactor) * battingRating[batsmanId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj + (1 - expSmoothFactor) * bowlingRating[batsmanId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj + (1 - expSmoothFactor) * fieldingRating[batsmanId]
            totalLiveRating = expSmoothFactor * totalWSAdj + (1 - expSmoothFactor) * totalRating[batsmanId]

        c.execute('insert or ignore into winSharesFT20Live(matchId, startDate, playerId, ft20Id, battingRating, bowlingRating, fieldingRating, totalRating) values ' '(?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, startDate, batsmanId, ft20Id, battingLiveRating, bowlingLiveRating, fieldingLiveRating, totalLiveRating))

    for bowler in bowlingWinShares1:
        if bowler == "": continue
        bowlingWS = 0
        bowlingWSAdj = 0
        fieldingWS = 0
        fieldingWSAdj = 0
        bowlerId = bowler2Id1[bowler]
        bowlingWS = bowlingWinShares1[bowler]
        bowlingWSAdj = bowlingWinSharesAdj1[bowler]
        if bowler not in battingWinShares2:
            if bowler in fieldingWinShares1:
                fieldingWS = fieldingWinShares1[bowler]
                fieldingWSAdj = fieldingWinSharesAdj1[bowler]
            totalWS = bowlingWS + fieldingWS
            totalWSAdj =  bowlingWSAdj + fieldingWSAdj
            matchId = repr(int(ft20Id)) + repr(bowlerId)
            print bowler + ": " + `bowlingWS` + ": " + `bowlingWSAdj`
            c.execute('insert or ignore into winSharesFT20Match (matchId, playerId, player, ft20Id, battingWS, bowlingWS, fieldingWS, totalWS, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, bowlerId, bowler, ft20Id, 0, bowlingWS, fieldingWS, totalWS, 0, bowlingWSAdj, fieldingWSAdj, totalWSAdj))

        c.execute('select matchId, battingRating, bowlingRating, fieldingRating, totalRating from winSharesFT20Live where playerId=? order by matchId desc', (bowlerId, ))
        liveRating = c.fetchone()
        if liveRating is None:
            battingRating[bowlerId] = 0
            bowlingRating[bowlerId] = 0
            fieldingRating[bowlerId] = 0
            totalRating[bowlerId] = 0
            numCareerMatches[bowlerId] = 0
        else:
            battingRating[bowlerId] = liveRating[1]
            bowlingRating[bowlerId] = liveRating[2]
            fieldingRating[bowlerId] = liveRating[3]
            totalRating[bowlerId] = liveRating[4]
            numCareerMatches[bowlerId] = len(c.fetchall())+1

        battingLiveRating = 0
        bowlingLiveRating = 0
        fieldingLiveRating = 0
        totalLiveRating = 0
        if numCareerMatches[bowlerId] == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            battingLiveRating = battingWSAdj * 0.15
            bowlingLiveRating = bowlingWSAdj * 0.15
            fieldingLiveRating = fieldingWSAdj * 0.15
            totalLiveRating = totalWSAdj * 0.15
        elif numCareerMatches[bowlerId] < 20:
            battingLiveRating = expSmoothFactor * battingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * battingRating[bowlerId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * bowlingRating[bowlerId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * fieldingRating[bowlerId]
            totalLiveRating = expSmoothFactor * totalWSAdj * (0.235 + newPlayerPenaltyFactor*(numCareerMatches[bowlerId]-1)) + (1 - expSmoothFactor) * totalRating[bowlerId]
        else:
            battingLiveRating = expSmoothFactor * battingWSAdj + (1 - expSmoothFactor) * battingRating[bowlerId]
            bowlingLiveRating = expSmoothFactor * bowlingWSAdj + (1 - expSmoothFactor) * bowlingRating[bowlerId]
            fieldingLiveRating = expSmoothFactor * fieldingWSAdj + (1 - expSmoothFactor) * fieldingRating[bowlerId]
            totalLiveRating = expSmoothFactor * totalWSAdj + (1 - expSmoothFactor) * totalRating[bowlerId]

        c.execute('insert or ignore into winSharesFT20Live(matchId, startDate, playerId, ft20Id, battingRating, bowlingRating, fieldingRating, totalRating) values ' '(?, ?, ?, ?, ?, ?, ?, ?)',
                (matchId, startDate, bowlerId, ft20Id, battingLiveRating, bowlingLiveRating, fieldingLiveRating, totalLiveRating))
    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

#!/usr/bin/env python
import time
import sqlite3
import math
import sys
start = time.clock()

# startTest = int(input('Enter starting Test #: '))
startTest = int(sys.argv[1])

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

# constant fields
defaultBattingRating = [300.0, 300.0, 350.0, 350.0, 325.0, 275.0, 225.0, 150.0, 125.0, 100.0, 100.0]
pointOfEntryRatio = {1: 1.04, 2: 1.02, 3: 1, 4: 1, 5: 1.03, 6: 1.06, 7: 1.13, 8: 1.21, 9: 1.3}
wktPosVal = {1:1.2, 2:1.2, 3:1.4, 4:1.4, 5:1.3, 6:1.1, 7:0.9, 8:0.6, 9:0.5, 10:0.4}
defaultBowlingRating = 275.0
defaultAllRoundRating = 150.0
newPlayerPenaltyFactor = [0.51, 0.21485333, 0.12174525]
newPlayerPenaltyInns = [10, 15, 20]
expSmoothFactor = 0.05

# get tests info
c.execute('select * from testInfo')
testsInfo = c.fetchall()

def dumpInningsDetails(inningsNum, detailInnings, batInnings, bowlInnings, teamRating, batHighInnPct, batSecHighInnPct, margin, seriesStatus):
    # print('\nDumping details for innings #'+repr(inningsNum))
    # print('Bowling details:')

    # load test details
    wktOrder = {}
    teamBattingRating = 0.0
    wktsRating = {}
    battingLiveRating = {}
    battingLastInningsId = {}
    battingNumCareerInnings = {}
    teamBat = detailInnings[3]
    teamBowl = detailInnings[4]
    totalBalls = detailInnings[7]
    totalWkts = detailInnings[9]
    totalWktsMod = 1 if totalWkts == 0 else totalWkts
    numBatInns = 11 if totalWkts == 10 else totalWkts + 2

    for battingInn in batInnings:
        batsmanId = battingInn[1]
        position = battingInn[5]
        batRuns = battingInn[8]
        c.execute('select inningsId, rating from battingTestLive where playerId=? order by inningsId desc', (batsmanId, ))
        battingLiveRating[batsmanId] = c.fetchone()
        if battingLiveRating[batsmanId] is None:
            battingLiveRating[batsmanId] = defaultBattingRating[position-1]
            battingLastInningsId[batsmanId] = None
            battingNumCareerInnings[batsmanId] = 0
        else:
            battingLastInningsId[batsmanId] = battingLiveRating[batsmanId][0]
            battingLiveRating[batsmanId] = battingLiveRating[batsmanId][1]
            battingNumCareerInnings[batsmanId] = len(c.fetchall())+1
        teamBattingRating += battingLiveRating[batsmanId] / numBatInns

        dismissalInfo = battingInn[6]
        if 'b ' in dismissalInfo:
            bowlerIndex = dismissalInfo.index('b ')
            bowlerName = dismissalInfo[(bowlerIndex+2):]
            if bowlerName in wktsRating:
                wktsRating[bowlerName] = wktsRating[bowlerName] + max(0, battingLiveRating[batsmanId] - batRuns * 15.444)
            else:
                wktsRating[bowlerName] = max(0, battingLiveRating[batsmanId] - batRuns * 15.444)

    ###########################################################################################################################
    # store bowling live ratings data
    rating = {}
    teamBowlingRating = 0.0;
    # testBowlingFile = open("testBowlingInningsRatings.csv", "a")
    for bowlInn in bowlInnings:
        bowlerId = bowlInn[1]
        bowlerName = bowlInn[2]
        wkts = bowlInn[6]
        ballsBowled = bowlInn[9]
        runsConceded = bowlInn[11]
        homeAway = bowlInn[12]
        resultNum = bowlInn[14]

        bowlingLiveRating = {}
        c.execute('select inningsId, rating from bowlingTestLive where playerId=? order by inningsId desc', (bowlerId, ))
        bowlingLiveRating = c.fetchone()
        if bowlingLiveRating is None:
            bowlingLiveRating = defaultBowlingRating
            bowlingNumCareerInnings = 0
            bowlingLastInningsId = None
        else:
            bowlingLastInningsId = bowlingLiveRating[0]
            bowlingLiveRating = bowlingLiveRating[1]
            bowlingNumCareerInnings = len(c.fetchall())+1
        totalBalls = 1 if totalBalls == 0 else totalBalls
        teamBowlingRating += bowlingLiveRating * ballsBowled / totalBalls

        lastName = bowlerName.split()[len(bowlerName.split())-1]
        if lastName in wktsRating and wkts > 0:
            dismissalRating = wktsRating[lastName]
        elif bowlerName in wktsRating and wkts > 0: # more than one instance of the same last name
            dismissalRating = wktsRating[bowlerName]
        else: #no wickets
            dismissalRating = 0.0

        wktPct = float(wkts) * 100 / float(totalWktsMod)
        sigContrib = 12.5 if (math.pow(wkts, 2) / float(1 + runsConceded)) > 0.08 else (math.pow(wkts, 2) / float(1 + runsConceded)) * 156.25
        wktsPerRun = math.pow(wkts, 2) * 420 / float(30 + runsConceded)
        wktsPerBall = math.pow(wkts, 2) * 315 / float(60 + ballsBowled)
        ballsPerRun = math.pow(ballsBowled / 6, 2) * 1.3333 / float(30 + runsConceded)

        pitchQuality = sigContrib * (avg1stPitchRuns**2) / (200 * 323)
        if inningsNum == 3:
            pitchQuality = sigContrib * (252 * avg1stPitchRuns) / (200 * 323)
        elif inningsNum == 4:
            pitchQuality = sigContrib * (211 * avg1stPitchRuns) / (200 * 323)

        dismissalRatingMod = dismissalRating * 3.75 / float(30 + runsConceded) if wkts > 0 else 0
        battingRatingMod = teamBattingRating * sigContrib / 165
        resultRating = resultNum * (2 * sigContrib - 12.5) * teamRating[teamBat] / 500 if sigContrib > 6.25 else 0
        homeAwayMod = 2 * homeAway * sigContrib
        milestone = 5 if wkts >= 5 else 0
        # points for significant contribution in winning 4th innings defense and coming back from behind on 3rd innings
        status = 0
        if inningsNum == 3 and wktPct > 25:
            if battingTeam[2] == teamBowl and float(inningsRuns[2])/float(inningsRuns[1]) <= 0.7:
                runsBehind = inningsRuns[1] - inningsRuns[2]
                if resultNum == 1:
                    status = (2 * sigContrib - 12.5) * min(4, 1.5 * float(runsBehind)/252) * 3 if sigContrib > 6.25 else 0
                elif resultNum == 2:
                    status = (2 * sigContrib - 12.5) * min(4, 1.5 * float(runsBehind)/252) * 7.5 if sigContrib > 6.25 else 0
        if inningsNum == 4 and wktPct > 25:
            runsToDefend = inningsRuns[1] + inningsRuns[3] - inningsRuns[2] if testId != 1483 else inningsRuns[1]
            if resultNum == 1:
                status = (2 * sigContrib - 12.5) * min(3, 211 / runsToDefend) * 3 if sigContrib > 6.25 else 0
            elif resultNum == 2:
                status = (2 * sigContrib - 12.5) * min(3, 211 / runsToDefend) * 7.5 if sigContrib > 6.25 else 0

        closeMatchRating = 0.0
        if resultNum >= 1 and margin.find("inns &") == -1:
            runWktMargin = margin.split()[len(margin.split())-2]
            if margin.find(" runs") != -1:
                closeMatchRating = (2 * sigContrib - 12.5) * 62.5 / max(10.0, float(runWktMargin)) if sigContrib > 6.25 else 0
            elif margin.find(" wicket") != -1:
                closeMatchRating = (2 * sigContrib - 12.5) * 6.25 / float(runWktMargin) if sigContrib > 6.25 else 0

        # adjustment for series status (Deciding game or dead rubber?)
        seriesStatusAdj = 0
        if seriesStatus == "Dead":
            seriesStatusAdj = -4 * sigContrib
        elif seriesStatus == "Decider":
            seriesStatusAdj = 3 * (2 * sigContrib - 12.5) if sigContrib > 6.25 else 0

        # bowling innings rating
        rating = (wktsPerRun + wktsPerBall + ballsPerRun + pitchQuality + dismissalRatingMod + battingRatingMod + resultRating + homeAwayMod + milestone + status + closeMatchRating + seriesStatusAdj) * 5
        if rating < 0: rating = 0

        # for innings where <75 overs were bowled (with bowler bowling <15 overs and conceding < 50), avoid unnecessarily penalizing by assuming a performance in line with the bowler's live rating if rating of performance is lower
        rating = bowlingLiveRating if (totalBalls < 450 and ballsBowled < 90 and bowlingLiveRating > rating and runsConceded < 50) else rating

        allRoundName['' + repr(bowlerId)] = bowlerName
        if ('' + repr(bowlerId)) in allRoundWkts:
            allRoundWkts['' + repr(bowlerId)]['2'] = wkts
            allRoundBowlRuns['' + repr(bowlerId)]['2'] = runsConceded
        else:
            allRoundWkts['' + repr(bowlerId)] = {}
            allRoundBowlRuns['' + repr(bowlerId)] = {}
            allRoundWkts['' + repr(bowlerId)]['1'] = wkts
            allRoundBowlRuns['' + repr(bowlerId)]['1'] = runsConceded
        if ('' + repr(bowlerId)) in allRoundBowling:
            allRoundBowling['' + repr(bowlerId)]['2'] = rating
        else:
            allRoundBowling['' + repr(bowlerId)] = {}
            allRoundBowling['' + repr(bowlerId)]['1'] = rating

        inningsId = repr(int(testId)) + repr(inningsNum) + repr(bowlerId)
        # testBowlingFile.write(str(inningsId) + "," + str(wktsPerRun) + "," + str(wktsPerBall) + "," + str(ballsPerRun) + "," + str(pitchQuality) + "," + str(dismissalRatingMod) + "," + str(battingRatingMod) + "," + str(resultRating) + "," + str(homeAwayMod) + "," + str(milestone) + "," + str(status) + "," + str(closeMatchRating) + "," + str(seriesStatusAdj) + "\n")
        c.execute('update bowlingTestInnings set battingRating=?,wktsRating=?,status=?,rating=? where inningsId=?', (battingRatingMod, dismissalRatingMod, status, rating, inningsId))

        # update next innings rating to measure prediction error
        c.execute('update bowlingTestLive set nextInningsRating=? where inningsId=?', (rating, bowlingLastInningsId))

        liveRating = rating
        if bowlingNumCareerInnings == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif bowlingNumCareerInnings < newPlayerPenaltyInns[ppI]:
            liveRating = expSmoothFactor * rating * (0.2 + newPlayerPenaltyFactor[ppI]*(bowlingNumCareerInnings-1)) + (1 - expSmoothFactor) * bowlingLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * bowlingLiveRating

        if bowlerId not in playedInMatch: playedInMatch.append(bowlerId)
        c.execute('insert or replace into bowlingTestLive(inningsId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, bowlerId, testId, bowlerName, liveRating))
        # print(repr(inningsId)+",",repr(bowlerId)+", "+repr(inningsNum)+", "+bowlerName+", wkts: "+repr(wkts)+'/'+repr(runsConceded)+', current: '+repr(int(liveRating))+', innings: '+repr(int(rating))  )
    # testBowlingFile.close()

    partnershipRuns = {}
    entryRunsWkts = {}
    maxEntryWkts = 0
    for batInn in batInnings:
        entryRuns = batInn[15]
        entryWkts = batInn[16]
        entryRunsWkts[entryWkts] = entryRuns
        maxEntryWkts = entryWkts if entryWkts > maxEntryWkts else maxEntryWkts
    entryRunsWkts[maxEntryWkts+1] = inningsRuns[inningsNum]

    for i in range(1, len(entryRunsWkts)):
        partnershipRuns[i] = entryRunsWkts[i] - entryRunsWkts[i-1]

    # testBattingFile = open("testBattingInningsRatings.csv", "a")
    # print('\nBatting details:')
    ###########################################################################################################################
    # store batting live ratings data
    for batInn in batInnings:
        batsmanId = batInn[1]
        batsmanName = batInn[2]
        notOut = batInn[7]
        runs = batInn[8]
        balls = batInn[10]
        totalPct = batInn[13]
        entryRuns = batInn[15]
        entryWkts = batInn[16]
        wktsAtCrease = batInn[17]
        homeAway = batInn[18]
        resultNum = batInn[20]

        sigContrib = 12.5 if float(runs) > 62.5 else float(runs) / 5
        #runsMod = -0.0025 * float(runs)**2 + 2*float(runs) - 100 if runs > 200 else runs # reward runs linearly till 40, then diminishing returns for each extra run scored
        # diminishing returns for each extra run scored, with significant discounts past 200 runs
        if runs <= 40:
            runsMod = runs
        elif runs > 40 and runs <= 200:
            runsMod = -0.0011 * float(runs)**2 + 0.9961*float(runs) + 2.0026
        else:
            runsMod = -0.0021 * float(runs)**2 + 1.5822*float(runs) - 73.771
        runsMod = runsMod * 0.85
        totalPctRating = totalPct * (2 * sigContrib - 12.5) / 30 if sigContrib > 6.25 else 0
        pitchQuality = float(runs) * 80 * 323 / (avg1stPitchRuns**2) if runs < 200 else 5168000 / float(avg1stPitchRuns**2)
        if inningsNum == 3:
            pitchQuality = float(runs) * 80 * 323 / (252 * avg1stPitchRuns) if runs < 200 else 5168000 / float(252 * avg1stPitchRuns) # avg 3rd innings score = 252
        elif inningsNum == 4:
            pitchQuality = float(runs) * 80 * 323 / (211 * avg1stPitchRuns) if runs < 200 else 5168000 / float(211 * avg1stPitchRuns) # avg 4th innings score = 211

        if balls != None:
            strikeRate = float(runs) / float(balls) if balls > 0 else 0
        else: strikeRate = 0.425 # assume 42.5 strike rate for innings with no ball data
        strikeRateMod = float(strikeRate) * float(runsMod) / 7.5
        entryRunsMod = 1 if entryRuns == 0 else entryRuns
        pointOfEntry = 20 if entryWkts == 0 else entryRunsMod * pointOfEntryRatio[entryWkts]/entryWkts
        pointOfEntry = 10 if pointOfEntry < 10 else pointOfEntry

        maxPartnership = 0
        maxPartnershipMatchPct = 0.0
        for j in range(entryWkts+1, min(entryWkts + wktsAtCrease+2, len(partnershipRuns)+1)):
            maxPartnership = partnershipRuns[j] if partnershipRuns[j] > maxPartnership else maxPartnership
        maxPartnershipMatchPct = float(maxPartnership) / float(matchRuns) if matchRuns > 0 else 0
        partnership = maxPartnershipMatchPct * (2 * sigContrib - 12.5) * 12.5 if sigContrib > 6.25 else 0

        wktsAtCreaseEffVal = 0.0
        for wp in range(entryWkts + 1, entryWkts + wktsAtCrease + 1):
            wktsAtCreaseEffVal += float(wktPosVal[wp])
        pointOfEntry = (2 * sigContrib - 12.5) * math.sqrt(entryWkts + wktsAtCreaseEffVal) * 40 / pointOfEntry if sigContrib > 6.25 else 0
        resultRating = resultNum * (2 * sigContrib - 12.5) * teamRating[teamBowl] / 500 if sigContrib > 6.25 else 0
        bowlingRatingMod = teamBowlingRating * sigContrib / 75
        homeAwayMod = 2 * homeAway * sigContrib
        milestone = 0
        if float(runs) >= 100:
            milestone = 5
        if float(runs) >= 200:
            milestone = 10
        if float(runs) >= 300:
            milestone = 15

        # points for significant contribution in winning 4th innings chase and coming back from behind on 3rd innings
        status = 0
        runsBehind = 0
        if inningsNum == 3 and wktsAtCrease > 2 and totalPct > 25 and resultNum >= 1:
            if battingTeam[1] == teamBat and float(inningsRuns[1])/float(inningsRuns[2]) <= 0.7:
                runsBehind = inningsRuns[2] - inningsRuns[1]
            elif battingTeam[2] == teamBat and float(inningsRuns[2])/float(inningsRuns[1]) <= 0.7:
                runsBehind = inningsRuns[1] - inningsRuns[2]
            if runsBehind > 0:
                if resultNum == 1:
                    status = (2 * sigContrib - 12.5) * min(4, 1.5 * float(runsBehind)/252) * 3 if sigContrib > 6.25 else 0
                elif resultNum == 2:
                    status = (2 * sigContrib - 12.5) * min(4, 1.5 * float(runsBehind)/252) * 7.5 if sigContrib > 6.25 else 0
        if inningsNum == 4 and wktsAtCrease > 2 and totalPct > 25 and resultNum >= 1:
            runsToChase = inningsRuns[1] + inningsRuns[3] - inningsRuns[2] + 1 if testId != 1483 else inningsRuns[1] + 1
            if resultNum == 1:
                status = (2 * sigContrib - 12.5) * min(4, float(runsToChase) / 211) * 3 if sigContrib > 6.25 else 0
            elif resultNum == 2:
                status = (2 * sigContrib - 12.5) * min(4, float(runsToChase) / 211) * 7.5 if sigContrib > 6.25 else 0

        supportPct = 0.0
        if totalPct == batHighInnPct[inningsNum]:
            supportPct = batSecHighInnPct[inningsNum]
        else:
            supportPct = batHighInnPct[inningsNum]
        supportRating = max(0, (totalPct - supportPct) * 2.5) if inningsWkts[inningsNum] >= 8 else 0

        closeMatchRating = 0.0
        if resultNum >= 1 and margin.find("inns &") == -1:
            runWktMargin = margin.split()[len(margin.split())-2]
            if margin.find(" runs") != -1:
                closeMatchRating = (2 * sigContrib - 12.5) * 62.5 / max(10.0, float(runWktMargin)) if sigContrib > 6.25 else 0
            elif margin.find(" wicket") != -1:
                closeMatchRating = (2 * sigContrib - 12.5) * 6.25 / float(runWktMargin) if sigContrib > 6.25 else 0

        # adjustment for series status (Deciding game or dead rubber?)
        seriesStatusAdj = 0
        if seriesStatus == "Dead":
            seriesStatusAdj = -4 * sigContrib
        elif seriesStatus == "Decider":
            seriesStatusAdj = 3 * (2 * sigContrib - 12.5) if sigContrib > 6.25 else 0

        # batting innings rating
        rating = (runsMod + totalPctRating + pitchQuality + supportRating + strikeRateMod + bowlingRatingMod + partnership + pointOfEntry + resultRating + homeAwayMod + milestone + status + closeMatchRating + seriesStatusAdj) * 5.2
        if rating < 0: rating = 0

        allRoundName['' + repr(batsmanId)] = batsmanName
        if ('' + repr(batsmanId)) in allRoundRuns:
            allRoundRuns['' + repr(batsmanId)]['2'] = runs
            allRoundNotOut['' + repr(batsmanId)]['2'] = notOut
        else:
            allRoundRuns['' + repr(batsmanId)] = {}
            allRoundNotOut['' + repr(batsmanId)] = {}
            allRoundRuns['' + repr(batsmanId)]['1'] = runs
            allRoundNotOut['' + repr(batsmanId)]['1'] = notOut
        if ('' + repr(batsmanId)) in allRoundBatting:
            allRoundBatting['' + repr(batsmanId)]['2'] = rating
        else:
            allRoundBatting['' + repr(batsmanId)] = {}
            allRoundBatting['' + repr(batsmanId)]['1'] = rating

        # avoid penalizing not out innings unnecessarily, diminishing points for not outs thie higher the runs
        if notOut == 1:
            if battingLiveRating[batsmanId] > rating:
                rating = battingLiveRating[batsmanId]
            else: rating += 50 * math.exp(-float(runs)/150)

        inningsId = repr(int(testId)) + repr(inningsNum) + repr(batsmanId)
        # testBattingFile.write(str(inningsId) + "," + str(runsMod) + "," + str(totalPctRating) + "," + str(pitchQuality) + "," + str(supportRating) + "," + str(strikeRateMod) + "," + str(bowlingRatingMod) + "," + str(pointOfEntry) + "," + str(resultRating) + "," + str(homeAwayMod) + "," + str(milestone) + "," + str(status) + "," + str(closeMatchRating)+ "," + str(seriesStatusAdj) + "\n")
        c.execute('update battingTestInnings set bowlingRating=?,status=?,rating=? where inningsId=?', (bowlingRatingMod, status, rating, inningsId))

        # update next innings rating to measure prediction error
        c.execute('update battingTestLive set nextInningsRating=? where inningsId=?', (rating, battingLastInningsId[batsmanId]))

        liveRating = rating
        if battingNumCareerInnings[batsmanId] == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif battingNumCareerInnings[batsmanId] < newPlayerPenaltyInns[ppI]:
            liveRating = expSmoothFactor * rating * (0.2 + newPlayerPenaltyFactor[ppI]*(battingNumCareerInnings[batsmanId]-1)) + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * battingLiveRating[batsmanId]

        if batsmanId not in playedInMatch: playedInMatch.append(batsmanId)
        c.execute('insert or replace into battingTestLive(inningsId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, batsmanId, testId, batsmanName, liveRating))
        # print(repr(inningsId)+",",repr(batsmanId)+", "+repr(inningsNum)+", "+batsmanName+", runs: "+repr(int(runs))+', current: '+repr(int(liveRating))+', innings: '+repr(int(rating)))
    # testBattingFile.close()
    conn.commit()

# loop through test matches
for x in range(startTest, len(testsInfo)):
    # load test info
    testId = int(testsInfo[x][0])
    startDate = testsInfo[x][1]
    location = testsInfo[x][2]
    team1  = testsInfo[x][3]
    team2  = testsInfo[x][4]
    result = testsInfo[x][8]
    margin = testsInfo[x][9]
    seriesStatus = testsInfo[x][11]

    playedInMatch = []
    teamRating = {}
    c.execute('select rating from teamTestLive where team=? and startDate<? order by startDate desc', (team1, startDate))
    res = c.fetchone()
    teamRating[team1] = 400.0 if res is None else res[0]
    c.execute('select rating from teamTestLive where team=? and startDate<? order by startDate desc', (team2, startDate))
    res = c.fetchone()
    teamRating[team2] = 400.0 if res is None else res[0]

    # Different new player penalties based on era
    ppI = 2
    if testId <= 319:
        ppI = 1
    elif testId > 320 and testId <= 1133:
        ppI = 1

    print('\nDumping innings ratings for test #'+repr(int(testId)))
    inningsRuns = {}
    inningsWkts = {}
    battingTeam = {}
    bowlingTeam = {}
    batHighInnPct = {}
    batSecHighInnPct = {}
    pitchRuns = 0
    pitchInns = 0
    matchRuns = 0
    c.execute('select innings, batTeam, bowlTeam, runs, wickets, batHighInnPct, batSecHighInnPct from detailsTestInnings where testId=?', (testId, ))
    for inn in c.fetchall():
        innings = inn[0]
        batTeam = inn[1]
        bowlTeam = inn[2]
        runs = inn[3]
        wkts = inn[4]
        batHighInnPct[innings] = inn[5]
        batSecHighInnPct[innings] = inn[6]
        inningsRuns[innings] = runs
        inningsWkts[innings] = wkts
        battingTeam[innings] = batTeam
        bowlingTeam[innings] = bowlTeam
        matchRuns += runs
        if innings <= 2 and (wkts >= 7 or runs >= 400):
            pitchRuns += runs
            pitchInns += 1

    avg1stPitchRuns = pitchRuns / float(pitchInns) if pitchInns >= 1 else 323 # average first innings score
    avg1stPitchRuns = 150 if avg1stPitchRuns < 150 else avg1stPitchRuns # to handle edge cases
    allRoundName = {}
    allRoundRuns = {}
    allRoundNotOut = {}
    allRoundWkts = {}
    allRoundBowlRuns = {}
    allRoundBatting = {}
    allRoundBowling = {}
    c.execute('select innings from detailsTestInnings where testId=?', (testId, ))
    for inn in c.fetchall():
        innings = inn[0]
        c.execute('select * from detailsTestInnings where testId=? and innings=?', (testId, innings))
        detailInnings = c.fetchall()
        c.execute('select * from battingTestInnings where testId=? and innings=?', (testId, innings))
        batInnings = c.fetchall()
        c.execute('select * from bowlingTestInnings where testId=? and innings=?', (testId, innings))
        bowlInnings = c.fetchall()
        dumpInningsDetails(innings, detailInnings[0], batInnings, bowlInnings, teamRating, batHighInnPct, batSecHighInnPct, margin, seriesStatus)

    # print('\nAll-Round details:')
    for aRId in allRoundName.keys():
        allRoundLiveRating = {}
        c.execute('select matchId, rating from allRoundTestLive where playerId=? order by matchId desc', (aRId, ))
        allRoundLiveRating = c.fetchone()
        if allRoundLiveRating is None:
            allRoundLiveRating = defaultAllRoundRating
            allRoundNumCareerTests = 0
            allRoundLastMatchId = None
        else:
            allRoundLastMatchId = allRoundLiveRating[0]
            allRoundLiveRating = allRoundLiveRating[1]
            allRoundNumCareerTests = len(c.fetchall())+1

        matchRuns = 0
        if aRId in allRoundBatting:
            if '2' in allRoundBatting[aRId]:
                battingRating = float(allRoundBatting[aRId]['1'] + allRoundBatting[aRId]['2'])
                matchRuns += int(allRoundRuns[aRId]['1']) + int(allRoundRuns[aRId]['2'])
            else:
                battingRating = allRoundBatting[aRId]['1']
                matchRuns += int(allRoundRuns[aRId]['1'])
                allRoundBatting[aRId]['2'] = None
                allRoundRuns[aRId]['2'] = None
                allRoundNotOut[aRId]['2'] = None

        else:
            battingRating = None
            matchRuns = None
            allRoundBatting[aRId] = {}
            allRoundRuns[aRId] = {}
            allRoundNotOut[aRId] = {}
            allRoundBatting[aRId]['1'] = None
            allRoundRuns[aRId]['1'] = None
            allRoundNotOut[aRId]['1'] = None
            allRoundBatting[aRId]['2'] = None
            allRoundRuns[aRId]['2'] = None
            allRoundNotOut[aRId]['2'] = None

        matchWkts = 0
        if aRId in allRoundBowling:
            if '2' in allRoundBowling[aRId]:
                bowlingRating = float(allRoundBowling[aRId]['1'] + allRoundBowling[aRId]['2'])
                matchWkts += int(allRoundWkts[aRId]['1']) + int(allRoundWkts[aRId]['2'])
            else:
                bowlingRating = allRoundBowling[aRId]['1']
                matchWkts += int(allRoundWkts[aRId]['1'])
                allRoundBowling[aRId]['2'] = None
                allRoundWkts[aRId]['2'] = None
                allRoundBowlRuns[aRId]['2'] = None
        else:
            bowlingRating = None
            matchWkts = 0
            allRoundBowling[aRId] = {}
            allRoundWkts[aRId] = {}
            allRoundBowlRuns[aRId] = {}
            allRoundBowling[aRId]['1'] = None
            allRoundWkts[aRId]['1'] = None
            allRoundBowlRuns[aRId]['1'] = None
            allRoundBowling[aRId]['2'] = None
            allRoundWkts[aRId]['2'] = None
            allRoundBowlRuns[aRId]['2'] = None

        milestone = 75 if matchRuns >= 100 and matchWkts >= 5 else 0

        # avoid penalizing for not having a chance to bat or bowl
        if battingRating != None and bowlingRating != None:
            # square root of half of the product of batting and bowling ratings to get all-round rating, with bonus for 100 runs + 5 wkts in match
            rating = 2 * math.sqrt(battingRating * bowlingRating / 2) + milestone
        else:
            rating = allRoundLiveRating

        matchId = repr(int(testId)) + repr(int(aRId))
        c.execute('''insert or replace into allRoundTestMatch (matchId, playerId, player, testId, runs1, notOut1, runs2, notOut2, wkts1, bowlRuns1, wkts2, bowlRuns2, battingRating, bowlingRating, rating)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (matchId, aRId, allRoundName[aRId], testId, allRoundRuns[aRId]['1'], allRoundNotOut[aRId]['1'], allRoundRuns[aRId]['2'], allRoundNotOut[aRId]['2'],
                 allRoundWkts[aRId]['1'], allRoundBowlRuns[aRId]['1'], allRoundWkts[aRId]['2'], allRoundBowlRuns[aRId]['2'], battingRating, bowlingRating, rating))

        # update next test rating to measure prediction error
        c.execute('update allRoundTestLive set nextTestRating=? where matchId=?', (rating, allRoundLastMatchId))

        liveRating = rating
        if allRoundNumCareerTests == 0: # discount live ratings for a player's first 10 matches to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif allRoundNumCareerTests < newPlayerPenaltyInns[0]:
            liveRating = expSmoothFactor * rating * (0.2 + newPlayerPenaltyFactor[0]*(allRoundNumCareerTests-1)) + (1 - expSmoothFactor) * allRoundLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * allRoundLiveRating

        c.execute('insert or replace into allRoundTestLive(matchId, startDate, playerId, testId, player, rating, nextTestRating) values (?, ?, ?, ?, ?, ?, ?)',
                    (matchId, startDate, aRId, testId, allRoundName[aRId], liveRating, None))
        # print(repr(matchId)+",",repr(aRId)+", "+allRoundName[aRId] + ", batting: " + repr(matchRuns) + " bowling: " + repr(matchWkts)+", current: "+repr(int(liveRating))+', match: '+repr(int(rating)))

    # decay current rating of players who missed matches
    c.execute('select distinct playerId, player from allRoundTestLive where testId>? and testId<?', (testId-100, testId))
    for playerDetails in c.fetchall():
        playerId = playerDetails[0]
        playerName = playerDetails[1]
        c.execute('select country from playerInfo where playerId=?', (playerId, ))
        team = c.fetchone()
        if team[0] not in [team1, team2]: continue # team not part of this match

        c.execute('select retireTest from retiredPlayers where playerId=?', (playerId, ))
        retireTestId = c.fetchone()
        if retireTestId != None:
            if retireTestId[0] < testId: continue # retired before match
        if playerId in playedInMatch: continue # played in match

        inningsId = repr(int(testId)) + '5' + repr(playerId) # inningsNum = 5 since fake innings
        matchId = repr(int(testId)) + repr(int(playerId))
        c.execute('select rating from battingTestLive where playerId=? order by inningsId desc', (playerId, ))
        battingLiveRating = c.fetchone()
        if battingLiveRating != None:
            # print('Decaying ' + playerName + '\'s batting rating...')
            battingLiveRating = battingLiveRating[0]
            decayedRating = battingLiveRating * 0.99 # decay live rating by 1%
            c.execute('insert or replace into battingTestLive(inningsId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, playerId, testId, playerName, decayedRating))

        c.execute('select rating from bowlingTestLive where playerId=? order by inningsId desc', (playerId, ))
        bowlingLiveRating = c.fetchone()
        if bowlingLiveRating != None:
            # print('Decaying ' + playerName + '\'s bowling rating...')
            bowlingLiveRating = bowlingLiveRating[0]
            decayedRating = bowlingLiveRating * 0.99 # decay live rating by 1%
            c.execute('insert or replace into bowlingTestLive(inningsId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, playerId, testId, playerName, decayedRating))

        c.execute('select rating from allRoundTestLive where playerId=? order by matchId desc', (playerId, ))
        allRoundLiveRating = c.fetchone()
        if allRoundLiveRating != None:
            # print('Decaying ' + playerName + '\'s all-round rating...')
            allRoundLiveRating = allRoundLiveRating[0]
            decayedRating = allRoundLiveRating * 0.99 # decay live rating by 1%
            c.execute('insert or replace into allRoundTestLive(matchId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (matchId, startDate, playerId, testId, playerName, decayedRating))

    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')

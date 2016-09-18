#!/usr/bin/env python
import time
import sqlite3
import math
start = time.clock()

startTest = int(input('Enter starting Test #: '))

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

def dumpInningsDetails(inningsNum, detailInnings, batInnings, bowlInnings, teamRating, batHighInnPct, batSecHighInnPct, margin):
    print('\nDumping details for innings #'+repr(inningsNum))
    print('Bowling details:')

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
    numBatInns = totalWkts if totalWkts == 10 else totalWkts + 2
        
    for battingInn in batInnings:        
        batsmanId = battingInn[1]
        position = battingInn[5]
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
                wktsRating[bowlerName] += battingLiveRating[batsmanId]
            else:
                wktsRating[bowlerName] = battingLiveRating[batsmanId]
    
    ###########################################################################################################################
    # store bowling live ratings data
    rating = {}
    teamBowlingRating = 0.0;    
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
        wktsPerBall = math.pow(wkts, 2) * 210 / float(60 + ballsBowled)
        ballsPerRun = math.pow(ballsBowled / 6, 2) * 2 / float(30 + runsConceded)
        dismissalRatingMod = dismissalRating * 2.5 / float(30 + runsConceded) if wkts > 0 else 0
        battingRatingMod = teamBattingRating * sigContrib / 165
        resultRating = resultNum * sigContrib * teamRating[teamBat] / 125
        homeAwayMod = homeAway * sigContrib
        milestone = 10 if wkts >= 5 else 0
        # points for significant contribution in winning 4th innings defense and coming back from behind on 3rd innings
        status = 0
        if inningsNum == 3 and wktPct > 25:
            if battingTeam[1] == teamBowl and float(inningsRuns[1])/float(inningsRuns[2]) <= 0.7:
                if resultNum == 1:
                    status = sigContrib * 3
                elif resultNum == 2:
                    status = sigContrib * 4
            elif battingTeam[2] == teamBowl and float(inningsRuns[2])/float(inningsRuns[1]) <= 0.7:
                if resultNum == 1:
                    status = sigContrib * 3
                elif resultNum == 2:
                    status = sigContrib * 4
        if inningsNum == 4 and wktPct > 25:
            if resultNum == 1:
                status = sigContrib * 4.5
            elif resultNum == 2:
                status = sigContrib * 6

        closeMatchRating = 0.0        
        if resultNum >= 1 and margin.find("inns &") == -1:
            runWktMargin = margin.split()[len(margin.split())-2]
            if margin.find(" runs") != -1:
                closeMatchRating = sigContrib * 50 / max(10.0, float(runWktMargin))
            elif margin.find(" wicket") != -1:
                closeMatchRating = sigContrib * 5 / float(runWktMargin)

        # bowling innings rating
        rating = (wktsPerRun + wktsPerBall + ballsPerRun + dismissalRatingMod + battingRatingMod + resultRating + homeAwayMod + milestone + status + closeMatchRating) * 5.6
        
        # for innings where <75 overs were bowled (with bowler bowling <15 overs), avoid unnecessarily penalizing by assuming a performance in line with the bowler's live rating if rating of performance is lower
        rating = bowlingLiveRating if (totalBalls < 450 and ballsBowled < 90 and bowlingLiveRating > rating) else rating
        
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
        c.execute('update bowlingTestInnings set battingRating=?,wktsRating=?,status=?,rating=? where inningsId=?', (battingRatingMod, dismissalRatingMod, status, rating, inningsId))
        
        # update next innings rating to measure prediction error        
        c.execute('update bowlingTestLive set nextInningsRating=? where inningsId=?', (rating, bowlingLastInningsId))

        liveRating = rating
        if bowlingNumCareerInnings == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif bowlingNumCareerInnings < newPlayerPenaltyInns[ppI]:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor[ppI]*(bowlingNumCareerInnings-1)) + (1 - expSmoothFactor) * bowlingLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * bowlingLiveRating
        c.execute('insert or ignore into bowlingTestLive(inningsId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, bowlerId, testId, bowlerName, liveRating))
        print(repr(inningsId)+",",repr(bowlerId)+", "+repr(inningsNum)+", "+bowlerName+", wkts: "+repr(wkts)+'/'+repr(runsConceded)+', current: '+repr(int(liveRating))+', innings: '+repr(int(rating))  )
        
    print('\nBatting details:')
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
        
        sigContrib = 12.5 if float(runs) > 50 else float(runs) / 4
        #runsMod = -0.0025 * float(runs)**2 + 2*float(runs) - 100 if runs > 200 else runs # reward runs linearly till 250, then diminishing returns for each extra run scored
        # diminishing returns for each extra run scored, with significant discounts past 200 runs
        if runs <= 40:
            runsMod = runs
        elif runs > 40 and runs <= 200:
            runsMod = -0.0011 * float(runs)**2 + 0.9961*float(runs) + 2.0026
        else:
            runsMod = -0.0021 * float(runs)**2 + 1.5822*float(runs) - 73.771
        totalPctRating = totalPct * float(runs) / 100 if runs < 200 else totalPct * 1.5
        if balls != None:
            strikeRate = float(runs) / float(balls) if balls > 0 else 0
        else: strikeRate = 0.425 # assume 42.5 strike rate for innings with no ball data
        strikeRateMod = float(strikeRate) * float(runsMod) / 15
        entryRunsMod = 1 if entryRuns == 0 else entryRuns
        pointOfEntry = 20 if entryWkts == 0 else entryRunsMod * pointOfEntryRatio[entryWkts]/entryWkts
        pointOfEntry = 10 if pointOfEntry < 10 else pointOfEntry

        wktsAtCreaseEffVal = 0.0
        for wp in range(entryWkts + 1, entryWkts + wktsAtCrease + 1):
            wktsAtCreaseEffVal += float(wktPosVal[wp])
        pointOfEntry = sigContrib * math.sqrt(entryWkts + wktsAtCreaseEffVal) * 50 / pointOfEntry
        resultRating = resultNum * sigContrib * teamRating[teamBowl] / 125
        bowlingRatingMod = teamBowlingRating * sigContrib / 75
        homeAwayMod = homeAway * sigContrib
        milestone = 0
        if float(runs) >= 100:
            milestone = 5
        if float(runs) >= 200:
            milestone = 10
        if float(runs) >= 300:
            milestone = 15
        # points for significant contribution in winning 4th innings chase and coming back from behind on 3rd innings
        status = 0                        
        if inningsNum == 3 and wktsAtCrease > 2 and totalPct > 25:
            if battingTeam[1] == teamBat and float(inningsRuns[1])/float(inningsRuns[2]) <= 0.7:
                if resultNum == 1:
                    status = sigContrib * 3
                elif resultNum == 2:
                    status = sigContrib * 4
            elif battingTeam[2] == teamBat and float(inningsRuns[2])/float(inningsRuns[1]) <= 0.7:
                if resultNum == 1:
                    status = sigContrib * 3
                elif resultNum == 2:
                    status = sigContrib * 2.5
        if inningsNum == 4 and wktsAtCrease > 2 and totalPct > 25:
            if resultNum == 1:
                status = sigContrib * 4.5
            elif resultNum == 2:
                status = sigContrib * 6
        
        supportPct = 0.0
        if totalPct == batHighInnPct[inningsNum]:
            supportPct = batSecHighInnPct[inningsNum]
        else:
            supportPct = batHighInnPct[inningsNum]
        supportRating = max(0, (totalPct - supportPct) * 3)
        
        closeMatchRating = 0.0
        if resultNum >= 1 and margin.find("inns &") == -1:
            runWktMargin = margin.split()[len(margin.split())-2]
            if margin.find(" runs") != -1:                
                closeMatchRating = sigContrib * 50 / max(10.0, float(runWktMargin))
            elif margin.find(" wicket") != -1:
                closeMatchRating = sigContrib * 5 / float(runWktMargin)        
        
        # batting innings rating
        rating = (runsMod + totalPctRating + supportRating + strikeRateMod + bowlingRatingMod + pointOfEntry + resultRating + homeAwayMod + milestone + status + closeMatchRating) * 4.86
                 
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
        c.execute('update battingTestInnings set bowlingRating=?,status=?,rating=? where inningsId=?', (bowlingRatingMod, status, rating, inningsId))
    
        # update next innings rating to measure prediction error        
        c.execute('update battingTestLive set nextInningsRating=? where inningsId=?', (rating, battingLastInningsId[batsmanId]))
        
        liveRating = rating
        if battingNumCareerInnings[batsmanId] == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif battingNumCareerInnings[batsmanId] < newPlayerPenaltyInns[ppI]:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor[ppI]*(battingNumCareerInnings[batsmanId]-1)) + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        c.execute('insert or ignore into battingTestLive(inningsId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, batsmanId, testId, batsmanName, liveRating))
        print(repr(inningsId)+",",repr(batsmanId)+", "+repr(inningsNum)+", "+batsmanName+", runs: "+repr(int(runs))+', current: '+repr(int(liveRating))+', innings: '+repr(int(rating)))
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
    
    teamRating = {}
    c.execute('select rating from teamTestLive where team=? and startDate<? order by startDate desc', (team1, startDate))    
    res = c.fetchone()
    teamRating[team1] = 100.0 if res is None else res[0]        
    c.execute('select rating from teamTestLive where team=? and startDate<? order by startDate desc', (team2, startDate))
    res = c.fetchone()
    teamRating[team2] = 100.0 if res is None else res[0]        

    # Different new player penalties based on era
    ppI = 2
    if testId <= 319:
        ppI = 1
    elif testId > 320 and testId <= 1133:
        ppI = 1

    print('\nDumping innings ratings for test #'+repr(int(testId)))
    inningsRuns = {}
    battingTeam = {}
    bowlingTeam = {}
    batHighInnPct = {}
    batSecHighInnPct = {}
    c.execute('select innings, batTeam, bowlTeam, runs, batHighInnPct, batSecHighInnPct from detailsTestInnings where testId=?', (testId, ))
    for inn in c.fetchall():
        innings = inn[0]
        batTeam = inn[1]
        bowlTeam = inn[2]
        runs = inn[3]
        batHighInnPct[innings] = inn[4]
        batSecHighInnPct[innings] = inn[5]
        inningsRuns[innings] = runs
        battingTeam[innings] = batTeam
        bowlingTeam[innings] = bowlTeam

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
        dumpInningsDetails(innings, detailInnings[0], batInnings, bowlInnings, teamRating, batHighInnPct, batSecHighInnPct, margin)

    print('\nAll-Round details:')
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
            bowlingRating = 0
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

        milestone = 50 if matchRuns >= 100 and matchWkts >= 5 else 0

        # avoid penalizing for not having a chance to bat
        if battingRating != None:
            # square root of half of the product of batting and bowling ratings to get all-round rating, with bonus for 100 runs + 5 wkts in match
            rating = 2 * math.sqrt(battingRating * bowlingRating / 2) + milestone
        else:
            rating = allRoundLiveRating
        
        matchId = repr(int(testId)) + repr(int(aRId))
        c.execute('''insert or ignore into allRoundTestMatch (matchId, playerId, player, testId, runs1, notOut1, runs2, notOut2, wkts1, bowlRuns1, wkts2, bowlRuns2, battingRating, bowlingRating, rating)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (matchId, aRId, allRoundName[aRId], testId, allRoundRuns[aRId]['1'], allRoundNotOut[aRId]['1'], allRoundRuns[aRId]['2'], allRoundNotOut[aRId]['2'],
                 allRoundWkts[aRId]['1'], allRoundBowlRuns[aRId]['1'], allRoundWkts[aRId]['2'], allRoundBowlRuns[aRId]['2'], battingRating, bowlingRating, rating))

        # update next test rating to measure prediction error        
        c.execute('update allRoundTestLive set nextTestRating=? where matchId=?', (rating, allRoundLastMatchId))
        
        liveRating = rating
        if allRoundNumCareerTests == 0: # discount live ratings for a player's first 10 matches to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif allRoundNumCareerTests < newPlayerPenaltyInns[0]:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor[0]*(allRoundNumCareerTests-1)) + (1 - expSmoothFactor) * allRoundLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * allRoundLiveRating
                        
        c.execute('insert or ignore into allRoundTestLive(matchId, startDate, playerId, testId, player, rating, nextTestRating) values (?, ?, ?, ?, ?, ?, ?)',
                    (matchId, startDate, aRId, testId, allRoundName[aRId], liveRating, None))
        print(repr(matchId)+",",repr(aRId)+", "+allRoundName[aRId] + ", batting: " + repr(matchRuns) + " bowling: " + repr(matchWkts)+", current: "+repr(int(liveRating))+', match: '+repr(int(rating)))
    conn.commit()  
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')
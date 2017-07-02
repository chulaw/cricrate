#!/usr/bin/env python
import time
import sqlite3
import math
start = time.clock()

startFT20 = int(input('Enter starting FT20 #: '))

# connect to db
conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()

# constant fields
defaultBattingRating = [300.0, 300.0, 350.0, 350.0, 325.0, 275.0, 225.0, 150.0, 125.0, 100.0, 100.0]
defaultBowlingRating = 275.0
defaultAllRoundRating = 250.0
newPlayerPenaltyFactor = 0.085
expSmoothFactor = 0.1

# get ft20s info
c.execute('select * from ft20Info')
ft20sInfo = c.fetchall()

def dumpInningsDetails(inningsNum, detailInnings, batInnings, bowlInnings, teamRating):
    print '\nDumping details for innings #'+`inningsNum`
    print 'Bowling details:'

    # load ft20 details
    teamBattingRating = 0.0
    wktsRating = {}
    battingLiveRating = {}
    battingLastInningsId = {}
    battingNumCareerInnings = {}
    teamBat = detailInnings[3]
    teamBowl = detailInnings[4]
    totalRuns = detailInnings[6]
    totalBalls = detailInnings[7]
    totalWkts = detailInnings[9]
    totalWktsMod = 1 if totalWkts == 0 else totalWkts
    numBatInns = totalWkts if totalWkts == 10 else totalWkts + 2

    for battingInn in batInnings:
        batsmanId = battingInn[1]
        position = battingInn[5]
        c.execute('select inningsId, rating from battingFT20Live where playerId=? order by inningsId desc', (batsmanId, ))
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
        resultNum = bowlInn[13]

        bowlingLiveRating = {}
        c.execute('select inningsId, rating from bowlingFT20Live where playerId=? order by inningsId desc', (bowlerId, ))
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

        teamEcon = float(totalRuns) * 6 / float(totalBalls)
        if runsConceded > 0 and ballsBowled > 0:
            econRate = float(runsConceded) / (float(ballsBowled) / 6)
        elif runsConceded > 0 and ballsBowled == 0:
            econRate = float(runsConceded) * 6
        elif runsConceded == 0 and ballsBowled == 0:
            econRate = 6
        else:
            econRate = 6 / float(ballsBowled)

        sigContrib = 12.5 if (math.pow(wkts, 2) / float(1 + runsConceded) * teamEcon / econRate) > 0.04 else (math.pow(wkts, 2) / float(1 + runsConceded) * teamEcon / econRate) * 312.5
        wktsPerRun = math.pow(wkts, 2) * 100 / float(15 + runsConceded)
        economy = 7.5 * (float(teamEcon / econRate) + 50 / math.pow((econRate + 2), 2)) * math.pow(float(ballsBowled), 2) / float(totalBalls)
        dismissalRatingMod = dismissalRating * 2 / float(15 + runsConceded) if wkts > 0 else 0
        battingRatingMod = teamBattingRating * sigContrib / 75
        teamBat = "Rising Pune Supergiants" if teamBat == "Rising Pune Supergiant" else teamBat
        resultRating = resultNum * sigContrib * teamRating[teamBat] / 625
        milestone = 15 if wkts >= 3 else 0

        # points for significant contribution in winning significant matches (finals, world cup knock-out matches)
        status = 0
        if "final" in series.lower(): status = 6 * sigContrib

        # bowling innings rating
        rating = (wktsPerRun + economy + dismissalRatingMod + battingRatingMod + resultRating + milestone + status) * 5.25

        # for innings where <10 overs were bowled (with bowler bowling <2 overs), avoid unnecessarily penalizing by assuming a performance in line with the bowler's live rating if rating of performance is lower
        rating = bowlingLiveRating if (totalBalls < 60 and ballsBowled < 12 and bowlingLiveRating > rating) else rating

        allRoundName[bowlerId] = bowlerName
        allRoundWkts[bowlerId] = wkts
        allRoundBowlRuns[bowlerId] = runsConceded
        allRoundBowling[bowlerId] = rating

        inningsId = `int(ft20Id)` + `inningsNum` + `bowlerId`
        c.execute('update bowlingFT20Innings set battingRating=?,wktsRating=?,status=?,rating=? where inningsId=?', (battingRatingMod, dismissalRatingMod, status, rating, inningsId))

        # update next innings rating to measure prediction error
        c.execute('update bowlingFT20Live set nextInningsRating=? where inningsId=?', (rating, bowlingLastInningsId))

        liveRating = rating
        if bowlingNumCareerInnings == 0: # discount live ratings for a player's first 10 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif bowlingNumCareerInnings < 10:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(bowlingNumCareerInnings-1)) + (1 - expSmoothFactor) * bowlingLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * bowlingLiveRating
        c.execute('insert or ignore into bowlingFT20Live(inningsId, startDate, playerId, ft20Id, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, bowlerId, ft20Id, bowlerName, liveRating))
        print `inningsId`+",",`bowlerId`+", "+`inningsNum`+", "+bowlerName+", wkts: "+`wkts`+'/'+`runsConceded`+', econ: '+`int(econRate * 100 / teamEcon)`+', current: '+`int(liveRating)`+', innings: '+`int(rating)`

    print '\nBatting details:'
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
        resultNum = batInn[19]

        strikeRate = 100 * float(runs) / float(balls) if float(balls) > 0 else 0
        teamSR = 100 * float(totalRuns) / float(totalBalls) if float(totalBalls) > 0 else 100
        sigContrib = 12.5 if (float(runs) + 12.5 * strikeRate / teamSR) > 50 else (float(runs) + 12.5 * strikeRate / teamSR) / 4
        entryRunsMod = 1 if entryRuns == 0 else entryRuns
        pointOfEntry = 35 if entryWkts == 0 else entryRunsMod / entryWkts
        pointOfEntry = 10 if pointOfEntry < 10 else pointOfEntry
        pointOfEntry = sigContrib * math.sqrt(entryWkts) * 50 / pointOfEntry
        teamBowl = "Rising Pune Supergiants" if teamBowl == "Rising Pune Supergiant" else teamBowl
        resultRating = resultNum * sigContrib * teamRating[teamBowl] / 625
        bowlingRatingMod = teamBowlingRating * sigContrib / 60
        if float(runs) >= 50: milestone = 15

        # points for significant contribution in winning significant matches (finals, world cup knock-out matches)
        status = 0
        if ("final" in series.lower()) and totalPct > 25:
            status = 6 * sigContrib

        # avoid overrating short high SR innings by lowering the weight given to SR (harder to maintain SR over longer innings)
        if runs < 10:
            strikeRateMod = 2.5 * min(strikeRate, 100) / teamSR + min(strikeRate, 100) / 170
        elif runs >= 10 and runs < 25:
            strikeRateMod = 2.5 * min(strikeRate, 150) / teamSR + min(strikeRate, 200) / 170
        else:
            strikeRateMod = 2.5 * min(strikeRate, 200) / teamSR + min(strikeRate, 300) / 170

        # batting innings rating
        rating = (float(runs) * strikeRateMod + totalPct / 100 + bowlingRatingMod + pointOfEntry + resultRating + milestone + status) * 4

        allRoundName[batsmanId] = batsmanName
        allRoundRuns[batsmanId] = runs
        allRoundNotOut[batsmanId] = notOut
        allRoundBatting[batsmanId] = rating

        # avoid penalizing not out innings unnecessarily, diminishing points for not outs the higher the runs
        if notOut == 1:
            if battingLiveRating[batsmanId] > rating:
                rating = battingLiveRating[batsmanId]
            else: rating += 15 * math.exp(-float(runs)/50)

        inningsId = `int(ft20Id)` + `inningsNum` + `batsmanId`
        c.execute('update battingFT20Innings set bowlingRating=?,status=?,rating=? where inningsId=?', (bowlingRatingMod, status, rating, inningsId))

        # update next innings rating to measure prediction error
        c.execute('update battingFT20Live set nextInningsRating=? where inningsId=?', (rating, battingLastInningsId[batsmanId]))

        liveRating = rating
        if battingNumCareerInnings[batsmanId] == 0: # discount live ratings for a player's first 10 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif battingNumCareerInnings[batsmanId] < 10:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(battingNumCareerInnings[batsmanId]-1)) + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        c.execute('insert or ignore into battingFT20Live(inningsId, startDate, playerId, ft20Id, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, batsmanId, ft20Id, batsmanName, liveRating))
        print `inningsId`+",",`batsmanId`+", "+`inningsNum`+", "+batsmanName+", runs: "+`int(runs)`+", sr: "+`int(strikeRate)`+', current: '+`int(liveRating)`+', innings: '+`int(rating)`
    conn.commit()

# loop through ft20 matches
for x in range(startFT20, len(ft20sInfo)):
#for x in range(startFT20, startFT20+1):
    # load cricinfo scorecard html
    ft20Id = ft20sInfo[x][0]
    startDate = ft20sInfo[x][1]
    team1  = ft20sInfo[x][2]
    team2  = ft20sInfo[x][3]
    result = ft20sInfo[x][6]
    series = ft20sInfo[x][8]
    if series == None: series = ""

    teamRating = {}
    c.execute('select rating from teamFT20Live where team=? and startDate<? order by startDate desc', (team1, startDate))
    res = c.fetchone()
    teamRating[team1] = 500.0 if res is None else res[0]
    c.execute('select rating from teamFT20Live where team=? and startDate<? order by startDate desc', (team2, startDate))
    res = c.fetchone()
    teamRating[team2] = 500.0 if res is None else res[0]

    print '\nDumping innings ratings for ft20 #'+`int(ft20Id)`
    allRoundName = {}
    allRoundRuns = {}
    allRoundNotOut = {}
    allRoundWkts = {}
    allRoundBowlRuns = {}
    allRoundBatting = {}
    allRoundBowling = {}
    c.execute('select innings from detailsFT20Innings where ft20Id=?', (ft20Id, ))
    for inn in c.fetchall():
        innings = inn[0]
        c.execute('select * from detailsFT20Innings where ft20Id=? and innings=?', (ft20Id, innings))
        detailInnings = c.fetchall()
        c.execute('select * from battingFT20Innings where ft20Id=? and innings=?', (ft20Id, innings))
        batInnings = c.fetchall()
        c.execute('select * from bowlingFT20Innings where ft20Id=? and innings=?', (ft20Id, innings))
        bowlInnings = c.fetchall()
        dumpInningsDetails(innings, detailInnings[0], batInnings, bowlInnings, teamRating)

    print '\nAll-Round details:'
    for aRId in allRoundName.keys():
        allRoundLiveRating = {}
        c.execute('select matchId, rating from allRoundFT20Live where playerId=? order by matchId desc', (aRId, ))
        allRoundLiveRating = c.fetchone()
        if allRoundLiveRating is None:
            allRoundLiveRating = defaultAllRoundRating
            allRoundNumCareerFT20s = 0
            allRoundLastMatchId = None
        else:
            allRoundLastMatchId = allRoundLiveRating[0]
            allRoundLiveRating = allRoundLiveRating[1]
            allRoundNumCareerFT20s = len(c.fetchall())+1

        if aRId not in allRoundBatting:
            allRoundBatting[aRId] = None
            allRoundRuns[aRId] = None
            allRoundNotOut[aRId] = None

        if aRId not in allRoundBowling:
            allRoundBowling[aRId] = 0
            allRoundWkts[aRId] = None
            allRoundBowlRuns[aRId] = None

        milestone = 50 if allRoundRuns[aRId] >= 30 and allRoundWkts[aRId] >= 2 else 0

        # avoid penalizing for not having a chance to bat
        if allRoundBatting[aRId] != None:
            # square root of half of the product of batting and bowling ratings to get all-round rating, with bonus for 30 runs + 2 wkts in match
            rating = 2 * math.sqrt(float(allRoundBatting[aRId]) * float(allRoundBowling[aRId])) + milestone
        else:
            rating = allRoundLiveRating

        matchId = `int(ft20Id)` + `int(aRId)`
        c.execute('''insert or ignore into allRoundFT20Match (matchId, playerId, player, ft20Id, runs, notOut, wkts, bowlRuns, battingRating, bowlingRating, rating)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (matchId, aRId, allRoundName[aRId], ft20Id, allRoundRuns[aRId], allRoundNotOut[aRId], allRoundWkts[aRId], allRoundBowlRuns[aRId], allRoundBatting[aRId], allRoundBowling[aRId], rating))

        # update next ft20 rating to measure prediction error
        c.execute('update allRoundFT20Live set nextFT20Rating=? where matchId=?', (rating, allRoundLastMatchId))

        liveRating = rating
        if allRoundNumCareerFT20s == 0: # discount live ratings for a player's first 10 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif allRoundNumCareerFT20s < 10:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(allRoundNumCareerFT20s-1)) + (1 - expSmoothFactor) * allRoundLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * allRoundLiveRating

        c.execute('insert or ignore into allRoundFT20Live(matchId, startDate, playerId, ft20Id, player, rating, nextFT20Rating) values (?, ?, ?, ?, ?, ?, ?)',
                    (matchId, startDate, aRId, ft20Id, allRoundName[aRId], liveRating, None))
        if allRoundBatting[aRId] == None:
            print `matchId`+",",`aRId`+", "+allRoundName[aRId] + ", batting: " + `allRoundBatting[aRId]` + " bowling: " + `int(allRoundBowling[aRId])`+", current: "+`int(liveRating)`+', match: '+`int(rating)`
        else:
            print `matchId`+",",`aRId`+", "+allRoundName[aRId] + ", batting: " + `int(allRoundBatting[aRId])` + " bowling: " + `int(allRoundBowling[aRId])`+", current: "+`int(liveRating)`+', match: '+`int(rating)`
    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

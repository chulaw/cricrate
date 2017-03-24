#!/usr/bin/env python
import time
import sqlite3
import math
import sys
start = time.clock()

# startT20I = int(input('Enter starting T20I #: '))
startT20I = int(sys.argv[1])

# connect to db
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()

# constant fields
teamMod = {'U.A.E.':'United Arab Emirates', 'U.S.A.':'United States of America', 'P.N.G.':'Papua New Guinea'}
defaultBattingRating = [300.0, 300.0, 350.0, 350.0, 325.0, 275.0, 225.0, 150.0, 125.0, 100.0, 100.0]
defaultBowlingRating = 275.0
defaultAllRoundRating = 250.0
newPlayerPenaltyFactor = 0.085
expSmoothFactor = 0.1

# get t20is info
c.execute('select * from t20iInfo')
t20isInfo = c.fetchall()

def dumpInningsDetails(inningsNum, detailInnings, batInnings, bowlInnings, teamRating):
    print '\nDumping details for innings #'+`inningsNum`
    print 'Bowling details:'

    # load t20i details
    wktOrder = {}
    retiredNotOut = {}
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
        c.execute('select inningsId, rating from battingT20ILive where playerId=? order by inningsId desc', (batsmanId, ))
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
        c.execute('select inningsId, rating from bowlingT20ILive where playerId=? order by inningsId desc', (bowlerId, ))
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
        resultRating = resultNum * sigContrib * teamRating[teamBat] / 625
        homeAwayMod = homeAway * sigContrib
        milestone = 15 if wkts >= 3 else 0

        # points for significant contribution in winning significant matches (finals, world cup knock-out matches)
        status = 0
        if series != None:
            if "final" in series.lower():
                if "world" in series.lower():
                    status = 6 * sigContrib
                else:
                    status = 3 * sigContrib

        # bowling innings rating
        rating = (wktsPerRun + economy + dismissalRatingMod + battingRatingMod + resultRating + homeAwayMod + milestone + status) * 5.85

        # for innings where <10 overs were bowled (with bowler bowling <2 overs), avoid unnecessarily penalizing by assuming a performance in line with the bowler's live rating if rating of performance is lower
        rating = bowlingLiveRating if (totalBalls < 60 and ballsBowled < 12 and bowlingLiveRating > rating) else rating

        allRoundName[bowlerId] = bowlerName
        allRoundWkts[bowlerId] = wkts
        allRoundBowlRuns[bowlerId] = runsConceded
        allRoundBowling[bowlerId] = rating

        inningsId = `int(t20iId)` + `inningsNum` + `bowlerId`
        c.execute('update bowlingT20IInnings set battingRating=?,wktsRating=?,status=?,rating=? where inningsId=?', (battingRatingMod, dismissalRatingMod, status, rating, inningsId))

        # update next innings rating to measure prediction error
        c.execute('update bowlingT20ILive set nextInningsRating=? where inningsId=?', (rating, bowlingLastInningsId))

        liveRating = rating
        if bowlingNumCareerInnings == 0: # discount live ratings for a player's first 10 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif bowlingNumCareerInnings < 10:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(bowlingNumCareerInnings-1)) + (1 - expSmoothFactor) * bowlingLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * bowlingLiveRating
        c.execute('insert or ignore into bowlingT20ILive(inningsId, startDate, playerId, t20iId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, bowlerId, t20iId, bowlerName, liveRating))
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
        homeAway = batInn[18]
        resultNum = batInn[20]

        strikeRate = 100 * float(runs) / float(balls) if float(balls) > 0 else 0
        teamSR = 100 * float(totalRuns) / float(totalBalls) if float(totalBalls) > 0 else 100
        sigContrib = 12.5 if (float(runs) + 12.5 * strikeRate / teamSR) > 50 else (float(runs) + 12.5 * strikeRate / teamSR) / 4
        entryRunsMod = 1 if entryRuns == 0 else entryRuns
        pointOfEntry = 35 if entryWkts == 0 else entryRunsMod / entryWkts
        pointOfEntry = 10 if pointOfEntry < 10 else pointOfEntry
        pointOfEntry = sigContrib * math.sqrt(entryWkts) * 50 / pointOfEntry
        resultRating = resultNum * sigContrib * teamRating[teamBowl] / 625
        bowlingRatingMod = teamBowlingRating * sigContrib / 60
        homeAwayMod = homeAway * sigContrib
        if float(runs) >= 50: milestone = 15

        # points for significant contribution in winning significant matches (finals, world cup knock-out matches)
        status = 0
        if series != None:
            if ("final" in series.lower()) and totalPct > 25:
                if "world" in series.lower():
                    status = 6 * sigContrib
                else:
                    status = 3 * sigContrib

        # batting innings rating
        rating = (2.5 * float(runs) * min(strikeRate, 300) / teamSR + totalPct / 100 + bowlingRatingMod + pointOfEntry + resultRating + homeAwayMod + milestone + status) * 4.7

        allRoundName[batsmanId] = batsmanName
        allRoundRuns[batsmanId] = runs
        allRoundNotOut[batsmanId] = notOut
        allRoundBatting[batsmanId] = rating

        # avoid penalizing not out innings unnecessarily, diminishing points for not outs the higher the runs
        if notOut == 1:
            if battingLiveRating[batsmanId] > rating:
                rating = battingLiveRating[batsmanId]
            else: rating += 15 * math.exp(-float(runs)/50)

        inningsId = `int(t20iId)` + `inningsNum` + `batsmanId`
        c.execute('update battingT20IInnings set bowlingRating=?,status=?,rating=? where inningsId=?', (bowlingRatingMod, status, rating, inningsId))

        # update next innings rating to measure prediction error
        c.execute('update battingT20ILive set nextInningsRating=? where inningsId=?', (rating, battingLastInningsId[batsmanId]))

        liveRating = rating
        if battingNumCareerInnings[batsmanId] == 0: # discount live ratings for a player's first 10 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif battingNumCareerInnings[batsmanId] < 10:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(battingNumCareerInnings[batsmanId]-1)) + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        c.execute('insert or ignore into battingT20ILive(inningsId, startDate, playerId, t20iId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, batsmanId, t20iId, batsmanName, liveRating))
        print `inningsId`+",",`batsmanId`+", "+`inningsNum`+", "+batsmanName+", runs: "+`int(runs)`+", sr: "+`int(strikeRate)`+', current: '+`int(liveRating)`+', innings: '+`int(rating)`
    conn.commit()

# loop through t20i matches
for x in range(startT20I, len(t20isInfo)):
    # load cricinfo scorecard html
    t20iId = t20isInfo[x][0]
    startDate = t20isInfo[x][1]
    location = t20isInfo[x][2]
    team1  = t20isInfo[x][3]
    team2  = t20isInfo[x][4]
    result = t20isInfo[x][7]
    series = t20isInfo[x][9]

    teamRating = {}
    c.execute('select rating from teamT20ILive where team=? and startDate<? order by startDate desc', (team1, startDate))
    res = c.fetchone()
    teamRating[team1] = 500.0 if res is None else res[0]
    if team1 in teamMod:
        teamRating[teamMod[team1]] = teamRating[team1]
    c.execute('select rating from teamT20ILive where team=? and startDate<? order by startDate desc', (team2, startDate))
    res = c.fetchone()
    teamRating[team2] = 500.0 if res is None else res[0]
    if team2 in teamMod:
        teamRating[teamMod[team2]] = teamRating[team2]

    print '\nDumping innings ratings for t20i #'+`int(t20iId)`
    allRoundName = {}
    allRoundRuns = {}
    allRoundNotOut = {}
    allRoundWkts = {}
    allRoundBowlRuns = {}
    allRoundBatting = {}
    allRoundBowling = {}
    c.execute('select innings from detailsT20IInnings where t20iId=?', (t20iId, ))
    for inn in c.fetchall():
        innings = inn[0]
        c.execute('select * from detailsT20IInnings where t20iId=? and innings=?', (t20iId, innings))
        detailInnings = c.fetchall()
        c.execute('select * from battingT20IInnings where t20iId=? and innings=?', (t20iId, innings))
        batInnings = c.fetchall()
        c.execute('select * from bowlingT20IInnings where t20iId=? and innings=?', (t20iId, innings))
        bowlInnings = c.fetchall()
        dumpInningsDetails(innings, detailInnings[0], batInnings, bowlInnings, teamRating)

    print '\nAll-Round details:'
    for aRId in allRoundName.keys():
        allRoundLiveRating = {}
        c.execute('select matchId, rating from allRoundT20ILive where playerId=? order by matchId desc', (aRId, ))
        allRoundLiveRating = c.fetchone()
        if allRoundLiveRating is None:
            allRoundLiveRating = defaultAllRoundRating
            allRoundNumCareerT20Is = 0
            allRoundLastMatchId = None
        else:
            allRoundLastMatchId = allRoundLiveRating[0]
            allRoundLiveRating = allRoundLiveRating[1]
            allRoundNumCareerT20Is = len(c.fetchall())+1

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

        matchId = `int(t20iId)` + `int(aRId)`
        c.execute('''insert or ignore into allRoundT20IMatch (matchId, playerId, player, t20iId, runs, notOut, wkts, bowlRuns, battingRating, bowlingRating, rating)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (matchId, aRId, allRoundName[aRId], t20iId, allRoundRuns[aRId], allRoundNotOut[aRId], allRoundWkts[aRId], allRoundBowlRuns[aRId], allRoundBatting[aRId], allRoundBowling[aRId], rating))

        # update next t20i rating to measure prediction error
        c.execute('update allRoundT20ILive set nextT20IRating=? where matchId=?', (rating, allRoundLastMatchId))

        liveRating = rating
        if allRoundNumCareerT20Is == 0: # discount live ratings for a player's first 10 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif allRoundNumCareerT20Is < 10:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(allRoundNumCareerT20Is-1)) + (1 - expSmoothFactor) * allRoundLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * allRoundLiveRating

        c.execute('insert or ignore into allRoundT20ILive(matchId, startDate, playerId, t20iId, player, rating, nextT20IRating) values (?, ?, ?, ?, ?, ?, ?)',
                    (matchId, startDate, aRId, t20iId, allRoundName[aRId], liveRating, None))
        if allRoundBatting[aRId] == None:
            print `matchId` + ",", `aRId` + ", " + allRoundName[aRId] + ", batting: " + `allRoundBatting[aRId]` + " bowling: " + `int(allRoundBowling[aRId])` + ", current: " + `int(liveRating)` + ', match: ' + `int(rating)`
        else:
            print `matchId` + ",", `aRId` + ", " + allRoundName[aRId] + ", batting: " + `int(allRoundBatting[aRId])` + " bowling: " + `int(allRoundBowling[aRId])` + ", current: " + `int(liveRating)` + ', match: ' + `int(rating)`
    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'

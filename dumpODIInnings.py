#!/usr/bin/env python
import time
import sqlite3
import math
start = time.clock()

startODI = int(input('Enter starting ODI #: '))

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

# constant fields
defaultBattingRating = [300.0, 300.0, 350.0, 350.0, 325.0, 275.0, 225.0, 150.0, 125.0, 100.0, 100.0]
pointOfEntryRatio = {1: 1, 2: 1.01, 3: 1.02, 4: 1.06, 5: 1.13, 6: 1.23, 7: 1.36, 8: 1.51, 9: 1.67}
wktPosVal = {1:1.2, 2:1.2, 3:1.4, 4:1.4, 5:1.3, 6:1.1, 7:0.9, 8:0.6, 9:0.5, 10:0.4}
teamMod = {'U.A.E.':'United Arab Emirates', 'U.S.A.':'United States of America', 'P.N.G.':'Papua New Guinea'}
defaultBowlingRating = 275.0
defaultAllRoundRating = 150.0
newPlayerPenaltyFactor = 0.0425
expSmoothFactor = 0.05

# get odis info
c.execute('select * from odiInfo')
odisInfo = c.fetchall()

def dumpInningsDetails(inningsNum, detailInnings, batInnings, bowlInnings, teamRating):
    print('\nDumping details for innings #'+repr(inningsNum))
    print('Bowling details:')

    # load odi details
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
    numBatInns = totalWkts if totalWkts == 10 else totalWkts + 2
    
    for battingInn in batInnings:   
        batsmanId = battingInn[1]
        position = battingInn[5]
        c.execute('select inningsId, rating from battingODILive where playerId=? order by inningsId desc', (batsmanId, ))
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
        c.execute('select inningsId, rating from bowlingODILive where playerId=? order by inningsId desc', (bowlerId, ))
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
        
        sigContrib = 12.5 if (math.pow(wkts, 2) / float(1 + runsConceded) * teamEcon / econRate) > 0.08 else (math.pow(wkts, 2) / float(1 + runsConceded) * teamEcon / econRate) * 156.25
        wktsPerRun = math.pow(wkts, 2) * 225 / float(15 + runsConceded)
        economy = 2.1 * (float(teamEcon / econRate) * 1.1 + 45 / math.pow((econRate + 3), 2)) * math.pow(float(ballsBowled), 2) / float(totalBalls)
        wktsPerBall = math.pow(wkts, 2) * 125 / float(30 + ballsBowled)
        dismissalRatingMod = dismissalRating * 5 / float(15 + runsConceded) if wkts > 0 else 0
        battingRatingMod = teamBattingRating * sigContrib / 75
        resultRating = resultNum * sigContrib * teamRating[teamBat] / 125
        homeAwayMod = homeAway * sigContrib
        milestone = 15 if wkts >= 5 else 0
        
        # points for significant contribution in winning significant matches (finals, world cup knock-out matches)
        status = 0
        if "final" in series.lower():
            if "world cup" in series.lower():
                status = 8 * sigContrib
            else:
                status = 4 * sigContrib
        
        # bowling innings rating
        rating = (wktsPerRun + economy + wktsPerBall + dismissalRatingMod + battingRatingMod + resultRating + homeAwayMod + milestone + status) * 3.7

        # discount short bowling performances
        if ballsBowled < 30: rating = rating * (0.5 + ballsBowled / 60)
        # for innings where <25 overs were bowled (with bowler bowling <5 overs), avoid unnecessarily penalizing by assuming a performance in line with the bowler's live rating if rating of performance is lower
        rating = (ballsBowled * rating + (30 - ballsBowled) * bowlingLiveRating) / 30 if (totalBalls < 150 and ballsBowled < 30 and bowlingLiveRating > rating) else rating
        if int(startDate) > 19920101 and int(startDate) < 20050101:
            rating = rating / 0.96
        elif int(startDate) >= 20050101 and int(startDate) < 20121030:
            rating = rating / 0.94
        elif int(startDate) >= 20121030:
            rating = rating / 0.925

        allRoundName[bowlerId] = bowlerName        
        allRoundWkts[bowlerId] = wkts            
        allRoundBowlRuns[bowlerId] = runsConceded
        allRoundBowling[bowlerId] = rating
        
        inningsId = repr(int(odiId)) + repr(inningsNum) + repr(bowlerId)
        c.execute('update bowlingODIInnings set battingRating=?,wktsRating=?,status=?,rating=? where inningsId=?', (battingRatingMod, dismissalRatingMod, status, rating, inningsId))    
        
        # update next innings rating to measure prediction error        
        c.execute('update bowlingODILive set nextInningsRating=? where inningsId=?', (rating, bowlingLastInningsId))
        
        liveRating = rating
        if bowlingNumCareerInnings == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15            
        elif bowlingNumCareerInnings < 20:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(bowlingNumCareerInnings-1)) + (1 - expSmoothFactor) * bowlingLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * bowlingLiveRating
        c.execute('insert or ignore into bowlingODILive(inningsId, startDate, playerId, odiId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, bowlerId, odiId, bowlerName, liveRating))
        print(repr(inningsId)+",",repr(bowlerId)+", "+repr(inningsNum)+", "+bowlerName+", wkts: "+repr(wkts)+'/'+repr(runsConceded)+', econ: '+repr(int(econRate * 100 / teamEcon))+', current: '+repr(int(liveRating))+', innings: '+repr(int(rating)))
        
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

        strikeRate = 100 * float(runs) / float(balls) if float(balls) > 0 else 0
        teamSR = 100 * float(totalRuns) / float(totalBalls) if float(totalBalls) > 0 else 100
        sigContrib = 12.5 if (float(runs) + 12.5 * strikeRate / teamSR) > 50 else (float(runs) + 12.5 * strikeRate / teamSR) / 4
        entryRunsMod = 1 if entryRuns == 0 else entryRuns
        pointOfEntry = 22.5 if entryWkts == 0 else entryRunsMod * pointOfEntryRatio[entryWkts]/entryWkts
        pointOfEntry = 10 if pointOfEntry < 10 else pointOfEntry

        wktsAtCreaseEffVal = 0.0
        for wp in range(entryWkts+1, entryWkts+wktsAtCrease+1):
            wktsAtCreaseEffVal += float(wktPosVal[wp])
        pointOfEntry = sigContrib * math.sqrt(entryWkts + wktsAtCreaseEffVal) * 40 / pointOfEntry
        resultRating = resultNum * sigContrib * teamRating[teamBowl] / 125
        bowlingRatingMod = teamBowlingRating * sigContrib / 65
        homeAwayMod = homeAway * sigContrib
        if float(runs) >= 100: milestone = 15

        # points for significant contribution in winning significant matches (finals, world cup knock-out matches)
        status = 0
        if ("final" in series.lower()) and totalPct > 25:
            if "world cup" in series.lower():
                status = 8 * sigContrib
            else:
                status = 4 * sigContrib

        # avoid overrating short high SR innings by lowering the weight given to SR (harder to maintain SR over longer innings)
        if runs < 10:
            strikeRateMod = 2.75 * min(strikeRate, 100) / teamSR + min(strikeRate, 100) / 170
        elif runs >= 10 and runs < 25:
            strikeRateMod = 2.75 * min(strikeRate, 150) / teamSR + min(strikeRate, 200) / 170
        else:
            strikeRateMod = 2.75 * min(strikeRate, 200) / teamSR + min(strikeRate, 300) / 170

        # batting innings rating
        rating = (float(runs) * strikeRateMod + totalPct / 95 + bowlingRatingMod + pointOfEntry + resultRating + homeAwayMod + milestone + status) * 3.6
        if int(startDate) > 19920101 and int(startDate) < 20050101:
            rating = rating * 0.96
        elif int(startDate) >= 20050101 and int(startDate) < 20121030:
            rating = rating * 0.94
        elif int(startDate) >= 20121030:
            rating = rating * 0.925

        allRoundName[batsmanId] = batsmanName       
        allRoundRuns[batsmanId] = runs
        allRoundNotOut[batsmanId] = notOut                    
        allRoundBatting[batsmanId] = rating
                        
        # avoid penalizing not out innings unnecessarily, diminishing points for not outs the higher the runs
        if notOut == 1:
            if battingLiveRating[batsmanId] > rating:
                rating = battingLiveRating[batsmanId]
            else: rating += 30 * math.exp(-float(runs)/100)
        
        inningsId = repr(int(odiId)) + repr(inningsNum) + repr(batsmanId)
        c.execute('update battingODIInnings set bowlingRating=?,status=?,rating=? where inningsId=?', (bowlingRatingMod, status, rating, inningsId))
        
        # update next innings rating to measure prediction error        
        c.execute('update battingODILive set nextInningsRating=? where inningsId=?', (rating, battingLastInningsId[batsmanId]))
        
        liveRating = rating
        if battingNumCareerInnings[batsmanId] == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15            
        elif battingNumCareerInnings[batsmanId] < 20:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(battingNumCareerInnings[batsmanId]-1)) + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * battingLiveRating[batsmanId]
        c.execute('insert or ignore into battingODILive(inningsId, startDate, playerId, odiId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (inningsId, startDate, batsmanId, odiId, batsmanName, liveRating))
        print(repr(inningsId)+",",repr(batsmanId)+", "+repr(inningsNum)+", "+batsmanName+", runs: "+repr(int(runs))+", sr: "+repr(int(strikeRate))+', current: '+repr(int(liveRating))+', innings: '+repr(int(rating)))
    conn.commit()
    
# loop through odi matches
for x in range(startODI, len(odisInfo)):
#for x in range(startODI, (startODI+1)):
    # load odi info
    odiId = odisInfo[x][0]
    startDate = odisInfo[x][1]
    location = odisInfo[x][2]
    team1  = odisInfo[x][3]
    team2  = odisInfo[x][4]
    result = odisInfo[x][8]
    series = odisInfo[x][10]
    
    teamRating = {}
    c.execute('select rating from teamODILive where team=? and startDate<? order by startDate desc', (team1, startDate))    
    res = c.fetchone()
    teamRating[team1] = 100.0 if res is None else res[0]
    if team1 in teamMod:
        teamRating[teamMod[team1]] = teamRating[team1]
    c.execute('select rating from teamODILive where team=? and startDate<? order by startDate desc', (team2, startDate))
    res = c.fetchone()
    teamRating[team2] = 100.0 if res is None else res[0]
    if team2 in teamMod:
        teamRating[teamMod[team2]] = teamRating[team2]    
    
    print('\nDumping innings ratings for odi #'+repr(int(odiId)))
    allRoundName = {}
    allRoundRuns = {}
    allRoundNotOut = {}
    allRoundWkts = {}
    allRoundBowlRuns = {}
    allRoundBatting = {}
    allRoundBowling = {}
    c.execute('select innings from detailsODIInnings where odiId=?', (odiId, ))    
    for inn in c.fetchall():
        innings = inn[0]        
        c.execute('select * from detailsODIInnings where odiId=? and innings=?', (odiId, innings))        
        detailInnings = c.fetchall()        
        c.execute('select * from battingODIInnings where odiId=? and innings=?', (odiId, innings))        
        batInnings = c.fetchall()        
        c.execute('select * from bowlingODIInnings where odiId=? and innings=?', (odiId, innings))        
        bowlInnings = c.fetchall()        
        dumpInningsDetails(innings, detailInnings[0], batInnings, bowlInnings, teamRating)
        
    print('\nAll-Round details:')
    for aRId in allRoundName.keys():
        allRoundLiveRating = {}
        c.execute('select matchId, rating from allRoundODILive where playerId=? order by matchId desc', (aRId, ))
        allRoundLiveRating = c.fetchone()

        if allRoundLiveRating is None:
            allRoundLiveRating = defaultAllRoundRating
            allRoundNumCareerODIs = 0
            allRoundLastMatchId = None
        else:
            allRoundLastMatchId = allRoundLiveRating[0]
            allRoundLiveRating = allRoundLiveRating[1]
            allRoundNumCareerODIs = len(c.fetchall())+1
          
        if aRId not in allRoundBatting:
            allRoundBatting[aRId] = None
            allRoundRuns[aRId] = None
            allRoundNotOut[aRId] = None
            
        if aRId not in allRoundBowling:
            allRoundBowling[aRId] = 0
            allRoundWkts[aRId] = None
            allRoundBowlRuns[aRId] = None

        milestone = 50 if allRoundRuns[aRId] >= 50 and allRoundWkts[aRId] >= 3 else 0

        # avoid penalizing for not having a chance to bat
        if allRoundBatting[aRId] != None:
            # square root of half of the product of batting and bowling ratings to get all-round rating, with bonus for 50 runs + 3 wkts in match
            rating = 2 * math.sqrt(float(allRoundBatting[aRId]) * float(allRoundBowling[aRId])) + milestone
        else:
            rating = allRoundLiveRating

        matchId = repr(int(odiId)) + repr(int(aRId))
        c.execute('''insert or replace into allRoundODIMatch (matchId, playerId, player, odiId, runs, notOut, wkts, bowlRuns, battingRating, bowlingRating, rating)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (matchId, aRId, allRoundName[aRId], odiId, allRoundRuns[aRId], allRoundNotOut[aRId], allRoundWkts[aRId], allRoundBowlRuns[aRId], allRoundBatting[aRId], allRoundBowling[aRId], rating))

        # update next odi rating to measure prediction error        
        c.execute('update allRoundODILive set nextODIRating=? where matchId=?', (rating, allRoundLastMatchId))        
        
        liveRating = rating
        if allRoundNumCareerODIs == 0: # discount live ratings for a player's first 20 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif allRoundNumCareerODIs < 20:
            liveRating = expSmoothFactor * rating * (0.235 + newPlayerPenaltyFactor*(allRoundNumCareerODIs-1)) + (1 - expSmoothFactor) * allRoundLiveRating
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * allRoundLiveRating
                        
        c.execute('insert or ignore into allRoundODILive(matchId, startDate, playerId, odiId, player, rating, nextODIRating) values (?, ?, ?, ?, ?, ?, ?)',
                    (matchId, startDate, aRId, odiId, allRoundName[aRId], liveRating, None))
        if allRoundBatting[aRId] == None:
            print(repr(matchId)+",",repr(aRId)+", "+allRoundName[aRId] + ", batting: " + repr(allRoundBatting[aRId]) + " bowling: " + repr(int(allRoundBowling[aRId]))+", current: "+repr(int(liveRating))+', match: '+repr(int(rating)))
        else:
            print(repr(matchId)+",",repr(aRId)+", "+allRoundName[aRId] + ", batting: " + repr(int(allRoundBatting[aRId])) + " bowling: " + repr(int(allRoundBowling[aRId]))+", current: "+repr(int(liveRating))+', match: '+repr(int(rating)))
    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')
#!/usr/bin/env python
from datetime import date
import sqlite3
import math

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

c.execute('drop table fieldingTestCareer')
c.execute('drop table bowlerFieldingTestCareer')
c.execute('drop table batsmanFieldingTestCareer')
c.execute('''create table fieldingTestCareer (startDate date, endDate date, playerId integer unique, player text, tests integer, keeper integer, catches integer, droppedCatches integer, misfields integer,
            stumpings integer, missedStumpings integer, greatCatches integer, directHits integer, greatFieldings integer, runsSaved integer, matPerCatch real, matPerDrop real, dropRate real, matPerRunSaved real,
            matPerMisfield real, stumpRate real, matPerGreatCatch real, matPerDirectHit real, matPerGreatFielding real, rating real)''')
c.execute('''create table bowlerFieldingTestCareer (startDate date, endDate date, playerId integer unique, player text, innings integer, droppedCatches integer, missedStumpings integer,
            greatCatches integer, runsSaved integer, matPerDrop real, matPerRunSaved real, matPerMissedStumping real, matPerGreatCatch real)''')
c.execute('''create table batsmanFieldingTestCareer (startDate date, endDate date, playerId integer unique, player text, innings integer, droppedCatches integer, missedStumpings integer,
            greatCatches integer, directHits integer, runsLost integer, matPerDrop real, matPerRunLost real, matPerMissedStumping real, matPerGreatCatch real,
            matPerDirectHit real)''')

# Fielding Career
#c.execute('select playerId, player, country from playerInfo where player=?',('Faf du Plessis',))
c.execute('select playerId, player, country from playerInfo')
for player in c.fetchall():
    #print player[1]
    country = player[2]
    startDate = ""
    endDate = ""
    tests = 0
    c.execute('select startDate, endDate, tests from allRoundTestCareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        tests = playerInfo[2]

    c.execute('select testId, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatSaves, runsSaved, rating from fieldingTestMatch where playerId=?',(player[0], ))
    numMat = 0
    keeping = 0
    firstTest = 99999
    lastTest = 0
    catches = 0
    droppedCatches = 0
    misfields = 0
    stumpings = 0
    missedStumpings = 0
    greatCatches = 0
    directHits = 0
    greatFieldings = 0
    runsSaved = 0
    rating = 0
    for fieldingMatch in c.fetchall():
        if fieldingMatch[0] < firstTest: firstTest = fieldingMatch[0]
        if fieldingMatch[0] > lastTest: lastTest = fieldingMatch[0]
        numMat += 1
        keeping += fieldingMatch[1]
        catches += fieldingMatch[2]
        droppedCatches += fieldingMatch[3]
        misfields += fieldingMatch[4]
        stumpings += fieldingMatch[5]
        missedStumpings += fieldingMatch[6]
        greatCatches += fieldingMatch[7]
        directHits += fieldingMatch[8]
        greatFieldings += fieldingMatch[9]
        runsSaved += fieldingMatch[10]
        rating += fieldingMatch[11]
    dropRate = float(droppedCatches) / float(droppedCatches + catches) if (droppedCatches + catches) > 0 else None
    stumpRate = float(stumpings) / float(stumpings + missedStumpings) if (stumpings + missedStumpings) > 0 else None
    keepRate = float(keeping) / float(numMat) if numMat > 0 else None
    matPerCatch = float(tests) / float(catches) if catches > 0 else None
    matPerRunSaved = float(tests) / float(runsSaved) if runsSaved > 0 else None
    matPerDrop = float(tests) / float(droppedCatches) if droppedCatches > 0 else None
    matPerMisfield = float(tests) / float(misfields) if misfields > 0 else None
    matPerMissedStumping = float(tests) / float(missedStumpings) if missedStumpings > 0 else None
    matPerGreatCatch = float(tests) / float(greatCatches) if greatCatches > 0 else None
    matPerDirectHit = float(tests) / float(directHits) if directHits > 0 else None
    matPerGreatFielding = float(tests) / float(greatFieldings) if greatFieldings > 0 else None
    rating = rating * 17.5 / numMat if numMat > 0 else None
    # discount rating for those that have played <40 tests
    if numMat < 40 and numMat >= 20 and rating != None: rating = rating * math.exp(-float(40-numMat)/50)
    if numMat < 20 and numMat >= 10 and rating != None: rating = rating * math.exp(-float(40-numMat)/25)
    if numMat < 10 and rating != None: rating = rating * math.exp(-float(40-numMat)/10)
    if numMat < 5 and rating != None: rating = rating * math.exp(-float(40-numMat)/5)

    c.execute('select startDate from testInfo where testId=?',(firstTest, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from testInfo where testId=?',(lastTest, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    c.execute('select testTeamId, startDate from teamTestLive where team=? and startDate>=? and startDate<=?',(country, startDate, endDate))
    teamTests = 0
    noTestYears = 0
    if startDate != None: lastStart = int(startDate)
    for teamMatch in c.fetchall():
        if int(teamMatch[1]) > (lastStart + 10000): noTestYears = noTestYears + 1
        lastStart = int(teamMatch[1])
        teamTests += 1

    if startDate != None and endDate != None:
        startD = date(int(startDate[:4]), int(startDate[4:-2]), int(startDate[6:]))
        endD = date(int(endDate[:4]), int(endDate[4:-2]), int(endDate[6:]))
        careerDays = endD - startD
        longevity = (careerDays.days - noTestYears * 365 * 0.5) * (float(numMat)/float(teamTests)) / 15000 if teamTests > 0 else 0
    if rating != None and rating > 0: rating = (rating + rating * longevity)
    keeper = 1 if keepRate > 0.5 else 0
    # drop rate bonus:
    rating = rating + (1 - dropRate) * 200 if not dropRate == None else rating

    c.execute('''insert or ignore into fieldingTestCareer (startDate, endDate, playerId, player, tests, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatFieldings,
                runsSaved, matPerCatch, matPerDrop, dropRate, matPerRunSaved, matPerMisfield, stumpRate, matPerGreatCatch, matPerDirectHit, matPerGreatFielding, rating)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], numMat, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatFieldings, runsSaved, matPerCatch, matPerDrop,
               dropRate, matPerRunSaved, matPerMisfield, stumpRate, matPerGreatCatch, matPerDirectHit, matPerGreatFielding, rating))

# Bowler Fielding Career
c.execute('select playerId, player from playerInfo')
for player in c.fetchall():
    #print player[1]
    startDate = ""
    endDate = ""
    innings = 0
    c.execute('select startDate, endDate, innings from bowlingTestCareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        innings = playerInfo[2]

    c.execute('select droppedCatch, missedStumping, greatCatch, runsSaved from fieldingEventTest where bowlerId=?',(player[0], ))
    droppedCatches = 0
    missedStumpings = 0
    greatCatches = 0
    runsSaved = 0
    for fieldingEvent in c.fetchall():
        droppedCatches += fieldingEvent[0]
        missedStumpings += fieldingEvent[1]
        greatCatches += fieldingEvent[2]
        runsSaved += fieldingEvent[3]
    matPerDrop = float(innings) / float(droppedCatches) if droppedCatches > 0 else None
    matPerMissedStumping = float(innings) / float(missedStumpings) if missedStumpings > 0 else None
    matPerGreatCatch = float(innings) / float(greatCatches) if greatCatches > 0 else None
    matPerRunSaved = float(innings) / float(runsSaved) if runsSaved > 0 else None

    c.execute('''insert or ignore into bowlerFieldingTestCareer (startDate, endDate, playerId, player, innings, droppedCatches, missedStumpings, greatCatches, runsSaved, matPerDrop,
                matPerRunSaved, matPerMissedStumping, matPerGreatCatch) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, droppedCatches, missedStumpings, greatCatches, runsSaved, matPerDrop, matPerRunSaved, matPerMissedStumping, matPerGreatCatch))

# Batsman Fielding Career
c.execute('select playerId, player from playerInfo')
for player in c.fetchall():
    #print player[1]
    startDate = ""
    endDate = ""
    innings = 0
    c.execute('select startDate, endDate, innings from battingTestCareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        innings = playerInfo[2]

    c.execute('select droppedCatch, missedStumping, greatCatch, directHit, runsSaved from fieldingEventTest where batsmanId=?',(player[0], ))
    droppedCatches = 0
    missedStumpings = 0
    greatCatches = 0
    directHits = 0
    runsLost = 0
    for fieldingEvent in c.fetchall():
        droppedCatches += fieldingEvent[0]
        missedStumpings += fieldingEvent[1]
        greatCatches += fieldingEvent[2]
        directHits += fieldingEvent[3]
        runsLost += fieldingEvent[4]
    matPerDrop = float(innings) / float(droppedCatches) if droppedCatches > 0 else None
    matPerMissedStumping = float(innings) / float(missedStumpings) if missedStumpings > 0 else None
    matPerGreatCatch = float(innings) / float(greatCatches) if greatCatches > 0 else None
    matPerDirectHit = float(innings) / float(directHits) if directHits > 0 else None
    matPerRunsLost = float(innings) / float(runsLost) if runsLost > 0 else None

    c.execute('''insert or ignore into batsmanFieldingTestCareer (startDate, endDate, playerId, player, innings, droppedCatches, missedStumpings, greatCatches, directHits, runsLost, matPerDrop,
                matPerRunLost, matPerMissedStumping, matPerGreatCatch, matPerDirectHit) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, droppedCatches, missedStumpings, greatCatches, directHits, runsLost, matPerDrop, matPerRunsLost, matPerMissedStumping,
               matPerGreatCatch, matPerDirectHit))
conn.commit()
conn.close()
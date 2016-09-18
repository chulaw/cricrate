#!/usr/bin/env python
from datetime import date
import sqlite3
import math

# connect to db
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()

c.execute('drop table fieldingT20ICareer')
c.execute('drop table bowlerFieldingT20ICareer')
c.execute('drop table batsmanFieldingT20ICareer')
c.execute('''create table fieldingT20ICareer (startDate date, endDate date, playerId integer unique, player text, t20is integer, keeper integer, catches integer, droppedCatches integer, misfields integer,
            stumpings integer, missedStumpings integer, greatCatches integer, directHits integer, greatFieldings integer, runsSaved integer, matPerCatch real, matPerDrop real, dropRate real, matPerRunSaved real,
            matPerMisfield real, stumpRate real, matPerGreatCatch real, matPerDirectHit real, matPerGreatFielding real, rating real)''')
c.execute('''create table bowlerFieldingT20ICareer (startDate date, endDate date, playerId integer unique, player text, innings integer, droppedCatches integer, missedStumpings integer,
            greatCatches integer, runsSaved integer, matPerDrop real, matPerRunSaved real, matPerMissedStumping real, matPerGreatCatch real)''')
c.execute('''create table batsmanFieldingT20ICareer (startDate date, endDate date, playerId integer unique, player text, innings integer, droppedCatches integer, missedStumpings integer,
            greatCatches integer, directHits integer, runsLost integer, matPerDrop real, matPerRunLost real, matPerMissedStumping real, matPerGreatCatch real,
            matPerDirectHit real)''')

# Fielding Career
#c.execute('select playerId, player, country from playerInfo where player=?',('Kumar Sangakkara',))
c.execute('select playerId, player from playerInfo')
for player in c.fetchall():
    #print player[1]
    startDate = ""
    endDate = ""
    t20is = 0
    c.execute('select startDate, endDate, t20is from allRoundT20ICareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        t20is = playerInfo[2]

    c.execute('select t20iId, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatSaves, runsSaved, rating from fieldingT20IMatch where playerId=?',(player[0], ))
    numMat = 0
    keeping = 0
    firstT20I = 99999
    lastT20I = 0
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
        if fieldingMatch[0] < firstT20I: firstT20I = fieldingMatch[0]
        if fieldingMatch[0] > lastT20I: lastT20I = fieldingMatch[0]
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
    matPerCatch = float(t20is) / float(catches) if catches > 0 else None
    matPerRunSaved = float(t20is) / float(runsSaved) if runsSaved > 0 else None
    matPerDrop = float(t20is) / float(droppedCatches) if droppedCatches > 0 else None
    matPerMisfield = float(t20is) / float(misfields) if misfields > 0 else None
    matPerGreatCatch = float(t20is) / float(greatCatches) if greatCatches > 0 else None
    matPerDirectHit = float(t20is) / float(directHits) if directHits > 0 else None
    matPerGreatFielding = float(t20is) / float(greatFieldings) if greatFieldings > 0 else None
    rating = rating * 25 / numMat if numMat > 0 else None
    # discount rating for those that have played <100 t20is
    if numMat < 40 and numMat >= 20 and rating != None: rating = rating * math.exp(-float(40-numMat)/10)
    if numMat < 20 and numMat >= 10 and rating != None: rating = rating * math.exp(-float(20-numMat)/5)
    if numMat < 10 and rating != None: rating = rating * math.exp(-float(10-numMat)/2)
    if rating != None: rating = rating + rating * numMat / 400

    c.execute('select startDate from t20iInfo where t20iId=?',(firstT20I, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from t20iInfo where t20iId=?',(lastT20I, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    keeper = 1 if keepRate > 0.5 else 0
    # drop rate bonus:
    rating = rating + (1 - dropRate) * 200 if not dropRate == None else rating

    c.execute('''insert or ignore into fieldingT20ICareer (startDate, endDate, playerId, player, t20is, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatFieldings,
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
    c.execute('select startDate, endDate, innings from bowlingT20ICareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        innings = playerInfo[2]

    c.execute('select droppedCatch, missedStumping, greatCatch, runsSaved from fieldingEventT20I where bowlerId=?',(player[0], ))
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

    c.execute('''insert or ignore into bowlerFieldingT20ICareer (startDate, endDate, playerId, player, innings, droppedCatches, missedStumpings, greatCatches, runsSaved, matPerDrop,
                matPerRunSaved, matPerMissedStumping, matPerGreatCatch) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, droppedCatches, missedStumpings, greatCatches, runsSaved, matPerDrop, matPerRunSaved, matPerMissedStumping, matPerGreatCatch))

# Batsman Fielding Career
c.execute('select playerId, player from playerInfo')
for player in c.fetchall():
    #print player[1]
    startDate = ""
    endDate = ""
    innings = 0
    c.execute('select startDate, endDate, innings from battingT20ICareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        innings = playerInfo[2]

    c.execute('select droppedCatch, missedStumping, greatCatch, directHit, runsSaved from fieldingEventT20I where batsmanId=?',(player[0], ))
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

    c.execute('''insert or ignore into batsmanFieldingT20ICareer (startDate, endDate, playerId, player, innings, droppedCatches, missedStumpings, greatCatches, directHits, runsLost, matPerDrop,
                matPerRunLost, matPerMissedStumping, matPerGreatCatch, matPerDirectHit) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, droppedCatches, missedStumpings, greatCatches, directHits, runsLost, matPerDrop, matPerRunsLost, matPerMissedStumping,
               matPerGreatCatch, matPerDirectHit))
conn.commit()
conn.close()
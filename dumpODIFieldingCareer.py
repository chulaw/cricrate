#!/usr/bin/env python
from datetime import date
import sqlite3
import math

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

c.execute('drop table fieldingODICareer')
c.execute('drop table bowlerFieldingODICareer')
c.execute('drop table batsmanFieldingODICareer')
c.execute('''create table fieldingODICareer (startDate date, endDate date, playerId integer unique, player text, odis integer, keeper integer, catches integer, droppedCatches integer, misfields integer,
            stumpings integer, missedStumpings integer, greatCatches integer, directHits integer, greatFieldings integer, runsSaved integer, matPerCatch real, matPerDrop real, dropRate real, matPerRunSaved real,
            matPerMisfield real, stumpRate real, matPerGreatCatch real, matPerDirectHit real, matPerGreatFielding real, rating real)''')
c.execute('''create table bowlerFieldingODICareer (startDate date, endDate date, playerId integer unique, player text, innings integer, droppedCatches integer, missedStumpings integer,
            greatCatches integer, runsSaved integer, matPerDrop real, matPerRunSaved real, matPerMissedStumping real, matPerGreatCatch real)''')
c.execute('''create table batsmanFieldingODICareer (startDate date, endDate date, playerId integer unique, player text, innings integer, droppedCatches integer, missedStumpings integer,
            greatCatches integer, directHits integer, runsLost integer, matPerDrop real, matPerRunLost real, matPerMissedStumping real, matPerGreatCatch real,
            matPerDirectHit real)''')

# Fielding Career
#c.execute('select playerId, player, country from playerInfo where player=?',('Kumar Sangakkara',))
c.execute('select playerId, player, country from playerInfo')
for player in c.fetchall():
    country = player[2]
    if country == "United Arab Emirates": country = "U.A.E."
    if country == "United States of America": country = "U.S.A."
    if country == "Papua New Guinea": country = "P.N.G."
    if player[1] == "Dale Steyn": country = "South Africa"
    if player[1] == "Morne Morkel": country = "South Africa"
    #print player[1]
    startDate = ""
    endDate = ""
    odis = 0
    c.execute('select startDate, endDate, odis from allRoundODICareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        odis = playerInfo[2]

    c.execute('select odiId, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatSaves, runsSaved, rating from fieldingODIMatch where playerId=?',(player[0], ))
    numMat = 0
    keeping = 0
    firstODI = 99999
    lastODI = 0
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
        if fieldingMatch[0] < firstODI: firstODI = fieldingMatch[0]
        if fieldingMatch[0] > lastODI: lastODI = fieldingMatch[0]
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
    matPerCatch = float(odis) / float(catches) if catches > 0 else None
    matPerRunSaved = float(odis) / float(runsSaved) if runsSaved > 0 else None
    matPerDrop = float(odis) / float(droppedCatches) if droppedCatches > 0 else None
    matPerMisfield = float(odis) / float(misfields) if misfields > 0 else None
    matPerGreatCatch = float(odis) / float(greatCatches) if greatCatches > 0 else None
    matPerDirectHit = float(odis) / float(directHits) if directHits > 0 else None
    matPerGreatFielding = float(odis) / float(greatFieldings) if greatFieldings > 0 else None
    rating = rating * 25 / numMat if numMat > 0 else None
    # discount rating for those that have played <100 odis
    if numMat < 100 and numMat >= 50 and rating != None: rating = rating * math.exp(-float(100-numMat)/100)
    if numMat < 50 and numMat >= 25 and rating != None: rating = rating * math.exp(-float(100-numMat)/50)
    if numMat < 25 and rating != None: rating = rating * math.exp(-float(100-numMat)/25)
    if numMat < 10 and rating != None: rating = rating * math.exp(-float(100-numMat)/12.5)

    c.execute('select startDate from odiInfo where odiId=?',(firstODI, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from odiInfo where odiId=?',(lastODI, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    c.execute('select odiTeamId, startDate from teamODILive where team=? and startDate>=? and startDate<=?',(country, startDate, endDate))
    teamODIs = 0
    noODIYears = 0
    if startDate != None: lastStart = int(startDate)
    for teamMatch in c.fetchall():
        if int(teamMatch[1]) > (lastStart + 10000): noODIYears = noODIYears + 1
        lastStart = int(teamMatch[1])
        teamODIs += 1

    if startDate != None and endDate != None:
        startD = date(int(startDate[:4]), int(startDate[4:-2]), int(startDate[6:]))
        endD = date(int(endDate[:4]), int(endDate[4:-2]), int(endDate[6:]))
        careerDays = endD - startD
        longevity = (careerDays.days - noODIYears * 365 * 0.5) * (float(numMat)/float(teamODIs)) / 15000 if teamODIs > 0 else 0
    if rating != None and rating > 0: rating = (rating + rating * longevity)
    keeper = 1 if keepRate > 0.5 else 0
    # drop rate bonus:
    rating = rating + (1 - dropRate) * 200 if not dropRate == None else rating

    c.execute('''insert or ignore into fieldingODICareer (startDate, endDate, playerId, player, odis, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatFieldings,
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
    c.execute('select startDate, endDate, innings from bowlingODICareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        innings = playerInfo[2]

    c.execute('select droppedCatch, missedStumping, greatCatch, runsSaved from fieldingEventODI where bowlerId=?',(player[0], ))
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

    c.execute('''insert or ignore into bowlerFieldingODICareer (startDate, endDate, playerId, player, innings, droppedCatches, missedStumpings, greatCatches, runsSaved, matPerDrop,
                matPerRunSaved, matPerMissedStumping, matPerGreatCatch) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, droppedCatches, missedStumpings, greatCatches, runsSaved, matPerDrop, matPerRunSaved, matPerMissedStumping, matPerGreatCatch))

# Batsman Fielding Career
c.execute('select playerId, player from playerInfo')
for player in c.fetchall():
    #print player[1]
    startDate = ""
    endDate = ""
    innings = 0
    c.execute('select startDate, endDate, innings from battingODICareer where playerId=?',(player[0], ))
    for playerInfo in c.fetchall():
        startDate = playerInfo[0]
        endDate = playerInfo[1]
        innings = playerInfo[2]

    c.execute('select droppedCatch, missedStumping, greatCatch, directHit, runsSaved from fieldingEventODI where batsmanId=?',(player[0], ))
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

    c.execute('''insert or ignore into batsmanFieldingODICareer (startDate, endDate, playerId, player, innings, droppedCatches, missedStumpings, greatCatches, directHits, runsLost, matPerDrop,
                matPerRunLost, matPerMissedStumping, matPerGreatCatch, matPerDirectHit) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, droppedCatches, missedStumpings, greatCatches, directHits, runsLost, matPerDrop, matPerRunsLost, matPerMissedStumping,
               matPerGreatCatch, matPerDirectHit))
conn.commit()
conn.close()
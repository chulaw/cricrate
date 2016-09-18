#!/usr/bin/env python
from datetime import date
import sqlite3
import math

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

c.execute('drop table winSharesODICareer')
c.execute('''create table winSharesODICareer (startDate date, endDate date, playerId integer unique, player text, odis integer, battingWS real, bowlingWS real, fieldingWS real, totalWS real, battingWSAvg real, bowlingWSAvg real, fieldingWSAvg real,
            totalWSAvg real, battingAdjWS real, bowlingAdjWS real, fieldingAdjWS real, totalAdjWS real, battingAdjWSAvg real, bowlingAdjWSAvg real, fieldingAdjWSAvg real, totalAdjWSAvg real, battingRating real, bowlingRating real, fieldingRating real,
            totalRating real)''')

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

    c.execute('select odiId, battingWS, bowlingWS, fieldingWS, totalWS, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS from winSharesODIMatch where playerId=?',(player[0], ))
    numMat = 0
    keeping = 0
    firstODI = 99999
    lastODI = 0
    battingWS = 0.0
    bowlingWS = 0.0
    fieldingWS = 0.0
    totalWS = 0.0
    battingAdjWS = 0.0
    bowlingAdjWS = 0.0
    fieldingAdjWS = 0.0
    totalAdjWS = 0.0
    for wsMatch in c.fetchall():
        if wsMatch[0] < firstODI: firstODI = wsMatch[0]
        if wsMatch[0] > lastODI: lastODI = wsMatch[0]
        numMat += 1
        battingWS += wsMatch[1]
        bowlingWS += wsMatch[2]
        fieldingWS += wsMatch[3]
        totalWS += wsMatch[4]
        battingAdjWS += wsMatch[5]
        bowlingAdjWS += wsMatch[6]
        fieldingAdjWS += wsMatch[7]
        totalAdjWS += wsMatch[8]
    battingWSAvg = float(battingWS) / float(numMat) if numMat > 0 else None
    bowlingWSAvg = float(bowlingWS) / float(numMat) if numMat > 0 else None
    fieldingWSAvg = float(fieldingWS) / float(numMat) if numMat > 0 else None
    totalWSAvg = float(totalWS) / float(numMat) if numMat > 0 else None
    battingAdjWSAvg = float(battingAdjWS) / float(numMat) if numMat > 0 else None
    bowlingAdjWSAvg = float(bowlingAdjWS) / float(numMat) if numMat > 0 else None
    fieldingAdjWSAvg = float(fieldingAdjWS) / float(numMat) if numMat > 0 else None
    totalAdjWSAvg = float(totalAdjWS) / float(numMat) if numMat > 0 else None

    # discount rating for those that have played <100 odis
    battingRating = battingAdjWSAvg
    bowlingRating = bowlingAdjWSAvg
    fieldingRating = fieldingAdjWSAvg
    totalRating = totalAdjWSAvg
    if numMat < 100 and numMat >= 50 and totalRating != None:
        battingRating = battingRating * math.exp(-float(100-numMat)/100)
        bowlingRating = bowlingRating * math.exp(-float(100-numMat)/100)
        fieldingRating = fieldingRating * math.exp(-float(100-numMat)/100)
        totalRating = totalRating * math.exp(-float(100-numMat)/100)
    if numMat < 50 and numMat >= 25 and totalRating != None:
        battingRating = battingRating * math.exp(-float(100-numMat)/50)
        bowlingRating = bowlingRating * math.exp(-float(100-numMat)/50)
        fieldingRating = fieldingRating * math.exp(-float(100-numMat)/50)
        totalRating = totalRating * math.exp(-float(100-numMat)/50)
    if numMat < 25 and totalRating != None:
        battingRating = battingRating * math.exp(-float(100-numMat)/25)
        bowlingRating = bowlingRating * math.exp(-float(100-numMat)/25)
        fieldingRating = fieldingRating * math.exp(-float(100-numMat)/25)
        totalRating = totalRating * math.exp(-float(100-numMat)/25)
    if numMat < 10 and totalRating != None:
        battingRating = battingRating * math.exp(-float(100-numMat)/12.5)
        bowlingRating = bowlingRating * math.exp(-float(100-numMat)/12.5)
        fieldingRating = fieldingRating * math.exp(-float(100-numMat)/12.5)
        totalRating = totalRating * math.exp(-float(100-numMat)/12.5)

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
    if totalRating != None:
        battingRating = (battingRating + battingRating * longevity)
        bowlingRating = (bowlingRating + bowlingRating * longevity)
        fieldingRating = (fieldingRating + fieldingRating * longevity)
        totalRating = (totalRating + totalRating * longevity)

    c.execute('''insert or ignore into winSharesODICareer (startDate, endDate, playerId, player, odis, battingWS, bowlingWS, fieldingWS, totalWS, battingWSAvg, bowlingWSAvg, fieldingWSAvg, totalWSAvg, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS,
                battingAdjWSAvg, bowlingAdjWSAvg, fieldingAdjWSAvg, totalAdjWSAvg, battingRating, bowlingRating, fieldingRating, totalRating)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (startDate, endDate, player[0], player[1], numMat, battingWS, bowlingWS, fieldingWS, totalWS, battingWSAvg, bowlingWSAvg, fieldingWSAvg, totalWSAvg, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS, battingAdjWSAvg, bowlingAdjWSAvg,
                 fieldingAdjWSAvg, totalAdjWSAvg, battingRating, bowlingRating, fieldingRating, totalRating))
conn.commit()
conn.close()
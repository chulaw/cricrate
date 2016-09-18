#!/usr/bin/env python
from datetime import date
import sqlite3
import math

# connect to db
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()

c.execute('drop table winSharesT20ICareer')
c.execute('''create table winSharesT20ICareer (startDate date, endDate date, playerId integer unique, player text, t20is integer, battingWS real, bowlingWS real, fieldingWS real, totalWS real, battingWSAvg real, bowlingWSAvg real, fieldingWSAvg real,
            totalWSAvg real, battingAdjWS real, bowlingAdjWS real, fieldingAdjWS real, totalAdjWS real, battingAdjWSAvg real, bowlingAdjWSAvg real, fieldingAdjWSAvg real, totalAdjWSAvg real, battingRating real, bowlingRating real, fieldingRating real,
            totalRating real)''')

# Fielding Career
#c.execute('select playerId, player from playerInfo where player=?',('Kumar Sangakkara',))
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

    c.execute('select t20iId, battingWS, bowlingWS, fieldingWS, totalWS, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS from winSharesT20IMatch where playerId=?',(player[0], ))
    numMat = 0
    keeping = 0
    firstT20I = 99999
    lastT20I = 0
    battingWS = 0.0
    bowlingWS = 0.0
    fieldingWS = 0.0
    totalWS = 0.0
    battingAdjWS = 0.0
    bowlingAdjWS = 0.0
    fieldingAdjWS = 0.0
    totalAdjWS = 0.0
    for wsMatch in c.fetchall():
        if wsMatch[0] < firstT20I: firstT20I = wsMatch[0]
        if wsMatch[0] > lastT20I: lastT20I = wsMatch[0]
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

    # discount rating for those that have played <100 t20is
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

    if battingRating != None: battingRating = battingRating + battingRating * numMat / 400
    if bowlingRating != None: bowlingRating = bowlingRating + bowlingRating * numMat / 400
    if fieldingRating != None: fieldingRating = fieldingRating + fieldingRating * numMat / 400
    if totalRating != None: totalRating = totalRating + totalRating * numMat / 400

    c.execute('select startDate from t20iInfo where t20iId=?',(firstT20I, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from t20iInfo where t20iId=?',(lastT20I, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    c.execute('''insert or ignore into winSharesT20ICareer (startDate, endDate, playerId, player, t20is, battingWS, bowlingWS, fieldingWS, totalWS, battingWSAvg, bowlingWSAvg, fieldingWSAvg, totalWSAvg, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS,
                battingAdjWSAvg, bowlingAdjWSAvg, fieldingAdjWSAvg, totalAdjWSAvg, battingRating, bowlingRating, fieldingRating, totalRating)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (startDate, endDate, player[0], player[1], numMat, battingWS, bowlingWS, fieldingWS, totalWS, battingWSAvg, bowlingWSAvg, fieldingWSAvg, totalWSAvg, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS, battingAdjWSAvg, bowlingAdjWSAvg,
                 fieldingAdjWSAvg, totalAdjWSAvg, battingRating, bowlingRating, fieldingRating, totalRating))
conn.commit()
conn.close()
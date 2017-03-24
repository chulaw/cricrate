#!/usr/bin/env python
from datetime import date
import sqlite3
import math
import numpy as np
from scipy.stats import t

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

c.execute('drop table battingODICareer')
c.execute('drop table bowlingODICareer')
c.execute('drop table allRoundODICareer')
c.execute('''create table battingODICareer (startDate text, endDate text, playerId integer unique, player text, innings integer, notOuts integer, runs integer, average real, strikeRate real,
          fifties integer, hundreds integer, rating real, confInt95 real)''')
c.execute('''create table bowlingODICareer (startDate text, endDate text, playerId integer unique, player text, innings integer, balls integer, runs integer, wickets integer, average real,
          strikeRate real, econRate real, threeWkts integer, fiveWkts integer, rating real, confInt95 real)''')
c.execute('''create table allRoundODICareer (startDate text, endDate text, playerId integer unique, player text, odis integer, runs integer, battingAverage real, fifties integer, wickets integer,
          bowlingAverage real, threeWkts integer, fiftyThreeWkts integer, rating real, confInt95 real)''')

c.execute('select playerId, player, country from playerInfo')
for player in c.fetchall():
    country = player[2]
    if country == "United Arab Emirates": country = "U.A.E."
    if country == "United States of America": country = "U.S.A."
    if country == "Papua New Guinea": country = "P.N.G."
    if player[1] == "Dale Steyn": country = "South Africa"
    if player[1] == "Morne Morkel": country = "South Africa"

    # Batting career
    c.execute('select odiId, notOut, runs, balls, rating from battingODIInnings where playerId=?',(player[0], ))
    innings = 0
    notOuts = 0
    runs = 0
    balls = 0
    rating = 0.0
    mean = 0.0
    firstODI = 99999
    lastODI = 0
    fifties = 0
    hundreds = 0
    samples = []
    for battingInning in c.fetchall():
        if battingInning[0] < firstODI: firstODI = battingInning[0]
        if battingInning[0] > lastODI: lastODI = battingInning[0]
        innings += 1
        notOuts = notOuts + battingInning[1]
        runs = runs + battingInning[2]
        balls = balls + battingInning[3]
        if battingInning[2] >= 50 and battingInning[2] < 100: fifties += 1
        if battingInning[2] >= 100: hundreds += 1
        rating = rating + battingInning[4]
        samples.append(battingInning[4])

    if innings > 1:
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        tstat = (t.interval(0.95, innings-1))[1]
        ci95 = tstat * std / math.sqrt(innings)
    else:
        ci95 = None

    battingAverage = float(runs) / float(innings - notOuts) if innings != notOuts else None
    strikeRate = 100 * float(runs) / float(balls) if balls > 0 else 100 * float(runs)
    rating = rating / innings if innings > 0 else None
    # discount rating for those that have played <100 odis
    if innings < 100 and innings >= 50 and rating != None: rating = rating * math.exp(-float(100-innings)/150)
    if innings < 50 and innings >= 25 and rating != None: rating = rating * math.exp(-float(100-innings)/100)
    if innings < 25 and rating != None: rating = rating * math.exp(-float(100-innings)/50)
    if innings < 10 and rating != None: rating = rating * math.exp(-float(100-innings)/25)

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
        longevity = (careerDays.days - noODIYears * 365 * 0.5) * (float(innings)/float(teamODIs)) / 15500
    if rating != None: rating = (rating + rating * longevity) * 1.1
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('''insert or ignore into battingODICareer (startDate, endDate, playerId, player, innings, notOuts, runs, average, strikeRate, fifties, hundreds, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, notOuts, runs, battingAverage, strikeRate, fifties, hundreds, rating, ci95))

    # Bowling career
    c.execute('select odiId, wkts, balls, runs, rating from bowlingODIInnings where playerId=?',(player[0], ))
    innings = 0
    wkts = 0
    runs = 0
    balls = 0
    rating = 0.0
    mean = 0.0
    firstODI = 99999
    lastODI = 0
    threeWkts = 0
    fiveWkts = 0
    samples = []
    for bowlingInning in c.fetchall():
        if bowlingInning[0] < firstODI: firstODI = bowlingInning[0]
        if bowlingInning[0] > lastODI: lastODI = bowlingInning[0]
        innings += 1
        wkts = wkts + bowlingInning[1]
        balls = balls + bowlingInning[2]
        runs = runs + bowlingInning[3]
        if bowlingInning[1] >= 3 and bowlingInning[1] < 5: threeWkts += 1
        if bowlingInning[1] >= 5: fiveWkts += 1
        rating = rating + bowlingInning[4]
        samples.append(bowlingInning[4])

    if innings > 1:
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        tstat = (t.interval(0.95, innings-1))[1]
        ci95 = tstat * std / math.sqrt(innings)
    else:
        ci95 = None

    bowlingAverage = float(runs) / float(wkts) if wkts != 0 else None
    strikeRate = float(balls) / float(wkts) if wkts != 0 else None
    econRate = float(runs) * 6 / float(balls) if balls != 0 else None
    rating = rating / innings if innings > 0 else None
    # discount rating for those that have played <100 odis
    if innings < 100 and innings >= 50 and rating != None: rating = rating * math.exp(-float(100-innings)/150)
    if innings < 50 and innings >= 25 and rating != None: rating = rating * math.exp(-float(100-innings)/100)
    if innings < 25 and rating != None: rating = rating * math.exp(-float(100-innings)/50)
    if innings < 10 and rating != None: rating = rating * math.exp(-float(100-innings)/25)

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
        longevity = (careerDays.days - noODIYears * 365 * 0.5) * (float(innings)/float(teamODIs)) / 11000
    if rating != None: rating = (rating + rating * longevity) * 1.15
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('''insert or ignore into bowlingODICareer (startDate, endDate, playerId, player, innings, balls, runs, wickets, average, strikeRate, econRate, threeWkts, fiveWkts, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, balls, runs, wkts, bowlingAverage, strikeRate, econRate, threeWkts, fiveWkts, rating, ci95))

    # All-round career
    c.execute('select odiId, runs, wkts, rating from allRoundODIMatch where playerId=?',(player[0], ))
    wkts = 0
    runs = 0
    rating = 0.0
    mean = 0.0
    firstODI = 99999
    lastODI = 0
    fiftyThreeWkts = 0
    odis = 0
    samples = []
    for allRoundMatch in c.fetchall():
        if allRoundMatch[0] < firstODI: firstODI = allRoundMatch[0]
        if allRoundMatch[0] > lastODI: lastODI = allRoundMatch[0]
        odis += 1
        runsInns = 0 if allRoundMatch[1] == None else allRoundMatch[1]
        wktsInns = 0 if allRoundMatch[2] == None else allRoundMatch[2]
        runs = runs + runsInns
        wkts = wkts + wktsInns
        if runsInns >= 50 and wktsInns >= 3 : fiftyThreeWkts += 1
        rating = rating + allRoundMatch[3]
        samples.append(allRoundMatch[3])

    if odis > 1:
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        tstat = (t.interval(0.95, odis-1))[1]
        ci95 = tstat * std / math.sqrt(odis)
    else:
        ci95 = None

    rating = rating / odis if odis > 0 else None
    # discount rating for those that have played <100 odis
    if odis < 100 and odis >= 50 and rating != None: rating = rating * math.exp(-float(100-innings)/150)
    if odis < 50 and odis >= 25 and rating != None: rating = rating * math.exp(-float(100-innings)/100)
    if odis < 25 and rating != None: rating = rating * math.exp(-float(100-innings)/50)
    if odis < 10 and rating != None: rating = rating * math.exp(-float(100-innings)/25)

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
        longevity = (careerDays.days - noODIYears * 365 * 0.5) * (float(odis)/float(teamODIs)) / 12500
    if rating != None: rating = (rating + rating * longevity) * 1.05
    if rating != None and battingAverage != None and bowlingAverage != None:
        battingAverageMod = 60.0 if float(battingAverage) > 60.0 else float(battingAverage)
        bowlingAverageMod = 15.0 if float(bowlingAverage) < 15.0 else float(bowlingAverage)
        rating = rating + float(battingAverageMod) * 50 /float(bowlingAverageMod) # add battingAvg/bowlingAvg bonus
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('''insert or ignore into allRoundODICareer (startDate, endDate, playerId, player, odis, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, fiftyThreeWkts, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], odis, runs, battingAverage, fifties, wkts, bowlingAverage, threeWkts, fiftyThreeWkts, rating, ci95))
    conn.commit()
conn.close()

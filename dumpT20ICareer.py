#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
import math
import numpy as np
from scipy.stats import t

# connect to db
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()

c.execute('drop table battingT20ICareer')
c.execute('drop table bowlingT20ICareer')
c.execute('drop table allRoundT20ICareer')
c.execute('''create table battingT20ICareer (startDate text, endDate text, playerId integer unique, player text, innings integer, notOuts integer, runs integer, average real, strikeRate real,
          fifties integer, hundreds integer, rating real, confInt95 real)''')
c.execute('''create table bowlingT20ICareer (startDate text, endDate text, playerId integer unique, player text, innings integer, balls integer, runs integer, wickets integer, average real,
          strikeRate real, econRate real, threeWkts integer, fiveWkts integer, rating real, confInt95 real)''')
c.execute('''create table allRoundT20ICareer (startDate text, endDate text, playerId integer unique, player text, t20is integer, runs integer, battingAverage real, fifties integer, wickets integer,
          bowlingAverage real, threeWkts integer, thirtyTwoWkts integer, rating real, confInt95 real)''')

c.execute('select playerId, player from playerInfo')
for player in c.fetchall():
    # Batting career
    c.execute('select t20iId, notOut, runs, balls, rating from battingT20IInnings where playerId=?',(player[0], ))
    innings = 0
    notOuts = 0
    runs = 0
    balls = 0
    rating = 0.0
    mean = 0.0
    firstT20I = 99999
    lastT20I = 0
    fifties = 0
    hundreds = 0
    samples = []
    for battingInning in c.fetchall():
        if battingInning[0] < firstT20I: firstT20I = battingInning[0]
        if battingInning[0] > lastT20I: lastT20I = battingInning[0]
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
    # discount rating for those that have played <40 t20is
    if innings < 40 and innings >= 20 and rating != None: rating = rating * math.exp(-float(40-innings)/40)
    if innings < 20 and innings >= 10 and rating != None: rating = rating * math.exp(-float(20-innings)/5)
    if innings < 10 and rating != None: rating = rating * math.exp(-float(10-innings)/2)
    if rating != None: rating = (rating + rating * innings / 400) * 1.1
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('select startDate from t20iInfo where t20iId=?',(firstT20I, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from t20iInfo where t20iId=?',(lastT20I, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    c.execute('''insert or ignore into battingT20ICareer (startDate, endDate, playerId, player, innings, notOuts, runs, average, strikeRate, fifties, hundreds, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, notOuts, runs, battingAverage, strikeRate, fifties, hundreds, rating, ci95))

    # Bowling career
    c.execute('select t20iId, wkts, balls, runs, rating from bowlingT20IInnings where playerId=?',(player[0], ))
    innings = 0
    wkts = 0
    runs = 0
    balls = 0
    rating = 0.0
    mean = 0.0
    firstT20I = 99999
    lastT20I = 0
    threeWkts = 0
    fiveWkts = 0
    samples = []
    for bowlingInning in c.fetchall():
        if bowlingInning[0] < firstT20I: firstT20I = bowlingInning[0]
        if bowlingInning[0] > lastT20I: lastT20I = bowlingInning[0]
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
    # discount rating for those that have played <40 t20is
    if innings < 40 and innings >= 20 and rating != None: rating = rating * math.exp(-float(40-innings)/40)
    if innings < 20 and innings >= 10 and rating != None: rating = rating * math.exp(-float(20-innings)/5)
    if innings < 10 and rating != None: rating = rating * math.exp(-float(10-innings)/2)
    if rating != None: rating = (rating + rating * innings / 400) * 1.1
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('select startDate from t20iInfo where t20iId=?',(firstT20I, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from t20iInfo where t20iId=?',(lastT20I, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]
    c.execute('''insert or ignore into bowlingT20ICareer (startDate, endDate, playerId, player, innings, balls, runs, wickets, average, strikeRate, econRate, threeWkts, fiveWkts, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, balls, runs, wkts, bowlingAverage, strikeRate, econRate, threeWkts, fiveWkts, rating, ci95))

    # All-round career
    c.execute('select t20iId, runs, wkts, rating from allRoundT20IMatch where playerId=?',(player[0], ))
    wkts = 0
    runs = 0
    rating = 0.0
    mean = 0.0
    firstT20I = 99999
    lastT20I = 0
    thirtyTwoWkts = 0
    t20is = 0
    samples = []
    for allRoundMatch in c.fetchall():
        if allRoundMatch[0] < firstT20I: firstT20I = allRoundMatch[0]
        if allRoundMatch[0] > lastT20I: lastT20I = allRoundMatch[0]
        t20is += 1
        runsInns = 0 if allRoundMatch[1] == None else allRoundMatch[1]
        wktsInns = 0 if allRoundMatch[2] == None else allRoundMatch[2]
        runs = runs + runsInns
        wkts = wkts + wktsInns
        if runsInns >= 30 and wktsInns >= 2 : thirtyTwoWkts += 1
        rating = rating + allRoundMatch[3]
        samples.append(allRoundMatch[3])

    if t20is > 1:
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        tstat = (t.interval(0.95, t20is-1))[1]
        ci95 = tstat * std / math.sqrt(t20is)
    else:
        ci95 = None

    rating = rating / t20is if t20is > 0 else None
    # discount rating for those that have played <40 t20is
    if t20is < 40 and t20is >= 20 and rating != None: rating = rating * math.exp(-float(40-t20is)/40)
    if t20is < 20 and t20is >= 10 and rating != None: rating = rating * math.exp(-float(20-t20is)/5)
    if t20is < 10 and rating != None: rating = rating * math.exp(-float(10-t20is)/2)
    if rating != None: rating = (rating + rating * t20is / 400) * 0.9
    if rating != None and battingAverage != None and bowlingAverage != None:
        battingAverageMod = 50.0 if float(battingAverage) > 50.0 else float(battingAverage)
        bowlingAverageMod = 15.0 if float(bowlingAverage) < 15.0 else float(bowlingAverage)
        rating = rating + float(battingAverageMod) * 50 /float(bowlingAverageMod) # add battingAvg/bowlingAvg bonus
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean
    c.execute('select startDate from t20iInfo where t20iId=?',(firstT20I, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from t20iInfo where t20iId=?',(lastT20I, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    c.execute('''insert or ignore into allRoundT20ICareer (startDate, endDate, playerId, player, t20is, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, thirtyTwoWkts, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], t20is, runs, battingAverage, fifties, wkts, bowlingAverage, threeWkts, thirtyTwoWkts, rating, ci95))
    conn.commit()
conn.close()

#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
import math

# connect to db
conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()

c.execute('drop table battingFT20Career')
c.execute('drop table bowlingFT20Career')
c.execute('drop table allRoundFT20Career')
c.execute('''create table battingFT20Career (startDate text, endDate text, playerId integer unique, player text, innings integer, notOuts integer, runs integer, average real, strikeRate real,
          fifties integer, hundreds integer, rating real)''')
c.execute('''create table bowlingFT20Career (startDate text, endDate text, playerId integer unique, player text, innings integer, balls integer, runs integer, wickets integer, average real,
          strikeRate real, econRate real, threeWkts integer, fiveWkts integer, rating real)''')
c.execute('''create table allRoundFT20Career (startDate text, endDate text, playerId integer unique, player text, ft20s integer, runs integer, battingAverage real, fifties integer, wickets integer,
          bowlingAverage real, threeWkts integer, thirtyTwoWkts integer, rating real)''')

c.execute('select playerId, player from playerInfo')
for player in c.fetchall():
    # Batting career
    c.execute('select ft20Id, notOut, runs, balls, rating from battingFT20Innings where playerId=?',(player[0], ))
    innings = 0
    notOuts = 0
    runs = 0
    balls = 0
    rating = 0.0
    firstFT20 = 99999
    lastFT20 = 0
    fifties = 0
    hundreds = 0
    for battingInning in c.fetchall():
        if battingInning[0] < firstFT20: firstFT20 = battingInning[0]
        if battingInning[0] > lastFT20: lastFT20 = battingInning[0]
        innings += 1
        notOuts = notOuts + battingInning[1]
        runs = runs + battingInning[2]
        balls = balls + battingInning[3]
        if battingInning[2] >= 50 and battingInning[2] < 100: fifties += 1
        if battingInning[2] >= 100: hundreds += 1
        rating = rating + battingInning[4]
    battingAverage = float(runs) / float(innings - notOuts) if innings != notOuts else None
    strikeRate = 100 * float(runs) / float(balls) if balls > 0 else 100 * float(runs)
    rating = rating / innings if innings > 0 else None
    # discount rating for those that have played <20 ft20s
    if innings < 40 and innings >= 20 and rating != None: rating = rating * math.exp(-float(40-innings)/25)
    if innings < 20 and innings >= 10 and rating != None: rating = rating * math.exp(-float(20-innings)/10)
    if innings < 10 and rating != None: rating = rating * math.exp(-float(10-innings)/5)
    if rating != None: rating = rating + rating * innings / 400
    
    c.execute('select startDate from ft20Info where ft20Id=?',(firstFT20, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from ft20Info where ft20Id=?',(lastFT20, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]
    
    c.execute('''insert or ignore into battingFT20Career (startDate, endDate, playerId, player, innings, notOuts, runs, average, strikeRate, fifties, hundreds, rating)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, notOuts, runs, battingAverage, strikeRate, fifties, hundreds, rating))  
               
    # Bowling career
    c.execute('select ft20Id, wkts, balls, runs, rating from bowlingFT20Innings where playerId=?',(player[0], ))
    innings = 0
    wkts = 0
    runs = 0
    balls = 0
    rating = 0.0
    firstFT20 = 99999
    lastFT20 = 0
    threeWkts = 0
    fiveWkts = 0
    for bowlingInning in c.fetchall():
        if bowlingInning[0] < firstFT20: firstFT20 = bowlingInning[0]
        if bowlingInning[0] > lastFT20: lastFT20 = bowlingInning[0]                
        innings += 1        
        wkts = wkts + bowlingInning[1]
        balls = balls + bowlingInning[2]
        runs = runs + bowlingInning[3]
        if bowlingInning[1] >= 3 and bowlingInning[1] < 5: threeWkts += 1
        if bowlingInning[1] >= 5: fiveWkts += 1
        rating = rating + bowlingInning[4]        
    bowlingAverage = float(runs) / float(wkts) if wkts != 0 else None
    strikeRate = float(balls) / float(wkts) if wkts != 0 else None
    econRate = float(runs) * 6 / float(balls) if balls != 0 else None
    rating = rating / innings if innings > 0 else None
    # discount rating for those that have played <20 ft20s
    if innings < 40 and innings >= 20 and rating != None: rating = rating * math.exp(-float(40-innings)/25)
    if innings < 20 and innings >= 10 and rating != None: rating = rating * math.exp(-float(20-innings)/10)
    if innings < 10 and rating != None: rating = rating * math.exp(-float(10-innings)/5)
    if rating != None: rating = rating + rating * innings / 400
    
    c.execute('select startDate from ft20Info where ft20Id=?',(firstFT20, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from ft20Info where ft20Id=?',(lastFT20, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]
    c.execute('''insert or ignore into bowlingFT20Career (startDate, endDate, playerId, player, innings, balls, runs, wickets, average, strikeRate, econRate, threeWkts, fiveWkts, rating)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], innings, balls, runs, wkts, bowlingAverage, strikeRate, econRate, threeWkts, fiveWkts, rating))
        
    # All-round career        
    c.execute('select ft20Id, runs, wkts, rating from allRoundFT20Match where playerId=?',(player[0], ))
    wkts = 0
    runs = 0
    rating = 0.0
    firstFT20 = 99999
    lastFT20 = 0
    thirtyTwoWkts = 0
    ft20s = 0
    for allRoundMatch in c.fetchall():
        if allRoundMatch[0] < firstFT20: firstFT20 = allRoundMatch[0]
        if allRoundMatch[0] > lastFT20: lastFT20 = allRoundMatch[0]                
        ft20s += 1
        runsInns = 0 if allRoundMatch[1] == None else allRoundMatch[1]
        wktsInns = 0 if allRoundMatch[2] == None else allRoundMatch[2]
        runs = runs + runsInns
        wkts = wkts + wktsInns
        if runsInns >= 30 and wktsInns >= 2 : thirtyTwoWkts += 1
        rating = rating + allRoundMatch[3]
    rating = rating / ft20s if ft20s > 0 else None    
    # discount rating for those that have played <20 ft20s
    if ft20s < 40 and ft20s >= 20 and rating != None: rating = rating * math.exp(-float(40-ft20s)/25)
    if ft20s < 20 and ft20s >= 10 and rating != None: rating = rating * math.exp(-float(20-ft20s)/10)
    if ft20s < 10 and rating != None: rating = rating * math.exp(-float(10-ft20s)/5)
    if rating != None: rating = rating + rating * ft20s / 400
    if rating != None and battingAverage != None and bowlingAverage != None:
        battingAverageMod = 50.0 if float(battingAverage) > 50.0 else float(battingAverage)
        bowlingAverageMod = 15.0 if float(bowlingAverage) < 15.0 else float(bowlingAverage)
        rating = rating + float(battingAverageMod) * 50 /float(bowlingAverageMod) # add battingAvg/bowlingAvg bonus
    
    c.execute('select startDate from ft20Info where ft20Id=?',(firstFT20, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from ft20Info where ft20Id=?',(lastFT20, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]
    c.execute('''insert or ignore into allRoundFT20Career (startDate, endDate, playerId, player, ft20s, runs, battingAverage, fifties, wickets, bowlingAverage, threeWkts, thirtyTwoWkts, rating)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], ft20s, runs, battingAverage, fifties, wkts, bowlingAverage, threeWkts, thirtyTwoWkts, rating))    
    conn.commit()    
conn.close()
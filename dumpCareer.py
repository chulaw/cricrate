#!/usr/bin/env python
import sqlite3
import math
import numpy as np
from scipy.stats import t
from datetime import date

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

c.execute('drop table battingTestCareer')
c.execute('drop table bowlingTestCareer')
c.execute('drop table allRoundTestCareer')
c.execute('''create table battingTestCareer (startDate text, endDate text, playerId integer unique, player text, tests integer, innings integer, notOuts integer, runs integer, average real, strikeRate real,
          fifties integer, hundreds integer, dblHundreds integer, tripleHundreds integer, rating real, confInt95 real)''')
c.execute('''create table bowlingTestCareer (startDate text, endDate text, playerId integer unique, player text, tests integer, innings integer, balls integer, runs integer, wickets integer, average real,
          strikeRate real, econRate real, fiveWkts integer, tenWkts integer, rating real, confInt95 real)''')
c.execute('''create table allRoundTestCareer (startDate text, endDate text, playerId integer unique, player text, tests integer, runs integer, battingAverage real, hundreds integer, wickets integer,
          bowlingAverage real, fiveWkts integer, hundredFiveWkts integer, rating real, confInt95 real)''')

c.execute('select playerId, player, country from playerInfo')
for player in c.fetchall():
    # Batting career
    # print player[1]
    c.execute('select testId, notOut, runs, balls, rating, totalPct, bowlingRating, entryRuns, entryWkts, wicketsAtCrease, homeAway, status, result from battingTestInnings where playerId=?',(player[0], ))
    tests = {}
    innings = 0
    notOuts = 0
    runs = 0
    runsWithBalls = 0
    balls = 0
    rating = 0.0
    mean = 0.0
    firstTest = 99999
    lastTest = 0
    fifties = 0
    hundreds = 0
    dblHundreds = 0
    tripleHundreds = 0
    samples = []
    for battingInning in c.fetchall():
        if battingInning[0] < firstTest: firstTest = battingInning[0]
        if battingInning[0] > lastTest: lastTest = battingInning[0]
        tests[battingInning[0]] = 1
        innings += 1
        notOuts = notOuts + battingInning[1]
        runs = runs + battingInning[2]
        if battingInning[3] != None:
            runsWithBalls = runsWithBalls + battingInning[2]
            balls = balls + battingInning[3]
        if battingInning[2] >= 50 and battingInning[2] < 100: fifties += 1
        if battingInning[2] >= 100: hundreds += 1
        if battingInning[2] >= 200: dblHundreds += 1
        if battingInning[2] >= 300: tripleHundreds += 1
        rating = rating + battingInning[4]
        samples.append(battingInning[4])

    if innings > 1:
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        tstat = (t.interval(0.95, innings-1))[1]
        ci95 = tstat * std / math.sqrt(innings)
    else:
        ci95 = None

    tests = len(tests)
    battingAverage = float(runs) / float(innings - notOuts) if innings != notOuts else None
    strikeRate = 100 * float(runsWithBalls) / float(balls) if balls > 0 else None
    rating = rating * 1.05 / innings if innings > 0 else None
    # discount rating for those that have played <40 tests
    if tests < 50 and tests >= 40 and rating != None: rating = rating * math.exp(-float(50-tests)/200)
    if tests < 40 and tests >= 20 and rating != None: rating = rating * math.exp(-float(50-tests)/165)
    if tests < 20 and tests >= 10 and rating != None: rating = rating * math.exp(-float(50-tests)/85)
    if tests < 10 and rating != None: rating = rating * math.exp(-float(50-tests)/40)
    if tests < 5 and rating != None: rating = rating * math.exp(-float(50-tests)/20)

    c.execute('select startDate from testInfo where testId=?',(firstTest, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from testInfo where testId=?',(lastTest, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]
    c.execute('select testTeamId, startDate from teamTestLive where team=? and startDate>=? and startDate<=?',(player[2], startDate, endDate))
    teamTests = 0
    noTestYears = 0
    if startDate != None: lastStart = int(startDate)
    for teamMatch in c.fetchall():
        if int(teamMatch[1]) > (lastStart + 10100): noTestYears = noTestYears + 1
        lastStart = int(teamMatch[1])
        teamTests += 1

    if startDate != None and endDate != None:
        startD = date(int(startDate[:4]), int(startDate[4:-2]), int(startDate[6:]))
        endD = date(int(endDate[:4]), int(endDate[4:-2]), int(endDate[6:]))
        careerDays = endD - startD
        longevity = (careerDays.days - noTestYears * 365 * 0.5) * (float(tests)/float(teamTests)) / 16500
    if rating != None: rating = (rating + rating * longevity) * 0.97
    if rating != None: battingCareerRating = rating
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('''insert or ignore into battingTestCareer (startDate, endDate, playerId, player, tests, innings, notOuts, runs, average, strikeRate, fifties, hundreds, dblHundreds, tripleHundreds, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], tests, innings, notOuts, runs, battingAverage, strikeRate, fifties, hundreds, dblHundreds, tripleHundreds, rating, ci95))

    # Bowling career
    c.execute('select testId, wkts, balls, runs, rating, battingRating, wktsRating, status, result, homeAway from bowlingTestInnings where playerId=?',(player[0], ))
    tests = {}
    innings = 0
    wkts = 0
    runs = 0
    balls = 0
    rating = 0.0
    mean = 0.0
    firstTest = 99999
    lastTest = 0
    fiveWkts = 0
    tenWkts = 0
    samples = []
    for bowlingInning in c.fetchall():
        if bowlingInning[0] < firstTest: firstTest = bowlingInning[0]
        if bowlingInning[0] > lastTest: lastTest = bowlingInning[0]
        innings += 1
        wkts = wkts + bowlingInning[1]
        balls = balls + bowlingInning[2]
        runs = runs + bowlingInning[3]
        if bowlingInning[0] in tests:
            tests[bowlingInning[0]] += bowlingInning[1]
        else:
            tests[bowlingInning[0]] = bowlingInning[1]
        if bowlingInning[1] >= 5: fiveWkts += 1
        rating = rating + bowlingInning[4]
        samples.append(bowlingInning[4])
    for test in tests:
        if tests[test] >= 10: tenWkts = tenWkts + 1

    if innings > 1:
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        tstat = (t.interval(0.95, innings-1))[1]
        ci95 = tstat * std / math.sqrt(innings)
    else:
        ci95 = None

    tests = len(tests)
    bowlingAverage = float(runs) / float(wkts) if wkts != 0 else None
    strikeRate = float(balls) / float(wkts) if wkts != 0 else None
    econRate = float(runs) * 6 / float(balls) if balls != 0 else None
    rating = rating * 1.05 / innings if innings > 0 else None
    # discount rating for those that have played <40 tests
    if tests < 50 and tests >= 40 and rating != None: rating = rating * math.exp(-float(50-tests)/170)
    if tests < 40 and tests >= 20 and rating != None: rating = rating * math.exp(-float(50-tests)/135)
    if tests < 20 and tests >= 10 and rating != None: rating = rating * math.exp(-float(50-tests)/85)
    if tests < 10 and rating != None: rating = rating * math.exp(-float(50-tests)/40)
    if tests < 5 and rating != None: rating = rating * math.exp(-float(50-tests)/20)

    c.execute('select startDate from testInfo where testId=?',(firstTest, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from testInfo where testId=?',(lastTest, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    c.execute('select testTeamId, startDate from teamTestLive where team=? and startDate>=? and startDate<=?',(player[2], startDate, endDate))
    teamTests = 0
    noTestYears = 0
    if startDate != None: lastStart = int(startDate)
    for teamMatch in c.fetchall():
        if int(teamMatch[1]) > (lastStart + 10100): noTestYears = noTestYears + 1
        lastStart = int(teamMatch[1])
        teamTests += 1

    if startDate != None and endDate != None:
        startD = date(int(startDate[:4]), int(startDate[4:-2]), int(startDate[6:]))
        endD = date(int(endDate[:4]), int(endDate[4:-2]), int(endDate[6:]))
        careerDays = endD - startD
        longevity = (careerDays.days - noTestYears * 365 * 0.5) * (float(tests)/float(teamTests)) / 20000
    if rating != None: rating = (rating + rating * longevity) * 1.02
    if rating != None: bowlingCareerRating = rating
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('''insert or ignore into bowlingTestCareer (startDate, endDate, playerId, player, tests, innings, balls, runs, wickets, average, strikeRate, econRate, fiveWkts, tenWkts, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], tests, innings, balls, runs, wkts, bowlingAverage, strikeRate, econRate, fiveWkts, tenWkts, rating, ci95))

    # All-round career
    c.execute('select testId, runs1, runs2, wkts1, wkts2, battingRating, bowlingRating, rating from allRoundTestMatch where playerId=?',(player[0], ))
    tests = {}
    wkts = 0
    runs = 0
    rating = 0.0
    mean = 0.0
    firstTest = 99999
    lastTest = 0
    hundredFiveWkts = 0
    tests = 0
    samples = []
    for allRoundMatch in c.fetchall():
        if allRoundMatch[0] < firstTest: firstTest = allRoundMatch[0]
        if allRoundMatch[0] > lastTest: lastTest = allRoundMatch[0]
        tests += 1
        runs1 = 0 if allRoundMatch[1] == None else allRoundMatch[1]
        runs2 = 0 if allRoundMatch[2] == None else allRoundMatch[2]
        wkts1 = 0 if allRoundMatch[3] == None else allRoundMatch[3]
        wkts2 = 0 if allRoundMatch[4] == None else allRoundMatch[4]
        runs = runs + runs1 + runs2
        wkts = wkts + wkts1 + wkts2
        if (runs1 + runs2) >= 100 and (wkts1 + wkts2) >= 5 : hundredFiveWkts += 1
        rating = rating + allRoundMatch[7]
        samples.append(allRoundMatch[7])

    if tests > 1:
        mean = np.mean(samples)
        std = np.std(samples, ddof=1)
        tstat = (t.interval(0.95, tests-1))[1]
        ci95 = tstat * std / math.sqrt(tests)
    else:
        ci95 = None

    rating = rating * 0.88 / tests if tests > 0 else None
    # discount rating for those that have played <40 tests
    if tests < 50 and tests >= 40 and rating != None: rating = rating * math.exp(-float(50-tests)/170)
    if tests < 40 and tests >= 20 and rating != None: rating = rating * math.exp(-float(50-tests)/130)
    if tests < 20 and tests >= 10 and rating != None: rating = rating * math.exp(-float(50-tests)/85)
    if tests < 10 and rating != None: rating = rating * math.exp(-float(50-tests)/40)
    if tests < 5 and rating != None: rating = rating * math.exp(-float(50-tests)/20)

    c.execute('select startDate from testInfo where testId=?',(firstTest, ))
    startDate = c.fetchone()
    if startDate != None: startDate = startDate[0]
    c.execute('select startDate from testInfo where testId=?',(lastTest, ))
    endDate = c.fetchone()
    if endDate != None: endDate = endDate[0]

    c.execute('select testTeamId, startDate from teamTestLive where team=? and startDate>=? and startDate<=?',(player[2], startDate, endDate))
    teamTests = 0
    noTestYears = 0
    if startDate != None: lastStart = int(startDate)
    for teamMatch in c.fetchall():
        if int(teamMatch[1]) > (lastStart + 10100): noTestYears = noTestYears + 1
        lastStart = int(teamMatch[1])
        teamTests += 1

    if startDate != None and endDate != None:
        startD = date(int(startDate[:4]), int(startDate[4:-2]), int(startDate[6:]))
        endD = date(int(endDate[:4]), int(endDate[4:-2]), int(endDate[6:]))
        careerDays = endD - startD
        longevity = (careerDays.days - noTestYears * 365 * 0.5) * (float(tests)/float(teamTests)) / 15500
    if rating != None: rating = (rating + rating * longevity) * 0.76
    if rating != None and battingCareerRating != None and bowlingCareerRating != None: rating = rating + float(battingCareerRating) * float(bowlingCareerRating) / 5000
    if ci95 != None and mean != 0: ci95 = ci95 * rating / mean

    c.execute('''insert or ignore into allRoundTestCareer (startDate, endDate, playerId, player, tests, runs, battingAverage, hundreds, wickets, bowlingAverage, fiveWkts, hundredFiveWkts, rating, confInt95)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (startDate, endDate, player[0], player[1], tests, runs, battingAverage, hundreds, wkts, bowlingAverage, fiveWkts, hundredFiveWkts, rating, ci95))
    conn.commit()
conn.close()

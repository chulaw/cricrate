#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import math
start = time.clock()

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

#c.execute('drop table testInfo')
c.execute('drop table teamTestLive')
c.execute('drop table teamTestOverall')
#c.execute('''create table testInfo (testId integer unique, startDate text, location text, team1 text, team2 text, season text, ground text, ballsPerOver integer, result text, margin text, series text,
#          seriesStatus text, scoreLink text)''')
c.execute('create table teamTestLive (testTeamId integer unique, startDate text, team text, opposition integer, location text, result integer, scoreLink text, homeRating real, awayRating real, rating real)')
c.execute('create table teamTestOverall (teamSpan text unique, startDate text, endDate text, span text, team text, tests integer, wins integer, draws integer, losses integer, winPct real, rating real)')

month2Num = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
relativeURL = '/ci/engine/records/team/match_results.html?class=1;id=1877;type=year'
defaultTeamRating = 400.0
expSmoothFactor = 0.025

# loop through test matches
for x in range(0, 127):
    # load cricinfo annual match list
    yearURL = 'http://stats.espncricinfo.com' + relativeURL
    yearPage = requests.get(yearURL)
    yearTree = html.fromstring(yearPage.text)

    data1 = yearTree.xpath('//a[@class="data-link"]/text()')
    data2 = yearTree.xpath('//td[@nowrap="nowrap"]/text()')
    links = yearTree.xpath('//a[@class="data-link"]/@href')

    modD2 = []
    # handle one-off match forfeit
    if '2006' in relativeURL:
        for k in range(0, len(data2)):
            if 'Aug 17-21, 2006' in data2[k]:
                modD2.append('forfeit')
                modD2.append(data2[k])
            else:
                modD2.append(data2[k])
        data2 = modD2

    relativeURL = yearTree.xpath('//a[@class="QuoteSummary"]/@href')
    relativeURL = relativeURL[len(relativeURL)-1]

    groundLinks = []
    scoreLinks = []
    for j in range(0, len(links)):
        if 'match' in links[j]: scoreLinks.append(links[j])
        if 'ground' in links[j]: groundLinks.append(links[j])
    testNum = int(len(data2) / 2)

    i = 0
    k = 0
    teams1 = []
    teams2 = []
    grounds = []
    results = []
    testIds = []
    locations = {}
    while (i < len(data1)):
        team1 = data1[i]
        team2 = data1[i+1]
        teams1.append(team1)
        teams2.append(team2)
        result = ''
        testId = None
        if team1 in data1[i+2] or team2 in data1[i+2]:
            results.append(data1[i+2])
            grounds.append(data1[i+3])
            testIds.append(data1[i+4].split()[2])
            testId = data1[i+4].split()[2]
            result = data1[i+2]
            i = i + 5
        else:
            results.append('Draw')
            grounds.append(data1[i+2])
            testIds.append(data1[i+3].split()[2])
            testId = data1[i+3].split()[2]
            result = 'Draw'
            i = i + 4

        team1Ratings = {}
        c.execute('select rating, homeRating, awayRating from teamTestLive where team=? order by testTeamId desc', (team1, ))
        team1Ratings = c.fetchone()
        if team1Ratings is None:
            team1LiveRating = defaultTeamRating
            team1LiveHomeRating = defaultTeamRating
            team1LiveAwayRating = defaultTeamRating
        else:
            team1LiveRating = team1Ratings[0]
            team1LiveHomeRating = team1Ratings[1]
            team1LiveAwayRating = team1Ratings[2]

        team2Ratings = {}
        c.execute('select rating, homeRating, awayRating from teamTestLive where team=? order by testTeamId desc', (team2, ))
        team2Ratings = c.fetchone()
        if team2Ratings is None:
            team2LiveRating = defaultTeamRating
            team2LiveHomeRating = defaultTeamRating
            team2LiveAwayRating = defaultTeamRating
        else:
            team2LiveRating = team2Ratings[0]
            team2LiveHomeRating = team2Ratings[1]
            team2LiveAwayRating = team2Ratings[2]

        groundURL = 'http://www.espncricinfo.com' + groundLinks[k]
        groundPage = requests.get(groundURL)
        groundTree = html.fromstring(groundPage.text)
        location = groundTree.xpath('(//span[@class="SubnavSubsection"]/text())')[0]
        locations[testId] = location
        k += 1

        team1LocWin = 1
        team2LocWin = 1
        team1LocLoss = 1
        team2LocLoss = 1
        if location == team1:
            team1LocWin = 0.75
            team2LocWin = 1.25
            team1LocLoss = 1.25
            team2LocLoss = 0.75
        elif location == team2:
            team1LocWin = 1.25
            team2LocWin = 0.75
            team1LocLoss = 0.75
            team2LocLoss = 1.25

        if (result == team1):
            team1LiveRating = expSmoothFactor * (500 + (team2LiveRating / team1LiveRating) * 1000 * team1LocWin) + (1 - expSmoothFactor) * team1LiveRating
            team2LiveRating = expSmoothFactor * (500 - (team2LiveRating / team1LiveRating) * 1000 * team2LocLoss) + (1 - expSmoothFactor) * team2LiveRating
            if location == team1:
                team1LiveHomeRating = expSmoothFactor * (500 + (team2LiveAwayRating / team1LiveHomeRating) * 1000) + (1 - expSmoothFactor) * team1LiveHomeRating
                team2LiveAwayRating = expSmoothFactor * (500 - (team2LiveAwayRating / team1LiveHomeRating) * 1000) + (1 - expSmoothFactor) * team2LiveAwayRating
            elif location == team2:
                team1LiveAwayRating = expSmoothFactor * (500 + (team2LiveHomeRating / team1LiveAwayRating) * 1000) + (1 - expSmoothFactor) * team1LiveAwayRating
                team2LiveHomeRating = expSmoothFactor * (500 - (team2LiveHomeRating / team1LiveAwayRating) * 1000) + (1 - expSmoothFactor) * team2LiveHomeRating
        elif (result == team2):
            team1LiveRating = expSmoothFactor * (500 - (team1LiveRating / team2LiveRating) * 1000 * team1LocLoss) + (1 - expSmoothFactor) * team1LiveRating
            team2LiveRating = expSmoothFactor * (500 + (team1LiveRating / team2LiveRating) * 1000 * team2LocWin) + (1 - expSmoothFactor) * team2LiveRating
            if location == team1:
                team1LiveHomeRating = expSmoothFactor * (500 - (team1LiveHomeRating / team2LiveAwayRating) * 1000) + (1 - expSmoothFactor) * team1LiveHomeRating
                team2LiveAwayRating = expSmoothFactor * (500 + (team1LiveHomeRating / team2LiveAwayRating) * 1000) + (1 - expSmoothFactor) * team2LiveAwayRating
            elif location == team2:
                team1LiveAwayRating = expSmoothFactor * (500 - (team1LiveAwayRating / team2LiveHomeRating) * 1000) + (1 - expSmoothFactor) * team1LiveAwayRating
                team2LiveHomeRating = expSmoothFactor * (500 + (team1LiveAwayRating / team2LiveHomeRating) * 1000) + (1 - expSmoothFactor) * team2LiveHomeRating
        else:
            if (team1LiveRating > team2LiveRating):
                team1LiveRating = expSmoothFactor * (500 - (team1LiveRating / team2LiveRating) * 500 * team1LocLoss) + (1 - expSmoothFactor) * team1LiveRating
                team2LiveRating = expSmoothFactor * (500 + (team1LiveRating / team2LiveRating) * 500 * team2LocWin) + (1 - expSmoothFactor) * team2LiveRating
                if location == team1:
                    team1LiveHomeRating = expSmoothFactor * (500 - (team1LiveHomeRating / team2LiveAwayRating) * 500) + (1 - expSmoothFactor) * team1LiveHomeRating
                    team2LiveAwayRating = expSmoothFactor * (500 + (team1LiveHomeRating / team2LiveAwayRating) * 500) + (1 - expSmoothFactor) * team2LiveAwayRating
                elif location == team2:
                    team1LiveAwayRating = expSmoothFactor * (500 - (team1LiveAwayRating / team2LiveHomeRating) * 500) + (1 - expSmoothFactor) * team1LiveAwayRating
                    team2LiveHomeRating = expSmoothFactor * (500 + (team1LiveAwayRating / team2LiveHomeRating) * 500) + (1 - expSmoothFactor) * team2LiveHomeRating
            elif (team1LiveRating < team2LiveRating):
                team1LiveRating = expSmoothFactor * (500 + (team2LiveRating / team1LiveRating) * 500 * team1LocWin) + (1 - expSmoothFactor) * team1LiveRating
                team2LiveRating = expSmoothFactor * (500 - (team2LiveRating / team1LiveRating) * 500 * team2LocLoss) + (1 - expSmoothFactor) * team2LiveRating
                if location == team1:
                    team1LiveHomeRating = expSmoothFactor * (500 + (team2LiveAwayRating / team1LiveHomeRating) * 500) + (1 - expSmoothFactor) * team1LiveHomeRating
                    team2LiveAwayRating = expSmoothFactor * (500 - (team2LiveAwayRating / team1LiveHomeRating) * 500) + (1 - expSmoothFactor) * team2LiveAwayRating
                elif location == team2:
                    team1LiveAwayRating = expSmoothFactor * (500 + (team2LiveHomeRating / team1LiveAwayRating) * 500) + (1 - expSmoothFactor) * team1LiveAwayRating
                    team2LiveHomeRating = expSmoothFactor * (500 - (team2LiveHomeRating / team1LiveAwayRating) * 500) + (1 - expSmoothFactor) * team2LiveHomeRating

        testTeam1Id = repr(int(testId)) + '1'
        testTeam2Id = repr(int(testId)) + '2'
        c.execute('insert or replace into teamTestLive (testTeamId, team, opposition, result, homeRating, awayRating, rating) values (?, ?, ?, ?, ?, ?, ?)',
                  (testTeam1Id, team1, team2, result, team1LiveHomeRating, team1LiveAwayRating, team1LiveRating))
        c.execute('insert or replace into teamTestLive (testTeamId, team, opposition, result, homeRating, awayRating, rating) values (?, ?, ?, ?, ?, ?, ?)',
                  (testTeam2Id, team2, team1, result, team2LiveHomeRating, team2LiveAwayRating, team2LiveRating))
        # print testId
        # print team1
        # print team2
        # print team1LiveRating
        # print team2LiveRating
        conn.commit()

    startDates = {}
    for i in range(0, testNum):
        margin = data2[2*i]
        startDate = data2[2*i+1]
        startDate = startDate.split(" - ")[0];
        month = startDate.split()[0]
        year = startDate.split()[len(startDate.split())-1]
        day = startDate.split()[1].split('-')[0]
        day = day.split(',')[0]
        day = '0' + day if int(day) < 10 else day
        startDate = year + month2Num[month] + day
        startDates[testIds[i]] = startDate
        print('Dumping details for test #'+repr(testIds[i])+' '+teams1[i]+' vs '+teams2[i]+', startDate: '+startDate+', result: '+results[i]+', margin: '+margin+', scoreLink: '+scoreLinks[i]+', ground: '+grounds[i]+', location: '+location)
        c.execute('insert or ignore into testInfo (testId, startDate, location, team1, team2, ground, result, margin, scoreLink) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (testIds[i], startDate, location, teams1[i], teams2[i], grounds[i], results[i], margin, scoreLinks[i]))
        conn.commit()

    for i in range(0, testNum):
        testTeam1Id = repr(int(testIds[i])) + '1'
        testTeam2Id = repr(int(testIds[i])) + '2'
        c.execute('update teamTestLive set startDate=?,location=?,scoreLink=? where testTeamId=?', (startDates[testIds[i]], locations[testIds[i]], scoreLinks[i], testTeam1Id))
        c.execute('update teamTestLive set startDate=?,location=?,scoreLink=? where testTeamId=?', (startDates[testIds[i]], locations[testIds[i]], scoreLinks[i], testTeam2Id))
        conn.commit()

spans = ['1877-2099', '1877-1914', '1915-1929', '1930-1939', '1940-1949', '1950-1959', '1960-1969', '1970-1979', '1980-1989', '1990-1999', '2000-2009', '2010-2019']
c.execute('select distinct team from teamTestLive')
for team in c.fetchall():
    for span in spans:
        startSpan = span.split('-')[0] + "0000"
        endSpan = span.split('-')[1] + "9999"
        c.execute('select testTeamId, result, rating, startDate from teamTestLive where team=? and startDate>? and startDate<?',(team[0], startSpan, endSpan))
        tests = 0
        rating = 0.0
        firstTest = 99999
        lastTest = 0
        wins = 0
        draws = 0
        losses = 0
        for teamMatch in c.fetchall():
            testId = int((repr(teamMatch[0]))[0:-1])
            if testId < firstTest: firstTest = testId
            if testId > lastTest: lastTest = testId
            tests += 1
            if teamMatch[1] == team[0]:
                wins += 1
            elif teamMatch[1] == "Draw":
                draws += 1
            else: losses += 1
            rating = rating + teamMatch[2]
            teamMatch[3]
        rating = rating / tests if tests > 0 else None
        if tests == 0:
            continue
        winPct = 100.0 * wins / tests

        if tests < 40 and tests >= 20 and rating != None: rating = rating * math.exp(-float(40-tests)/150)
        if tests < 20 and tests >= 10 and rating != None: rating = rating * math.exp(-float(20-tests)/100)
        if tests < 10 and tests >= 5  and rating != None: rating = rating * math.exp(-float(10-tests)/50)
        if tests < 5 and rating != None: rating = rating * math.exp(-float(5-tests)/25)
        if rating != None: rating = rating + rating * tests / 15000
        c.execute('select startDate from testInfo where testId=?',(firstTest, ))
        startDate = c.fetchone()
        if startDate != None: startDate = startDate[0]
        c.execute('select startDate from testInfo where testId=?',(lastTest, ))
        endDate = c.fetchone()
        if endDate != None: endDate = endDate[0]
        print(team[0] + ' ' + repr(startDate)+ ' ' + repr(endDate) + ' ' + span + ' ' + repr(tests) + ' ' + repr(wins) + ' ' + repr(draws) + ' ' + repr(losses) + ' ' + repr(winPct) + ' '+ repr(rating))
        teamSpan = team[0] + "_" + span
        c.execute('''insert or replace into teamTestOverall (teamSpan, startDate, endDate, span, team, tests, wins, draws, losses, winPct, rating)
                  values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (teamSpan, startDate, endDate, span, team[0], tests, wins, draws, losses, winPct, rating))
        conn.commit()
conn.close()
elapsed = (time.clock() - start)
print('Time elapsed: ' + repr(elapsed) + 'sec')

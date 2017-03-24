#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import math
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()

#c.execute('drop table t20iInfo')
c.execute('drop table teamT20ILive')
c.execute('drop table teamT20IOverall')
#c.execute('''create table t20iInfo (t20iId integer unique, startDate text, location text, team1 text, team2 text, season text, ground text, result text, margin text, series text,
#          seriesStatus text, scoreLink text)''')
c.execute('create table teamT20ILive (t20iTeamId integer unique, startDate text, team text, opposition integer, location text, result integer, scoreLink text, homeRating real, awayRating real, rating real)')
c.execute('create table teamT20IOverall (teamSpan text unique, startDate text, endDate text, span text, team text, t20is integer, wins integer, ties integer, losses integer, winPct real, rating real)')

month2Num = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
relativeURL = '/ci/engine/records/team/match_results.html?class=3;id=2005;type=year'
defaultTeamRating = 350.0
expSmoothFactor = 0.025

# loop through t20i matches
for x in range(0, 13):
    # load cricinfo annual match list
    yearURL = 'http://stats.espncricinfo.com' + relativeURL
    yearPage = requests.get(yearURL)
    yearTree = html.fromstring(yearPage.text)

    data1 = yearTree.xpath('//a[@class="data-link"]/text()')
    data2 = yearTree.xpath('//td[@nowrap="nowrap"]/text()')
    links = yearTree.xpath('//a[@class="data-link"]/@href')

    relativeURL = yearTree.xpath('//a[@class="QuoteSummary"]/@href')
    relativeURL = relativeURL[len(relativeURL)-1]

    groundLinks = []
    scoreLinks = []
    for j in range(0, len(links)):
        if 'match' in links[j]: scoreLinks.append(links[j])
        if 'ground' in links[j]: groundLinks.append(links[j])
    t20iNum = len(data2) / 2

    i = 0
    k = 0
    teams1 = []
    teams2 = []
    grounds = []
    results = []
    t20iIds = []
    locations = {}
    while (i < len(data1)):
        team1 = data1[i]
        team2 = data1[i+1]
        teams1.append(team1)
        teams2.append(team2)
        t20iId = None
        if team1 in data1[i+2] or team2 in data1[i+2]:
            results.append(data1[i+2])
            result = data1[i+2]
            grounds.append(data1[i+3])
            t20iIds.append(data1[i+4].split()[2])
            t20iId = data1[i+4].split()[2]
            i = i + 5
        else:
            results.append('Tie/NR')
            result = 'Tie/NR'
            grounds.append(data1[i+2])
            t20iIds.append(data1[i+3].split()[2])
            t20iId = data1[i+3].split()[2]
            i = i + 4

        team1Ratings = {}
        c.execute('select rating, homeRating, awayRating from teamT20ILive where team=? order by t20iTeamId desc', (team1, ))
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
        c.execute('select rating, homeRating, awayRating from teamT20ILive where team=? order by t20iTeamId desc', (team2, ))
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
        locations[t20iId] = location
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

        t20iTeam1Id = `int(t20iId)` + '1'
        t20iTeam2Id = `int(t20iId)` + '2'
        c.execute('insert or ignore into teamT20ILive (t20iTeamId, startDate, team, opposition, location, result, scoreLink, homeRating, awayRating, rating) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (t20iTeam1Id, None, team1, team2, None, result, None, team1LiveHomeRating, team1LiveAwayRating, team1LiveRating))
        c.execute('insert or ignore into teamT20ILive (t20iTeamId, startDate, team, opposition, location, result, scoreLink, homeRating, awayRating, rating) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (t20iTeam2Id, None, team2, team1, None, result, None, team2LiveHomeRating, team2LiveAwayRating, team2LiveRating))
        conn.commit()

    startDates = {}
    locations = {}
    for i in range(0, t20iNum):
        margin = data2[2*i]
        startDate = data2[2*i+1]
        month = startDate.split()[0]
        year = startDate.split()[len(startDate.split())-1]
        day = startDate.split()[1].split('-')[0]
        day = day.split(',')[0]
        day = '0' + day if int(day) < 10 else day
        startDate = year + month2Num[month] + day
        startDates[t20iIds[i]] = startDate
        print 'Dumping details for t20i #'+`t20iIds[i]`+' '+teams1[i]+' vs '+teams2[i]+', startDate: '+startDate+', result: '+results[i]+', margin: '+margin+', scoreLink: '+scoreLinks[i]+', ground: '+grounds[i]+', location: '+location
        c.execute('insert or ignore into t20iInfo (t20iId, startDate, location, team1, team2, ground, result, margin, scoreLink) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (t20iIds[i], startDate, location, teams1[i], teams2[i], grounds[i], results[i], margin, scoreLinks[i]))
        conn.commit()

    for i in range(0, t20iNum):
       t20iTeam1Id = `int(t20iIds[i])` + '1'
       t20iTeam2Id = `int(t20iIds[i])` + '2'
       c.execute('update teamT20ILive set startDate=?,location=?,scoreLink=? where t20iTeamId=?', (startDates[t20iIds[i]], location, scoreLinks[i], t20iTeam1Id))
       c.execute('update teamT20ILive set startDate=?,location=?,scoreLink=? where t20iTeamId=?', (startDates[t20iIds[i]], location, scoreLinks[i], t20iTeam2Id))
       conn.commit()

spans = ['2005-2099', '2005-2009', '2010-2014']
c.execute('select distinct team from teamT20ILive')
for team in c.fetchall():
    for span in spans:
        startSpan = span.split('-')[0] + "0000"
        endSpan = span.split('-')[1] + "9999"
        c.execute('select t20iTeamId, result, rating from teamT20ILive where team=? and startDate>? and startDate<?',(team[0], startSpan, endSpan))
        t20is = 0
        rating = 0.0
        firstT20I = 99999
        lastT20I = 0
        wins = 0
        ties = 0
        losses = 0
        for teamMatch in c.fetchall():
            t20iId = int((`teamMatch[0]`)[0:-1])
            if t20iId < firstT20I: firstT20I = t20iId
            if t20iId > lastT20I: lastT20I = t20iId
            t20is += 1
            if teamMatch[1] == team[0]:
                wins += 1
            elif teamMatch[1] == "Tie/NR":
                ties += 1
            else: losses += 1
            rating = rating + teamMatch[2]
        rating = rating / t20is if t20is > 0 else None
        if t20is == 0:
            continue
        winPct = 100.0 * wins / t20is
        # discount rating for those that have played <20 t20is
        if t20is < 20 and t20is >= 10 and rating != None: rating = rating * math.exp(-float(20-t20is)/100)
        if t20is < 10 and t20is >= 5  and rating != None: rating = rating * math.exp(-float(10-t20is)/50)
        if t20is < 5 and rating != None: rating = rating * math.exp(-float(5-t20is)/25)

        c.execute('select startDate from t20iInfo where t20iId=?',(firstT20I, ))
        startDate = c.fetchone()
        if startDate != None: startDate = startDate[0]
        c.execute('select startDate from t20iInfo where t20iId=?',(lastT20I, ))
        endDate = c.fetchone()
        if endDate != None: endDate = endDate[0]
        print team[0] + ' ' + `startDate`+ ' ' + `endDate` + ' ' + `t20is` + ' ' + `wins` + ' ' + `ties` + ' ' + `losses` + ' ' + `winPct` + ' '+ `rating`
        teamSpan = team[0] + "_" + span
        c.execute('''insert or ignore into teamT20IOverall (teamSpan, startDate, endDate, span, team, t20is, wins, ties, losses, winPct, rating)
                  values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (teamSpan, startDate, endDate, span, team[0], t20is, wins, ties, losses, winPct, rating))
        conn.commit()
conn.close()
elapsed = (time.clock() - start)
print 'Time elapsed: ' + `elapsed` + 'sec'

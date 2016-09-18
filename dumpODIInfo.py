#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import math
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

#c.execute('drop table odiInfo')
c.execute('drop table teamODILive')
c.execute('drop table teamODIOverall')
#c.execute('''create table odiInfo (odiId integer unique, startDate text, location text, team1 text, team2 text, season text, ground text, ballsPerOver integer, result text, margin text, series text,
#          seriesStatus text, scoreLink text)''')
c.execute('create table teamODILive (odiTeamId integer unique, startDate text, team text, opposition integer, location text, result integer, scoreLink text, rating real)')
c.execute('create table teamODIOverall (teamSpan text unique, startDate text, endDate text, span text, team text, odis integer, wins integer, ties integer, losses integer, winPct real, rating real)')

month2Num = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
relativeURL = '/ci/engine/records/team/match_results.html?class=2;id=1971;type=year'
defaultTeamRating = 100.0

# loop through odi matches
for x in range(0, 46):
    # load cricinfo annual match list    
    yearURL = 'http://stats.espncricinfo.com' + relativeURL
    yearPage = requests.get(yearURL)
    yearTree = html.fromstring(yearPage.text)

    data1 = yearTree.xpath('//a[@class="data-link"]/text()')
    data2 = yearTree.xpath('//td[@nowrap="nowrap"]/text()')
    links = yearTree.xpath('//a[@class="data-link"]/@href')
    
    modD2 = []
    # handle forfeits, incomplete matches
    if '1978' in relativeURL or '1987' in relativeURL or '1988' in relativeURL or '1996' in relativeURL or '2001' in relativeURL:
        for k in range(0, len(data2)):
            if 'Nov 3, 1978' in data2[k] or 'Mar 20, 1987' in data2[k] or 'Oct 14, 1988' in data2[k] or 'Mar 13, 1996' in data2[k] or 'Jun 17, 2001' in data2[k]:
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
    odiNum = int(len(data2) / 2)
    
    i = 0
    teams1 = []
    teams2 = []
    grounds = []
    results = []
    odiIds = []    
    while (i < len(data1)):
        team1 = data1[i]
        team2 = data1[i+1]
        teams1.append(team1)
        teams2.append(team2)                
        odiId = None
        if team1 in data1[i+2] or team2 in data1[i+2]:
            results.append(data1[i+2])
            result = data1[i+2]
            grounds.append(data1[i+3])
            odiIds.append(data1[i+4].split()[2])
            odiId = data1[i+4].split()[2]
            i = i + 5
        else:
            results.append('Tie/NR')
            result = 'Tie/NR'
            grounds.append(data1[i+2])
            odiIds.append(data1[i+3].split()[2])
            odiId = data1[i+3].split()[2]
            i = i + 4

        team1LiveRating = {}
        c.execute('select rating from teamODILive where team=? order by odiTeamId desc', (team1, ))
        team1LiveRating = c.fetchone()
        if team1LiveRating is None:
            team1LiveRating = defaultTeamRating
        else:
            team1LiveRating = team1LiveRating[0]
            
        team2LiveRating = {}        
        c.execute('select rating from teamODILive where team=? order by odiTeamId desc', (team2, ))
        team2LiveRating = c.fetchone()
        if team2LiveRating is None:
            team2LiveRating = defaultTeamRating
        else:
            team2LiveRating = team2LiveRating[0]
        
        if (result == team1):
            team1LiveRating = team1LiveRating + (team2LiveRating / team1LiveRating) * 2
            team2LiveRating = team2LiveRating - (team2LiveRating / team1LiveRating) * 2
        elif (result == team2):
            team1LiveRating = team1LiveRating - (team1LiveRating / team2LiveRating) * 2
            team2LiveRating = team2LiveRating + (team1LiveRating / team2LiveRating) * 2
        else:
            if (team1LiveRating > team2LiveRating):
                team1LiveRating = team1LiveRating - (team1LiveRating / team2LiveRating)
                team2LiveRating = team2LiveRating + (team1LiveRating / team2LiveRating)
            elif (team1LiveRating < team2LiveRating):
                team1LiveRating = team1LiveRating + (team2LiveRating / team1LiveRating)
                team2LiveRating = team2LiveRating - (team2LiveRating / team1LiveRating)          
        
        odiTeam1Id = repr(int(odiId)) + '1'
        odiTeam2Id = repr(int(odiId)) + '2'
        c.execute('insert or ignore into teamODILive (odiTeamId, team, opposition, result, rating) values (?, ?, ?, ?, ?)',
                  (odiTeam1Id, team1, team2, result, team1LiveRating))
        c.execute('insert or ignore into teamODILive (odiTeamId, team, opposition, result, rating) values (?, ?, ?, ?, ?)',
                  (odiTeam2Id, team2, team1, result, team2LiveRating))
        conn.commit()
 
    startDates = {}
    locations = {}
    for i in range(0, odiNum):
        margin = data2[2*i]
        startDate = data2[2*i+1]
        month = startDate.split()[0]
        year = startDate.split()[len(startDate.split())-1]
        day = startDate.split()[1].split('-')[0]
        day = day.split(',')[0]
        day = '0' + day if int(day) < 10 else day    
        startDate = year + month2Num[month] + day
        startDates[odiIds[i]] = startDate
        groundURL = 'http://www.espncricinfo.com' + groundLinks[i]
        groundPage = requests.get(groundURL)
        groundTree = html.fromstring(groundPage.text)
        location = groundTree.xpath('(//span[@class="SubnavSubsection"]/text())')[0]
        locations[odiIds[i]] = location
        print('Dumping details for odi #'+repr(odiIds[i])+' '+teams1[i]+' vs '+teams2[i]+', startDate: '+startDate+', result: '+results[i]+', margin: '+margin+', scoreLink: '+scoreLinks[i]+', ground: '+grounds[i]+', location: '+location)
        c.execute('insert or ignore into odiInfo (odiId, startDate, location, team1, team2, ground, result, margin, scoreLink) values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  (odiIds[i], startDate, location, teams1[i], teams2[i], grounds[i], results[i], margin, scoreLinks[i]))
        conn.commit()
    
    for i in range(0, odiNum):
       odiTeam1Id = repr(int(odiIds[i])) + '1'
       odiTeam2Id = repr(int(odiIds[i])) + '2'
       c.execute('update teamODILive set startDate=?,location=?,scoreLink=? where odiTeamId=?', (startDates[odiIds[i]], locations[odiIds[i]], scoreLinks[i], odiTeam1Id))
       c.execute('update teamODILive set startDate=?,location=?,scoreLink=? where odiTeamId=?', (startDates[odiIds[i]], locations[odiIds[i]], scoreLinks[i], odiTeam2Id))
       conn.commit()

spans = ['1971-2099', '1971-1984', '1985-1989', '1990-1994', '1995-1999', '2000-2004', '2005-2009', '2010-2014']
c.execute('select distinct team from teamODILive')
for team in c.fetchall():
    for span in spans:
        startSpan = span.split('-')[0] + "0000"
        endSpan = span.split('-')[1] + "9999"
        c.execute('select odiTeamId, result, rating from teamODILive where team=? and startDate>? and startDate<?',(team[0], startSpan, endSpan))
        odis = 0
        rating = 0.0
        firstODI = 99999
        lastODI = 0
        wins = 0
        ties = 0
        losses = 0
        for teamMatch in c.fetchall():
            odiId = int((repr(teamMatch[0]))[0:-1])
            if odiId < firstODI: firstODI = odiId
            if odiId > lastODI: lastODI = odiId
            odis += 1        
            if teamMatch[1] == team[0]:
                wins += 1
            elif teamMatch[1] == "Tie/NR":
                ties += 1
            else: losses += 1
            rating = rating + teamMatch[2]
        rating = rating / odis if odis > 0 else None
        if odis == 0:
            continue
        winPct = 100.0 * wins / odis
        # discount rating for those that have played <100 odis
        if odis < 50 and odis >= 25 and rating != None: rating = rating * math.exp(-float(50-odis)/150)
        if odis < 25 and odis >= 10 and rating != None: rating = rating * math.exp(-float(25-odis)/25)
        if odis < 10 and rating != None: rating = rating * math.exp(-float(10-odis)/10)
        if rating != None: rating = rating + rating * odis / 20000
        
        c.execute('select startDate from odiInfo where odiId=?',(firstODI, ))
        startDate = c.fetchone()
        if startDate != None: startDate = startDate[0]
        c.execute('select startDate from odiInfo where odiId=?',(lastODI, ))
        endDate = c.fetchone()
        if endDate != None: endDate = endDate[0]
        print(team[0] + ' ' + repr(startDate)+ ' ' + repr(endDate) + ' ' + repr(odis) + ' ' + repr(wins) + ' ' + repr(ties) + ' ' + repr(losses) + ' ' + repr(winPct) + ' '+ repr(rating))
        teamSpan = team[0] + "_" + span
        c.execute('''insert or ignore into teamODIOverall (teamSpan, startDate, endDate, span, team, odis, wins, ties, losses, winPct, rating)
                  values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (teamSpan, startDate, endDate, span, team[0], odis, wins, ties, losses, winPct, rating))
        conn.commit()
conn.close()
elapsed = (time.clock() - start)
print('Time elapsed: ' + repr(elapsed) + 'sec')
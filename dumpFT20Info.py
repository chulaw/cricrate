#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import math
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()

c.execute('drop table ft20Info')
c.execute('drop table teamFT20Live')
c.execute('drop table teamFT20Overall')
c.execute('''create table ft20Info (ft20Id integer unique, startDate text, team1 text, team2 text, season text, ground text, result text, margin text, series text, scoreLink text)''')
c.execute('create table teamFT20Live (ft20TeamId integer unique, startDate text, team text, opposition integer, ground text, result integer, scoreLink text, rating real)')
c.execute('create table teamFT20Overall (teamSpan text unique, startDate text, endDate text, span text, team text, ft20s integer, wins integer, ties integer, losses integer, winPct real, rating real)')

month2Num = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
teamNameChange = {'Chennai T20':'Chennai Super Kings', 'Delhi T20':'Delhi Daredevils', 'Punjab T20':'Kings XI Punjab', 'Bangalore':'Royal Challengers Bangalore', 'Hyderabad':'Sunrisers Hyderabad',
                    'Rajasthan':'Rajasthan Royals', 'Mumbai T20':'Mumbai Indians', 'Kolkata T20':'Kolkata Knight Riders', 'Super Kings':'Chennai Super Kings', 'Daredevils':'Delhi Daredevils',
                    'Kings XI':'Kings XI Punjab', 'RCB':'Royal Challengers Bangalore', 'Sunrisers':'Sunrisers Hyderabad', 'Royals':'Rajasthan Royals', 'Mum Indians':'Mumbai Indians', 'Scorchers':'Perth Scorchers',
                    'KKR':'Kolkata Knight Riders', 'Chargers':'Deccan Chargers', 'Kochi':'Kochi Tuskers Kerala', 'Warriors':'Pune Warriors', 'Tridents':'Barbados Tridents', 'Zouks':'St Lucia Zouks',
                    'Amazon':'Guyana Amazon Warriors', 'Red Steel':'Trinidad & Tobago Red Steel', 'Hawksbills':'Antigua Hawksbills', 'Tallawahs':'Jamaica Tallawahs', 'Melb Stars':'Melbourne Stars',
                    'Melb Reneg':'Melbourne Renegades', 'Syd Sixers':'Sydney Sixers', 'Syd Thunder':'Sydney Thunder', 'Hurricanes':'Hobart Hurricanes', 'Strikers':'Adelaide Strikers', 'Heat':'Brisbane Heat',
                    'Red Steel':'Trinidad & Tobago Red Steel', 'Patriots':'St Kitts and Nevis Patriots', 'Supergiants':'Rising Pune Supergiants', 'Guj Lions': 'Gujarat Lions', 'T&T Riders': 'Trinbago Knight Riders'}

relativeURLs = ['/indian-premier-league-2014/engine/records/team/match_results.html?id=2007%2F08;trophy=117;type=season',
                '/indian-premier-league-2014/engine/records/team/match_results.html?id=2009;trophy=117;type=season',
                '/indian-premier-league-2014/engine/records/team/match_results.html?id=2009%2F10;trophy=117;type=season',
                '/indian-premier-league-2014/engine/records/team/match_results.html?id=2011;trophy=117;type=season',
                '/big-bash-league-2013/engine/records/team/match_results.html?id=2011%2F12;trophy=158;type=season',
                '/indian-premier-league-2014/engine/records/team/match_results.html?id=2012;trophy=117;type=season',
                '/big-bash-league-2013/engine/records/team/match_results.html?id=2012%2F13;trophy=158;type=season',
                '/indian-premier-league-2014/engine/records/team/match_results.html?id=2013;trophy=117;type=season',
                '/caribbean-premier-league-2013/engine/records/team/match_results.html?id=2013;trophy=118;type=season',
                '/big-bash-league-2013/engine/records/team/match_results.html?id=2013%2F14;trophy=158;type=season',
                '/indian-premier-league-2014/engine/records/team/match_results.html?id=2014;trophy=117;type=season',
                '/caribbean-premier-league-2014/engine/records/team/match_results.html?id=2014;trophy=118;type=season',
                '/big-bash-league-2014/engine/records/team/match_results.html?id=2014%2F15;trophy=158;type=season',
                '/indian-premier-league-2015/engine/records/team/match_results.html?id=2015;trophy=117;type=season',
                '/caribbean-premier-league-2015/engine/records/team/match_results.html?id=2015;trophy=118;type=season',
                '/big-bash-league-2015/engine/records/team/match_results.html?id=2015%2F16;trophy=158;type=season',
                '/indian-premier-league-2016/engine/records/team/match_results.html?id=2016;trophy=117;type=season',
                '/caribbean-premier-league-2016/engine/records/team/match_results.html?id=2016;trophy=118;type=season']

defaultTeamRating = 100.0
ft20MatchNum = 0 #661

# loop through ft20 matches
for x in range(len(relativeURLs)):
    # load cricinfo annual match list    
    yearURL = 'http://stats.espncricinfo.com' + relativeURLs[x]
    yearPage = requests.get(yearURL)
    yearTree = html.fromstring(yearPage.text)

    data1 = yearTree.xpath('//a[@class="data-link"]/text()')
    data2 = yearTree.xpath('//td[@nowrap="nowrap"]/text()')
    links = yearTree.xpath('//a[@class="data-link"]/@href')
        
    scoreLinks = []
    for j in range(0, len(links)):
        if 'match' in links[j]: scoreLinks.append(links[j])
    ft20Num = len(data2) / 2

    i = 0
    matchCount = 0
    teams1 = []
    teams2 = []
    grounds = []
    results = []
    while (i < len(data1)):
        team1 = data1[i]
        team2 = data1[i+1]
        team1 = teamNameChange[team1] if team1 in teamNameChange.keys() else team1
        team2 = teamNameChange[team2] if team2 in teamNameChange.keys() else team2    
        teams1.append(team1)
        teams2.append(team2)        
        if data1[i] in data1[i+2] or data1[i+1] in data1[i+2]:
            result = data1[i+2]
            result = teamNameChange[result] if result in teamNameChange.keys() else result
            results.append(result)            
            grounds.append(data1[i+3])
            i = i + 5
        else:
            results.append('Tie/NR')
            result = 'Tie/NR'
            grounds.append(data1[i+2])
            i = i + 4
        
        team1LiveRating = {}
        c.execute('select rating from teamFT20Live where team=? order by ft20TeamId desc', (team1, ))
        team1LiveRating = c.fetchone()
        if team1LiveRating is None:
            team1LiveRating = defaultTeamRating
        else:
            team1LiveRating = team1LiveRating[0]
            
        team2LiveRating = {}        
        c.execute('select rating from teamFT20Live where team=? order by ft20TeamId desc', (team2, ))
        team2LiveRating = c.fetchone()
        if team2LiveRating is None:
            team2LiveRating = defaultTeamRating
        else:
            team2LiveRating = team2LiveRating[0]
        
        if (result == team1):
            team1LiveRating = team1LiveRating + (team2LiveRating / team1LiveRating) * 3
            team2LiveRating = team2LiveRating - (team2LiveRating / team1LiveRating) * 3
        elif (result == team2):
            team1LiveRating = team1LiveRating - (team1LiveRating / team2LiveRating) * 3
            team2LiveRating = team2LiveRating + (team1LiveRating / team2LiveRating) * 3
        else:
            if (team1LiveRating > team2LiveRating):
                team1LiveRating = team1LiveRating - (team1LiveRating / team2LiveRating) * 1.5
                team2LiveRating = team2LiveRating + (team1LiveRating / team2LiveRating) * 1.5
            elif (team1LiveRating < team2LiveRating):
                team1LiveRating = team1LiveRating + (team2LiveRating / team1LiveRating) * 1.5
                team2LiveRating = team2LiveRating - (team2LiveRating / team1LiveRating) * 1.5         
        
        ft20MatchId = ft20MatchNum + (matchCount+1)
        ft20Team1Id = `ft20MatchId` + '1'
        ft20Team2Id = `ft20MatchId` + '2'
        c.execute('insert or ignore into teamFT20Live (ft20TeamId, startDate, team, opposition, ground, result, scoreLink, rating) values (?, ?, ?, ?, ?, ?, ?, ?)',
                  (ft20Team1Id, None, team1, team2, None, result, None, team1LiveRating))
        c.execute('insert or ignore into teamFT20Live (ft20TeamId, startDate, team, opposition, ground, result, scoreLink, rating) values (?, ?, ?, ?, ?, ?, ?, ?)',
                  (ft20Team2Id, None, team2, team1, None, result, None, team2LiveRating))
        conn.commit()
        matchCount = matchCount + 1
 
    startDates = {}
    for i in range(0, ft20Num):
        margin = data2[2*i]
        startDate = data2[2*i+1]
        month = startDate.split()[0]
        year = startDate.split()[len(startDate.split())-1]
        day = startDate.split()[1].split('-')[0]
        day = day.split(',')[0]
        day = '0' + day if int(day) < 10 else day    
        startDate = year + month2Num[month] + day
        startDates[i] = startDate
        ft20MatchId = ft20MatchNum + (i+1)
        print 'Dumping details for ft20 #'+`ft20MatchId`+' '+teams1[i]+' vs '+teams2[i]+', startDate: '+startDate+', result: '+results[i]+', margin: '+margin+', scoreLink: '+scoreLinks[i]+', ground: '+grounds[i]
        c.execute('insert or ignore into ft20Info (ft20Id, startDate, team1, team2, ground, result, margin, scoreLink) values (?, ?, ?, ?, ?, ?, ?, ?)',
                  (ft20MatchId, startDate, teams1[i], teams2[i], grounds[i], results[i], margin, scoreLinks[i]))
        conn.commit()
        
    for i in range(0, ft20Num):
       ft20MatchId = ft20MatchNum + (i+1)
       ft20Team1Id = `ft20MatchId` + '1'
       ft20Team2Id = `ft20MatchId` + '2'
       c.execute('update teamFT20Live set startDate=?,ground=?,scoreLink=? where ft20TeamId=?', (startDates[i], grounds[i], scoreLinks[i], ft20Team1Id))
       c.execute('update teamFT20Live set startDate=?,ground=?,scoreLink=? where ft20TeamId=?', (startDates[i], grounds[i], scoreLinks[i], ft20Team2Id))
       conn.commit()
    ft20MatchNum = ft20MatchNum + ft20Num    
       
spans = ['2008-2099', '2008-2010', '2011-2014']
c.execute('select distinct team from teamFT20Live')
for team in c.fetchall():
    for span in spans:
        startSpan = span.split('-')[0] + "0000"
        endSpan = span.split('-')[1] + "9999"
        c.execute('select ft20TeamId, result, rating from teamFT20Live where team=? and startDate>? and startDate<?',(team[0], startSpan, endSpan))
        ft20s = 0
        rating = 0.0
        firstFT20 = 99999
        lastFT20 = 0
        wins = 0
        ties = 0
        losses = 0
        for teamMatch in c.fetchall():
            ft20Id = int((`teamMatch[0]`)[0:-1])
            if ft20Id < firstFT20: firstFT20 = ft20Id
            if ft20Id > lastFT20: lastFT20 = ft20Id
            ft20s += 1
            if teamMatch[1] == team[0]:
                wins += 1
            elif teamMatch[1] == "Tie/NR":
                ties += 1
            else: losses += 1
            rating = rating + teamMatch[2]
        rating = rating / ft20s if ft20s > 0 else None
        if ft20s == 0:
            continue
        winPct = 100.0 * wins / ft20s
        # discount rating for those that have played <20 ft20s
        if ft20s < 20 and ft20s >= 10 and rating != None: rating = rating * math.exp(-float(20-ft20s)/100)
        if ft20s < 10 and ft20s >= 5  and rating != None: rating = rating * math.exp(-float(10-ft20s)/50)
        if ft20s < 5 and rating != None: rating = rating * math.exp(-float(5-ft20s)/25)            
        
        c.execute('select startDate from ft20Info where ft20Id=?',(firstFT20, ))
        startDate = c.fetchone()
        if startDate != None: startDate = startDate[0]
        c.execute('select startDate from ft20Info where ft20Id=?',(lastFT20, ))
        endDate = c.fetchone()
        if endDate != None: endDate = endDate[0]
        print team[0] + ' ' + `startDate`+ ' ' + `endDate` + ' ' + `ft20s` + ' ' + `wins` + ' ' + `ties` + ' ' + `losses` + ' ' + `winPct` + ' '+ `rating`
        teamSpan = team[0] + "_" + span
        c.execute('''insert or ignore into teamFT20Overall (teamSpan, startDate, endDate, span, team, ft20s, wins, ties, losses, winPct, rating)
                  values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (teamSpan, startDate, endDate, span, team[0], ft20s, wins, ties, losses, winPct, rating))
        conn.commit()
conn.close()
elapsed = (time.clock() - start)
print 'Time elapsed: ' + `elapsed` + 'sec'
#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
conn = sqlite3.connect('ccr.db')

c = conn.cursor()
c.execute('drop table retiredPlayers')
c.execute('create table retiredPlayers (playerId integer unique, retireTest integer)')

# for row in c.execute('select playerId, max(testId) from battingTestInnings group by playerId'):
#       print row

playerMaxTest = {}
c.execute('select playerId, max(testId) from battingTestInnings group by playerId')
for batsmanLastTest in c.fetchall():
    pid = batsmanLastTest[0]
    lastTestId = batsmanLastTest[1]
    playerMaxTest[pid] = lastTestId

c.execute('select playerId, max(testId) from bowlingTestInnings group by playerId')
for bowlerLastTest in c.fetchall():
    pid = bowlerLastTest[0]
    lastTestId = bowlerLastTest[1]
    if pid in playerMaxTest:
        if lastTestId > playerMaxTest[pid]:
            playerMaxTest[pid] = lastTestId
    else:
        playerMaxTest[pid] = lastTestId

for playerId in playerMaxTest:
    if playerMaxTest[playerId] < 2156: # 01/03/2015
        print `playerId` + ' ' + `playerMaxTest[playerId]`
        c.execute('insert or replace into retiredPlayers(playerId, retireTest) values (?, ?)',
                (playerId, playerMaxTest[playerId]))

c.execute('insert into retiredPlayers values (11561, 2156)')
c.execute('insert into retiredPlayers values (101423, 2177)')
c.execute('insert into retiredPlayers values (14779, 2178)')
c.execute('insert into retiredPlayers values (9159, 2178)')
c.execute('insert into retiredPlayers values (12069, 2187)')
c.execute('insert into retiredPlayers values (75477, 2202)')
c.execute('insert into retiredPlayers values (16241, 2233)')


# c.execute('''create table battingTestInnings (inningsId integer unique, playerId integer, player text, testId integer, innings integer, position integer, dismissalInfo text, notOut integer, runs integer,
#           minutes integer, balls integer, fours integer, sixes integer, totalPct real, bowlingRating real, entryRuns integer, entryWkts integer, wicketsAtCrease integer, homeAway integer, status integer,
#           result integer, rating real)''')
# c.execute('''create table bowlingTestInnings (inningsId integer unique, playerId integer, player text, testId integer, innings integer, position integer, wkts integer, battingRating real, wktsRating real,
#           balls integer, maidens integer, runs integer, homeAway integer, status integer, result integer, rating real)''')
conn.commit()
conn.close()

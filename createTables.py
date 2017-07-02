#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
conn = sqlite3.connect('ccr.db')

c = conn.cursor()
#c.execute('drop table detailsTestInnings')
#c.execute('drop table fowTestInnings')
#c.execute('drop table playerInfo')
#c.execute('drop table retiredPlayers')
# c.execute('drop table battingTestLive')
# c.execute('drop table bowlingTestLive')
# c.execute('drop table allRoundTestLive')
#c.execute('drop table battingTestInnings')
#c.execute('drop table bowlingTestInnings')
#c.execute('drop table allRoundTestMatch')
# c.execute('drop table overComparisonTest')
# c.execute('drop table commentaryEventTest')
c.execute('drop table fieldingEventTest')
c.execute('drop table fieldingTestMatch')
c.execute('drop table fieldingTestLive')
#
#c.execute('create table playerInfo (playerId integer unique, player text, fullName text, country text, cid integer)')
#c.execute('create table retiredPlayers (playerId integer unique, retireDate text)')
# c.execute('create table battingTestLive (inningsId integer unique, startDate text, playerId integer, testId integer, player text, rating real, nextInningsRating real)')
# c.execute('create table bowlingTestLive (inningsId integer unique, startDate text, playerId integer, testId integer, player text, rating real, nextInningsRating real)')
# c.execute('create table allRoundTestLive (matchId integer unique, startDate text, playerId integer, testId integer, player text, rating real, nextTestRating real)')
#c.execute('''create table detailsTestInnings (inningsId integer unique, testId integer, innings integer, batTeam text, bowlTeam text, extras integer, runs integer, balls integer, minutes integer, wickets integer,
#          inningsEndDetail text, batHighInnPct real, batSecHighInnPct real)''')
#c.execute('create table fowTestInnings (fowId integer unique, testId integer, innings integer, runs integer, wicket integer, player text, balls integer)')
# c.execute('''create table battingTestInnings (inningsId integer unique, playerId integer, player text, testId integer, innings integer, position integer, dismissalInfo text, notOut integer, runs integer,
#           minutes integer, balls integer, fours integer, sixes integer, totalPct real, bowlingRating real, entryRuns integer, entryWkts integer, wicketsAtCrease integer, homeAway integer, status integer,
#           result integer, rating real)''')
# c.execute('''create table bowlingTestInnings (inningsId integer unique, playerId integer, player text, testId integer, innings integer, position integer, wkts integer, battingRating real, wktsRating real,
#           balls integer, maidens integer, runs integer, homeAway integer, status integer, result integer, rating real)''')
# c.execute('''create table allRoundTestMatch (matchId integer unique, playerId integer, player text, testId integer, runs1 integer, notOut1 integer, runs2 integer, notOut2 integer,
#            wkts1 integer, bowlRuns1 integer, wkts2 integer, bowlRuns2 integer, battingRating real, bowlingRating real, rating)''')
# c.execute('''create table overComparisonTest (ocId integer unique, testId integer, innings integer, teamBat text, overs integer, runs integer, wkts integer, runsReq integer, ballsRem integer, day integer,
#           winOdds real, drawOdds real, adjWinOdds real, adjDrawOdds real, result integer)''')
# c.execute('''create table commentaryEventTest (eventId integer unique, testId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, commentary text)''')
c.execute('''create table fieldingEventTest (eventId integer unique, testId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, fielder text, fielderId integer,
             droppedCatch integer, misfield integer, missedStumping integer, greatCatch integer, directHit integer, greatFielding integer, runsSaved integer, commentary text)''')
c.execute('''create table fieldingTestMatch (matchId integer unique, playerId integer, player text, testId integer, keeper integer, catches integer, droppedCatches integer, misfields integer, stumpings integer, missedStumpings integer,
             greatCatches integer, directHits integer, greatSaves integer, runsSaved integer, rating real)''')
c.execute('''create table fieldingTestLive (matchId integer unique, startDate text, playerId integer, testId integer, player text, rating real)''')
conn.commit()
conn.close()

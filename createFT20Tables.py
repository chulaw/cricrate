#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
conn = sqlite3.connect('ccrFT20.db')

c = conn.cursor()
# c.execute('drop table detailsFT20Innings')
# c.execute('drop table fowFT20Innings')
# c.execute('drop table playerInfo')
# c.execute('drop table battingFT20Live')
# c.execute('drop table bowlingFT20Live')
# c.execute('drop table allRoundFT20Live')
# c.execute('drop table battingFT20Innings')
# c.execute('drop table bowlingFT20Innings')
# c.execute('drop table allRoundFT20Match')
# c.execute('drop table winSharesFT20Match')
# c.execute('drop table winSharesFT20Live')
#c.execute('drop table overComparison')
# c.execute('drop table commentaryEventFT20')
c.execute('drop table fieldingEventFT20')
c.execute('drop table fieldingFT20Match')
c.execute('drop table fieldingFT20Live')

# c.execute('create table playerInfo (playerId integer unique, player text, fullName text, teams text, cid integer)')
# c.execute('''create table detailsFT20Innings (inningsId integer unique, ft20Id integer, innings integer, batTeam text, bowlTeam text, extras integer, runs integer, balls integer, minutes integer, wickets integer,
#           inningsEndDetail text)''')
# c.execute('create table fowFT20Innings (fowId integer unique, ft20Id integer, innings integer, runs integer, wicket integer, player text, balls integer)')
# c.execute('create table battingFT20Live (inningsId integer unique, startDate text, playerId integer, ft20Id integer, player text, rating real, nextInningsRating real)')
# c.execute('create table bowlingFT20Live (inningsId integer unique, startDate text, playerId integer, ft20Id integer, player text, rating real, nextInningsRating real)')
# c.execute('create table allRoundFT20Live (matchId integer unique, startDate text, playerId integer, ft20Id integer, player text, rating real, nextFT20Rating real)')
# c.execute('''create table battingFT20Innings (inningsId integer unique, playerId integer, player text, ft20Id integer, innings integer, position integer, dismissalInfo text, notOut integer, runs integer,
#          minutes integer, balls integer, fours integer, sixes integer, totalPct real, bowlingRating real, entryRuns integer, entryWkts integer, wicketsAtCrease integer, status integer,
#          result integer, rating real)''')
# c.execute('''create table bowlingFT20Innings (inningsId integer unique, playerId integer, player text, ft20Id integer, innings integer, position integer, wkts integer, battingRating real, wktsRating real,
#           balls integer, maidens integer, runs integer, status integer, result integer, rating real)''')
# c.execute('''create table allRoundFT20Match (matchId integer unique, playerId integer, player text, ft20Id integer, runs integer, notOut integer, wkts integer, bowlRuns integer,
#           battingRating real, bowlingRating real, rating)''')
# c.execute('''create table overComparisonFT20 (ocId integer unique, t20Id integer, innings integer, teamBat text, overs integer, runs integer, wkts integer, overRuns integer, runRate real, reqRate real,
#            runsReq integer, ballsRem integer, matchOdds real, adjMatchOdds1 real, adjMatchOdds2 real, result integer)''')
# c.execute('''create table commentaryEventFT20 (eventId integer unique, ft20Id integer, bowler text, batsman text, bowlerId integer, batsmanId integer, commentary text)''')
c.execute('''create table fieldingEventFT20 (eventId integer unique, ft20Id integer, bowler text, batsman text, bowlerId integer, batsmanId integer, fielder text, fielderId integer,
              catch integer, droppedCatch integer, misfield integer, stumping integer, missedStumping integer, greatCatch integer, directHit integer, greatFielding integer, runsSaved integer, commentary text)''')
c.execute('''create table fieldingFT20Match (matchId integer unique, playerId integer, player text, ft20Id integer, keeper integer, catches integer, droppedCatches integer, misfields integer, stumpings integer, missedStumpings integer,
              greatCatches integer, directHits integer, greatSaves integer, runsSaved integer, rating real)''')
c.execute('''create table fieldingFT20Live (matchId integer unique, startDate text, playerId integer, ft20Id integer, player text, rating real)''')
# c.execute('''create table winSharesFT20Match (matchId integer unique, playerId integer, player text, ft20Id integer, battingWS real, bowlingWS real, fieldingWS real, totalWS real, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS)''')
# c.execute('''create table winSharesFT20Live (matchId integer unique, startDate text, playerId integer, ft20Id integer, player text, battingRating real, bowlingRating real, fieldingRating real, totalRating real)''')
conn.commit()
conn.close()
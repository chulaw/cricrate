#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
conn = sqlite3.connect('ccrT20I.db')

c = conn.cursor()
# c.execute('drop table detailsT20IInnings')
# c.execute('drop table fowT20IInnings')
# c.execute('drop table playerInfo')
# c.execute('drop table battingT20ILive')
# c.execute('drop table bowlingT20ILive')
# c.execute('drop table allRoundT20ILive')
# c.execute('drop table battingT20IInnings')
# c.execute('drop table bowlingT20IInnings')
# c.execute('drop table allRoundT20IMatch')
# c.execute('drop table retiredPlayers')
c.execute('drop table overComparison')
c.execute('drop table winSharesT20IMatch')
c.execute('drop table winSharesT20ILive')
# c.execute('drop table commentaryEventT20I')
# c.execute('drop table fieldingEventT20I')
# c.execute('drop table fieldingT20IMatch')
# c.execute('drop table fieldingT20ILive')

# c.execute('create table playerInfo (playerId integer unique, player text, fullName text, country text, cid integer)')
# c.execute('create table battingT20ILive (inningsId integer unique, startDate text, playerId integer, t20iId integer, player text, rating real, nextInningsRating real)')
# c.execute('create table bowlingT20ILive (inningsId integer unique, startDate text, playerId integer, t20iId integer, player text, rating real, nextInningsRating real)')
# c.execute('create table allRoundT20ILive (matchId integer unique, startDate text, playerId integer, t20iId integer, player text, rating real, nextT20IRating real)')
# c.execute('''create table detailsT20IInnings (inningsId integer unique, t20iId integer, innings integer, batTeam text, bowlTeam text, extras integer, runs integer, balls integer, minutes integer, wickets integer,
#           inningsEndDetail text)''')
# c.execute('create table fowT20IInnings (fowId integer unique, t20iId integer, innings integer, runs integer, wicket integer, player text, balls integer)')
# c.execute('''create table battingT20IInnings (inningsId integer unique, playerId integer, player text, t20iId integer, innings integer, position integer, dismissalInfo text, notOut integer, runs integer,
#          minutes integer, balls integer, fours integer, sixes integer, totalPct real, bowlingRating real, entryRuns integer, entryWkts integer, wicketsAtCrease integer, homeAway integer, status integer,
#          result integer, rating real)''')
# c.execute('''create table bowlingT20IInnings (inningsId integer unique, playerId integer, player text, t20iId integer, innings integer, position integer, wkts integer, battingRating real, wktsRating real,
#           balls integer, maidens integer, runs integer, homeAway integer, status integer, result integer, rating real)''')
# c.execute('''create table allRoundT20IMatch (matchId integer unique, playerId integer, player text, t20iId integer, runs integer, notOut integer, wkts integer, bowlRuns integer,
#           battingRating real, bowlingRating real, rating)''')
# c.execute('''create table overComparison (ocId integer unique, t20Id integer, innings integer, teamBat text, overs integer, runs integer, wkts integer, overRuns integer, runRate real, reqRate real,
#           runsReq integer, ballsRem integer, matchOdds real, adjMatchOdds1 real, adjMatchOdds2 real, result integer)''')
# c.execute('''create table commentaryEventT20I (eventId integer unique, t20iId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, commentary text)''')
# c.execute('''create table fieldingEventT20I (eventId integer unique, t20iId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, fielder text, fielderId integer,
#               catch integer, droppedCatch integer, misfield integer, stumping integer, missedStumping integer, greatCatch integer, directHit integer, greatFielding integer, runsSaved integer, commentary text)''')
# c.execute('''create table fieldingT20IMatch (matchId integer unique, playerId integer, player text, t20iId integer, keeper integer, catches integer, droppedCatches integer, misfields integer, stumpings integer, missedStumpings integer,
#               greatCatches integer, directHits integer, greatSaves integer, runsSaved integer, rating real)''')
# c.execute('''create table fieldingT20ILive (matchId integer unique, startDate text, playerId integer, t20iId integer, player text, rating real)''')
c.execute('''create table winSharesT20IMatch (matchId integer unique, playerId integer, player text, t20iId integer, battingWS real, bowlingWS real, fieldingWS real, totalWS real, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS)''')
c.execute('''create table winSharesT20ILive (matchId integer unique, startDate text, playerId integer, t20iId integer, player text, battingRating real, bowlingRating real, fieldingRating real, totalRating real)''')
# c.execute('create table retiredPlayers (playerId integer unique)')
c.execute('ATTACH DATABASE "ccrFT20.db" AS ccrFT20DB')
c.execute('CREATE TABLE overComparison AS SELECT * FROM ccrFT20DB.overComparison')
conn.commit()
conn.close()
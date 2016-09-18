#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
conn = sqlite3.connect('ccrODI.db')

c = conn.cursor()
# c.execute('drop table detailsODIInnings')
# c.execute('drop table fowODIInnings')
# c.execute('drop table playerInfo')
# c.execute('drop table retiredPlayers')
# c.execute('drop table battingODILive')
# c.execute('drop table bowlingODILive')
# c.execute('drop table allRoundODILive')
# c.execute('drop table battingODIInnings')
# c.execute('drop table bowlingODIInnings')
#c.execute('drop table allRoundODIMatch')
c.execute('drop table winSharesODIMatch')
c.execute('drop table winSharesODILive')
# c.execute('drop table overComparisonODI')
# c.execute('drop table commentaryEventODI')
# c.execute('drop table fieldingEventODI')
# c.execute('drop table fieldingODIMatch')
# c.execute('drop table fieldingODILive')

# c.execute('create table playerInfo (playerId integer unique, player text, fullName text, country text, cid integer)')
# c.execute('create table retiredPlayers (playerId integer unique)')
# c.execute('''create table detailsODIInnings (inningsId integer unique, odiId integer, innings integer, batTeam text, bowlTeam text, extras integer, runs integer, balls integer, minutes integer, wickets integer,
#           inningsEndDetail text)''')
# c.execute('create table fowODIInnings (fowId integer unique, odiId integer, innings integer, runs integer, wicket integer, player text, balls integer)')
# c.execute('create table battingODILive (inningsId integer unique, startDate text, playerId integer, odiId integer, player text, rating real, nextInningsRating real)')
# c.execute('create table bowlingODILive (inningsId integer unique, startDate text, playerId integer, odiId integer, player text, rating real, nextInningsRating real)')
# c.execute('create table allRoundODILive (matchId integer unique, startDate text, playerId integer, odiId integer, player text, rating real, nextODIRating real)')
# c.execute('''create table battingODIInnings (inningsId integer unique, playerId integer, player text, odiId integer, innings integer, position integer, dismissalInfo text, notOut integer, runs integer,
#          minutes integer, balls integer, fours integer, sixes integer, totalPct real, bowlingRating real, entryRuns integer, entryWkts integer, wicketsAtCrease integer, homeAway integer, status integer,
#          result integer, rating real)''')
# c.execute('''create table bowlingODIInnings (inningsId integer unique, playerId integer, player text, odiId integer, innings integer, position integer, wkts integer, battingRating real, wktsRating real,
#           balls integer, maidens integer, runs integer, homeAway integer, status integer, result integer, rating real)''')
# c.execute('''create table allRoundODIMatch (matchId integer unique, playerId integer, player text, odiId integer, runs integer, notOut integer, wkts integer, bowlRuns integer
#            , battingRating real, bowlingRating real, rating)''')
# c.execute('''create table overComparisonODI (ocId integer unique, odiId integer, innings integer, teamBat text, overs integer, runs integer, wkts integer, overRuns integer, runRate real, reqRate real,
#            runsReq integer, ballsRem integer, matchOdds real, adjMatchOdds1 real, adjMatchOdds2 real, result integer)''')
# c.execute('''create table commentaryEventODI (eventId integer unique, odiId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, commentary text)''')
# c.execute('''create table fieldingEventODI (eventId integer unique, odiId integer, bowler text, batsman text, bowlerId integer, batsmanId integer, fielder text, fielderId integer,
#              catch integer, droppedCatch integer, misfield integer, stumping integer, missedStumping integer, greatCatch integer, directHit integer, greatFielding integer, runsSaved integer, commentary text)''')
# c.execute('''create table fieldingODIMatch (matchId integer unique, playerId integer, player text, odiId integer, keeper integer, catches integer, droppedCatches integer, misfields integer, stumpings integer, missedStumpings integer,
#              greatCatches integer, directHits integer, greatSaves integer, runsSaved integer, rating real)''')
# c.execute('''create table fieldingODILive (matchId integer unique, startDate text, playerId integer, odiId integer, player text, rating real)''')
c.execute('''create table winSharesODIMatch (matchId integer unique, playerId integer, player text, odiId integer, battingWS real, bowlingWS real, fieldingWS real, totalWS real, battingAdjWS, bowlingAdjWS, fieldingAdjWS, totalAdjWS)''')
c.execute('''create table winSharesODILive (matchId integer unique, startDate text, playerId integer, odiId integer, player text, battingRating real, bowlingRating real, fieldingRating real, totalRating real)''')
conn.commit()
conn.close()
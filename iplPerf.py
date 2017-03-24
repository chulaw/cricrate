#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
import math
import datetime
import csv

def dumpPerf(liveTable, currentTable, innMat, matchType):
    pid = {}
    playerNumInns = {}
    playerBatting = {}
    playerBowling = {}
    playerFielding = {}
    playerTotal = {}
    playerRating = {}
    if "winShares" in liveTable:
        f = open('iplPerfWR.csv','a')
        f.write("Player,MatchDate,Batting,Bowling,Fielding,Total\n")
        currentTableStr = "select p.player, count(b.matchId), avg(b.battingAdjWS), avg(b.bowlingAdjWS), avg(b.fieldingAdjWS), avg(b.totalAdjWS) from "+liveTable+" b, playerInfo p where p.playerId=b.playerId and b.ft20Id>782 and b.ft20Id<843 group by p.player"
    else:
        f = open('iplPerf'+liveTable+'.csv','a')
        f.write("Player,NumInns,AvgRating\n")
        if "fielding" in liveTable:
            currentTableStr = "select p.player, count(b.matchId), avg(b.rating) from "+liveTable+" b, playerInfo p where p.playerId=b.playerId and b.ft20Id>782 and b.ft20Id<843 group by p.player"
        else:
            currentTableStr = "select p.player, count(b.inningsId), avg(b.rating) from "+liveTable+" b, playerInfo p where p.playerId=b.playerId and b.ft20Id>782 and b.ft20Id<843 group by p.player"
    for row in c.execute(currentTableStr):
        player = row[0]
        if "winShares" in liveTable:
            playerNumInns[player] = row[1]
            playerBatting[player] = row[2]
            playerBowling[player] = row[3]
            playerFielding[player] = row[4]
            playerTotal[player] = row[5]
        else:
            playerNumInns[player] = row[1]
            playerRating[player] = row[2]

    if "winShares" in liveTable:
        for p in playerNumInns:
            f.write(p + ',' + `playerNumInns[p]` + ',' + `round(playerBatting[p], 3)` + ',' + `round(playerBowling[p], 3)` + ',' + `round(playerFielding[p], 3)` + ',' + `round(playerTotal[p], 3)` + '\n')
    else:
        for p in playerNumInns:
            f.write(p + ',' + `playerNumInns[p]` + ',' + `round(playerRating[p], 0)` + '\n')
    f.close()

conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()
# c.execute('drop table teamFT20Current')
# # c.execute('drop table battingFT20Current')
# # c.execute('drop table bowlingFT20Current')
# # c.execute('drop table allRoundFT20Current')
# # c.execute('drop table fieldingFT20Current')
# c.execute('drop table winSharesFT20Current')
# # c.execute('drop table battingFT20CurrentAllTime')
# # c.execute('drop table bowlingFT20CurrentAllTime')
# # c.execute('drop table allRoundFT20CurrentAllTime')
# # c.execute('drop table fieldingFT20CurrentAllTime')
# c.execute('drop table winSharesFT20CurrentAllTime')
# c.execute('''create table teamFT20Current (team text unique, startDate text, rankDiff integer, rank integer, homeRating real, awayRating real, rating real, bestCurrentRating text)''')
# # c.execute('''create table battingFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # c.execute('''create table bowlingFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # c.execute('''create table allRoundFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # c.execute('''create table fieldingFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table winSharesFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # c.execute('''create table battingFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # c.execute('''create table bowlingFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # c.execute('''create table allRoundFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # c.execute('''create table fieldingFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table winSharesFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # # # #
# print("Generating current table for ft20 teams...\n")
# dumpCurrentTeam("teamFT20Live","teamFT20Current","ft20")
print("Generating current table for ft20 batting...\n")
dumpPerf("battingFT20Innings","battingFT20Current","innings","ft20")
print("Generating current table for ft20 bowling...\n")
dumpPerf("bowlingFT20Innings","bowlingFT20Current","innings","ft20")
print("Generating current table for ft20 allRound...\n")
dumpPerf("fieldingFT20Match","fieldingFT20Current","match","ft20")
print("Generating current table for ft20 win shares...\n")
dumpPerf("winSharesFT20Match","winSharesFT20Current","match","ft20")
conn.close()

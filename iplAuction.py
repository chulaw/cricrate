#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
import math
import datetime
import csv

today = datetime.datetime.now()
date12mAgo = datetime.datetime.now() + datetime.timedelta(days=-365)
date6mAgo = datetime.datetime.now() + datetime.timedelta(days=-180)
date1mAgo = datetime.datetime.now() + datetime.timedelta(days=-30)
date12mAgo = date12mAgo.strftime('%Y%m%d')
date6mAgo = date6mAgo.strftime('%Y%m%d')
date1mAgo = date1mAgo.strftime('%Y%m%d')

def dumpCurrent(liveTable, currentTable, innMat, matchType):
    pid = {}
    playerMatchDate = {}
    playerBatting = {}
    playerBowling = {}
    playerFielding = {}
    playerTotal = {}
    playerRating = {}
    if "winShares" in liveTable:
        f = open('iplAuctionWR.csv','a')
        f.write("Player,MatchDate,Batting,Bowling,Fielding,Total\n")
        currentTableStr = "select p.player, b.startDate, b.battingRating, b.bowlingRating, b.fieldingRating, b.totalRating from "+liveTable+" b, playerInfo p  where p.playerId=b.playerId and b.startDate>'20150206' and b.startDate<'20160206' order by b.totalRating asc"
    else:
        f = open('iplAuction'+liveTable+'.csv','a')
        f.write("Player,MatchDate,Rating\n")
        currentTableStr = "select p.player, b.startDate, b.rating from "+liveTable+" b, playerInfo p  where p.playerId=b.playerId and b.startDate>'20150206' and b.startDate<'20160206' order by b.rating asc"
    for row in c.execute(currentTableStr):
        player = row[0]
        if "winShares" in liveTable:
            if player in playerMatchDate:
                if playerMatchDate[player] < row[1]:
                    playerMatchDate[player] = row[1]
                    playerBatting[player] = row[2]
                    playerBowling[player] = row[3]
                    playerFielding[player] = row[4]
                    playerTotal[player] = row[5]
            else:
                playerMatchDate[player] = row[1]
                playerBatting[player] = row[2]
                playerBowling[player] = row[3]
                playerFielding[player] = row[4]
                playerTotal[player] = row[5]
        else:
            if player in playerMatchDate:
                if playerMatchDate[player] < row[1]:
                    playerMatchDate[player] = row[1]
                    playerRating[player] = row[2]
            else:
                playerMatchDate[player] = row[1]
                playerRating[player] = row[2]

    if "winShares" in liveTable:
        for p in playerMatchDate:
            f.write(p + ',' + playerMatchDate[p] + ',' + `round(playerBatting[p], 3)` + ',' + `round(playerBowling[p], 3)` + ',' + `round(playerFielding[p], 3)` + ',' + `round(playerTotal[p], 3)` + '\n')
    else:
        for p in playerMatchDate:
            f.write(p + ',' + playerMatchDate[p] + ',' + `round(playerRating[p], 0)` + '\n')
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
dumpCurrent("battingFT20Live","battingFT20Current","innings","ft20")
print("Generating current table for ft20 bowling...\n")
dumpCurrent("bowlingFT20Live","bowlingFT20Current","innings","ft20")
print("Generating current table for ft20 allRound...\n")
dumpCurrent("fieldingFT20Live","fieldingFT20Current","match","ft20")
print("Generating current table for ft20 win shares...\n")
dumpCurrent("winSharesFT20Live","winSharesFT20Current","match","ft20")
conn.close()

#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
import math
import datetime

today = datetime.datetime.now()
date12mAgo = datetime.datetime.now() + datetime.timedelta(days=-365)
date6mAgo = datetime.datetime.now() + datetime.timedelta(days=-180)
date1mAgo = datetime.datetime.now() + datetime.timedelta(days=-30)
date12mAgo = date12mAgo.strftime('%Y%m%d')
date6mAgo = date6mAgo.strftime('%Y%m%d')
date1mAgo = date1mAgo.strftime('%Y%m%d')

def dumpCurrentTeam(liveTable, currentTable, matchType):
    bestCurrent = {}
    bestCurrentStr = "select t.team, t.startDate, t.rating from "+liveTable+" t inner join (select team, max(rating) maxRating from "+liveTable+" group by team) as tt on tt.team=t.team and tt.maxRating=t.rating order by t.rating desc"
    for row in c.execute(bestCurrentStr):
        team = row[0]
        startDate = row[1]
        dateMod = startDate[0:4]+"-"+startDate[4:6]+"-"+startDate[6:8]
        rating = int(round(row[2]))
        bestCurrent[team] = repr(rating)+", "+dateMod

    pastRank = {}
    k = 1
    pastRankStr = "select t.team from "+liveTable+" t inner join(select team, max("+matchType+"TeamId) maxMatchId from "+liveTable+" where startDate<'"+date1mAgo+"' group by team) tt on t.team = tt.team and t."+matchType+"TeamId = tt.maxMatchId and t.startDate>'"+date6mAgo+"' and t.startDate<'"+date1mAgo+"' order by t.rating desc"
    for row in c.execute(pastRankStr):
        pastRank[row[0]] = k
        k = k + 1

    k = 1
    rankDiff = {}
    rank = {}
    rating = {}
    homeRating = {}
    awayRating = {}
    startDate = {}
    if matchType == "ft20":
        currentTableStr = "select t.team, t.rating, t.rating, t.rating, t.startDate from "+liveTable+" t inner join(select team, max("+matchType+"TeamId) maxMatchId from "+liveTable+" group by team) tt on t.team = tt.team and t."+matchType+"TeamId = tt.maxMatchId and t.startDate>'"+date12mAgo+"' order by t.rating desc"
    else:
        currentTableStr = "select t.team, t.homeRating, t.awayRating, t.rating, t.startDate from "+liveTable+" t inner join(select team, max("+matchType+"TeamId) maxMatchId from "+liveTable+" group by team) tt on t.team = tt.team and t."+matchType+"TeamId = tt.maxMatchId and t.startDate>'"+date12mAgo+"' order by t.rating desc"
    for row in c.execute(currentTableStr):
        rankDiff[row[0]] = pastRank[row[0]] - k if row[0] in pastRank else 0
        rank[row[0]] = k
        homeRating[row[0]] = row[1]
        awayRating[row[0]] = row[2]
        rating[row[0]] = row[3]
        startDate[row[0]] = row[4]
        k = k + 1

    for team in rank:
        print(repr(team)+' '+repr(rankDiff[team])+' '+repr(rank[team])+' '+repr(rating[team])+' '+repr(bestCurrent[team]))
        c.execute("insert or ignore into "+currentTable+" (team, startDate, rankDiff, rank, homeRating, awayRating, rating, bestCurrentRating) values (?, ?, ?, ?, ?, ?, ?, ?)",
                  (team, startDate[team], rankDiff[team], rank[team], homeRating[team], awayRating[team], rating[team], bestCurrent[team]))
        conn.commit()

def dumpCurrent(liveTable, currentTable, innMat, matchType):
    bestCurrent = {}
    if matchType == "ft20":
        if "winShares" in liveTable:
            bestCurrentStr = "select b.playerId, p.player, t.startDate, p.teams, t.team1, t.team2, b.totalRating from "+liveTable+" b, playerInfo p, "+matchType+"Info t inner join (select playerId, max(totalRating) maxRating from "+liveTable+" group by playerId) as bb on bb.playerId=b.playerId and bb.maxRating=b.totalRating and p.playerId=b.playerId and t."+matchType+"Id=b."+matchType+"Id order by b.totalRating desc"
        else:
            bestCurrentStr = "select b.playerId, b.player, t.startDate, p.teams, t.team1, t.team2, b.rating from "+liveTable+" b, playerInfo p, "+matchType+"Info t inner join (select playerId, max(rating) maxRating from "+liveTable+" group by playerId) as bb on bb.playerId=b.playerId and bb.maxRating=b.rating and p.playerId=b.playerId and t."+matchType+"Id=b."+matchType+"Id order by b.rating desc"
    elif "winShares" in liveTable:
        bestCurrentStr = "select b.playerId, p.player, t.startDate, p.country, t.team1, t.team2, b.totalRating from "+liveTable+" b, playerInfo p, "+matchType+"Info t inner join (select playerId, max(totalRating) maxRating from "+liveTable+" group by playerId) as bb on bb.playerId=b.playerId and bb.maxRating=b.totalRating and p.playerId=b.playerId and t."+matchType+"Id=b."+matchType+"Id order by b.totalRating desc"
    else:
        bestCurrentStr = "select b.playerId, b.player, t.startDate, p.country, t.team1, t.team2, b.rating from "+liveTable+" b, playerInfo p, "+matchType+"Info t inner join (select playerId, max(rating) maxRating from "+liveTable+" group by playerId) as bb on bb.playerId=b.playerId and bb.maxRating=b.rating and p.playerId=b.playerId and t."+matchType+"Id=b."+matchType+"Id order by b.rating desc"
    pidAll = {}
    country = {}
    bestRating = {}
    for row in c.execute(bestCurrentStr):
        pid = row[0]
        startDate = row[2]
        dateMod = startDate[0:4]+"-"+startDate[4:6]+"-"+startDate[6:8]
        opposition = row[4]
        if (row[3] == row[4]):
            opposition = row[5]
        if "winShares" in liveTable:
            rating = round(row[6], 3)
        else:
            rating = int(round(row[6]))
        pidAll[pid] = row[1]
        country[pid] = row[3]
        bestRating[pid] = row[6]
        bestCurrent[pid] = repr(rating)+" vs "+opposition+", "+dateMod
    k = 1
    for playerId in pidAll:
        if matchType == "ft20":
            c.execute("insert or ignore into "+currentTable+"AllTime (playerId, rank, rating, player, teams, bestCurrentRating) values (?, ?, ?, ?, ?, ?)",
                    (playerId, k, bestRating[playerId], pidAll[playerId], country[playerId], bestCurrent[playerId]))
        else:
            c.execute("insert or ignore into "+currentTable+"AllTime (playerId, rank, rating, player, country, bestCurrentRating) values (?, ?, ?, ?, ?, ?)",
                    (playerId, k, bestRating[playerId], pidAll[playerId], country[playerId], bestCurrent[playerId]))
        conn.commit()
        k = k + 1

    pastRank = {}
    k = 1
    if "winShares" in liveTable:
        pastRankStr = "select b.playerId, p.player from "+liveTable+" b, playerInfo p inner join(select playerId, max("+innMat+"Id) maxInningsId from "+liveTable+" where startDate<'"+date1mAgo+"' group by playerId) bb on b.playerId = bb.playerId and p.playerId=b.playerId and b."+innMat+"Id = bb.maxInningsId and b.startDate>'"+date12mAgo+"' and b.startDate<'"+date1mAgo+"' order by b.totalRating desc"
    else:
        pastRankStr = "select b.playerId, b.player from "+liveTable+" b inner join(select playerId, max("+innMat+"Id) maxInningsId from "+liveTable+" where startDate<'"+date1mAgo+"' group by playerId) bb on b.playerId = bb.playerId and b."+innMat+"Id = bb.maxInningsId and b.startDate>'"+date12mAgo+"' and b.startDate<'"+date1mAgo+"' order by b.rating desc"
    for row in c.execute(pastRankStr):
        pastRank[row[0]] = k
        k = k + 1

    k = 1
    pid = {}
    rankDiff = {}
    rank = {}
    rating = {}
    startDate = {}
    if matchType == "ft20":
        if "winShares" in liveTable:
            currentTableStr = "select b.playerId, b.totalRating, p.player, b.startDate from "+liveTable+" b, playerInfo p inner join(select playerId, max("+innMat+"Id) maxInningsId from "+liveTable+" group by playerId) bb on b.playerId = bb.playerId and p.playerId=b.playerId and b."+innMat+"Id = bb.maxInningsId and b.startDate>'"+date6mAgo+"' order by b.totalRating desc"
        else:
            currentTableStr = "select b.playerId, b.rating, b.player, b.startDate from "+liveTable+" b inner join(select playerId, max("+innMat+"Id) maxInningsId from "+liveTable+" group by playerId) bb on b.playerId = bb.playerId and b."+innMat+"Id = bb.maxInningsId and b.startDate>'"+date6mAgo+"' order by b.rating desc"
    else:
        if "winShares" in liveTable:
            currentTableStr = "select b.playerId, b.totalRating, p.player, b.startDate from " + liveTable + " b, playerInfo p inner join(select playerId, max(" + innMat + "Id) maxInningsId from " + liveTable + " group by playerId) bb on b.playerId = bb.playerId and p.playerId=b.playerId and b." + innMat + "Id = bb.maxInningsId and b.startDate>'" + date12mAgo + "' order by b.totalRating desc"
        else:
            currentTableStr = "select b.playerId, b.rating, b.player, b.startDate from " + liveTable + " b inner join(select playerId, max(" + innMat + "Id) maxInningsId from " + liveTable + " group by playerId) bb on b.playerId = bb.playerId and b." + innMat + "Id = bb.maxInningsId and b.startDate>'" + date12mAgo + "' order by b.rating desc"
    for row in c.execute(currentTableStr):
        pid[row[0]] = row[2]
        rankDiff[row[0]] = pastRank[row[0]] - k if row[0] in pastRank else 0
        rank[row[0]] = k
        rating[row[0]] = row[1]
        startDate[row[0]] = row[3]
        k = k + 1

    for playerId in pid:
        #print repr(playerId)+' '+repr(rankDiff[playerId])+' '+repr(rank[playerId])+' '+repr(pid[playerId])+' '+repr(country[playerId])+' '+repr(bestCurrent[playerId])
        if matchType == "ft20":
            c.execute("insert or ignore into "+currentTable+" (playerId, startDate, rankDiff, rank, rating, player, teams, bestCurrentRating) values (?, ?, ?, ?, ?, ?, ?, ?)",
                    (playerId, startDate[playerId], rankDiff[playerId], rank[playerId], rating[playerId], pid[playerId], country[playerId], bestCurrent[playerId]))
        else:
            c.execute("insert or ignore into "+currentTable+" (playerId, startDate, rankDiff, rank, rating, player, country, bestCurrentRating) values (?, ?, ?, ?, ?, ?, ?, ?)",
                    (playerId, startDate[playerId], rankDiff[playerId], rank[playerId], rating[playerId], pid[playerId], country[playerId], bestCurrent[playerId]))
    conn.commit()

# conn = sqlite3.connect('ccr.db')
# c = conn.cursor()
# c.execute('drop table teamTestCurrent')
# c.execute('drop table battingTestCurrent')
# c.execute('drop table bowlingTestCurrent')
# c.execute('drop table allRoundTestCurrent')
# c.execute('drop table fieldingTestCurrent')
# c.execute('drop table battingTestCurrentAllTime')
# c.execute('drop table bowlingTestCurrentAllTime')
# c.execute('drop table allRoundTestCurrentAllTime')
# c.execute('drop table fieldingTestCurrentAllTime')
# c.execute('''create table teamTestCurrent (team text unique, startDate text, rankDiff integer, rank integer, homeRating real, awayRating real, rating real, bestCurrentRating text)''')
# c.execute('''create table battingTestCurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table bowlingTestCurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table allRoundTestCurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table fieldingTestCurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table battingTestCurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table bowlingTestCurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table allRoundTestCurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table fieldingTestCurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
#
# print("Generating current table for test teams...\n")
# dumpCurrentTeam("teamTestLive","teamTestCurrent","test")
# print("Generating current table for test batting...\n")
# dumpCurrent("battingTestLive","battingTestCurrent","innings","test")
# print("Generating current table for test bowling...\n")
# dumpCurrent("bowlingTestLive","bowlingTestCurrent","innings","test")
# print("Generating current table for test allRound...\n")
# dumpCurrent("allRoundTestLive","allRoundTestCurrent","match","test")
# print("Generating current table for test fielding...\n")
# dumpCurrent("fieldingTestLive","fieldingTestCurrent","match","test")
# conn.close()

conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()
c.execute('drop table teamODICurrent')
c.execute('drop table battingODICurrent')
c.execute('drop table bowlingODICurrent')
c.execute('drop table allRoundODICurrent')
c.execute('drop table fieldingODICurrent')
c.execute('drop table winSharesODICurrent')
c.execute('drop table battingODICurrentAllTime')
c.execute('drop table bowlingODICurrentAllTime')
c.execute('drop table allRoundODICurrentAllTime')
c.execute('drop table fieldingODICurrentAllTime')
c.execute('drop table winSharesODICurrentAllTime')
c.execute('''create table teamODICurrent (team text unique, startDate text, rankDiff integer, rank integer, homeRating real, awayRating real, rating real, bestCurrentRating text)''')
c.execute('''create table battingODICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table bowlingODICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table allRoundODICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table fieldingODICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table winSharesODICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table battingODICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table bowlingODICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table allRoundODICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table fieldingODICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
c.execute('''create table winSharesODICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
#
print("Generating current table for odi teams...\n")
dumpCurrentTeam("teamODILive","teamODICurrent","odi")
print("Generating current table for odi batting...\n")
dumpCurrent("battingODILive","battingODICurrent","innings","odi")
print("Generating current table for odi bowling...\n")
dumpCurrent("bowlingODILive","bowlingODICurrent","innings","odi")
print("Generating current table for odi allRound...\n")
dumpCurrent("allRoundODILive","allRoundODICurrent","match","odi")
print("Generating current table for odi fielding...\n")
dumpCurrent("fieldingODILive","fieldingODICurrent","match","odi")
print("Generating current table for odi win shares...\n")
dumpCurrent("winSharesODILive","winSharesODICurrent","match","odi")
conn.close()
# #
# conn = sqlite3.connect('ccrT20I.db')
# c = conn.cursor()
# c.execute('drop table teamT20ICurrent')
# c.execute('drop table battingT20ICurrent')
# c.execute('drop table bowlingT20ICurrent')
# c.execute('drop table allRoundT20ICurrent')
# # # # # # c.execute('drop table fieldingT20ICurrent')
# # # # # # c.execute('drop table winSharesT20ICurrent')
# c.execute('drop table battingT20ICurrentAllTime')
# c.execute('drop table bowlingT20ICurrentAllTime')
# c.execute('drop table allRoundT20ICurrentAllTime')
# # # # # # c.execute('drop table fieldingT20ICurrentAllTime')
# # # # # # c.execute('drop table winSharesT20ICurrentAllTime')
# c.execute('''create table teamT20ICurrent (team text unique, startDate text, rankDiff integer, rank integer, homeRating real, awayRating real, rating real, bestCurrentRating text)''')
# c.execute('''create table battingT20ICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table bowlingT20ICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table allRoundT20ICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# # # # # # c.execute('''create table fieldingT20ICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# # # # # # c.execute('''create table winSharesT20ICurrent (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table battingT20ICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table bowlingT20ICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# c.execute('''create table allRoundT20ICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# # # # # # c.execute('''create table fieldingT20ICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# # # # # # c.execute('''create table winSharesT20ICurrentAllTime (playerId integer unique, rank integer, rating real, player text, country text, bestCurrentRating text)''')
# # # # #
# print("Generating current table for t20i teams...\n")
# dumpCurrentTeam("teamT20ILive","teamT20ICurrent","t20i")
# print("Generating current table for t20i batting...\n")
# dumpCurrent("battingT20ILive","battingT20ICurrent","innings","t20i")
# print("Generating current table for t20i bowling...\n")
# dumpCurrent("bowlingT20ILive","bowlingT20ICurrent","innings","t20i")
# print("Generating current table for t20i allRound...\n")
# dumpCurrent("allRoundT20ILive","allRoundT20ICurrent","match","t20i")
# # # # print("Generating current table for t20i fielding...\n")
# # # # dumpCurrent("fieldingT20ILive","fieldingT20ICurrent","match","t20i")
# # # # print("Generating current table for t20i win shares...\n")
# # # # dumpCurrent("winSharesT20ILive","winSharesT20ICurrent","match","t20i")
# conn.close()
# #
# conn = sqlite3.connect('ccrFT20.db')
# c = conn.cursor()
# c.execute('drop table teamFT20Current')
# c.execute('drop table battingFT20Current')
# c.execute('drop table bowlingFT20Current')
# c.execute('drop table allRoundFT20Current')
# c.execute('drop table fieldingFT20Current')
# c.execute('drop table winSharesFT20Current')
# c.execute('drop table battingFT20CurrentAllTime')
# c.execute('drop table bowlingFT20CurrentAllTime')
# c.execute('drop table allRoundFT20CurrentAllTime')
# c.execute('drop table fieldingFT20CurrentAllTime')
# c.execute('drop table winSharesFT20CurrentAllTime')
# c.execute('''create table teamFT20Current (team text unique, startDate text, rankDiff integer, rank integer, homeRating real, awayRating real, rating real, bestCurrentRating text)''')
# c.execute('''create table battingFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table bowlingFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table allRoundFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table fieldingFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table winSharesFT20Current (playerId integer unique, startDate text, rankDiff integer, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table battingFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table bowlingFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table allRoundFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table fieldingFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# c.execute('''create table winSharesFT20CurrentAllTime (playerId integer unique, rank integer, rating real, player text, teams text, bestCurrentRating text)''')
# # # # #
# print("Generating current table for ft20 teams...\n")
# dumpCurrentTeam("teamFT20Live","teamFT20Current","ft20")
# print("Generating current table for ft20 batting...\n")
# dumpCurrent("battingFT20Live","battingFT20Current","innings","ft20")
# print("Generating current table for ft20 bowling...\n")
# dumpCurrent("bowlingFT20Live","bowlingFT20Current","innings","ft20")
# print("Generating current table for ft20 allRound...\n")
# dumpCurrent("allRoundFT20Live","allRoundFT20Current","match","ft20")
# print("Generating current table for ft20 fielding...\n")
# dumpCurrent("fieldingFT20Live","fieldingFT20Current","match","ft20")
# print("Generating current table for ft20 win shares...\n")
# dumpCurrent("winSharesFT20Live","winSharesFT20Current","match","ft20")
# conn.close()

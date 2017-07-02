#!/usr/bin/env python
from datetime import date
import sqlite3
import math
import time
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

c.execute('drop table teamODIPeaks')
c.execute('drop table teamPlayerODILive')
c.execute('drop table teamBattingODILive')
c.execute('drop table teamBowlingODILive')
c.execute('create table teamODIPeaks (odiTeamTypeId text unique, odiId integer, startDate text, team text, playerList text, ratingType text, rating real)')
c.execute('create table teamPlayerODILive (odiTeamId text unique, odiId integer, startDate text, team text, playerList text, rating real)')
c.execute('create table teamBattingODILive (odiTeamId text unique, odiId integer, startDate text, team text, playerList text, rating real)')
c.execute('create table teamBowlingODILive (odiTeamId text unique, odiId integer, startDate text, team text, playerList text, rating real)')

c.execute('select distinct team from teamODILive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, odiTeamId, rating from teamODILive where team="'+team[0]+'" order by startDate asc')
    print team[0]
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        odiTeamId = teamRating[1]
        rating = teamRating[2]
        odiId = int(str(odiTeamId)[:-1])
        print odiId

        teamPlayerRating = 0
        teamBattingRating = 0
        teamBowlingRating = 0
        teamPlayerIds = []
        teamPlayers = []
        teamPlayerList = ""
        teamBatsmenIds = []
        teamBatsmen = []
        teamBatsmenList = ""
        teamBowlerIds = []
        teamBowlers = []
        teamBowlerList = ""

        c.execute('select playerId, player, rating from battingODILive where startDate="'+startDate+'" and odiId=?',(odiId, ))
        playerRatings = c.fetchall()
        numBatsmen = 0
        for p in playerRatings:
            if numBatsmen == 8: continue
            playerId = p[0]
            player = p[1]
            playerRating = p[2]
            c.execute('select country from playerInfo where playerId=?',(playerId, ))
            playerTeam = c.fetchone()
            playerTeam = playerTeam[0]
            if playerTeam == team[0]:
                c.execute('select player from battingODIInnings where playerId="'+`playerId`+'" and odiId=?',(odiId, ))
                playerBatted = c.fetchone()
                c.execute('select player from bowlingODIInnings where playerId="'+`playerId`+'" and odiId=?',(odiId, ))
                playerBowled = c.fetchone()
                if playerBatted != None or playerBowled != None:
                    if playerId not in teamPlayerIds:
                        teamPlayerRating += playerRating
                        teamPlayerIds.append(playerId)
                        player = player.replace("Sir ", "")
                        player = player.replace(" Singh", "")
                        playerLastName = player.split(" ")
                        if len(playerLastName) == 2:
                            teamPlayers.append(playerLastName[1])
                        elif len(playerLastName) == 1:
                            teamPlayers.append(playerLastName[0])
                        elif len(playerLastName) > 2:
                            teamPlayers.append(playerLastName[1]+" "+playerLastName[2])
                    if playerId not in teamBatsmenIds:
                        numBatsmen += 1
                        teamBattingRating += playerRating
                        teamBatsmenIds.append(playerId)
                        player = player.replace("Sir ", "")
                        player = player.replace(" Singh", "")
                        playerLastName = player.split(" ")
                        if len(playerLastName) == 2:
                            teamBatsmen.append(playerLastName[1])
                        elif len(playerLastName) == 1:
                            teamBatsmen.append(playerLastName[0])
                        elif len(playerLastName) > 2:
                            teamBatsmen.append(playerLastName[1]+" "+playerLastName[2])

        c.execute('select playerId, player, rating from bowlingODILive where startDate="'+startDate+'" and odiId=?',(odiId, ))
        playerRatings = c.fetchall()
        numBowlers = 0
        for p in playerRatings:
            if numBowlers == 6: continue
            playerId = p[0]
            player = p[1]
            playerRating = p[2]
            c.execute('select country from playerInfo where playerId=?',(playerId, ))
            playerTeam = c.fetchone()
            playerTeam = playerTeam[0]
            if playerTeam == team[0]:
                c.execute('select player from battingODIInnings where playerId="'+`playerId`+'" and odiId=?',(odiId, ))
                playerBatted = c.fetchone()
                c.execute('select player from bowlingODIInnings where playerId="'+`playerId`+'" and odiId=?',(odiId, ))
                playerBowled = c.fetchone()
                if playerBatted != None or playerBowled != None:
                    if playerId not in teamBowlerIds:
                        numBowlers += 1
                        teamBowlingRating += playerRating
                        teamBowlerIds.append(playerId)
                        player = player.replace("Sir ", "")
                        player = player.replace(" Singh", "")
                        playerLastName = player.split(" ")
                        if len(playerLastName) == 2:
                            teamBowlers.append(playerLastName[1])
                        elif len(playerLastName) == 1:
                            teamBowlers.append(playerLastName[0])
                        elif len(playerLastName) > 2:
                            teamBowlers.append(playerLastName[1]+" "+playerLastName[2])

                        teamPlayerRating += playerRating
                        if playerId not in teamPlayerIds:
                            teamPlayerIds.append(playerId)
                            if len(playerLastName) == 2:
                                teamPlayers.append(playerLastName[1])
                            elif len(playerLastName) == 1:
                                teamPlayers.append(playerLastName[0])
                            elif len(playerLastName) > 2:
                                teamPlayers.append(playerLastName[1]+" "+playerLastName[2])

        for pl in teamPlayers:
            teamPlayerList = teamPlayerList + pl + ", "
        teamPlayerList = teamPlayerList[:-2]

        for pl in teamBatsmen:
            teamBatsmenList = teamBatsmenList + pl + ", "
        teamBatsmenList = teamBatsmenList[:-2]

        for pl in teamBowlers:
            teamBowlerList = teamBowlerList + pl + ", "
        teamBowlerList = teamBowlerList[:-2]

        odiTeamId = repr(odiId) + '_' + team[0]
        c.execute('insert or replace into teamPlayerODILive (odiTeamId, odiId, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (odiTeamId, odiId, teamRating[0], team[0], teamPlayerList, teamPlayerRating))

        odiTeamPeakId = repr(odiId) + '_' + team[0] + '_' + 'Batting'
        c.execute('insert or replace into teamBattingODILive (odiTeamId, odiId, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (odiTeamId, odiId, teamRating[0], team[0], teamBatsmenList, teamBattingRating))

        odiTeamPeakId = repr(odiId) + '_' + team[0] + '_' + 'Bowling'
        c.execute('insert or replace into teamBowlingODILive (odiTeamId, odiId, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (odiTeamId, odiId, teamRating[0], team[0], teamBowlerList, teamBowlingRating))

        c.execute('select rating from teamODILive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamODILive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            odiTeamTypeId = repr(odiId) + '_' + team[0] + '_' + 'Team'
            c.execute('insert or replace into teamODIPeaks (odiTeamTypeId, odiId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (odiTeamTypeId, odiId, teamRating[0], team[0], "", "Team", rating))
            # print team[0] + ' ' + startDate + ' ' + `int(rating)` + ' ' + teamPlayerList + ' ' + `int(teamTotalPlayerRating)`
        conn.commit()

# smooth out rating for incomplete matches
c.execute('select distinct team from teamPlayerODILive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, odiId from teamPlayerODILive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        odiId = teamRating[3]
        c.execute('select rating from teamPlayerODILive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 8: rating = beforeRating[0]
        c.execute('update teamPlayerODILive set rating=? where team=? and odiId=? and startDate=?', (rating, team[0], odiId, startDate))
        conn.commit()

c.execute('select distinct team from teamBattingODILive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, odiId from teamBattingODILive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        odiId = teamRating[3]
        c.execute('select rating from teamBattingODILive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 6: rating = beforeRating[0]
        c.execute('update teamBattingODILive set rating=? where team=? and odiId=? and startDate=?', (rating, team[0], odiId, startDate))
        conn.commit()

c.execute('select distinct team from teamBowlingODILive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, odiId from teamBowlingODILive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        odiId = teamRating[3]
        c.execute('select rating from teamBowlingODILive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 5: rating = beforeRating[0]
        c.execute('update teamBowlingODILive set rating=? where team=? and odiId=? and startDate=?', (rating, team[0], odiId, startDate))
        conn.commit()

# store peaks
c.execute('select distinct team from teamPlayerODILive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, odiId from teamPlayerODILive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        odiId = teamRating[3]
        c.execute('select rating from teamPlayerODILive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamPlayerODILive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            odiTeamTypeId = repr(odiId) + '_' + team[0] + '_' + 'Player'
            c.execute('insert or replace into teamODIPeaks (odiTeamTypeId, odiId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (odiTeamTypeId, odiId, startDate, team[0], playerList, "Player", rating))
            conn.commit()

c.execute('select distinct team from teamBattingODILive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, odiId from teamBattingODILive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        odiId = teamRating[3]
        c.execute('select rating from teamBattingODILive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamBattingODILive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            odiTeamTypeId = repr(odiId) + '_' + team[0] + '_' + 'Batting'
            c.execute('insert or replace into teamODIPeaks (odiTeamTypeId, odiId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (odiTeamTypeId, odiId, startDate, team[0], playerList, "Batting", rating))
            conn.commit()

c.execute('select distinct team from teamBowlingODILive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, odiId from teamBowlingODILive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        odiId = teamRating[3]
        c.execute('select rating from teamBowlingODILive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamBowlingODILive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            odiTeamTypeId = repr(odiId) + '_' + team[0] + '_' + 'Bowling'
            c.execute('insert or replace into teamODIPeaks (odiTeamTypeId, odiId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (odiTeamTypeId, odiId, startDate, team[0], playerList, "Bowling", rating))
            conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')

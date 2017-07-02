#!/usr/bin/env python
from datetime import date
import sqlite3
import math
import time
start = time.clock()

# connect to db
conn = sqlite3.connect('ccrFT20.db')
c = conn.cursor()

c.execute('drop table teamFT20Peaks')
c.execute('drop table teamPlayerFT20Live')
c.execute('drop table teamBattingFT20Live')
c.execute('drop table teamBowlingFT20Live')
c.execute('create table teamFT20Peaks (ft20TeamTypeId text unique, ft20Id integer, startDate text, team text, playerList text, ratingType text, rating real)')
c.execute('create table teamPlayerFT20Live (ft20TeamId text unique, ft20Id integer, startDate text, team text, playerList text, rating real)')
c.execute('create table teamBattingFT20Live (ft20TeamId text unique, ft20Id integer, startDate text, team text, playerList text, rating real)')
c.execute('create table teamBowlingFT20Live (ft20TeamId text unique, ft20Id integer, startDate text, team text, playerList text, rating real)')

c.execute('select distinct team from teamFT20Live order by team asc')
for team in c.fetchall():
    c.execute('select startDate, ft20TeamId, rating from teamFT20Live where team="'+team[0]+'" order by startDate asc')
    print team[0]
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        ft20TeamId = teamRating[1]
        rating = teamRating[2]
        ft20Id = int(str(ft20TeamId)[:-1])
        print ft20Id

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

        c.execute('select playerId, player, rating from battingFT20Live where startDate="'+startDate+'" and ft20Id=?',(ft20Id, ))
        playerRatings = c.fetchall()
        numBatsmen = 0
        for p in playerRatings:
            if numBatsmen == 7: continue
            playerId = p[0]
            player = p[1]
            playerRating = p[2]
            c.execute('select teams from playerInfo where playerId=?',(playerId, ))
            playerTeam = c.fetchone()
            playerTeam = playerTeam[0]
            if team[0] in playerTeam:
                c.execute('select player from battingFT20Innings where playerId="'+`playerId`+'" and ft20Id=?',(ft20Id, ))
                playerBatted = c.fetchone()
                c.execute('select player from bowlingFT20Innings where playerId="'+`playerId`+'" and ft20Id=?',(ft20Id, ))
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

        c.execute('select playerId, player, rating from bowlingFT20Live where startDate="'+startDate+'" and ft20Id=?',(ft20Id, ))
        playerRatings = c.fetchall()
        numBowlers = 0
        for p in playerRatings:
            if numBowlers == 6: continue
            playerId = p[0]
            player = p[1]
            playerRating = p[2]
            c.execute('select teams from playerInfo where playerId=?',(playerId, ))
            playerTeam = c.fetchone()
            playerTeam = playerTeam[0]
            if team[0] in playerTeam:
                c.execute('select player from battingFT20Innings where playerId="'+`playerId`+'" and ft20Id=?',(ft20Id, ))
                playerBatted = c.fetchone()
                c.execute('select player from bowlingFT20Innings where playerId="'+`playerId`+'" and ft20Id=?',(ft20Id, ))
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

        ft20TeamId = repr(ft20Id) + '_' + team[0]
        c.execute('insert or replace into teamPlayerFT20Live (ft20TeamId, ft20Id, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (ft20TeamId, ft20Id, teamRating[0], team[0], teamPlayerList, teamPlayerRating))

        ft20TeamPeakId = repr(ft20Id) + '_' + team[0] + '_' + 'Batting'
        c.execute('insert or replace into teamBattingFT20Live (ft20TeamId, ft20Id, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (ft20TeamId, ft20Id, teamRating[0], team[0], teamBatsmenList, teamBattingRating))

        ft20TeamPeakId = repr(ft20Id) + '_' + team[0] + '_' + 'Bowling'
        c.execute('insert or replace into teamBowlingFT20Live (ft20TeamId, ft20Id, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (ft20TeamId, ft20Id, teamRating[0], team[0], teamBowlerList, teamBowlingRating))

        c.execute('select rating from teamFT20Live where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamFT20Live where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            ft20TeamTypeId = repr(ft20Id) + '_' + team[0] + '_' + 'Team'
            c.execute('insert or replace into teamFT20Peaks (ft20TeamTypeId, ft20Id, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (ft20TeamTypeId, ft20Id, teamRating[0], team[0], "", "Team", rating))
            # print team[0] + ' ' + startDate + ' ' + `int(rating)` + ' ' + teamPlayerList + ' ' + `int(teamTotalPlayerRating)`
        conn.commit()

# smooth out rating for incomplete matches
c.execute('select distinct team from teamPlayerFT20Live order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, ft20Id from teamPlayerFT20Live where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        ft20Id = teamRating[3]
        c.execute('select rating from teamPlayerFT20Live where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 8: rating = beforeRating[0]
        c.execute('update teamPlayerFT20Live set rating=? where team=? and ft20Id=? and startDate=?', (rating, team[0], ft20Id, startDate))
        conn.commit()

c.execute('select distinct team from teamBattingFT20Live order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, ft20Id from teamBattingFT20Live where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        ft20Id = teamRating[3]
        c.execute('select rating from teamBattingFT20Live where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 6: rating = beforeRating[0]
        c.execute('update teamBattingFT20Live set rating=? where team=? and ft20Id=? and startDate=?', (rating, team[0], ft20Id, startDate))
        conn.commit()

c.execute('select distinct team from teamBowlingFT20Live order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, ft20Id from teamBowlingFT20Live where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        ft20Id = teamRating[3]
        c.execute('select rating from teamBowlingFT20Live where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 5: rating = beforeRating[0]
        c.execute('update teamBowlingFT20Live set rating=? where team=? and ft20Id=? and startDate=?', (rating, team[0], ft20Id, startDate))
        conn.commit()

# store peaks
c.execute('select distinct team from teamPlayerFT20Live order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, ft20Id from teamPlayerFT20Live where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        ft20Id = teamRating[3]
        c.execute('select rating from teamPlayerFT20Live where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamPlayerFT20Live where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            ft20TeamTypeId = repr(ft20Id) + '_' + team[0] + '_' + 'Player'
            c.execute('insert or replace into teamFT20Peaks (ft20TeamTypeId, ft20Id, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (ft20TeamTypeId, ft20Id, startDate, team[0], playerList, "Player", rating))
            conn.commit()

c.execute('select distinct team from teamBattingFT20Live order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, ft20Id from teamBattingFT20Live where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        ft20Id = teamRating[3]
        c.execute('select rating from teamBattingFT20Live where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamBattingFT20Live where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            ft20TeamTypeId = repr(ft20Id) + '_' + team[0] + '_' + 'Batting'
            c.execute('insert or replace into teamFT20Peaks (ft20TeamTypeId, ft20Id, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (ft20TeamTypeId, ft20Id, startDate, team[0], playerList, "Batting", rating))
            conn.commit()

c.execute('select distinct team from teamBowlingFT20Live order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, ft20Id from teamBowlingFT20Live where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        ft20Id = teamRating[3]
        c.execute('select rating from teamBowlingFT20Live where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamBowlingFT20Live where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            ft20TeamTypeId = repr(ft20Id) + '_' + team[0] + '_' + 'Bowling'
            c.execute('insert or replace into teamFT20Peaks (ft20TeamTypeId, ft20Id, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (ft20TeamTypeId, ft20Id, startDate, team[0], playerList, "Bowling", rating))
            conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')

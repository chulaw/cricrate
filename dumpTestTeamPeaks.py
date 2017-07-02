#!/usr/bin/env python
from datetime import date
import sqlite3
import math
import time
start = time.clock()

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

c.execute('drop table teamTestPeaks')
c.execute('drop table teamPlayerTestLive')
c.execute('drop table teamBattingTestLive')
c.execute('drop table teamBowlingTestLive')
c.execute('create table teamTestPeaks (testTeamTypeId text unique, testId integer, startDate text, team text, playerList text, ratingType text, rating real)')
c.execute('create table teamPlayerTestLive (testTeamId text unique, testId integer, startDate text, team text, playerList text, rating real)')
c.execute('create table teamBattingTestLive (testTeamId text unique, testId integer, startDate text, team text, playerList text, rating real)')
c.execute('create table teamBowlingTestLive (testTeamId text unique, testId integer, startDate text, team text, playerList text, rating real)')

c.execute('select distinct team from teamTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, testTeamId, rating from teamTestLive where team="'+team[0]+'" order by startDate asc')
    print team[0]
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        testTeamId = teamRating[1]
        rating = teamRating[2]
        testId = int(str(testTeamId)[:-1])
        print testId

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

        c.execute('select playerId, player, rating from battingTestLive where startDate="'+startDate+'" and testId=?',(testId, ))
        playerRatings = c.fetchall()
        for p in playerRatings:
            playerId = p[0]
            player = p[1]
            playerRating = p[2]
            c.execute('select country from playerInfo where playerId=?',(playerId, ))
            playerTeam = c.fetchone()
            playerTeam = playerTeam[0]
            if playerTeam == team[0]:
                c.execute('select player from battingTestInnings where playerId="'+`playerId`+'" and testId=?',(testId, ))
                playerBatted = c.fetchone()
                c.execute('select player from bowlingTestInnings where playerId="'+`playerId`+'" and testId=?',(testId, ))
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

        c.execute('select playerId, player, rating from bowlingTestLive where startDate="'+startDate+'" and testId=?',(testId, ))
        playerRatings = c.fetchall()
        numBowlers = 0
        for p in playerRatings:
            if numBowlers == 5: continue
            playerId = p[0]
            player = p[1]
            playerRating = p[2]
            c.execute('select country from playerInfo where playerId=?',(playerId, ))
            playerTeam = c.fetchone()
            playerTeam = playerTeam[0]
            if playerTeam == team[0]:
                c.execute('select player from battingTestInnings where playerId="'+`playerId`+'" and testId=?',(testId, ))
                playerBatted = c.fetchone()
                c.execute('select player from bowlingTestInnings where playerId="'+`playerId`+'" and testId=?',(testId, ))
                playerBowled = c.fetchone()
                if playerBatted != None or playerBowled != None:
                    if playerId not in teamBowlerIds:
                        numBowlers += 1
                        teamBowlingRating += playerRating * 1.5
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

                        teamPlayerRating += playerRating * 1.5 # adjust bowling rating to match batting aggregate
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

        testTeamId = repr(testId) + '_' + team[0]
        c.execute('insert or replace into teamPlayerTestLive (testTeamId, testId, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (testTeamId, testId, teamRating[0], team[0], teamPlayerList, teamPlayerRating))

        testTeamPeakId = repr(testId) + '_' + team[0] + '_' + 'Batting'
        c.execute('insert or replace into teamBattingTestLive (testTeamId, testId, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (testTeamId, testId, teamRating[0], team[0], teamBatsmenList, teamBattingRating))

        testTeamPeakId = repr(testId) + '_' + team[0] + '_' + 'Bowling'
        c.execute('insert or replace into teamBowlingTestLive (testTeamId, testId, startDate, team, playerList, rating) values (?, ?, ?, ?, ?, ?)',
                  (testTeamId, testId, teamRating[0], team[0], teamBowlerList, teamBowlingRating))

        c.execute('select rating from teamTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamTestLive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            testTeamTypeId = repr(testId) + '_' + team[0] + '_' + 'Team'
            c.execute('insert or replace into teamTestPeaks (testTeamTypeId, testId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (testTeamTypeId, testId, teamRating[0], team[0], "", "Team", rating))
            # print team[0] + ' ' + startDate + ' ' + `int(rating)` + ' ' + teamPlayerList + ' ' + `int(teamTotalPlayerRating)`
        conn.commit()


# smooth out rating for incomplete matches
c.execute('select distinct team from teamPlayerTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, testId from teamPlayerTestLive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        testId = teamRating[3]
        c.execute('select rating from teamPlayerTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 8: rating = beforeRating[0]
        c.execute('update teamPlayerTestLive set rating=? where team=? and testId=? and startDate=?', (rating, team[0], testId, startDate))
        conn.commit()

c.execute('select distinct team from teamBattingTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, testId from teamBattingTestLive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        testId = teamRating[3]
        c.execute('select rating from teamBattingTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 7: rating = beforeRating[0]
        c.execute('update teamBattingTestLive set rating=? where team=? and testId=? and startDate=?', (rating, team[0], testId, startDate))
        conn.commit()

c.execute('select distinct team from teamBowlingTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, testId from teamBowlingTestLive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        testId = teamRating[3]
        c.execute('select rating from teamBowlingTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        playerCount = len(playerList.split(","))
        if playerCount < 4: rating = beforeRating[0]
        c.execute('update teamBowlingTestLive set rating=? where team=? and testId=? and startDate=?', (rating, team[0], testId, startDate))
        conn.commit()

# store peaks
c.execute('select distinct team from teamPlayerTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, testId from teamPlayerTestLive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        testId = teamRating[3]
        c.execute('select rating from teamPlayerTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamPlayerTestLive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            testTeamTypeId = repr(testId) + '_' + team[0] + '_' + 'Player'
            c.execute('insert or replace into teamTestPeaks (testTeamTypeId, testId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (testTeamTypeId, testId, startDate, team[0], playerList, "Player", rating))
            conn.commit()

c.execute('select distinct team from teamBattingTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, testId from teamBattingTestLive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        testId = teamRating[3]
        c.execute('select rating from teamBattingTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamBattingTestLive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            testTeamTypeId = repr(testId) + '_' + team[0] + '_' + 'Batting'
            c.execute('insert or replace into teamTestPeaks (testTeamTypeId, testId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (testTeamTypeId, testId, startDate, team[0], playerList, "Batting", rating))
            conn.commit()

c.execute('select distinct team from teamBowlingTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, playerList, rating, testId from teamBowlingTestLive where team="'+team[0]+'" order by startDate asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        playerList = teamRating[1]
        rating = teamRating[2]
        testId = teamRating[3]
        c.execute('select rating from teamBowlingTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[0]

        c.execute('select rating from teamBowlingTestLive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[0]

        if rating > beforeRating and rating > afterRating:
            testTeamTypeId = repr(testId) + '_' + team[0] + '_' + 'Bowling'
            c.execute('insert or replace into teamTestPeaks (testTeamTypeId, testId, startDate, team, playerList, ratingType, rating) values (?, ?, ?, ?, ?, ?, ?)',
                      (testTeamTypeId, testId, startDate, team[0], playerList, "Bowling", rating))
            conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')

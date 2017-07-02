#!/usr/bin/env python
import time
import datetime
import sqlite3
import csv
import feedparser
import requests
from lxml import html
import re
import sys
import boto
import boto.s3
from boto.s3.key import Key
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import numpy as np
# from selenium.webdriver import Chrome # pip install selenium
# from selenium.webdriver.support.ui import WebDriverWait

start = time.clock()
teamNameChange = {'Chennai T20':'Chennai Super Kings', 'Delhi T20':'Delhi Daredevils', 'Punjab T20':'Kings XI Punjab', 'Bangalore':'Royal Challengers Bangalore', 'Hyderabad':'Sunrisers Hyderabad',
                    'Rajasthan':'Rajasthan Royals', 'Mumbai T20':'Mumbai Indians', 'Kolkata T20':'Kolkata Knight Riders', 'Super Kings':'Chennai Super Kings', 'Daredevils':'Delhi Daredevils',
                    'Kings XI':'Kings XI Punjab', 'RCB':'Royal Challengers Bangalore', 'Sunrisers':'Sunrisers Hyderabad', 'Royals':'Rajasthan Royals', 'Mum Indians':'Mumbai Indians', 'Scorchers':'Perth Scorchers',
                    'KKR':'Kolkata Knight Riders', 'Chargers':'Deccan Chargers', 'Kochi':'Kochi Tuskers Kerala', 'Warriors':'Pune Warriors', 'Tridents':'Barbados Tridents', 'Zouks':'St Lucia Zouks',
                    'Amazon':'Guyana Amazon Warriors', 'Red Steel':'Trinidad & Tobago Red Steel', 'Hawksbills':'Antigua Hawksbills', 'Tallawahs':'Jamaica Tallawahs', 'Melb Stars':'Melbourne Stars',
                    'Melb Reneg':'Melbourne Renegades', 'Syd Sixers':'Sydney Sixers', 'Syd Thunder':'Sydney Thunder', 'Hurricanes':'Hobart Hurricanes', 'Strikers':'Adelaide Strikers', 'Heat':'Brisbane Heat',
                    'Red Steel':'Trinidad & Tobago Red Steel', 'Patriots':'St Kitts and Nevis Patriots', 'Supergiants':'Rising Pune Supergiants', 'Guj Lions': 'Gujarat Lions', 'T&T Riders': 'Trinbago Knight Riders',
                    'Rising Pune Supergiant': 'Rising Pune Supergiants'}

scriptRunTime = 0
battingWktWeight = [0.15, 0.15, 0.15, 0.15, 0.125, 0.1, 0.075, 0.05, 0.025, 0.025]

def loadModel(matchFormat, inn, overRange):
    overData = pandas.read_csv(matchFormat + "ML" + `inn` + "Live.csv")
    overData['MatchOdds'] = overData['MatchOdds'].apply(str)
    if len(overData[overData['MatchOdds'] != "None"]) !=  len(overData):
        overData.loc[overData["MatchOdds"] == "None", "MatchOdds"] = 0.5
        overData[['MatchOdds']] = overData[['MatchOdds']].apply(pandas.to_numeric)
    overData['RunRate'] = overData['Runs'] / overData['Overs']
    if inn == 2:
        overData = overData[overData['BallsRem'] > 0]
        overData['ReqRunRate'] = overData['RunsReq'] * 6 / overData['BallsRem']
    overData = overData.fillna(0)
    overData['TeamRatingDiff'] = overData['Team1Rating'] - overData['Team2Rating']
    if matchFormat == "odi":
        PR = pandas.read_csv(matchFormat + "ML" + `inn` + "PRLive.csv")
        overData = overData.merge(PR, on=['Id', 'Overs'])
    overData['BatBowlDiff'] = overData['BattingRating'] - overData['BowlingRating']

    if inn == 1:
        if matchFormat == "odi":
            predictors = ["Runs", "Wkts", "MatchOdds", "RunRate", "TeamRatingDiff", "BatBowlDiff"]
        else:
            predictors = ["Runs", "Wkts", "MatchOdds", "RunRate", "BatBowlDiff"]
    else:
        if matchFormat == "odi":
            predictors = ["RunsReq", "Wkts", "MatchOdds", "ReqRunRate", "TeamRatingDiff", "BatBowlDiff"]
        else:
            predictors = ["RunsReq", "Wkts", "MatchOdds", "ReqRunRate", "BatBowlDiff"]

    # Predict probabilities
    if inn == 1:
        if matchFormat == "odi":
            if overRange == "early":
                overData = overData[(overData['Overs'] >= 1) & (overData['Overs'] <= 10)]
                alg = LogisticRegression()
            else:
                overData = overData[(overData['Overs'] >= 11) & (overData['Overs'] <= 50)]
                alg = GradientBoostingClassifier(n_estimators=50, min_samples_split=2, max_depth=2)
        else:
            alg = LogisticRegression()
    else:
        if matchFormat == "odi":
            if overRange == "early":
                overData = overData[(overData['Overs'] >= 1) & (overData['Overs'] <= 39)]
                alg = LogisticRegression()
            else:
                overData = overData[(overData['Overs'] >= 40) & (overData['Overs'] <= 50)]
                alg = LogisticRegression()
        else:
            if overRange == "early":
                overData = overData[(overData['Overs'] >= 1) & (overData['Overs'] <= 9)]
                alg = LogisticRegression()
            else:
                overData = overData[(overData['Overs'] >= 11) & (overData['Overs'] <= 20)]
                alg = LogisticRegression()

    #Fit the algorithm using the full training data.
    alg.fit(overData[predictors], overData["Result"])
    return alg

odi1early = loadModel("odi", 1, "early")
odi1late = loadModel("odi", 1, "late")
odi2early = loadModel("odi", 2, "early")
odi2late = loadModel("odi", 2, "late")
t201 = loadModel("t20", 1, "")
t202early = loadModel("t20", 2, "early")
t202late = loadModel("t20", 2, "late")

def getBattingBowlingRatings(teamBat, teamBowl, dbFormat):
    teamBattingRating = 0.0
    teamBowlingRating = 0.0
    conn = sqlite3.connect('ccr'+dbFormat+'.db')
    c = conn.cursor()
    matchDate = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    d = datetime.datetime(int(matchDate[0:4]), int(matchDate[4:-2]), int(matchDate[6:]))
    date2yAgo = d + datetime.timedelta(days=-720)
    date2yAgo = date2yAgo.strftime('%Y%m%d')
    dbFormatLower = dbFormat.lower()

    if dbFormat == "FT20":
        c.execute('select b.playerId, b.ft20Id from battingFT20Live b, playerInfo p where p.playerId=b.playerId and p.teams like ? and b.startDate>? and b.startDate<?', ('%'+teamBat+'%', date2yAgo, matchDate))
    else:
        c.execute('select b.playerId, b.'+dbFormatLower+'Id from batting'+dbFormat+'Live b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (teamBat, date2yAgo, matchDate))
    playerMatches = c.fetchall()
    playerLastMatch = {}
    for i in range(0, len(playerMatches)):
        pid = playerMatches[i][0]
        pMatchId = playerMatches[i][1]
        if pid in playerLastMatch:
            if pMatchId > playerLastMatch[pid]:
                playerLastMatch[pid] = pMatchId
        else:
            playerLastMatch[pid] = pMatchId

    battingRating = []
    for pid in playerLastMatch:
        c.execute('select player, rating from batting'+dbFormat+'Live where playerId=? and '+dbFormatLower+'Id=?', (pid, playerLastMatch[pid]))
        pRating = c.fetchone()
        battingRating.append(pRating[1])
    battingRating = sorted(battingRating, reverse=True)

    if len(battingRating) >= 7:
        for b in range(0, 7):
            teamBattingRating += battingRating[b]
        teamBattingRating = teamBattingRating / 7 * 5

    if dbFormat == "FT20":
        c.execute('select b.playerId, b.ft20Id from bowlingFT20Live b, playerInfo p where p.playerId=b.playerId and p.teams like ? and b.startDate>? and b.startDate<?', ('%'+teamBowl+'%', date2yAgo, matchDate))
    else:
        c.execute('select b.playerId, b.'+dbFormatLower+'Id from bowling'+dbFormat+'Live b, playerInfo p where p.playerId=b.playerId and p.country=? and b.startDate>? and b.startDate<?', (teamBowl, date2yAgo, matchDate))
    playerMatches = c.fetchall()
    playerLastMatch = {}
    for i in range(0, len(playerMatches)):
        pid = playerMatches[i][0]
        pMatchId = playerMatches[i][1]
        if pid in playerLastMatch:
            if pMatchId > playerLastMatch[pid]:
                playerLastMatch[pid] = pMatchId
        else:
            playerLastMatch[pid] = pMatchId

    bowlingRating = []
    for pid in playerLastMatch:
        c.execute('select player, rating from bowling'+dbFormat+'Live where playerId=? and '+dbFormatLower+'Id=?', (pid, playerLastMatch[pid]))
        pRating = c.fetchone()
        bowlingRating.append(pRating[1])
    bowlingRating = sorted(bowlingRating, reverse=True)

    if len(bowlingRating) >= 5:
        for b in range(0, 5):
            teamBowlingRating += bowlingRating[b]

    conn.close()
    return (teamBattingRating, teamBowlingRating)

def getRunsWktsOvers(url):
    team1ScoreDetails = {}
    team2ScoreDetails = {}
    scorecardPage = requests.get(url)
    scoreTree = html.fromstring(scorecardPage.text)
    team1Score = scoreTree.xpath('(//div[@class="team-1-name"]/span/text())')
    team1Score2 = scoreTree.xpath('(//div[@class="team-1-name"]/span/span/text())')

    if len(team1Score) != 1:
        if len(team1Score2) == 1:
            team1Score = team1Score2[0]
        else: team1Score = ""
    else:
        team1Score = team1Score[0]

    team2Score = scoreTree.xpath('(//div[@class="team-2-name"]/span/text())')
    team2Score2 = scoreTree.xpath('(//div[@class="team-2-name"]/span/span/text())')
    if len(team2Score) != 1:
        if len(team2Score2) == 1:
            team2Score = team2Score2[0]
        else:
            team2Score = ""
    else:
        team2Score = team2Score[0]

    team1ScoreOvers = team1Score.split(" ")
    if team1ScoreOvers[0] == "": return (team1ScoreDetails, team2ScoreDetails)
    team1RunsWkts = team1ScoreOvers[0].split("/")
    team1Runs = int(team1RunsWkts[0])
    team1Wkts = 10 if len(team1RunsWkts) == 1 else int(team1RunsWkts[1])
    team1Overs = ""
    if len(team1ScoreOvers) > 1:
        if "/" in team1ScoreOvers[1]:
            team1OversDetails = team1ScoreOvers[1].split("/")
            if team1OversDetails[0] == "": return (None, None)
            team1OversMod = team1OversDetails[0][1:]
            if "." not in team1OversMod:
                team1Overs = float(team1OversMod)
            else:
                team1OversModSplit = team1OversMod.split(".")
                team1Overs = float(team1OversModSplit[0]) + float(team1OversModSplit[1]) / 6
        elif "." not in team1ScoreOvers[1]:
            team1Overs = float(team1ScoreOvers[1][1:])
        else:
            team1OversDetails = team1ScoreOvers[1].split(".")
            team1Overs = float(team1OversDetails[0][1:]) + float(team1OversDetails[1]) / 6

    team1ScoreDetails['team1Runs'] = team1Runs
    team1ScoreDetails['team1Wkts'] = team1Wkts
    team1ScoreDetails['team1Overs'] = team1Overs
    team2ScoreOvers = team2Score.split(" ")
    if team2ScoreOvers[0] != "":
        team2RunsWkts = team2ScoreOvers[0].split("/")
        team2Runs = int(team2RunsWkts[0])
        team2Wkts = 10 if len(team2RunsWkts) == 1 else int(team2RunsWkts[1])
        team2Overs = ""
        if len(team2ScoreOvers) > 1:
            if "/" in team2ScoreOvers[1]:
                team2OversDetails = team2ScoreOvers[1].split("/")
                if team2OversDetails[0] == "": return (team1ScoreDetails, None)
                team2OversMod = team2OversDetails[0][1:]
                if "." not in team2OversMod:
                    team2Overs = float(team2OversMod)
                else:
                    team2OversModSplit = team2OversMod.split(".")
                    team2Overs = float(team2OversModSplit[0]) + float(team2OversModSplit[1]) / 6
            elif "." not in team2ScoreOvers[1]:
                team2Overs = float(team2ScoreOvers[1][1:])
            else:
                team2OversDetails = team2ScoreOvers[1].split(".")
                team2Overs = float(team2OversDetails[0][1:]) + float(team2OversDetails[1]) / 6

        team2ScoreDetails['team2Runs'] = team2Runs
        team2ScoreDetails['team2Wkts'] = team2Wkts
        team2ScoreDetails['team2Overs'] = team2Overs
    return (team1ScoreDetails, team2ScoreDetails)

def dumpScoresPricesOdds():
    # get betfair prices
    betfairURL = "https://www.betfair.com/exchange/cricket"
    betfairPage = requests.get(betfairURL)
    betfairTree = html.fromstring(betfairPage.text)
    markets = betfairTree.xpath('(//ul[@class="list-coupons"])')
    teamImpliedOdds = {}
    for market in markets:
        inplayFlag = market.xpath('.//li/span[@class="in-play-icon inplay"]')
        if len(inplayFlag) == 0: continue
        team1 = market.xpath('.//span[@class="home-team"]/text()')[0]
        team2 = market.xpath('.//span[@class="away-team"]/text()')[0]
        try:
            team1Back = float(market.xpath('.//li[@class="odds back selection-0 back-cell "]/button/span[@class="price"]/text()')[0].strip())
            team1Lay = float(market.xpath('.//li[@class="odds lay selection-0 lay-cell "]/button/span[@class="price"]/text()')[0].strip())
            team2Back = float(market.xpath('.//li[@class="odds back selection-1 back-cell "]/button/span[@class="price"]/text()')[0].strip())
            team2Lay = float(market.xpath('.//li[@class="odds lay selection-1 lay-cell "]/button/span[@class="price"]/text()')[0].strip())
            # print team1 + " " + `team1Back` + "/" + `team1Lay` + " vs " + team2 + " " + `team2Back` + "/" + `team2Lay`
            teamImpliedOdds[team1] = 200 / (team1Back + team1Lay)
            teamImpliedOdds[team2] = 200 / (team2Back + team2Lay)
        except ValueError:
            continue
        # marketId = market.xpath('.//li/@data-marketid')[0]
        # marketURL = "https://www.betfair.com/exchange/plus/#/cricket/market/" + marketId
        # marketPage = requests.get(marketURL)
        # marketTree = html.fromstring(marketPage.text)

    # get cricinfo live scores
    rss = feedparser.parse('http://static.cricinfo.com/rss/livescores.xml')
    # print teamImpliedOdds
    # print rss
    for i in range(0, len(rss['entries'])):
        scorecardURL = rss['entries'][i]['guid'] + "?view=scorecard;wrappertype=none;xhr=1"
        scorecardPage = requests.get(scorecardURL)
        scoreTree = html.fromstring(scorecardPage.text)
        matchDetails = scoreTree.xpath('(//a[@class="headLink"]/text())')
        if len(matchDetails) >= 2:
            matchDetails = matchDetails[1]
        else:
            continue

        if "Test" in matchDetails or "First-class" in matchDetails:
            matchType = "Test"
            dbFormat = "Test"
        elif "ODI" in matchDetails or "One-Day" in matchDetails or "List A" in matchDetails:
            matchType = "One-Day"
            dbFormat = "ODI"
        elif "Twenty20" in matchDetails or "T20I" in matchDetails:
            matchType = "Twenty20"
            if "T20I" in matchDetails:
                dbFormat = "T20I"
            else:
                dbFormat = "FT20"
        else:
            continue

        team1Name = scoreTree.xpath('(//div[@class="team-1-name"]/text())')[0].strip()
        team2Name = scoreTree.xpath('(//div[@class="team-2-name"]/text())')
        # print team1Name
        # print team2Name
        if len(team2Name) == 0: continue
        team2Name = team2Name[0].strip()
        matchResult = scoreTree.xpath('(//div[@class="innings-requirement"]/text())')
        if len(matchResult) == 0: continue
        matchResult = matchResult[0]
        if "won by" in matchResult or "tied" in matchResult or "drawn" in matchResult: continue

        if matchType == "One-Day" or matchType == "Twenty20":
            conn = sqlite3.connect('ccr' + dbFormat + '.db')
            c = conn.cursor()

            team1StartingOdds = 0.5
            team2StartingOdds = 0.5
            c.execute('select rating from team' +dbFormat+ 'Live where team=? order by startDate desc',(team1Name, ))
            team1Rating = c.fetchall()
            if len(team1Rating) > 0:
                team1Rating = team1Rating[len(team1Rating)-1][0]
            else:
                team1Rating = 500.0

            c.execute('select rating from team' +dbFormat+ 'Live where team=? order by startDate desc',(team2Name, ))
            team2Rating = c.fetchall()
            if len(team2Rating) > 0:
                team2Rating = team2Rating[len(team2Rating)-1][0]
            else:
                team2Rating = 500.0
            team1StartingOdds = team1Rating / (team1Rating + team2Rating)
            team2StartingOdds = 1 - team1StartingOdds

            scorecardURLs = [rss['entries'][i]['guid'] + "?view=scorecard;wrappertype=none;xhr=1", rss['entries'][i]['guid'] + "?innings=1;page=1;view=commentary;wrappertype=none", rss['entries'][i]['guid'] + "?innings=2;page=1;view=commentary;wrappertype=none"]
            team1Overs = 0.0
            team2Overs = 0.0
            # print scorecardURLs
            for url in scorecardURLs:
                (team1ScoreDetails, team2ScoreDetails) = getRunsWktsOvers(url)
                # print team1ScoreDetails
                # print team2ScoreDetails
                if team1ScoreDetails == None: continue
                if len(team1ScoreDetails) == 0: continue
                t1Runs = team1ScoreDetails['team1Runs']
                t1Wkts = team1ScoreDetails['team1Wkts']
                t1Overs = team1ScoreDetails['team1Overs']
                if t1Overs > team1Overs:
                    team1Runs = t1Runs
                    team1Wkts = t1Wkts
                    team1Overs = t1Overs

                if team2Name != "" and len(team2ScoreDetails) != 0:
                    t2Runs = team2ScoreDetails['team2Runs']
                    t2Wkts = team2ScoreDetails['team2Wkts']
                    t2Overs = team2ScoreDetails['team2Overs']
                    if t2Overs > team2Overs:
                        team2Runs = t2Runs
                        team2Wkts = t2Wkts
                        team2Overs = t2Overs

            if team1ScoreDetails == None: continue
            if len(team1ScoreDetails) == 0: continue

            matchOddsAdj = None
            if team2Name != "" and len(team2ScoreDetails) != 0:
                runsReq = team1Runs - team2Runs + 1
                # print team2Name + " " + `team2Runs` + " " + `team2Wkts` + " " + `team2Overs` + " " + `runsReq`

                # calculate innings 2 odds
                if matchType == "Twenty20":
                    ballsRem = 120 - team2Overs * 6
                    if ballsRem == 0: continue
                    try:
                        reqRate = runsReq * 1.04 / float(ballsRem / 6.0) # 4% adjustment since run-scoring easier since 2016
                    except ValueError:
                        continue

                    if ballsRem < 18:
                        c.execute('select avg(result), t20Id from overComparison where innings=2 and wkts='+`team2Wkts`+' and runsReq>='+`(runsReq*0.8)`+' and runsReq<'+`(runsReq*1.2)`+' and ballsRem<='+`(ballsRem+1)`+' and ballsRem>'+`(ballsRem-1)` + ' group by t20Id union '\
                        'select avg(result), t20Id from overComparison where innings=2 and wkts='+`(team2Wkts-1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.3)`+' and ballsRem<='+`(ballsRem+1)`+' and ballsRem>'+`(ballsRem-1)` + ' group by t20Id  union '\
                        'select avg(result), t20Id from overComparison where innings=2 and wkts='+`(team2Wkts+1)`+' and runsReq>='+`(runsReq*0.7)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem+1)`+' and ballsRem>'+`(ballsRem-1)` + ' group by t20Id ')
                    else:
                        c.execute('select avg(result), t20Id from overComparison where innings=2 and wkts='+`team2Wkts`+' and reqRate>='+`(reqRate*0.9)`+' and reqRate<'+`(reqRate*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id union '\
                        'select avg(result), t20Id from overComparison where innings=2 and wkts='+`(team2Wkts-1)`+' and reqRate>='+`(reqRate*0.95)`+' and reqRate<'+`(reqRate*1.15)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id  union '\
                        'select avg(result), t20Id from overComparison where innings=2 and wkts='+`(team2Wkts+1)`+' and reqRate>='+`(reqRate*0.85)`+' and reqRate<'+`(reqRate*1.05)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id ')
                else:
                    ballsRem = 300 - team2Overs * 6
                    if ballsRem == 0: continue
                    try:
                        reqRate = runsReq / float(ballsRem / 6.0)
                    except ValueError:
                        continue

                    if ballsRem < 18:
                        c.execute('select avg(result), odiId from overComparisonODI where odiId>=3000 and innings=2 and wkts='+`team2Wkts`+' and runsReq>='+`(runsReq*0.8)`+' and runsReq<'+`(runsReq*1.2)`+' and ballsRem<='+`(ballsRem+1)`+' and ballsRem>'+`(ballsRem-1)` + ' group by odiId union '\
                        'select avg(result), odiId from overComparisonODI where odiId>=3000 and innings=2 and wkts='+`(team2Wkts-1)`+' and runsReq>='+`(runsReq*0.9)`+' and runsReq<'+`(runsReq*1.3)`+' and ballsRem<='+`(ballsRem+1)`+' and ballsRem>'+`(ballsRem-1)` + ' group by odiId  union '\
                        'select avg(result), odiId from overComparisonODI where odiId>=3000 and innings=2 and wkts='+`(team2Wkts+1)`+' and runsReq>='+`(runsReq*0.7)`+' and runsReq<'+`(runsReq*1.1)`+' and ballsRem<='+`(ballsRem+1)`+' and ballsRem>'+`(ballsRem-1)` + ' group by odiId ')
                    else:
                        c.execute('select avg(result), odiId from overComparisonODI where odiId>=3000 and innings=2 and wkts='+`team2Wkts`+' and reqRate>='+`(reqRate*0.9)`+' and reqRate<'+`(reqRate*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by odiId union '\
                        'select avg(result), odiId from overComparisonODI where odiId>=3000 and innings=2 and wkts='+`(team2Wkts-1)`+' and reqRate>='+`(reqRate*0.95)`+' and reqRate<'+`(reqRate*1.15)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by odiId  union '\
                        'select avg(result), odiId from overComparisonODI where odiId>=3000 and innings=2 and wkts='+`(team2Wkts+1)`+' and reqRate>='+`(reqRate*0.85)`+' and reqRate<'+`(reqRate*1.05)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by odiId ')

                comp = c.fetchall()
                similarCount = len(comp)

                winCount = 0.0
                for j in range(0, len(comp)):
                    compResult = comp[j][0]
                    winCount = winCount + int(compResult) / 2
                matchOdds = 100 * winCount / similarCount if similarCount > 0 else None
                matchOdds = 100.0 if runsReq == 0 else matchOdds
                matchOdds = 0.0 if int(team2Overs) == 50 and runsReq != 0 else matchOdds
                matchOdds = 0.0 if int(team2Wkts) == 10 and runsReq != 0 else matchOdds
                matchOdds = 50.0 if matchOdds == None else matchOdds

                if matchOdds != None:
                    matchOdds = matchOdds / 100.0
                    oddsDiff = matchOdds - (1 - matchOdds)
                    matchOddsAdj = matchOdds

                    # team current ratings adjustment
                    if dbFormat != "FT20":
                        if team2StartingOdds >= 0.5:
                            oddsAdj = team2StartingOdds - 0.5
                            if matchOdds >= 0.5:
                                matchOddsAdj = matchOdds - oddsAdj * oddsDiff + oddsAdj
                            else:
                                matchOddsAdj = matchOdds + oddsAdj * oddsDiff + oddsAdj
                        elif team2StartingOdds < 0.5:
                            oddsAdj = 0.5 - team2StartingOdds
                            if matchOdds >= 0.5:
                                matchOddsAdj = matchOdds + oddsAdj * oddsDiff - oddsAdj
                            else:
                                matchOddsAdj = matchOdds - oddsAdj * oddsDiff - oddsAdj
                    matchOddsAdj = 100.0 * matchOddsAdj
                team1Name = teamNameChange[team1Name] if team1Name in teamNameChange.keys() else team1Name
                team2Name = teamNameChange[team2Name] if team2Name in teamNameChange.keys() else team2Name
                if team2Name in teamImpliedOdds and matchOdds is not None:
                    (teamBattingRating, teamBowlingRating) = getBattingBowlingRatings(team2Name, team1Name, dbFormat)
                    if matchType == "Twenty20":
                        battingRating = teamBattingRating * (40 - float(team2Overs)) / 40
                        if team2Wkts > 0:
                            for w in range(0, team2Wkts):
                                battingRating = battingRating - teamBattingRating * battingWktWeight[w]
                        battingRating = 0 if battingRating < 0 else battingRating
                        bowlingRating = teamBowlingRating * (20 - float(team2Overs)) / 20
                        liveData = [{'RunsReq': runsReq, 'Wkts': team2Wkts, 'MatchOdds': float(matchOdds), 'ReqRunRate': reqRate, 'BatBowlDiff': (battingRating - bowlingRating)}]
                        predictors = ["RunsReq", "Wkts", "MatchOdds", "ReqRunRate", "BatBowlDiff"]
                        df = pandas.DataFrame(liveData)
                        if team2Overs < 10:
                            mlOdds = t202early.predict_proba(df[predictors].astype(float))[:,1] * 100.0
                        else:
                            mlOdds = t202late.predict_proba(df[predictors].astype(float))[:,1] * 100.0
                    else:
                        battingRating = teamBattingRating * (100 - float(team2Overs)) / 100
                        if team2Wkts > 0:
                            for w in range(0, team2Wkts):
                                battingRating = battingRating - teamBattingRating * battingWktWeight[w]
                        battingRating = 0 if battingRating < 0 else battingRating
                        bowlingRating = teamBowlingRating * (50 - float(team2Overs)) / 50
                        liveData = [{'RunsReq': runsReq, 'Wkts': team2Wkts, 'MatchOdds': float(matchOdds), 'ReqRunRate': reqRate, 'TeamRatingDiff': (team1Rating - team2Rating), 'BatBowlDiff': (battingRating - bowlingRating)}]
                        predictors = ["RunsReq", "Wkts", "MatchOdds", "ReqRunRate", "TeamRatingDiff", "BatBowlDiff"]
                        df = pandas.DataFrame(liveData)
                        if team2Overs < 40:
                            mlOdds = odi2early.predict_proba(df[predictors].astype(float))[:,1] * 100.0
                        else:
                            mlOdds = odi2late.predict_proba(df[predictors].astype(float))[:,1] * 100.0

                    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    # print team1Name + " vs " + team2Name + ": " + team2Name + " " + `team2Runs` + "/" + `team2Wkts` + " (" + `int(team2Overs)` + " ov), Betfair Implied Odds: " + `round(teamImpliedOdds[team2Name], 2)` + "%, cricrate Odds: " + `round(matchOdds * 100, 2)` + "%, cricrate ML Odds: " + `round(mlOdds, 2)` + "%"
                    with open('liveOdds.csv', 'ab') as csvfile:
                        csvWriter = csv.writer(csvfile)
                        csvWriter.writerow([currentTime, matchType, team2Name, team1Name, 2, runsReq, team2Wkts, round(team2Overs, 2), round(reqRate, 2), round(teamImpliedOdds[team2Name], 2), round(matchOdds * 100, 2), round(mlOdds, 2), similarCount])
            elif team1Runs is not None:
                # calculate innings 1 odds
                try:
                    runRate = team1Runs / team1Overs
                except ValueError:
                    continue
                if matchType == "Twenty20":
                    runRate = team1Runs / (float(team1Overs) * 1.04) # 4% adjustment due to run scoring being easier since 2016
                    if team2Overs < 7:
                        c.execute('select avg(result), t20Id, runs, wkts, overs from overComparison where innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<='+`(team1Runs+2)`+' and runs>'+`(team1Runs-2)`+' and wkts='+`team1Wkts` + ' group by t20Id union '\
                        'select avg(result), t20Id, runs, wkts, overs from overComparison where innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<='+`(team1Runs+3)`+' and runs>'+`(team1Runs-1)`+' and wkts='+`(team1Wkts+1)` + ' group by t20Id union '\
                        'select avg(result), t20Id, runs, wkts, overs from overComparison where innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<='+`(team1Runs+1)`+' and runs>'+`(team1Runs-3)`+' and wkts='+`(team1Wkts-1)` + ' group by t20Id')
                    else:
                        c.execute('select avg(result), t20Id, runs, wkts, overs from overComparison where innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.1)`+' and runRate>'+`(runRate*0.9)`+' and wkts='+`team1Wkts` + ' group by t20Id union '\
                        'select avg(result), t20Id, runs, wkts, overs from overComparison where innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.15)`+' and runRate>'+`(runRate*0.95)`+' and wkts='+`(team1Wkts+1)` + ' group by t20Id union '\
                        'select avg(result), t20Id, runs, wkts, overs from overComparison where innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.05)`+' and runRate>'+`(runRate*0.85)`+' and wkts='+`(team1Wkts-1)` + ' group by t20Id')
                else:
                    if team2Overs < 11:
                        c.execute('select avg(result), odiId, runs, wkts, overs from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<='+`(team1Runs+2)`+' and runs>'+`(team1Runs-2)`+' and wkts='+`team1Wkts` + ' group by odiId union '\
                        'select avg(result), odiId, runs, wkts, overs from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<='+`(team1Runs+3)`+' and runs>'+`(team1Runs-1)`+' and wkts='+`(team1Wkts+1)` + ' group by odiId union '\
                        'select avg(result), odiId, runs, wkts, overs from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<='+`(team1Runs+1)`+' and runs>'+`(team1Runs-3)`+' and wkts='+`(team1Wkts-1)` + ' group by odiId')
                    else:
                        c.execute('select avg(result), odiId, runs, wkts, overs from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.1)`+' and runRate>'+`(runRate*0.9)`+' and wkts='+`team1Wkts` + ' group by odiId union '\
                        'select avg(result), odiId, runs, wkts, overs from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.15)`+' and runRate>'+`(runRate*0.95)`+' and wkts='+`(team1Wkts+1)` + ' group by odiId union '\
                        'select avg(result), odiId, runs, wkts, overs from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.05)`+' and runRate>'+`(runRate*0.85)`+' and wkts='+`(team1Wkts-1)` + ' group by odiId')

                comp = c.fetchall()
                similarCount = len(comp)
                winCount = 0.0
                for j in range(0, len(comp)):
                    compResult = comp[j][0]
                    resultString = ""
                    if compResult == 2:
                        resultString = "Win"
                    elif compResult == 1:
                        resultString = "Tie/NR"
                    else:
                        resultString = "Loss"
                    # print `comp[j][1]` + " " + `comp[j][2]` + "/" + `comp[j][3]` + " (" + `comp[j][4]` + " ov): " + resultString
                    winCount = winCount + int(compResult) / 2
                matchOdds = 100 * winCount / similarCount if similarCount > 0 else 50.0

                matchOddsAdj = 50.0
                if matchOdds != None:
                    matchOdds = matchOdds / 100.0
                    oddsDiff = matchOdds - (1 - matchOdds)
                    matchOddsAdj = matchOdds

                    # team current ratings adjustment
                    if dbFormat != "FT20":
                        if team1StartingOdds >= 0.5:
                            oddsAdj = team1StartingOdds - 0.5
                            if matchOdds >= 0.5:
                                matchOddsAdj = matchOdds - oddsAdj * oddsDiff + oddsAdj
                            else:
                                matchOddsAdj = matchOdds + oddsAdj * oddsDiff + oddsAdj
                        elif team1StartingOdds < 0.5:
                            oddsAdj = 0.5 - team1StartingOdds
                            if matchOdds >= 0.5:
                                matchOddsAdj = matchOdds + oddsAdj * oddsDiff - oddsAdj
                            else:
                                matchOddsAdj = matchOdds - oddsAdj * oddsDiff - oddsAdj
                    matchOddsAdj = 100.0 * matchOddsAdj

                team1Name = teamNameChange[team1Name] if team1Name in teamNameChange.keys() else team1Name
                team2Name = teamNameChange[team2Name] if team2Name in teamNameChange.keys() else team2Name
                if team1Name in teamImpliedOdds and matchOddsAdj is not None:
                    (teamBattingRating, teamBowlingRating) = getBattingBowlingRatings(team1Name, team2Name, dbFormat)
                    if matchType == "Twenty20":
                        battingRating = teamBattingRating * (40 - float(team1Overs)) / 40
                        if team1Wkts > 0:
                            for w in range(0, team1Wkts):
                                battingRating = battingRating - teamBattingRating * battingWktWeight[w]
                        battingRating = 0 if battingRating < 0 else battingRating
                        bowlingRating = teamBowlingRating * (20 - float(team1Overs)) / 20
                        liveData = [{'Runs': team1Runs, 'Wkts': team1Wkts, 'MatchOdds': float(matchOdds), 'RunRate': runRate, 'BatBowlDiff': (battingRating - bowlingRating)}]
                        predictors = ["Runs", "Wkts", "MatchOdds", "RunRate", "BatBowlDiff"]
                        df = pandas.DataFrame(liveData)
                        mlOdds = t201.predict_proba(df[predictors].astype(float))[:,1] * 100.0
                        # mlOdds = round(matchOdds * 100, 2)
                        # mlOdds = 75 if mlOdds >= 85 else mlOdds # adjust rating
                    else:
                        battingRating = teamBattingRating * (100 - float(team1Overs)) / 100
                        if team1Wkts > 0:
                            for w in range(0, team1Wkts):
                                battingRating = battingRating - teamBattingRating * battingWktWeight[w]
                        battingRating = 0 if battingRating < 0 else battingRating
                        bowlingRating = teamBowlingRating * (50 - float(team1Overs)) / 50
                        liveData = [{'Runs': team1Runs, 'Wkts': team1Wkts, 'MatchOdds': float(matchOdds), 'RunRate': runRate, 'TeamRatingDiff': (team1Rating - team2Rating), 'BatBowlDiff': (battingRating - bowlingRating)}]
                        predictors = ["Runs", "Wkts", "MatchOdds", "RunRate", "TeamRatingDiff", "BatBowlDiff"]
                        df = pandas.DataFrame(liveData)
                        if team1Overs < 11:
                            mlOdds = odi1early.predict_proba(df[predictors].astype(float))[:,1] * 100.0
                        else:
                            mlOdds = odi1late.predict_proba(df[predictors].astype(float))[:,1] * 100.0

                    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    # print team1Name + " vs " + team2Name + ": " + team1Name + " " + `team1Runs` + "/" + `team1Wkts` + " (" + `int(team1Overs)` + " ov), Betfair Implied Odds: " + `round(teamImpliedOdds[team1Name], 2)` + "%, cricrate Odds: " + `round(matchOdds * 100, 2)` + "%, cricrate ML Odds: " + `round(mlOdds, 2)` + "%"
                    with open('liveOdds.csv', 'ab') as csvfile:
                        csvWriter = csv.writer(csvfile)
                        csvWriter.writerow([currentTime, matchType, team1Name, team2Name, 1, team1Runs, team1Wkts, round(team1Overs, 2), round(runRate, 2), round(teamImpliedOdds[team1Name], 2), round(matchOdds * 100, 2), round(mlOdds, 2), similarCount])

    bucket_name = 'cricrate'
    conn = boto.connect_s3('AKIAJFA5625O5CW35Y4Q', '1Ks4FLRxgUTNSFOUnq67GL6e3yu3XZHLqq4P0IP1')

    bucket = conn.get_bucket(bucket_name)
    # bucket = conn.create_bucket(bucket_name,
    #     location=boto.s3.connection.Location.DEFAULT)

    # print 'Uploading %s to Amazon S3 bucket %s' % \
    #    ("liveOdds.csv", bucket_name)

    def percent_cb(complete, total):
        # sys.stdout.write('.')
        sys.stdout.flush()

    k = Key(bucket)
    k.key = "liveOdds.csv"
    k.set_contents_from_filename("liveOdds.csv", cb=percent_cb, num_cb=10)

    time.sleep(120)

# with open('scoresPricesOdds.csv', 'wb') as csvfile:
#     csvWriter = csv.writer(csvfile)
#     csvWriter.writerow(['Time', 'Format', 'Team', 'Opposition', 'Inn', 'Runs/RunsReq', 'Wkts', 'Overs', 'RunRate/ReqRate', 'BetfairOdds', 'cricrateOdds', 'AbsDiff', 'SimilarCount'])

while True:
    # use firefox to get page with javascript generated content
    # with closing(Chrome()) as browser:
    #      browser.get("https://www.betfair.com/exchange/plus/#/cricket/market/1.127499782")
    #      page_source = browser.page_source
    #      print(page_source)
    # asd
    scriptRunTime += 120
    if scriptRunTime < 172000:
        dumpScoresPricesOdds()
    else:
        sys.exit()

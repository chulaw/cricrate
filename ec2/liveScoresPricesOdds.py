#!/usr/bin/env python
import time
import datetime
import sqlite3
import csv
import feedparser
import requests
from lxml import html
import re
import boto
import boto.s3
import sys
from boto.s3.key import Key
# from selenium.webdriver import Chrome # pip install selenium
# from selenium.webdriver.support.ui import WebDriverWait

# import pandas
# from sklearn.linear_model import LogisticRegression
# from sklearn.cross_validation import KFold
# from sklearn import cross_validation
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# from sklearn.feature_selection import SelectKBest, f_classif
# from sklearn.metrics import f1_score, roc_auc_score
# from sklearn.grid_search import GridSearchCV
# import numpy as np
# import xgboost as xgb

start = time.clock()
teamNameChange = {'Chennai T20':'Chennai Super Kings', 'Delhi T20':'Delhi Daredevils', 'Punjab T20':'Kings XI Punjab', 'Bangalore':'Royal Challengers Bangalore', 'Hyderabad':'Sunrisers Hyderabad',
                    'Rajasthan':'Rajasthan Royals', 'Mumbai T20':'Mumbai Indians', 'Kolkata T20':'Kolkata Knight Riders', 'Super Kings':'Chennai Super Kings', 'Daredevils':'Delhi Daredevils',
                    'Kings XI':'Kings XI Punjab', 'RCB':'Royal Challengers Bangalore', 'Sunrisers':'Sunrisers Hyderabad', 'Royals':'Rajasthan Royals', 'Mum Indians':'Mumbai Indians', 'Scorchers':'Perth Scorchers',
                    'KKR':'Kolkata Knight Riders', 'Chargers':'Deccan Chargers', 'Kochi':'Kochi Tuskers Kerala', 'Warriors':'Pune Warriors', 'Tridents':'Barbados Tridents', 'Zouks':'St Lucia Zouks',
                    'Amazon':'Guyana Amazon Warriors', 'Red Steel':'Trinidad & Tobago Red Steel', 'Hawksbills':'Antigua Hawksbills', 'Tallawahs':'Jamaica Tallawahs', 'Melb Stars':'Melbourne Stars',
                    'Melb Reneg':'Melbourne Renegades', 'Syd Sixers':'Sydney Sixers', 'Syd Thunder':'Sydney Thunder', 'Hurricanes':'Hobart Hurricanes', 'Strikers':'Adelaide Strikers', 'Heat':'Brisbane Heat',
                    'Red Steel':'Trinidad & Tobago Red Steel', 'Patriots':'St Kitts and Nevis Patriots', 'Supergiants':'Rising Pune Supergiants', 'Guj Lions': 'Gujarat Lions', 'T&T Riders': 'Trinbago Knight Riders'}

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
    for i in range(0, len(rss['entries'])):
        scorecardURL = rss['entries'][i]['guid'] + "?view=scorecard;wrappertype=none;xhr=1"
        scorecardPage = requests.get(scorecardURL)
        scoreTree = html.fromstring(scorecardPage.text)
        matchDetails = scoreTree.xpath('(//a[@class="headLink"]/text())')[1]

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
            for url in scorecardURLs:
                (team1ScoreDetails, team2ScoreDetails) = getRunsWktsOvers(url)
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
                # print team2Name + " " + `team2Runs` + " " + `team2Wkts` + " " + `team2Overs` + " " + `runsReq` + " " + `ballsRem`

                # calculate innings 2 odds
                if matchType == "Twenty20":
                    ballsRem = 120 - team2Overs * 6
                    try:
                        reqRate = runsReq / float(ballsRem / 6.0)
                    except ValueError:
                        continue
                    c.execute('select avg(result), t20Id from overComparison where t20Id>=600 and innings=2 and wkts='+`team2Wkts`+' and reqRate>='+`(reqRate*0.9)`+' and reqRate<'+`(reqRate*1.1)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id union '\
                    'select avg(result), t20Id from overComparison where t20Id>=600 and innings=2 and wkts='+`(team2Wkts-1)`+' and reqRate>='+`(reqRate*0.95)`+' and reqRate<'+`(reqRate*1.15)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id  union '\
                    'select avg(result), t20Id from overComparison where t20Id>=600 and innings=2 and wkts='+`(team2Wkts+1)`+' and reqRate>='+`(reqRate*0.85)`+' and reqRate<'+`(reqRate*1.05)`+' and ballsRem<='+`(ballsRem*1.1)`+' and ballsRem>'+`(ballsRem*0.9)` + ' group by t20Id ')
                else:
                    ballsRem = 300 - team2Overs * 6
                    try:
                        reqRate = runsReq / float(ballsRem / 6.0)
                    except ValueError:
                        continue
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
                team2Name = teamNameChange[team2Name] if team1Name in teamNameChange.keys() else team2Name
                if team2Name in teamImpliedOdds and matchOddsAdj is not None:
                    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    # print team1Name + " vs " + team2Name + ": " + team2Name + " " + `team2Runs` + "/" + `team2Wkts` + " (" + `int(team2Overs)` + " ov), Betfair Implied Odds: " + `round(teamImpliedOdds[team2Name], 2)` + "%, cricrate Odds: " + `round(matchOddsAdj, 2)` + "%, Abs Diff: " + `round(abs(matchOddsAdj - teamImpliedOdds[team2Name]), 2)` + "%"
                    with open('liveOdds.csv', 'ab') as csvfile:
                        csvWriter = csv.writer(csvfile)
                        csvWriter.writerow([currentTime, matchType, team2Name, team1Name, 2, runsReq, team2Wkts, round(team2Overs, 2), round(reqRate, 2), round(teamImpliedOdds[team2Name], 2), round(matchOddsAdj, 2), round(abs(matchOddsAdj - teamImpliedOdds[team2Name]), 2), similarCount])
            elif team1Runs is not None:
                # calculate innings 1 odds
                try:
                    runRate = team1Runs / float(team1Overs)
                except ValueError:
                    continue
                if matchType == "Twenty20":
                    ballsRem = 120 - team2Overs * 6
                    if team1Runs < 50:
                        c.execute('select avg(result), t20Id, runs, wkts, overs from overComparison where t20Id>=600 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<=1 and wkts='+`team1Wkts`+ ' group by t20Id ')
                    else:
                        c.execute('select avg(result), t20Id, runs, wkts, overs  from overComparison where t20Id>=600 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.1)`+' and runRate>'+`(runRate*0.9)`+' and wkts='+`team1Wkts` + ' group by t20Id union '\
                        'select avg(result), t20Id, runs, wkts, overs from overComparison where t20Id>=600 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.15)`+' and runRate>'+`(runRate*0.95)`+' and wkts='+`(team1Wkts+1)` + ' group by t20Id union '\
                        'select avg(result), t20Id, runs, wkts, overs from overComparison where t20Id>=600 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.05)`+' and runRate>'+`(runRate*0.85)`+' and wkts='+`(team1Wkts-1)` + ' group by t20Id')
                else:
                    ballsRem = 300 - team2Overs * 6
                    if team1Runs < 50:
                        c.execute('select avg(result), odiId, runs, wkts, overs from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runs<=1 and wkts='+`team1Wkts`+ ' group by odiId ')
                    else:
                        c.execute('select avg(result), odiId, runs, wkts, overs  from overComparisonODI where odiId>=3000 and innings=1 and overs>='+`(team1Overs-1)`+' and overs<'+`(team1Overs+1)`+' and runRate<='+`(runRate*1.1)`+' and runRate>'+`(runRate*0.9)`+' and wkts='+`team1Wkts` + ' group by odiId union '\
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
                matchOdds = 100 * winCount / similarCount if similarCount > 0 else None

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
                team2Name = teamNameChange[team2Name] if team1Name in teamNameChange.keys() else team2Name
                if team1Name in teamImpliedOdds and matchOddsAdj is not None:
                    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    # print team1Name + " vs " + team2Name + ": " + team1Name + " " + `team1Runs` + "/" + `team1Wkts` + " (" + `int(team1Overs)` + " ov), Betfair Implied Odds: " + `round(teamImpliedOdds[team1Name], 2)` + "%, cricrate Odds: " + `round(matchOddsAdj, 2)` + "%, Abs Diff: " + `round(abs(matchOddsAdj - teamImpliedOdds[team1Name]), 2)` + "%"
                    with open('liveOdds.csv', 'ab') as csvfile:
                        csvWriter = csv.writer(csvfile)
                        csvWriter.writerow([currentTime, matchType, team1Name, team2Name, 1, team1Runs, team1Wkts, round(team1Overs, 2), round(runRate, 2), round(teamImpliedOdds[team1Name], 2), round(matchOddsAdj, 2), round(abs(matchOddsAdj - teamImpliedOdds[team1Name]), 2), similarCount])

    bucket_name = 'cricrate'
    conn = boto.connect_s3('AKIAJFA5625O5CW35Y4Q',
            '1Ks4FLRxgUTNSFOUnq67GL6e3yu3XZHLqq4P0IP1')

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
#     csvWriter.writerow(['Time', 'Format', 'Team', 'Opposition', 'Inn', 'Runs/RunsReq', 'Wkts', 'Overs', 'RunRate/ReqRate', 'BetfairOdds', 'cricrateOdds', 'cricrateMLOdds', 'SimilarCount'])

while True:
    # use firefox to get page with javascript generated content
    # with closing(Chrome()) as browser:
    #      browser.get("https://www.betfair.com/exchange/plus/#/cricket/market/1.127499782")
    #      page_source = browser.page_source
    #      print(page_source)
    # asd
    dumpScoresPricesOdds()

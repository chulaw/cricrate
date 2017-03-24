#!/usr/bin/env python
import time
import sqlite3
import csv
import feedparser
import requests
from lxml import html
import re

start = time.clock()

rss = feedparser.parse('http://static.cricinfo.com/rss/livescores.xml')

for i in range(0, len(rss['entries'])):
    scorecardURL = rss['entries'][i]['guid'] + "?view=scorecard;wrappertype=none;xhr=1"
    scorecardPage = requests.get(scorecardURL)
    scoreTree = html.fromstring(scorecardPage.text)

    matchDetails = scoreTree.xpath('(//a[@class="headLink"]/text())')[1]

    if "Test" in matchDetails or "First-class" in matchDetails:
        matchType = "Test"
    elif "ODI" in matchDetails or "One-Day" in matchDetails or "List A" in matchDetails:
        matchType = "One-Day"
    elif "Twenty20" in matchDetails or "T20I" in matchDetails:
        matchType = "Twenty20"

    team1Name = scoreTree.xpath('(//div[@class="team-1-name"]/text())')[0].strip()
    team1Score = scoreTree.xpath('(//div[@class="team-1-name"]/span/text())')
    team1Score2 = scoreTree.xpath('(//div[@class="team-1-name"]/span/span/text())')
    if len(team1Score) != 1:
        if len(team1Score2) == 1:
            team1Score = team1Score2[0]
        else: team1Score = ""
    else:
        team1Score = team1Score[0]
    team2Name = scoreTree.xpath('(//div[@class="team-2-name"]/text())')

    # print matchDetails
    if len(team2Name) == 0: continue
    team2Name = team2Name[0].strip()
    team2Score = scoreTree.xpath('(//div[@class="team-2-name"]/span/text())')
    team2Score2 = scoreTree.xpath('(//div[@class="team-2-name"]/span/span/text())')
    if len(team2Score) != 1:
        if len(team2Score2) == 1:
            team2Score = team2Score2[0]
        else:
            team2Score = ""
    else:
        team2Score = team2Score[0]
    matchResult = scoreTree.xpath('(//div[@class="innings-requirement"]/text())')[0]

    if "won by" in matchResult or "tied" in matchResult or "drawn" in matchResult: continue

    # print team1Name + " " +  team1Score + " " + team2Name + " " + team2Score + " " + matchResult + " " + matchType

    # if matchType == "Test":
    #     # firstNumPos = re.search("\d", team1Score)
    #     team1ScoreOvers = team1Score.split(" ")
    #     if team1ScoreOvers[0] == "": continue
    #     team1RunsWkts = team1ScoreOvers[0].split("/")
    #     team1Runs = team1RunsWkts[0]
    #     team1Wkts = 10 if len(team1RunsWkts) == 1 else team1RunsWkts[1]
    #     team1Overs = ""
    #     if len(team1ScoreOvers) > 1:
    #         team1OversDetails = team1ScoreOvers[1].split(".")
    #         team1Overs = float(team1OversDetails[0][1:]) + float(team1OversDetails[1]) / 6
    #
    #     if team2Name != "":
    #         team2ScoreOvers = team2Score.split(" ")
    #         if team2ScoreOvers[0] == "": continue
    #         team2RunsWkts = team2ScoreOvers[0].split("/")
    #         team2Runs = team2RunsWkts[0]
    #         team2Wkts = 10 if len(team2RunsWkts) == 1 else team2RunsWkts[1]
    #         team2Overs = ""
    #         if len(team2ScoreOvers) > 1:
    #             team2OversDetails = team2ScoreOvers[1].split(".")
    #             print team2OversDetails
    #             team2Overs = float(team2OversDetails[0][1:]) + float(team2OversDetails[1]) / 6
    if matchType == "One-Day":
        # team1NameFirstNum = re.search("\d", team1Name)
        # team1Name = team1Name[0:team1NameFirstNum.start()] if team1NameFirstNum != None else team1Name
        team1ScoreOvers = team1Score.split(" ")
        if team1ScoreOvers[0] == "": continue
        team1RunsWkts = team1ScoreOvers[0].split("/")
        team1Runs = int(team1RunsWkts[0])
        team1Wkts = 10 if len(team1RunsWkts) == 1 else int(team1RunsWkts[1])
        team1Overs = ""
        if len(team1ScoreOvers) > 1:
            if "." not in team1ScoreOvers[1]:
                team1Overs = float(team1ScoreOvers[1][1:])
            elif "/" in team1ScoreOvers[1]:
                continue
            else:
                team1OversDetails = team1ScoreOvers[1].split(".")
                team1Overs = float(team1OversDetails[0][1:]) + float(team1OversDetails[1]) / 6
        print team1Name + " " + `team1Runs` + " " + `team1Wkts` + " " + `team1Overs`

        team2ScoreOvers = team2Score.split(" ")
        if team2Name != "" and team2ScoreOvers[0] != "":
            # team2NameFirstNum = re.search("\d", team2Name)
            # team2Name = team2Name[0:team2NameFirstNum.start()] if team2NameFirstNum != None else team2Name
            team2RunsWkts = team2ScoreOvers[0].split("/")
            team2Runs = int(team2RunsWkts[0])
            team2Wkts = 10 if len(team2RunsWkts) == 1 else int(team2RunsWkts[1])
            team2Overs = ""
            if len(team2ScoreOvers) > 1:
                if "." not in team2ScoreOvers[1]:
                    team2Overs = float(team2ScoreOvers[1][1:])
                elif "/" in team2ScoreOvers[1]:
                    continue
                else:
                    team2OversDetails = team2ScoreOvers[1].split(".")
                    team2Overs = float(team2OversDetails[0][1:]) + float(team2OversDetails[1]) / 6

            runsReq = team1Runs - team2Runs + 1
            ballsRem = 300 - team2Overs * 6
            print team2Name + " " + `team2Runs` + " " + `team2Wkts` + " " + `team2Overs` + " " + `runsReq` + " " + `ballsRem`

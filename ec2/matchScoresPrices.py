import urllib2
import json
import datetime
import requests
import time
import csv
import re
import feedparser
from lxml import html

def callAping(url, request):
    try:
        req = urllib2.Request(url, request, headers)
        response = urllib2.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse

    except urllib2.URLError:
        print 'Oops there is some issue with the request'
        exit()
    except urllib2.HTTPError:
        print 'Oops there is some issue with the request' + urllib2.HTTPError.getcode()
        exit()

def getMarketCatalogue(eventTypeID):
    endPoint = 'https://api.betfair.com/exchange/betting/rest/v1.0/listMarketCatalogue/'
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    market_catalouge_req = '{"filter":{"eventTypeIds":["' + eventTypeID + '"],"marketTypeCodes":["MATCH_ODDS"],'\
                                                                          '"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START","maxResults":"10","marketProjection":["RUNNER_METADATA"]}'
    market_catalouge_response = callAping(endPoint, market_catalouge_req)
    market_catalouge_loads = json.loads(market_catalouge_response)
    return market_catalouge_loads

def getMarketIds(marketCatalogueResult):
    marketIds = []
    if(marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            marketIds.append(market['marketId'])
        return marketIds

def getSelectionId(marketCatalogueResult):
    if(marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            return market['runners'][0]['selectionId']

def getId2Team(marketCatalogueResult):
    id2Teams = {}
    if(marketCatalogueResult is not None):
        for market in marketCatalogueResult:
            id2Teams[market['runners'][0]['selectionId']] = market['runners'][0]['runnerName']
            id2Teams[market['runners'][1]['selectionId']] = market['runners'][1]['runnerName']
        return id2Teams

def getMarketBook(marketId):
    if( marketId is not None):
        print '\n'
        market_book_req = '{"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}'
        endPoint = 'https://api.betfair.com/exchange/betting/rest/v1.0/listMarketBook/'
        market_book_response = callAping(endPoint, market_book_req)
        market_book_loads = json.loads(market_book_response)
        return market_book_loads

def printPriceInfo(market_book_result, marketId, id2Team, teamScores):
    for marketBook in market_book_result:
        try:
            runners = marketBook['runners']
            for runner in runners:
                if (runner['status'] == 'ACTIVE'):
                    currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    team = id2Team[runner['selectionId']]
                    backPrice = runner['ex']['availableToBack'][0]['price']
                    backSize = runner['ex']['availableToBack'][0]['size']
                    layPrice = runner['ex']['availableToLay'][0]['price']
                    laySize = runner['ex']['availableToLay'][0]['size']
                    impliedOdds = round(200 / (backPrice + layPrice), 2)
                    liveScores = teamScores[team]
                    print 'Team: ' + team + ', Implied Odds: ' + `impliedOdds` + '%' + ', Back Price: ' + `backPrice` + ', Lay Price: ' + `layPrice` + ', Innings: ' + `liveScores[0]` + ', Runs: ' + `liveScores[1]` + ', Wkts: ' + `liveScores[2]` + ', Overs: ' + `liveScores[3]` + ', RunsReq: ' + `liveScores[4]` + ', BallsRem: ' + `liveScores[5]`

                    with open('scoresPrices.csv', 'ab') as csvfile:
                        csvWriter = csv.writer(csvfile)
                        csvWriter.writerow([marketId, currentTime, team, backPrice, layPrice, backSize, laySize, impliedOdds, liveScores[0], liveScores[1], liveScores[2], liveScores[3], liveScores[4], liveScores[5]])
                else:
                    print 'This runner is not active'
        except:
            print ''

appKey = 'OQplzjisTMojes3u'
url = 'https://identitysso.betfair.com/api/login'
payload = { 'username' : 'chinthanas@hotmail.com', 'password' : 'Chula1985' }
headers = {'Accept': 'application/json', 'X-Application': appKey}
res = requests.post(url, data=payload, headers=headers)
sessionToken = json.loads(res.text)["token"]
headers = {'X-Application': appKey, 'X-Authentication': sessionToken, 'content-type': 'application/json',
           'accept': 'application/json'}

marketCatalogueResult = getMarketCatalogue('4') # cricket event id = 4
marketIds = getMarketIds(marketCatalogueResult)
runnerId = getSelectionId(marketCatalogueResult)
id2Team = getId2Team(marketCatalogueResult)

with open('scoresPrices.csv', 'wb') as csvfile:
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(['MarketId', 'Time', 'Team', 'BackPrice', 'LayPrice', 'BackSize', 'LaySize', 'ImpliedOdds', 'Inn', 'Runs', 'Wkts', 'Overs', 'RunsReq', 'BallsRem'])

def getLiveScores():
    rss = feedparser.parse('http://static.cricinfo.com/rss/livescores.xml')

    teamScores = {}
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

        if matchType == "One-Day":
            team1ScoreOvers = team1Score.split(" ")
            if team1ScoreOvers[0] == "": continue
            team1RunsWkts = team1ScoreOvers[0].split("/")
            team1Runs = int(team1RunsWkts[0])
            team1Wkts = 10 if len(team1RunsWkts) == 1 else int(team1RunsWkts[1])
            team1Overs = ""
            if len(team1ScoreOvers) > 1:
                if "." not in team1ScoreOvers[1]:
                    team1Overs = float(team1ScoreOvers[1][1:])
                else:
                    team1OversDetails = team1ScoreOvers[1].split(".")
                    team1Overs = float(team1OversDetails[0][1:]) + float(team1OversDetails[1]) / 6

            if team2Name != "":
                team2ScoreOvers = team2Score.split(" ")
                if team2ScoreOvers[0] == "": continue
                team2RunsWkts = team2ScoreOvers[0].split("/")
                team2Runs = int(team2RunsWkts[0])
                team2Wkts = 10 if len(team2RunsWkts) == 1 else int(team2RunsWkts[1])
                team2Overs = ""
                if len(team2ScoreOvers) > 1:
                    if "." not in team2ScoreOvers[1]:
                        team2Overs = float(team2ScoreOvers[1][1:])
                    else:
                        team2OversDetails = team2ScoreOvers[1].split(".")
                        team2Overs = float(team2OversDetails[0][1:]) + float(team2OversDetails[1]) / 6

                runsReq = team1Runs - team2Runs + 1
                ballsRem = 300 - team2Overs * 6

            # print team1Name + " " + `team1Runs` + " " + `team1Wkts` + " " + `team1Overs`
            # print team2Name + " " + `team2Runs` + " " + `team2Wkts` + " " + `team2Overs` + " " + `runsReq` + " " + `ballsRem`
            teamScores[team1Name] = [1, team1Runs, team1Wkts, team1Overs, 0, 0]
            teamScores[team1Name] = [2, team2Runs, team2Wkts, team2Overs, runsReq, ballsRem]
    return teamScores

def matchScoresPrices(marketIds, teamScores):
    for marketId in marketIds:
        market_book_result = getMarketBook(marketId)
        printPriceInfo(market_book_result, marketId, id2Team, teamScores)
    time.sleep(300)

while True:
    teamScores = getLiveScores()
    matchScoresPrices(marketIds, teamScores)

# placeBet(marketid, runnerId)

# def placeBet(marketId, selectionId):
#     if( marketId is not None and selectionId is not None):
#         place_order_Req = '{"marketId":"' + marketId + '","instructions":'\
#                                                        '[{"selectionId":"' + str(
#             selectionId) + '","handicap":"0","side":"BACK","orderType":"LIMIT","limitOrder":{"size":"0.01","price":"1.50","persistenceType":"LAPSE"}}],"customerRef":"test12121212121"}'
#         endPoint = 'https://beta-api.betfair.com/rest/v1.0/placeOrders/'
#         place_order_Response = callAping(endPoint, place_order_Req)
#         place_order_load = json.loads(place_order_Response)
#         print 'Place order status is ' + place_order_load['status']
#         print 'Place order error status is ' + place_order_load['errorCode']
#         print 'Reason for Place order failure is ' + place_order_load['instructionReports'][0]['errorCode']
#         print place_order_Response

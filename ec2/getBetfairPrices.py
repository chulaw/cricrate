import urllib2
import json
import datetime
import requests
import time
import csv


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
                                                                          '"marketStartTime":{"from":"' + now + '"}},"inPlayOnly":"True","sort":"FIRST_TO_START","maxResults":"10","marketProjection":["RUNNER_METADATA"]}'
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

def printPriceInfo(market_book_result, marketId, id2Team):
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
                    with open('betfairPrices.csv', 'ab') as csvfile:
                        csvWriter = csv.writer(csvfile)
                        csvWriter.writerow([marketId, currentTime, team, backPrice, layPrice, backSize, laySize, impliedOdds])
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
print sessionToken
marketCatalogueResult = getMarketCatalogue('4') # cricket event id = 4
marketIds = getMarketIds(marketCatalogueResult)
print marketIds
runnerId = getSelectionId(marketCatalogueResult)
id2Team = getId2Team(marketCatalogueResult)

with open('betfairPrices.csv', 'wb') as csvfile:
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(['MarketId', 'Time', 'Team', 'BackPrice', 'LayPrice', 'BackSize', 'LaySize', 'ImpliedOdds'])

def getBetfairPrices(marketIds):
    for marketId in marketIds:
        market_book_result = getMarketBook(marketId)
        printPriceInfo(market_book_result, marketId, id2Team)
    time.sleep(300)

while True:
    getBetfairPrices(marketIds)

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

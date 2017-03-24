#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

seriesURL = 'http://stats.espncricinfo.com/ci/content/records/335431.html'
seriesPage = requests.get(seriesURL)
seriesTree = html.fromstring(seriesPage.text)

# seriesAll = seriesTree.xpath('(//table[@class="engineTable"]/tbody/tr[@class="data1"]')
# data1 = yearTree.xpath('//a[@class="data-link"]/text()')
data1 = seriesTree.xpath('//td[@nowrap="nowrap"]/text()')
data2 = seriesTree.xpath('//a[@class="data-link"]/text()')
links = seriesTree.xpath('//a[@class="data-link"]/@href')

seriesMatches = []
for i in range(1, len(data1)):
    if ("(" in data1[i]):
        seriesMatches.append(data1[i])

seriesMatches.insert(39, "0-0 (9)") # triangular tournament
seriesMatches.insert(206, "1-0 (1)")
seriesMatches.insert(225, "1-0 (1)")
seriesMatches.insert(229, "0-0 (1)")
seriesMatches.insert(288, "0-0 (1)")
seriesMatches.insert(357, "0-0 (1)")
seriesMatches.insert(411, "0-0 (4)") # asian test championship pak-draw-draw-pak
seriesMatches.insert(463, "0-0 (3)") # asian test championship pak-sl-sl
del seriesMatches[38]
del seriesMatches[37]
del seriesMatches[36]
seriesMatches[170] = "2-0 (6)"
seriesMatches[403] = "1-0 (2)"

seriesLinks = []
for i in range(0, len(links), 2):
    seriesLinks.append(links[i])

seriesDescs = []
for i in range(0, len(data2), 2):
    seriesDescs.append(data2[i])

#on-going test series
del seriesDescs[-1]
del seriesDescs[-1]
del seriesDescs[38]
del seriesDescs[37]
del seriesDescs[36]

del seriesLinks[-1]
del seriesLinks[-1]
del seriesLinks[38]
del seriesLinks[37]
del seriesLinks[36]

# conn = sqlite3.connect('ccr.db')
# c = conn.cursor()
# c.execute('select testId, team1, team2, result from testInfo where scoreLink = ?',('/ci/engine/match/63101.html', ))
# testsInfo = c.fetchone()
# print testsInfo
# asd
del seriesMatches[-1]
# print seriesMatches
# print seriesDescs
# print seriesLinks
# print len(seriesMatches)
# print len(seriesDescs)
# print len(seriesLinks)
# asd

scorecardURLOrder = []
for seriesLink in seriesLinks:
    seriesLinkURL = 'http://www.espncricinfo.com/'+ seriesLink
    seriesLinkPage = requests.get(seriesLinkURL)
    seriesLinkTree = html.fromstring(seriesLinkPage.text)
    scorecards = seriesLinkTree.xpath('//a[@class="potMatchMenuLink"]/@href')
    scorecards = [x for x in scorecards if "match" in x]
    for scorecard in scorecards:
        if scorecard == '/ci/engine/match/64135.html': continue
        if scorecard == '/ci/engine/match/64136.html': continue
        if scorecard == '/ci/engine/match/64137.html': continue
        if scorecard == '/ci/engine/match/64138.html': continue
        if scorecard == '/ci/engine/match/64139.html': continue
        if scorecard == '/ci/engine/match/64140.html': continue
        if scorecard == '/ci/engine/match/64141.html': continue
        if scorecard == '/ci/engine/match/64142.html': continue
        if scorecard == '/ci/engine/match/64143.html': continue
        if scorecard == '/ci/engine/match/64144.html': continue
        if scorecard == '/ci/engine/match/64145.html': continue
        if scorecard == '/ci/engine/match/64146.html': continue
        if scorecard == '/ci/engine/match/64147.html': continue
        if '/ci/engine' not in scorecard: scorecard = '/ci' + scorecard[scorecard.find('/engine'):]
        scorecardURLOrder.append(scorecard)

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()
#c.execute('''create table testInfo (testId integer unique, startDate text, location text, team1 text, team2 text, season text, ground text, ballsPerOver integer, result text, margin text, series text,
#          seriesStatus text, scoreLink text)''')

testNum = 0
for s in range(0, len(seriesMatches)):
    seriesDesc = seriesDescs[s]
    seriesDetails = seriesMatches[s].split("(")
    seriesMatchCount = int(seriesDetails[1].replace(")", ""))
    print seriesDetails[0]
    # print seriesMatchCount
    # print seriesDesc
    # print seriesMatchCount
    seriesDelta = 0
    seriesTeam1 = ""
    seriesTeam2 = ""
    for t in range(1, seriesMatchCount+1):
        # print t
        # print `(testNum+1)` + ' ' + scorecardURLOrder[testNum]
        c.execute('select testId, team1, team2, result from testInfo where scoreLink = ?',(scorecardURLOrder[testNum], ))
        testsInfo = c.fetchone()

        testId = testsInfo[0]
        result = testsInfo[3]
        if t == 1:
            seriesTeam1 = testsInfo[1]
            seriesTeam2 = testsInfo[2]

        testNum += 1
        seriesStatus = "All-to-Play-for"
        if seriesMatchCount == 1: seriesStatus = "Decider"
        if seriesMatchCount == 2 and t == 2: seriesStatus = "Decider"
        if seriesMatchCount == 3 and t == 2 and abs(seriesDelta) == 1 : seriesStatus = "Decider"
        if seriesMatchCount == 3 and t == 3 and abs(seriesDelta) > 1 : seriesStatus = "Dead"
        if seriesMatchCount == 3 and t == 3 and abs(seriesDelta) <= 1 : seriesStatus = "Decider"
        if seriesMatchCount == 4 and t == 3 and abs(seriesDelta) >= 1 : seriesStatus = "Decider"
        if seriesMatchCount == 4 and t == 4 and abs(seriesDelta) > 1 : seriesStatus = "Dead"
        if seriesMatchCount == 4 and t == 4 and abs(seriesDelta) <= 1 : seriesStatus = "Decider"
        if seriesMatchCount == 5 and t == 3 and abs(seriesDelta) > 1: seriesStatus = "Decider"
        if seriesMatchCount == 5 and t == 4 and abs(seriesDelta) >= 1: seriesStatus = "Decider"
        if seriesMatchCount == 5 and t == 4 and abs(seriesDelta) > 2: seriesStatus = "Dead"
        if seriesMatchCount == 5 and t == 5 and abs(seriesDelta) > 1: seriesStatus = "Dead"
        if seriesMatchCount == 5 and t == 5 and abs(seriesDelta) <= 1: seriesStatus = "Decider"
        if seriesMatchCount == 6 and t == 4 and abs(seriesDelta) > 2: seriesStatus = "Decider"
        if seriesMatchCount == 6 and t == 5 and abs(seriesDelta) > 2: seriesStatus = "Dead"
        if seriesMatchCount == 6 and t == 5 and abs(seriesDelta) == 2: seriesStatus = "Decider"
        if seriesMatchCount == 6 and t == 6 and abs(seriesDelta) > 1: seriesStatus = "Dead"
        if seriesMatchCount == 6 and t == 6 and abs(seriesDelta) <= 1: seriesStatus = "Decider"

        # tournaments
        if testId in (121, 122, 123, 124, 125, 126, 127, 128, 129, 1444, 1445, 1447, 1560, 1561): seriesStatus = "All-to-Play-for"
        if testId in (1450, 1592): seriesStatus = "Decider"

        if result == seriesTeam1:
            seriesDelta = seriesDelta + 1
        if result == seriesTeam2:
            seriesDelta = seriesDelta - 1

        print `testId` + ' : ' + seriesDesc + ' : ' + seriesTeam1 + ' vs ' + seriesTeam2 + ' : ' + result + ' : ' + `seriesDelta` + ' : ' + seriesStatus
        c.execute('update testInfo set series=?,seriesStatus=? where testId=?', (seriesDesc, seriesStatus, testId))

conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')

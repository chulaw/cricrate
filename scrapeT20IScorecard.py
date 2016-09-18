#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

startT20I = int(input('Enter starting T20I #: '))

# connect to db
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()

# get t20is info
c.execute('select * from t20iInfo')
t20isInfo = c.fetchall()

def dumpInningsDetails(inningsNum, teamBat, teamBowl, playerLinksBat, playersBat, dismissalsBat, runsBat, minutesBat, ballsBat, foursBat, sixesBat, totalBat, totalDetails, fow, playerLinksBowl, detailsBowl):
    print '\nDumping details for innings #'+`inningsNum`
    print 'Bowling details:'

    # parse innings total runs, wickets and overs (balls)
    wktOrder = {}
    retiredNotOut = {}
    totalWktsOvers = totalDetails.split(';')
    inningsEndDetail = totalWktsOvers[0].replace('(','')
    if inningsEndDetail == 'all out':
        totalWkts = 10
    else: totalWkts = int(inningsEndDetail.split()[0])
    totalBalls = totalWktsOvers[1].strip().split()[0]
    if '.' in totalBalls:
        totalBalls = int(totalBalls.split('.')[0]) * 6 + int(totalBalls.split('.')[1])
    else:
        totalBalls = int(totalBalls) * 6    
    if len(totalWktsOvers) == 3:
        totalMinutes = totalWktsOvers[2].replace(')','').split()[0]
    else: totalMinutes = 0
    extras = runsBat[len(runsBat)-1]    
    
    inningsId = `int(t20iId)` + `inningsNum`
    c.execute('''insert or ignore into detailsT20IInnings (inningsId, t20iId, innings, batTeam, bowlTeam, extras, runs, balls, minutes, wickets, inningsEndDetail) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (inningsId, t20iId, inningsNum, teamBat, teamBowl, extras, totalBat, totalBalls, totalMinutes, totalWkts, inningsEndDetail))

    # store bowling innings
    modDetailsBowl1 = []
    for ii in detailsBowl:
      if not '(' in ii: modDetailsBowl1.append(ii)
    detailsBowl = modDetailsBowl1
    for j in range(len(playerLinksBowl)):
        bowlerId = int(playerLinksBowl[j].split('/')[4].split('.')[0])
        bowlerURL = 'http://www.espncricinfo.com' + playerLinksBowl[j]
        bowlerPage = requests.get(bowlerURL)
        bowlerTree = html.fromstring(bowlerPage.text)    
        bowlerName = bowlerTree.xpath('(//div[@class="ciPlayernametxt"]/div/h1/text())')[0]
        bowlerFullName = bowlerTree.xpath('(//p[@class="ciPlayerinformationtxt"]/span/text())')[0]        
        
        c.execute('select playerId from playerInfo where cid=?', (bowlerId,))
        playerId = c.fetchone()        
        if playerId is None:            
            playerId = bowlerId * 2 + 3 # change id
            c.execute('insert or ignore into playerInfo (playerId, player, fullName, country, cid) values (?, ?, ?, ?, ?)', (playerId, bowlerName, bowlerFullName, teamBowl, bowlerId))                
        else: playerId = playerId[0]

        if t20iId in (436, 437, 438, 446):
            maidens = int(detailsBowl[1+j*6])
            runsConceded = int(detailsBowl[2+j*6])
            wkts = int(detailsBowl[3+j*6])
            if '.' in detailsBowl[j*6]:
                ballsBowled = int(detailsBowl[j*6].split('.')[0]) * 6 + int(detailsBowl[j*6].split('.')[1])
            else:
                ballsBowled = int(detailsBowl[j*6]) * 6
        elif t20iId in (3, 9, 14, 17, 18, 19, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79, 128, 129, 130, 131, 132, 133, 135, 136, 137, 138, 139, 140, 141, 142, 143, 219, 224, 225, 227, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 249, 250, 251, 252, 253, 254, 269, 282, 290, 295, 301, 302, 304, 307, 309, 310, 311, 313, 314, 319, 320, 330, 332, 333, 335, 337, 338, 339, 342, 344, 345, 346, 347, 348, 349, 359, 360, 410, 419, 420, 421, 422, 424, 425, 426, 427, 458, 459, 464, 465, 466, 467, 470, 471, 472, 487, 488, 490, 491, 492, 493, 494, 495, 498, 500, 501, 502, 504, 505, 507, 508, 564):
            maidens = int(detailsBowl[1+j*5])
            runsConceded = int(detailsBowl[2+j*5])
            wkts = int(detailsBowl[3+j*5])
            if '.' in detailsBowl[j*5]:
                ballsBowled = int(detailsBowl[j*5].split('.')[0]) * 6 + int(detailsBowl[j*5].split('.')[1])
            else:
                ballsBowled = int(detailsBowl[j*5]) * 6
        else:
            maidens = int(detailsBowl[1+j*8])
            runsConceded = int(detailsBowl[2+j*8])
            wkts = int(detailsBowl[3+j*8])
            if '.' in detailsBowl[j*8]:
                ballsBowled = int(detailsBowl[j*8].split('.')[0]) * 6 + int(detailsBowl[j*8].split('.')[1])
            else:
                ballsBowled = int(detailsBowl[j*8]) * 6
        
        if result == teamBowl:
            resultNum = 2
        elif result == 'Tie/NR':
            resultNum = 1
        else:
            resultNum = 0
            
        if teamBowl == location:
            homeAway = 0
        else:
            homeAway = 1
        
        inningsId = `int(t20iId)` + `inningsNum` + `playerId`
        c.execute('''insert or ignore into bowlingT20IInnings (inningsId, playerId, player, t20iId, innings, position, wkts, balls, maidens, runs, homeAway, result)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (inningsId, playerId, bowlerName, t20iId, inningsNum, (j+1), wkts, ballsBowled, maidens, runsConceded, homeAway, resultNum))      
        
        print `inningsId`+",",`playerId`+", "+`inningsNum`+", "+bowlerName+", wkts: "+`wkts`+'/'+`runsConceded`
        
    # parse batsmen fall of wicket order
    for k in range(len(fow)):
        batsmenFoW = fow[k].split('(')[1].replace(')','')
        player = batsmenFoW.split(',')[0]
        if 'retired not out' in batsmenFoW:
            retiredNotOut[player] = 1
        wktOrder[player] = k
        
        overs = batsmenFoW.split(',')
        if len(overs) == 2:
            overs = overs[1].split()[0]
            if 'retired' in overs:
                balls = None
            else:
                if '.' in overs:
                    balls = int(overs.split('.')[0]) * 6 + int(overs.split('.')[1])
                else:
                    balls = int(overs) * 6
        else: balls = None
        wicket = fow[k].split('(')[0].strip().split('-')[0]
        runs = fow[k].split('(')[0].strip().split('-')[1]        
        
        fowId = `int(t20iId)` + `inningsNum` + `(k+1)`
        c.execute('''insert or ignore into fowT20IInnings (fowId, t20iId, innings, runs, wicket, player, balls) values (?, ?, ?, ?, ?, ?, ?)''',
                (fowId, t20iId, inningsNum, runs, wicket, player, balls))
        
    print '\nBatting details:'
    # store batting innings
    b = 0 # balls index to parse
    for i in range(len(playerLinksBat)):
        batsmanId = int(playerLinksBat[i].split('/')[4].split('.')[0])
        batsmanURL = 'http://www.espncricinfo.com' + playerLinksBat[i]
        batsmanPage = requests.get(batsmanURL)
        batsmanTree = html.fromstring(batsmanPage.text)
        batsmanName = batsmanTree.xpath('(//div[@class="ciPlayernametxt"]/div/h1/text())')[0]
        batsmanFullName = batsmanTree.xpath('(//p[@class="ciPlayerinformationtxt"]/span/text())')[0]
        
        c.execute('select playerId from playerInfo where cid=?', (batsmanId,))    
        playerId = c.fetchone()        
        if playerId is None:
            playerId = batsmanId * 2 + 3 # change id
            c.execute('insert or ignore into playerInfo (playerId, player, fullName, country, cid) values (?, ?, ?, ?, ?)', (playerId, batsmanName, batsmanFullName, teamBat, batsmanId))
        else: playerId = playerId[0]
        
        dismissalInfo = dismissalsBat[i].strip()
        if dismissalInfo == 'not out':
            notOut = 1
        else:
            notOut = 0
        if runsBat[i] == '-': continue
        totalPct = float(runsBat[i]) * 100 / float(totalBat) if float(totalBat) > 0 else 0.0

        minutes = minutesBat[i]
        balls = ballsBat[i]
        fours = foursBat[i]
        sixes = sixesBat[i]

        if i < 2 :
            entryRuns = 0
            entryWkts = 0
        else:
            entryRuns = int(fow[i-2].split('-')[1].split()[0].replace('*',''))
            entryWkts = int(fow[i-2].split('-')[0])
        
        lastName = playersBat[i] if len(playersBat[i].split()) == 1 else playersBat[i].split()[1]
        if lastName in wktOrder:
            wktsAtCrease = wktOrder[lastName] - entryWkts
        elif playersBat[i] in wktOrder: # more than one instance of the same last name
            wktsAtCrease = wktOrder[playersBat[i]] - entryWkts
        else: #not out
            wktsAtCrease = totalWkts - entryWkts
                        
        if (playersBat[i] not in wktOrder and (lastName in retiredNotOut) or (playersBat[i] in retiredNotOut)): notOut = 1 
        if teamBat == location:
            homeAway = 0
        else:
            homeAway = 1
        if result == teamBat:
            resultNum = 2
        elif result == 'Tie/NR':
            resultNum = 1
        else:
            resultNum = 0        
        
        inningsId = `int(t20iId)` + `inningsNum` + `playerId`
        c.execute('''insert or ignore into battingT20IInnings (inningsId, playerId, player, t20iId, innings, position, dismissalInfo, notOut, runs, minutes, balls, fours, sixes, totalPct, entryRuns, entryWkts,
                  wicketsAtCrease, homeAway, result) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (inningsId, playerId, batsmanName, t20iId, inningsNum, (i+1), dismissalInfo, notOut, int(runsBat[i]), minutes, balls, fours, sixes, totalPct, entryRuns, entryWkts, wktsAtCrease, homeAway, resultNum))
        
        print `inningsId`+",",`playerId`+", "+`inningsNum`+", "+batsmanName+", runs: "+`int(runsBat[i])`
    conn.commit()
    
# loop through t20i matches
for x in range(startT20I, len(t20isInfo)):
    # load cricinfo scorecard html
    t20iId = t20isInfo[x][0]
    startDate = t20isInfo[x][1]
    location = t20isInfo[x][2]
    result = t20isInfo[x][7]
    
    scorecardURL = 'http://www.espncricinfo.com' + t20isInfo[x][11]
    print scorecardURL
    scorecardPage = requests.get(scorecardURL)
    scoreTree = html.fromstring(scorecardPage.text)
    
    # parse all relevant fields from scorecard
    series = scoreTree.xpath('(//a[@class="headLink"]/text())')[0]
    seriesT20I = scoreTree.xpath('(//div[@class="space-top-bottom-5"]/text())')
    seriesT20I = "" if not seriesT20I else seriesT20I[0]
    series = series + seriesT20I
    team1 = scoreTree.xpath('(//a[@class="teamLink"]/text())')[0]
    team2 = scoreTree.xpath('(//a[@class="teamLink"]/text())')[1]
    season = scoreTree.xpath('(//a[@class="headLink"]/text())')[2]
    season = season.split()[0]

    batInn1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
    batInn2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
    if len(batInn1[0]) != 0 and 'forfeit' not in batInn1[0] and 'innings' in batInn1[0]:
        teamBat1 = batInn1[0]
        teamBat1 = team1 if team1 in teamBat1 else team2
        teamBowl1 = team2 if teamBat1 == team1 else team1
        playerLinksBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class="batsman-name"]/a[@class="playerName"]/@href')
        playersBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class="batsman-name"]/a[@class="playerName"]/text()')
        dismissalsBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class="dismissal-info"]/text()')
        runsBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class="bold"]/text()')
        totalBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr[@class="total-wrap"]/td[@class="bold"]/b/text()')[0]
        totalDetails1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr[@class="total-wrap"]/td[@class="total-details"]/text()')[0]
        fow1 = scoreTree.xpath('(//div[@class="fow"])[1]/p/a[@class="fowLink"]/span/text()')
        playerLinksBowl1 = scoreTree.xpath('(//table[@class="bowling-table"])[1]/tr/td[@class="bowler-name"]/a[@class="playerName"]/@href')
        detailsBowl1 = scoreTree.xpath('(//table[@class="bowling-table"])[1]/tr/td/text()')
        detailsBowl1 = [x for x in detailsBowl1 if x.replace('.','',1).isdigit()]
        detailsHeadBat1 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr[@class="tr-heading"]/th[@scope="col"]')]
        detailsBat1 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class=""]')]

        del detailsHeadBat1[0]
        del detailsHeadBat1[0]
        i = 0
        minutesBat1 = []
        ballsBat1 = []
        foursBat1 = []
        sixesBat1 = []
        while i < len(detailsBat1):
            try:
                minIndex = detailsHeadBat1.index('M')
                minutesBat1.append(detailsBat1[minIndex + i])
            except ValueError:
                minutesBat1.append(None)
            try:
                ballIndex = detailsHeadBat1.index('B')
                ballsBat1.append(detailsBat1[ballIndex+i])
            except ValueError:
                ballsBat1.append(None)
            try:
                fourIndex = detailsHeadBat1.index('4s')
                foursBat1.append(detailsBat1[fourIndex+i])
            except ValueError:
                foursBat1.append(None)
            try:
                sixIndex = detailsHeadBat1.index('6s')
                sixesBat1.append(detailsBat1[sixIndex+i])
            except ValueError:
                sixesBat1.append(None)                
            i += len(detailsHeadBat1)
    if len(batInn2) != 0 and 'forfeit' not in batInn2[0] and 'innings' in batInn2[0]:
        teamBat2 = batInn2[0]
        teamBat2 = team2 if team2 in teamBat2 else team1
        teamBowl2 = team1 if teamBat2 == team2 else team2
        playerLinksBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class="batsman-name"]/a[@class="playerName"]/@href')
        playersBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class="batsman-name"]/a[@class="playerName"]/text()')
        dismissalsBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class="dismissal-info"]/text()')
        runsBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class="bold"]/text()')
        totalBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr[@class="total-wrap"]/td[@class="bold"]/b/text()')[0]
        totalDetails2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr[@class="total-wrap"]/td[@class="total-details"]/text()')[0]
        fow2 = scoreTree.xpath('(//div[@class="fow"])[2]/p/a[@class="fowLink"]/span/text()')
        playerLinksBowl2 = scoreTree.xpath('(//table[@class="bowling-table"])[2]/tr/td[@class="bowler-name"]/a[@class="playerName"]/@href')
        detailsBowl2 = scoreTree.xpath('(//table[@class="bowling-table"])[2]/tr/td/text()')
        detailsBowl2 = [x for x in detailsBowl2 if x.replace('.','',1).isdigit()]
        detailsHeadBat2 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr[@class="tr-heading"]/th[@scope="col"]')]
        detailsBat2 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class=""]')]

        del detailsHeadBat2[0]
        del detailsHeadBat2[0]
        i = 0
        minutesBat2 = []
        ballsBat2 = []
        foursBat2 = []
        sixesBat2 = []
        while i < len(detailsBat2):
            try:
                minIndex = detailsHeadBat2.index('M')
                minutesBat2.append(detailsBat2[minIndex + i])
            except ValueError:
                minutesBat2.append(None)
            try:
                ballIndex = detailsHeadBat2.index('B')
                ballsBat2.append(detailsBat2[ballIndex+i])
            except ValueError:
                ballsBat2.append(None)
            try:
                fourIndex = detailsHeadBat2.index('4s')
                foursBat2.append(detailsBat2[fourIndex+i])
            except ValueError:
                foursBat2.append(None)
            try:
                sixIndex = detailsHeadBat2.index('6s')
                sixesBat2.append(detailsBat2[sixIndex+i])
            except ValueError:
                sixesBat2.append(None)                
            i += len(detailsHeadBat2)
        
    print '\nDumping details for t20i #'+`int(t20iId)`
    c.execute('update t20iInfo set series=?,season=? where t20iId=?', (series, season, t20iId))

    if len(batInn1) != 0 and 'forfeit' not in batInn1[0] and 'innings' in batInn1[0]: dumpInningsDetails(1, teamBat1, teamBowl1, playerLinksBat1, playersBat1, dismissalsBat1, runsBat1, minutesBat1, ballsBat1, foursBat1, sixesBat1,
                                                                                totalBat1, totalDetails1, fow1, playerLinksBowl1, detailsBowl1)
    if len(batInn2) != 0 and 'forfeit' not in batInn2[0] and 'innings' in batInn2[0]: dumpInningsDetails(2, teamBat2, teamBowl2, playerLinksBat2, playersBat2, dismissalsBat2, runsBat2, minutesBat2, ballsBat2, foursBat2, sixesBat2,
                                                                                totalBat2, totalDetails2, fow2, playerLinksBowl2, detailsBowl2)

conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
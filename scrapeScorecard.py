#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

startTest = int(input('Enter starting Test #: '))

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

# get tests info
c.execute('select * from testInfo')
testsInfo = c.fetchall()

def dumpInningsDetails(inningsNum, teamBat, teamBowl, playerLinksBat, playersBat, dismissalsBat, runsBat, minutesBat, ballsBat, foursBat, sixesBat, totalBat, totalDetails, fow, playerLinksBowl, detailsBowl):
    print('\nDumping details for innings #'+repr(inningsNum))
    print('Bowling details:')
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
        totalBalls = int(totalBalls.split('.')[0]) * ballsPerOver + int(totalBalls.split('.')[1])
    else:
        totalBalls = int(totalBalls) * ballsPerOver
    if len(totalWktsOvers) == 3:
        totalMinutes = totalWktsOvers[2].replace(')','').split()[0]
    else: totalMinutes = 0
    extras = runsBat[len(runsBat)-1]
    
    batHighInnPct = 0.0
    batSecHighInnPct = 0.0
    for i in range(len(playerLinksBat)):
        if runsBat[i] == '-': continue
        pct = float(runsBat[i]) * 100 / float(totalBat) if float(totalBat) > 0 else 0.0
        if pct > batHighInnPct:
            batHighInnPct = pct
        elif pct > batSecHighInnPct and pct < batHighInnPct:
            batSecHighInnPct = pct
            
    inningsId = repr(int(testId)) + repr(inningsNum)
    c.execute('''insert or ignore into detailsTestInnings (inningsId, testId, innings, batTeam, bowlTeam, extras, runs, balls, minutes, wickets, inningsEndDetail, batHighInnPct, batSecHighInnPct)
              values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (inningsId, testId, inningsNum, teamBat, teamBowl, extras, totalBat, totalBalls, totalMinutes, totalWkts, inningsEndDetail, batHighInnPct, batSecHighInnPct))
    
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
            
        # handle scorecards with 0/4/6s hit against bowler        
        try:
            maidens = int(detailsBowl[1+j*8])
            runsConceded = int(detailsBowl[2+j*8])
            wkts = int(detailsBowl[3+j*8])
            if '.' in detailsBowl[j*8]:
                ballsBowled = int(detailsBowl[j*8].split('.')[0]) * ballsPerOver + int(detailsBowl[j*8].split('.')[1])
            else:
                ballsBowled = int(detailsBowl[j*8]) * ballsPerOver
        except (ValueError, IndexError):
            maidens = int(detailsBowl[1+j*5])
            runsConceded = int(detailsBowl[2+j*5])
            wkts = int(detailsBowl[3+j*5])
            if '.' in detailsBowl[j*5]:
                ballsBowled = int(detailsBowl[j*5].split('.')[0]) * ballsPerOver + int(detailsBowl[j*5].split('.')[1])
            else:
                ballsBowled = int(detailsBowl[j*5]) * ballsPerOver
                
        if result == teamBowl:
            resultNum = 2
        elif result == 'Draw': 
            resultNum = 1
        elif result == 'No Result':
            resultNum = 1
        else:
            resultNum = 0
            
        if teamBowl == location:
            homeAway = 0
        else:
            homeAway = 1                        
                   
        inningsId = repr(int(testId)) + repr(inningsNum) + repr(playerId)
        c.execute('''insert or ignore into bowlingTestInnings (inningsId, playerId, player, testId, innings, position, wkts, balls, maidens, runs, homeAway, result)
                  values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (inningsId, playerId, bowlerName, testId, inningsNum, (j+1), wkts, ballsBowled, maidens, runsConceded, homeAway, resultNum))
        
        print(repr(inningsId)+",",repr(playerId)+", "+repr(inningsNum)+", "+bowlerName+", "+repr(wkts)+'/'+repr(runsConceded))
            
    # parse batsmen fall of wicket order
    retiredNOAdj = 0
    for k in range(len(fow)):
        batsmenFoW = fow[k].split('(')[1].replace(')','')
        player = batsmenFoW.split(',')[0]        
        if 'retired not out' in batsmenFoW:
            retiredNotOut[player] = 1
            retiredNOAdj = retiredNOAdj + 1
        else:
            wktOrder[player] = k - retiredNOAdj
        
        overs = batsmenFoW.split(',')
        if len(overs) == 2:
            overs = overs[1].split()[0]
            if 'retired' in overs:
                balls = None
            else:
                if '.' in overs:
                    balls = int(overs.split('.')[0]) * ballsPerOver + int(overs.split('.')[1])
                else:
                    balls = int(overs) * ballsPerOver
        else: balls = None
        wicket = fow[k].split('(')[0].strip().split('-')[0]
        runs = fow[k].split('(')[0].strip().split('-')[1]        
        
        fowId = repr(int(testId)) + repr(inningsNum) + repr((k+1))
        c.execute('''insert or ignore into fowTestInnings (fowId, testId, innings, runs, wicket, player, balls) values (?, ?, ?, ?, ?, ?, ?)''',
                (fowId, testId, inningsNum, runs, wicket, player, balls))
        
    print('\nBatting details:')
    # store batting innings and live ratings data
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

        if ((playersBat[i] not in wktOrder and lastName not in wktOrder) and (lastName in retiredNotOut) or (playersBat[i] in retiredNotOut)): notOut = 1
        # hack fix for retired not out bug
        if (int(testId) == 1837 and inningsNum == 2 and playersBat[i] == "DPMD Jayawardene"): notOut = 0

        if teamBat == location:
            homeAway = 0
        else:
            homeAway = 1
        if result == teamBat:
            resultNum = 2
        elif result == 'Draw': 
            resultNum = 1
        elif result == 'No Result':
            resultNum = 1
        else:
            resultNum = 0        

        inningsId = repr(int(testId)) + repr(inningsNum) + repr(playerId)
        c.execute('''insert or ignore into battingTestInnings (inningsId, playerId, player, testId, innings, position, dismissalInfo, notOut, runs, minutes, balls, fours, sixes, totalPct, entryRuns, entryWkts,
                  wicketsAtCrease, homeAway, result) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (inningsId, playerId, batsmanName, testId, inningsNum, (i+1), dismissalInfo, notOut, int(runsBat[i]), minutes, balls, fours, sixes, totalPct, entryRuns, entryWkts, wktsAtCrease, homeAway,
                 resultNum))

        print(repr(inningsId)+",",repr(playerId)+", "+repr(inningsNum)+", "+batsmanName+", "+repr(int(runsBat[i])))
    conn.commit()
    
# loop through test matches
for x in range(startTest, len(testsInfo)):
    # load cricinfo scorecard html
    testId = testsInfo[x][0]
    startDate = testsInfo[x][1]
    location = testsInfo[x][2]
    result = testsInfo[x][8]
    
    scorecardURL = 'http://www.espncricinfo.com' + testsInfo[x][12]
    print scorecardURL
    scorecardPage = requests.get(scorecardURL)
    scoreTree = html.fromstring(scorecardPage.text)
    
    # parse all relevant fields from scorecard
    series = scoreTree.xpath('(//a[@class="headLink"]/text())')[0]
    seriesTest = scoreTree.xpath('(//div[@class="space-top-bottom-5"]/text())')[0]
    series = series + seriesTest
    team1 = scoreTree.xpath('(//a[@class="teamLink"]/text())')[0]
    team2 = scoreTree.xpath('(//a[@class="teamLink"]/text())')[1]
    season = scoreTree.xpath('(//a[@class="headLink"]/text())')[2]
    season = season.split()[0]

    # if balls per over not noted, assume 6
    if '-' in scoreTree.xpath('//div[@class="match-information"]/div[@class="bold space-top-bottom-10"]/text()')[0]: ballsPerOver = 6
    else : ballsPerOver = int(scoreTree.xpath('//div[@class="match-information"]/div[@class="bold space-top-bottom-10"]/span[@class="normal"]/text()')[0].strip())

    batInn1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
    batInn2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
    batInn3 = scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
    batInn4 = scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
    if len(batInn1[0]) != 0 and 'forfeit' not in batInn1[0] and 'innings' in batInn1[0]:
        teamBat1 = batInn1[0]
        teamBat1 = team1 if team1 in teamBat1 else team2
        teamBowl1 = team2 if teamBat1 == team1 else team1
        playerLinksBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class="batsman-name"]/a[@class="playerName"]/@href')
        playersBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class="batsman-name"]/a[@class="playerName"]/text()')
        dismissalsBat1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr/td[@class="dismissal-info"]/text()')
        while '\n  ' in dismissalsBat1: dismissalsBat1.remove('\n  ')
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
        teamBat2 = team1 if team1 in teamBat2 else team2
        teamBowl2 = team1 if teamBat2 == team2 else team2
        playerLinksBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class="batsman-name"]/a[@class="playerName"]/@href')
        playersBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class="batsman-name"]/a[@class="playerName"]/text()')
        dismissalsBat2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr/td[@class="dismissal-info"]/text()')
        while '\n  ' in dismissalsBat2: dismissalsBat2.remove('\n  ')
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
    if len(batInn3) != 0 and 'forfeit' not in batInn3[0]:
        teamBat3 = batInn3[0]
        teamBat3 = team1 if team1 in teamBat3 else team2
        teamBowl3 = team2 if teamBat3 == team1 else team1
        playerLinksBat3 = scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr/td[@class="batsman-name"]/a[@class="playerName"]/@href')
        playersBat3 = scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr/td[@class="batsman-name"]/a[@class="playerName"]/text()')
        dismissalsBat3 = scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr/td[@class="dismissal-info"]/text()')
        while '\n  ' in dismissalsBat3: dismissalsBat3.remove('\n  ')
        runsBat3 = scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr/td[@class="bold"]/text()')
        totalBat3 = scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr[@class="total-wrap"]/td[@class="bold"]/b/text()')[0]
        totalDetails3 = scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr[@class="total-wrap"]/td[@class="total-details"]/text()')[0]
        fow3 = scoreTree.xpath('(//div[@class="fow"])[3]/p/a[@class="fowLink"]/span/text()')
        playerLinksBowl3 = scoreTree.xpath('(//table[@class="bowling-table"])[3]/tr/td[@class="bowler-name"]/a[@class="playerName"]/@href')
        detailsBowl3 = scoreTree.xpath('(//table[@class="bowling-table"])[3]/tr/td/text()')
        detailsBowl3 = [x for x in detailsBowl3 if x.replace('.','',1).isdigit()]
        detailsHeadBat3 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr[@class="tr-heading"]/th[@scope="col"]')]
        detailsBat3 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[3]/tr/td[@class=""]')]
        del detailsHeadBat3[0]
        del detailsHeadBat3[0]
        i = 0
        minutesBat3 = []
        ballsBat3 = []
        foursBat3 = []
        sixesBat3 = []
        while i < len(detailsBat3):
            try:
                minIndex = detailsHeadBat3.index('M')
                minutesBat3.append(detailsBat3[minIndex + i])
            except ValueError:
                minutesBat3.append(None)
            try:
                ballIndex = detailsHeadBat3.index('B')
                ballsBat3.append(detailsBat3[ballIndex+i])
            except ValueError:
                ballsBat3.append(None)
            try:
                fourIndex = detailsHeadBat3.index('4s')
                foursBat3.append(detailsBat3[fourIndex+i])
            except ValueError:
                foursBat3.append(None)
            try:
                sixIndex = detailsHeadBat3.index('6s')
                sixesBat3.append(detailsBat3[sixIndex+i])
            except ValueError:
                sixesBat3.append(None)                
            i += len(detailsHeadBat3)
    if len(batInn4) != 0 and 'forfeit' not in batInn4[0]:        
        teamBat4 = batInn4[0]
        teamBat4 = team1 if team1 in teamBat4 else team2
        teamBowl4 = team2 if teamBat4 == team1 else team1
        playerLinksBat4 = scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr/td[@class="batsman-name"]/a[@class="playerName"]/@href')
        playersBat4 = scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr/td[@class="batsman-name"]/a[@class="playerName"]/text()')
        dismissalsBat4 = scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr/td[@class="dismissal-info"]/text()')
        while '\n  ' in dismissalsBat4: dismissalsBat4.remove('\n  ')
        runsBat4 = scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr/td[@class="bold"]/text()')
        totalBat4 = scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr[@class="total-wrap"]/td[@class="bold"]/b/text()')[0]
        totalDetails4 = scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr[@class="total-wrap"]/td[@class="total-details"]/text()')[0]
        fow4 = scoreTree.xpath('(//div[@class="fow"])[4]/p/a[@class="fowLink"]/span/text()')
        playerLinksBowl4 = scoreTree.xpath('(//table[@class="bowling-table"])[4]/tr/td[@class="bowler-name"]/a[@class="playerName"]/@href')
        detailsBowl4 = scoreTree.xpath('(//table[@class="bowling-table"])[4]/tr/td/text()')
        detailsBowl4 = [x for x in detailsBowl4 if x.replace('.','',1).isdigit()]
        detailsHeadBat4 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr[@class="tr-heading"]/th[@scope="col"]')]
        detailsBat4 = [y.text for y in scoreTree.xpath('(//table[@class="batting-table innings"])[4]/tr/td[@class=""]')]
        del detailsHeadBat4[0]
        del detailsHeadBat4[0]
        i = 0
        minutesBat4 = []
        ballsBat4 = []
        foursBat4 = []
        sixesBat4 = []
        while i < len(detailsBat4):
            try:
                minIndex = detailsHeadBat4.index('M')
                minutesBat4.append(detailsBat4[minIndex + i])
            except ValueError:
                minutesBat4.append(None)
            try:
                ballIndex = detailsHeadBat4.index('B')
                ballsBat4.append(detailsBat4[ballIndex+i])
            except ValueError:
                ballsBat4.append(None)
            try:
                fourIndex = detailsHeadBat4.index('4s')
                foursBat4.append(detailsBat4[fourIndex+i])
            except ValueError:
                foursBat4.append(None)
            try:
                sixIndex = detailsHeadBat4.index('6s')
                sixesBat4.append(detailsBat4[sixIndex+i])
            except ValueError:
                sixesBat4.append(None)                
            i += len(detailsHeadBat4)
    print('\nDumping details for test #'+repr(int(testId)))
    c.execute('update testInfo set series=?,season=?,ballsPerOver=? where testId=?', (series, season, ballsPerOver, testId))
    if len(batInn1) != 0 and 'forfeit' not in batInn1[0] and 'innings' in batInn1[0]: dumpInningsDetails(1, teamBat1, teamBowl1, playerLinksBat1, playersBat1, dismissalsBat1, runsBat1, minutesBat1, ballsBat1, foursBat1, sixesBat1,
                                                                               totalBat1, totalDetails1, fow1, playerLinksBowl1, detailsBowl1)
    if len(batInn2) != 0 and 'forfeit' not in batInn2[0] and 'innings' in batInn2[0]: dumpInningsDetails(2, teamBat2, teamBowl2, playerLinksBat2, playersBat2, dismissalsBat2, runsBat2, minutesBat2, ballsBat2, foursBat2, sixesBat2,
                                                                               totalBat2, totalDetails2, fow2, playerLinksBowl2, detailsBowl2)
    if len(batInn3) != 0 and 'forfeit' not in batInn3[0] and 'innings' in batInn3[0]: dumpInningsDetails(3, teamBat3, teamBowl3, playerLinksBat3, playersBat3, dismissalsBat3, runsBat3, minutesBat3, ballsBat3, foursBat3, sixesBat3,
                                                                               totalBat3, totalDetails3, fow3, playerLinksBowl3, detailsBowl3)
    if len(batInn4) != 0 and 'forfeit' not in batInn4[0] and 'innings' in batInn4[0]: dumpInningsDetails(4, teamBat4, teamBowl4, playerLinksBat4, playersBat4, dismissalsBat4, runsBat4, minutesBat4, ballsBat4, foursBat4, sixesBat4,
                                                                               totalBat4, totalDetails4, fow4, playerLinksBowl4, detailsBowl4)
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')
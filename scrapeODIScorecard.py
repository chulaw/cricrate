#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
import sys
start = time.clock()

# startODI = int(input('Enter starting ODI #: '))
startODI = int(sys.argv[1])

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()

# get odis info
c.execute('select * from odiInfo')
odisInfo = c.fetchall()

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

    inningsId = repr(int(odiId)) + repr(inningsNum)
    c.execute('''insert or ignore into detailsODIInnings (inningsId, odiId, innings, batTeam, bowlTeam, extras, runs, balls, minutes, wickets, inningsEndDetail) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (inningsId, odiId, inningsNum, teamBat, teamBowl, extras, totalBat, totalBalls, totalMinutes, totalWkts, inningsEndDetail))

    # store bowling innings
    modDetailsBowl1 = []
    for ii in detailsBowl:
      if not '(' in ii: modDetailsBowl1.append(ii)
    detailsBowl = modDetailsBowl1
    bugFixed = 0
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
        if odiId == 2725 and inningsNum == 1 and bugFixed == 0: # handle odi #2725 sami faridi case
            detailsBowl.insert(37, '0')
            detailsBowl.insert(38, '0')
            detailsBowl.insert(39, '0')
            bugFixed = 1
        if odiId > 1747 and odiId not in (1749, 1765, 1773, 1781, 1782, 1791, 1805, 1809, 1811, 1817, 1833, 1913, 1915, 1920, 2074, 2101, 2110, 2251, 2259, 2260, 2261, 2262, 2270, 2271, 2272, 2273, 2282, 2290, 2302, 2339, 2340, 2343, 2344, 2350, 2353,
                                          2355, 2356, 2374, 2375, 2376, 2378, 2390, 2391, 2396, 2397, 2399, 2400, 2401, 2406, 2407, 2444, 2445, 2446, 2448, 2450, 2451, 2453, 2454, 2455, 2456, 2465, 2467, 2476, 2477, 2480, 2481, 2483, 2484, 2489, 2491,
                                          2492, 2494, 2495, 2496, 2498, 2499, 2500, 2502, 2503, 2504, 2505, 2507, 2508, 2509, 2511, 2512, 2516, 2518, 2528, 2529, 2530, 2585, 2586, 2596, 2599, 2600, 2601, 2602, 2603, 2604, 2609, 2610, 2634, 2636, 2638,
                                          2640, 2641, 2690, 2693, 2694, 2695, 2722, 2727, 2728, 2729, 2731, 2737, 2738, 2739, 2740, 2741, 2743, 2744, 2746, 2747, 2749, 2751, 2752, 2753, 2763, 2764, 2765, 2766, 2767, 2768, 2769, 2770, 2771, 2772, 2776,
                                          2784, 2786, 2787, 2788, 2789, 2792, 2797, 2799, 2801, 2805, 2807, 2809, 2812, 2814, 2830, 2831, 2835, 2836, 2837, 2838, 2842, 2843, 2844, 2856, 2857, 2858, 2859, 2860, 2861, 2875, 2876, 2877, 2878, 2879, 2880,
                                          2881, 2908, 2909, 2910, 2911, 2912, 2922, 2926, 2928, 2949, 2951, 2953, 2956, 2957, 2958, 2959, 2977, 2978, 2992, 2997, 3005, 3006, 3007, 3008, 3009, 3010, 3012, 3013, 3014, 3015, 3016, 3017, 3019, 3020, 3021,
                                          3022, 3023, 3024, 3027, 3028, 3029, 3033, 3034, 3035, 3036, 3041, 3042, 3048, 3049, 3050, 3051, 3052, 3053, 3055, 3092, 3096, 3099, 3157, 3158, 3164, 3166, 3171, 3172, 3173, 3174, 3185, 3192, 3193, 3196, 3197,
                                          3230, 3232, 3234, 3242, 3245, 3270, 3271, 3282, 3287, 3306, 3307, 3335, 3336, 3337, 3338, 3339, 3341, 3342, 3344, 3345, 3356, 3357, 3358, 3359, 3379, 3381, 3384, 3386, 3405, 3407, 3410, 3411, 3413, 3417, 3418,
                                          3423, 3426, 3429, 3459, 3460, 3464, 3466, 3468, 3472, 3487, 3488, 3489, 3491, 3492, 3503, 3504, 3505, 3506, 3527, 3528, 3529, 3541, 3542, 3556, 3558, 3560, 3562, 3572, 3573, 3575, 3576, 3581, 3679, 3688, 3690,
                                          3691, 3693, 3694, 3696, 3697, 3699, 3709, 3711, 3729, 3748, 3749, 3759, 3760, 3761, 3762, 3763, 3764, 3765, 3766, 3767, 3778, 3779, 3780, 3781, 3782, 3783, 3786, 3801, 3802, 3803, 3823, 3825, 3827, 3835, 3837,
                                          3838, 3840, 3842, 3844, 3847): # cricinfo scorecards display 0s, 4s and 6s scored off bowler
            if odiId == 3482 and j == 2 and inningsNum == 1: # rehman 0-0-8-0
                detailsBowl.insert(19, 0)
            maidens = int(detailsBowl[1+j*8])
            runsConceded = int(detailsBowl[2+j*8])
            wkts = int(detailsBowl[3+j*8])
            if '.' in detailsBowl[j*8]:
                ballsBowled = int(detailsBowl[j*8].split('.')[0]) * ballsPerOver + int(detailsBowl[j*8].split('.')[1])
            else:
                ballsBowled = int(detailsBowl[j*8]) * ballsPerOver
        else:
            maidens = int(detailsBowl[1+j*5])
            runsConceded = int(detailsBowl[2+j*5])
            wkts = int(detailsBowl[3+j*5])
            if '.' in detailsBowl[j*5]:
                ballsBowled = int(detailsBowl[j*5].split('.')[0]) * ballsPerOver + int(detailsBowl[j*5].split('.')[1])
            else:
                ballsBowled = int(detailsBowl[j*5]) * ballsPerOver

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

        inningsId = repr(int(odiId)) + repr(inningsNum) + repr(playerId)
        c.execute('''insert or ignore into bowlingODIInnings (inningsId, playerId, player, odiId, innings, position, wkts, balls, maidens, runs, homeAway, result) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (inningsId, playerId, bowlerName, odiId, inningsNum, (j+1), wkts, ballsBowled, maidens, runsConceded, homeAway, resultNum))

        print(repr(inningsId)+",",repr(playerId)+", "+repr(inningsNum)+", "+bowlerName+", wkts: "+repr(wkts)+'/'+repr(runsConceded))

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
                    balls = int(overs.split('.')[0]) * ballsPerOver + int(overs.split('.')[1])
                else:
                    balls = int(overs) * ballsPerOver
        else: balls = None
        wicket = fow[k].split('(')[0].strip().split('-')[0]
        runs = fow[k].split('(')[0].strip().split('-')[1]

        fowId = repr(int(odiId)) + repr(inningsNum) + repr((k+1))
        c.execute('''insert or ignore into fowODIInnings (fowId, odiId, innings, runs, wicket, player, balls) values (?, ?, ?, ?, ?, ?, ?)''',
                (fowId, odiId, inningsNum, runs, wicket, player, balls))

    print('\nBatting details:')
    ###########################################################################################################################
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

        inningsId = repr(int(odiId)) + repr(inningsNum) + repr(playerId)
        c.execute('''insert or ignore into battingODIInnings (inningsId, playerId, player, odiId, innings, position, dismissalInfo, notOut, runs, minutes, balls, fours, sixes, totalPct, entryRuns, entryWkts,
                  wicketsAtCrease, homeAway, result) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (inningsId, playerId, batsmanName, odiId, inningsNum, (i+1), dismissalInfo, notOut, int(runsBat[i]), minutes, balls, fours, sixes, totalPct, entryRuns, entryWkts, wktsAtCrease, homeAway, resultNum))

        print(repr(inningsId)+",",repr(playerId)+", "+repr(inningsNum)+", "+batsmanName+", runs: "+repr(int(runsBat[i])))
    conn.commit()

# loop through odi matches
for x in range(startODI, len(odisInfo)):
    # load cricinfo scorecard html
    odiId = odisInfo[x][0]
    startDate = odisInfo[x][1]
    location = odisInfo[x][2]
    result = odisInfo[x][8]

    scorecardURL = 'http://www.espncricinfo.com' + odisInfo[x][12]
    scorecardPage = requests.get(scorecardURL)
    scoreTree = html.fromstring(scorecardPage.text)

    # parse all relevant fields from scorecard
    series = scoreTree.xpath('(//a[@class="headLink"]/text())')[0]
    seriesODI = scoreTree.xpath('(//div[@class="space-top-bottom-5"]/text())')
    seriesODI = "" if not seriesODI else seriesODI[0]
    series = series + seriesODI
    team1 = scoreTree.xpath('(//a[@class="teamLink"]/text())')[0]
    team2 = scoreTree.xpath('(//a[@class="teamLink"]/text())')[1]
    season = scoreTree.xpath('(//a[@class="headLink"]/text())')[2]
    season = season.split()[0]

    # if balls per over not noted, assume 6
    if ',' in  scoreTree.xpath('(//div[@class="bold space-top-bottom-10"]/span/text())')[0] or odiId > 3486: ballsPerOver = 6
    else : ballsPerOver = int(scoreTree.xpath('(//div[@class="bold space-top-bottom-10"]/span/text())')[0])

    batInn1 = scoreTree.xpath('(//table[@class="batting-table innings"])[1]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
    batInn2 = scoreTree.xpath('(//table[@class="batting-table innings"])[2]/tr[@class="tr-heading"]/th[@class="th-innings-heading"]/text()')
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
        teamBat2 = team2 if team2 in teamBat2 else team1
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

    print('\nDumping details for odi #'+repr(int(odiId)))
    c.execute('update odiInfo set series=?,season=?,ballsPerOver=? where odiId=?', (series, season, ballsPerOver, odiId))

    if len(batInn1) != 0 and 'forfeit' not in batInn1[0] and 'innings' in batInn1[0]: dumpInningsDetails(1, teamBat1, teamBowl1, playerLinksBat1, playersBat1, dismissalsBat1, runsBat1, minutesBat1, ballsBat1, foursBat1, sixesBat1,
                                                                               totalBat1, totalDetails1, fow1, playerLinksBowl1, detailsBowl1)
    if len(batInn2) != 0 and 'forfeit' not in batInn2[0] and 'innings' in batInn2[0]: dumpInningsDetails(2, teamBat2, teamBowl2, playerLinksBat2, playersBat2, dismissalsBat2, runsBat2, minutesBat2, ballsBat2, foursBat2, sixesBat2,
                                                                               totalBat2, totalDetails2, fow2, playerLinksBowl2, detailsBowl2)

conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')

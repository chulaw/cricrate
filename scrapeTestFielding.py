#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

startTest = int(input('Enter starting Test #: '))
startTest = 1774 if startTest == 0 else startTest

#set PYTHONIOENCTestNG=utf-8
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

# get tests info
c.execute('select testId, startDate, scoreLink from testInfo')
testsInfo = c.fetchall()
newPlayerPenaltyFactor = 0.0425
expSmoothFactor = 0.05

# loop through test matches
for x in range(startTest, len(testsInfo)):
    testId = testsInfo[x][0]
    startDate = testsInfo[x][1]
    print `testId` + "\n"

    team1 = ""
    team2 = ""
    team3 = ""
    team4 = ""
    c.execute('select player, playerId from bowlingTestInnings where testId=? and innings=1',(testId,))
    bowlers1 = c.fetchall()
    bowler1Names = []
    bowler2Id1 = {}

    for i in range(len(bowlers1)):
        bowler1Names.append(bowlers1[i][0])
        bowler2Id1[bowlers1[i][0]] = bowlers1[i][1]
        if team1 == "":
            c.execute('select country from playerInfo where playerId=?',(bowlers1[i][1],))
            team1 = c.fetchone()
            team1 = team1[0]

    c.execute('select player, playerId from battingTestInnings where testId=? and innings=1',(testId,))
    batsmen1 = c.fetchall()
    batsmen1Names = []
    batsman2Id1 = {}

    for i in range(len(batsmen1)):
        batsmen1Names.append(batsmen1[i][0])
        batsman2Id1[batsmen1[i][0]] = batsmen1[i][1]

    c.execute('select player, playerId from bowlingTestInnings where testId=? and innings=2',(testId,))
    bowlers2 = c.fetchall()
    bowler2Names = []
    bowler2Id2 = {}

    for i in range(len(bowlers2)):
        bowler2Names.append(bowlers2[i][0])
        bowler2Id2[bowlers2[i][0]] = bowlers2[i][1]
        if team2 == "":
                c.execute('select country from playerInfo where playerId=?',(bowlers2[i][1],))
                team2 = c.fetchone()
                team2 = team2[0]

    c.execute('select player, playerId from battingTestInnings where testId=? and innings=2',(testId,))
    batsmen2 = c.fetchall()
    batsmen2Names = []
    batsman2Id2 = {}

    for i in range(len(batsmen2)):
        batsmen2Names.append(batsmen2[i][0])
        batsman2Id2[batsmen2[i][0]] = batsmen2[i][1]

    c.execute('select player, playerId from bowlingTestInnings where testId=? and innings=3',(testId,))
    bowlers3 = c.fetchall()
    bowler3Names = []
    bowler2Id3 = {}

    for i in range(len(bowlers3)):
        if team3 == "":
            c.execute('select country from playerInfo where playerId=?',(bowlers3[i][1],))
            team3 = c.fetchone()
            team3 = team3[0]
        if team3 == team1:
            bowler1Names.append(bowlers3[i][0])
            bowler2Id1[bowlers3[i][0]] = bowlers3[i][1]
        else:
            bowler2Names.append(bowlers3[i][0])
            bowler2Id2[bowlers3[i][0]] = bowlers3[i][1]

    c.execute('select player, playerId from battingTestInnings where testId=? and innings=3',(testId,))
    batsmen3 = c.fetchall()
    batsmen3Names = []
    batsman2Id3 = {}

    for i in range(len(batsmen3)):
        if team3 == team1:
            batsmen1Names.append(batsmen3[i][0])
            batsman2Id1[batsmen3[i][0]] = batsmen3[i][1]
        else:
            batsmen2Names.append(batsmen3[i][0])
            batsman2Id2[batsmen3[i][0]] = batsmen3[i][1]

    c.execute('select player, playerId from bowlingTestInnings where testId=? and innings=4',(testId,))
    bowlers4 = c.fetchall()
    bowler4Names = []
    bowler2Id4 = {}

    for i in range(len(bowlers4)):
        if team4 == "":
            c.execute('select country from playerInfo where playerId=?',(bowlers4[i][1],))
            team4 = c.fetchone()
            team4 = team4[0]
        if team4 == team1:
            bowler1Names.append(bowlers4[i][0])
            bowler2Id1[bowlers4[i][0]] = bowlers4[i][1]
        else:
            bowler2Names.append(bowlers4[i][0])
            bowler2Id2[bowlers4[i][0]] = bowlers4[i][1]

    c.execute('select player, playerId from battingTestInnings where testId=? and innings=4',(testId,))
    batsmen4 = c.fetchall()
    batsmen4Names = []
    batsman2Id4 = {}

    for i in range(len(batsmen4)):
        if team4 == team1:
            batsmen1Names.append(batsmen4[i][0])
            batsman2Id1[batsmen4[i][0]] = batsmen4[i][1]
        else:
            batsmen2Names.append(batsmen4[i][0])
            batsman2Id2[batsmen4[i][0]] = batsmen4[i][1]

    followOn = 0
    if team1 == team4 or team2 == team3: followOn = 1

    fielderName = {}
    fielderCatches = {}
    fielderDroppedCatches = {}
    fielderMisfield = {}
    fielderStumpings = {}
    fielderMissedStumping = {}
    fielderGreatCatch = {}
    fielderDirectHit = {}
    fielderGreatSave = {}
    fielderRunsSaved = {}
    fieldingLiveRating = {}
    fieldingNumCareerMatches = {}
    batsmenDropped = {}
    batsmenGreatCatch = {}
    batsmenDirectHit = {}
    batsmenStumped = {}
    batsmenMissedStumping = {}
    batsmenCaught = {}
    keeper = {}
    detailedCommentaryCount = 0
    for inn in range(1, 5):
        for page in range (1, 8):
            fieldingURL = 'http://www.espncricinfo.com' + testsInfo[x][2] + '?innings=' + `inn` + ';page=' + `page` + ';view=commentary'
            fieldingPage = requests.get(fieldingURL)
            fieldingTree = html.fromstring(fieldingPage.text)

            commentaryEvent = fieldingTree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"])')
            overBalls = fieldingTree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"]/div[@class="commentary-overs"]/text())')
            commentary = fieldingTree.xpath('(//div[@class="commentary-section"]/div[@class="commentary-event"]/div[@class="commentary-text"])')

            for i in range(len(commentaryEvent)):
                eventText =  commentaryEvent[i].text_content()
                eventText = eventText.replace("\t\n", "")
                eventText = eventText.replace("\n\t", "")
                eventText = eventText.replace("\t", "")
                eventSplit = eventText.split("\n")
                commentary = ""
                eventBowler = ""
                eventBatsman = ""
                isKeeper = 0
                if len(eventSplit) == 4:
                    detailedCommentaryCount =+ 1
                    overBalls = eventSplit[0].split(".")
                    if overBalls[0] == "": continue
                    over = overBalls[0]
                    over = `over` if over > 9 else '0' + `over`
                    ball = overBalls[1]
                    bowlerBatsman = eventSplit[1].replace(",","").split(" to ")
                    bowler = bowlerBatsman[0].strip()
                    bowler = "Shamsudeen" if bowler == "Shamshudeen" else bowler
                    bowler = "Ahsan Malik" if bowler == "Jamil" else bowler
                    bowler = "M'shangwe" if bowler == "Mushangwe" else bowler
                    bowlerFI = ""
                    if " " in bowler:
                        bowlerFI = bowler.split(" ")[0]
                        bowlerFI = bowlerFI if bowlerFI.isupper() else ""
                        bowler = bowler.split(" ")[1]
                    batsman = bowlerBatsman[1].strip()
                    batsman = "Mohammad Yousuf" if batsman == "Yousuf Youhana" else batsman
                    batsman = "Shamsudeen" if batsman == "Shamshudeen" else batsman
                    batsman = "Ahsan Malik" if batsman == "Jamil" else batsman
                    batsman = "M'shangwe" if batsman == "Mushangwe" else batsman
                    batsman = "Ankur Vasishta" if batsman == "Ankur Sharma" else batsman
                    batsman = "Amini" if batsman == "Raho" and testId == 3541 else batsman
                    batsmanFI = ""
                    if " " in batsman:
                        batsmanFI = batsman.split(" ")[0]
                        batsmanFI = batsmanFI if batsmanFI.isupper() else ""
                        batsman = batsman.split(" ")[1]
                    commentary = eventSplit[3]

                    eventId = `testId` + `inn` + over + `ball`

                    if ((inn == 1 or inn == 3) and followOn == 0) or ((inn == 1 or inn == 4) and followOn == 1):
                        for bowlerName in bowler1Names:
                            if bowler in bowlerName and (bowlerFI == "" or bowlerName[0] in bowlerFI):
                                eventBowler = bowlerName

                        for batsmanName in batsmen1Names:
                            if batsman in batsmanName and (batsmanFI == "" or batsmanName[0] in batsmanFI):
                                eventBatsman = batsmanName

                        if batsmanFI == "JO" and batsman == "Ngoche":
                            eventBatsman = "James Ngoche"
                            batsman2Id1[eventBatsman] = 617385

                        c.execute('insert or ignore into commentaryEventTest (eventId, testId, bowler, batsman, bowlerId, batsmanId, commentary) values (?, ?, ?, ?, ?, ?, ?)',
                              (eventId, testId, eventBowler, eventBatsman, bowler2Id1[eventBowler], batsman2Id1[eventBatsman], commentary))
                    else:
                        for bowlerName in bowler2Names:
                            if bowler in bowlerName and (bowlerFI == "" or bowlerName[0] in bowlerFI):
                                eventBowler = bowlerName

                        for batsmanName in batsmen2Names:
                            if batsman in batsmanName and (batsmanFI == "" or batsmanName[0] in batsmanFI):
                                eventBatsman = batsmanName

                        if bowlerFI == "JO" and bowler == "Ngoche":
                            eventBowler = "James Ngoche"
                            bowler2Id1[eventBowler] = 617385

                        c.execute('insert or ignore into commentaryEventTest (eventId, testId, bowler, batsman, bowlerId, batsmanId, commentary) values (?, ?, ?, ?, ?, ?, ?)',
                              (eventId, testId, eventBowler, eventBatsman, bowler2Id2[eventBowler], batsman2Id2[eventBatsman], commentary))

                else:
                    # parse catcher in caught out event
                    if ("c " in eventText or "st" in eventText) and "SR:" in eventText:
                        beg = eventText.find("c ") if "c " in eventText else eventText.find("st ")
                        end = eventText.find(" b ")
                        catcherI = ""
                        batsmanI = ""
                        catcher = ""
                        catcherId = 0
                        catcherEventName = eventText[beg+2:end] if "c " in eventText else eventText[beg+3:end]
                        if u"†" in catcherEventName: isKeeper = 1
                        catcherEventName = catcherEventName.replace(u"†", "")
                        catcherLastName = catcherEventName
                        batsmanEventName = eventText[0:beg].strip()
                        batsmanEventName = batsmanEventName.replace(u"†", "")
                        batsmanLastName = batsmanEventName
                        battingLiveRating = None
                        if " " in catcherLastName:
                            catcherI = catcherLastName.split(" ")[0]
                            catcherI = catcherI if catcherI.isupper() else ""
                            catcherLastNameSplit = catcherLastName.split(" ")
                            catcherLastName = catcherLastNameSplit[1] if len(catcherLastNameSplit) == 2 else catcherLastNameSplit[2]
                        if " " in batsmanLastName:
                            batsmanI = batsmanLastName.split(" ")[0]
                            batsmanI = batsmanI if batsmanI.isupper() else ""
                            batsmanLastNameSplit = batsmanLastName.split(" ")
                            batsmanLastName = batsmanLastNameSplit[1] if len(batsmanLastNameSplit) == 2 else batsmanLastNameSplit[2]
                        if ((inn == 1 or inn == 3) and followOn == 0) or ((inn == 1 or inn == 4) and followOn == 1):
                            for bowler in bowler1Names:
                                if catcherEventName == bowler:
                                    catcher = bowler
                                    catcherId = bowler2Id1[bowler]
                            for batsman in batsmen2Names:
                                if catcherEventName == batsman:
                                    catcher = batsman
                                    catcherId = batsman2Id2[batsman]
                            for batsman in batsmen1Names:
                                if batsmanEventName == batsman:
                                    eventBatsman = batsman
                            if catcher == "":
                                for bowler in bowler1Names:
                                    bowlerSplit = bowler.split(" ")
                                    bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                                    if len(bowlerSplit) == 1: bowlerSplit.append("")
                                    if len(bowlerSplit) == 2: bowlerSplit.append("")
                                    if catcherLastName == bowlerSplit[0].strip() or catcherLastName == bowlerSplit[1].strip() or catcherLastName == bowlerSplit[2].strip() and (catcherI == "" or catcherI == bowler[0]):
                                        catcher = bowler
                                        catcherId = bowler2Id1[bowler]
                                for batsman in batsmen2Names:
                                    batsmanSplit = batsman.split(" ")
                                    batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                    if len(batsmanSplit) == 1: batsmanSplit.append("")
                                    if len(batsmanSplit) == 2: batsmanSplit.append("")
                                    if catcherLastName == batsmanSplit[0].strip() or catcherLastName == batsmanSplit[1].strip() or catcherLastName == batsmanSplit[2].strip() and (catcherI == "" or catcherI == batsman[0]):
                                        catcher = batsman
                                        catcherId = batsman2Id2[batsman]
                            if eventBatsman == "":
                                for batsman in batsmen1Names:
                                    batsmanSplit = batsman.split(" ")
                                    batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                    if len(batsmanSplit) == 1: batsmanSplit.append("")
                                    if len(batsmanSplit) == 2: batsmanSplit.append("")
                                    if batsmanLastName == batsmanSplit[0].strip() or batsmanLastName == batsmanSplit[1].strip() or batsmanLastName == batsmanSplit[2].strip() and (batsmanI == "" or batsmanI == batsman[0]):
                                        eventBatsman = batsman
                            if eventBatsman in batsman2Id1:
                                c.execute('select rating from battingTestLive where playerId=? and testId<? order by testId desc', (batsman2Id1[eventBatsman], testId))
                                battingLiveRating = c.fetchone()
                        else:
                            for bowler in bowler2Names:
                                if catcherEventName == bowler:
                                    catcher = bowler
                                    catcherId = bowler2Id2[bowler]
                            for batsman in batsmen1Names:
                                if catcherEventName == batsman:
                                    catcher = batsman
                                    catcherId = batsman2Id1[batsman]
                            for batsman in batsmen2Names:
                                if batsmanEventName == batsman:
                                    eventBatsman = batsman
                            if catcher == "":
                                for bowler in bowler2Names:
                                    bowlerSplit = bowler.split(" ")
                                    bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                                    if len(bowlerSplit) == 1: bowlerSplit.append("")
                                    if len(bowlerSplit) == 2: bowlerSplit.append("")
                                    if catcherLastName == bowlerSplit[0].strip() or catcherLastName == bowlerSplit[1].strip() or catcherLastName == bowlerSplit[2].strip() and (catcherI == "" or catcherI == bowler[0]):
                                        catcher = bowler
                                        catcherId = bowler2Id2[bowler]
                                for batsman in batsmen1Names:
                                    batsmanSplit = batsman.split(" ")
                                    batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                    if len(batsmanSplit) == 1: batsmanSplit.append("")
                                    if len(batsmanSplit) == 2: batsmanSplit.append("")
                                    if catcherLastName == batsmanSplit[0].strip() or catcherLastName == batsmanSplit[1].strip() or catcherLastName == batsmanSplit[2].strip() and (catcherI == "" or catcherI == batsman[0]):
                                        catcher = batsman
                                        catcherId = batsman2Id1[batsman]
                            if eventBatsman == "":
                                for batsman in batsmen2Names:
                                    batsmanSplit = batsman.split(" ")
                                    batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                                    if len(batsmanSplit) == 1: batsmanSplit.append("")
                                    if len(batsmanSplit) == 2: batsmanSplit.append("")
                                    if batsmanLastName == batsmanSplit[0].strip() or batsmanLastName == batsmanSplit[1].strip() or batsmanLastName == batsmanSplit[2].strip() and (batsmanI == "" or batsmanI == batsman[0]):
                                        eventBatsman = batsman
                            if eventBatsman in batsman2Id2:
                                 c.execute('select rating from battingTestLive where playerId=? and testId<? order by testId desc', (batsman2Id2[eventBatsman], testId))
                                 battingLiveRating = c.fetchone()
                        battingLiveRating = 236.36 if battingLiveRating is None else (236.36 + battingLiveRating[0]/5)
                        if isKeeper == 1: keeper[catcherId] = 1
                        if "c " in eventText:
                            batsmenCaught[catcherId] = batsmenCaught[catcherId] + battingLiveRating if catcherId in batsmenCaught else battingLiveRating
                            fielderName[catcherId] = catcher
                            fielderCatches[catcherId] = fielderCatches[catcherId] + 1 if catcherId in fielderCatches else 1
                        else:
                            batsmenStumped[catcherId] = batsmenStumped[catcherId] + battingLiveRating if catcherId in batsmenStumped else battingLiveRating
                            fielderName[catcherId] = catcher
                            fielderStumpings[catcherId] = fielderStumpings[catcherId] + 1 if catcherId in fielderStumpings else 1

                commentary = commentary.replace("'s ", " ")
                commentary = commentary.replace(",", "")
                commentary = commentary.replace(".", "")
                commentary = commentary.replace("!","") if "fielded!" not in commentary else commentary
                commentaryNoCaps = commentary.lower()
                commentarySplit = commentary.split(" ")
                fielder = ""
                fielderId = 0
                droppedCatch = 0
                misfield = 0
                greatCatch = 0
                greatSave = 0
                eventFound = 0
                runsSaved = 0
                directHit = 0
                missedStumping = 0

                for word in commentarySplit:
                    if len(word) < 2: continue
                    if not word[0].isupper(): continue
                    if ((inn == 1 or inn == 3) and followOn == 0) or ((inn == 1 or inn == 4) and followOn == 1):
                        for bowler in bowler1Names:
                            bowlerSplit = bowler.split(" ")
                            bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                            if len(bowlerSplit) == 1: bowlerSplit.append("")
                            if len(bowlerSplit) == 2: bowlerSplit.append("")
                            if word == bowlerSplit[0].strip() or word == bowlerSplit[1].strip() or word == bowlerSplit[2].strip():
                                if (fielder == "" or fielder == eventBowler or fielder == eventBatsman) and (bowlerFI == "" or bowlerFI == bowler[0]):
                                    fielder = bowler
                                    fielderId = bowler2Id1[bowler]
                                wordPos = commentary.find(word)
                                comChunk = commentary[wordPos:]
                                nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                                nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                                if nextWord == "": continue
                                if nextWord[0].isupper() and (word + " " + nextWord) == bowler and bowler != eventBatsman and bowler != eventBowler:
                                    fielder = bowler
                                    fielderId = bowler2Id1[bowler]
                        for batsman in batsmen2Names:
                            batsmanSplit = batsman.split(" ")
                            batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                            if len(batsmanSplit) == 1: batsmanSplit.append("")
                            if len(batsmanSplit) == 2: batsmanSplit.append("")
                            if word == batsmanSplit[0].strip() or word == batsmanSplit[1].strip() or word == batsmanSplit[2].strip():
                                if (fielder == "" or fielder == eventBatsman or fielder == eventBowler):
                                    fielder = batsman
                                    fielderId = batsman2Id2[batsman]
                                wordPos = commentary.find(word)
                                comChunk = commentary[wordPos:]
                                nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                                nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                                if nextWord == "": continue
                                if nextWord[0].isupper() and (word + " " + nextWord) == batsman and batsman != eventBatsman and batsman != eventBowler:
                                    fielder = batsman
                                    fielderId = batsman2Id2[batsman]
                    else:
                        for bowler in bowler2Names:
                            bowlerSplit = bowler.split(" ")
                            bowlerSplit = bowler.split("-") if len(bowlerSplit) == 1 else bowlerSplit
                            if len(bowlerSplit) == 1: bowlerSplit.append("")
                            if len(bowlerSplit) == 2: bowlerSplit.append("")
                            if word == bowlerSplit[0].strip() or word == bowlerSplit[1].strip() or word == bowlerSplit[2].strip():
                                if (fielder == "" or fielder == eventBowler or fielder == eventBatsman) and (bowlerFI == "" or bowlerFI == bowler[0]):
                                    fielder = bowler
                                    fielderId = bowler2Id2[bowler]
                                wordPos = commentary.find(word)
                                comChunk = commentary[wordPos:]
                                nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                                nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                                if nextWord == "": continue
                                if nextWord[0].isupper() and (word + " " + nextWord) == bowler and bowler != eventBatsman and bowler != eventBowler:
                                    fielder = bowler
                                    fielderId = bowler2Id2[bowler]
                        for batsman in batsmen1Names:
                            batsmanSplit = batsman.split(" ")
                            batsmanSplit = batsman.split("-") if len(batsmanSplit) == 1 else batsmanSplit
                            if len(batsmanSplit) == 1: batsmanSplit.append("")
                            if len(batsmanSplit) == 2: batsmanSplit.append("")
                            if word == batsmanSplit[0].strip() or word == batsmanSplit[1].strip() or word == batsmanSplit[2].strip():
                                if (fielder == "" or fielder == eventBatsman or fielder == eventBowler):
                                    fielder = batsman
                                    fielderId = batsman2Id1[batsman]
                                wordPos = commentary.find(word)
                                comChunk = commentary[wordPos:]
                                nextSpacePos = comChunk[comChunk.find(" ")+1:].find(" ")
                                nextWord = comChunk[comChunk.find(" ")+1:comChunk.find(" ")+1+nextSpacePos]
                                if nextWord == "": continue
                                if nextWord[0].isupper() and (word + " " + nextWord) == batsman and batsman != eventBatsman and batsman != eventBowler:
                                    fielder = batsman
                                    fielderId = batsman2Id1[batsman]
                    if (("missed the stumping" in commentaryNoCaps or "missed stumping" in commentaryNoCaps or "stumping missed" in commentaryNoCaps or "misses a stumping" in commentaryNoCaps) and "OUT" not in eventSplit[2] and fielder == eventBowler): fielder = "";

                fielderCatches[fielderId] = fielderCatches[fielderId] if fielderId in fielderCatches else 0
                batsmenCaught[fielderId] = batsmenCaught[fielderId] if fielderId in batsmenCaught else 0
                fielderStumpings[fielderId] = fielderStumpings[fielderId] if fielderId in fielderStumpings else 0
                batsmenStumped[fielderId] = batsmenStumped[fielderId] if fielderId in batsmenStumped else 0
                fielderName[fielderId] = fielder
                fielderDroppedCatches[fielderId] = fielderDroppedCatches[fielderId] if fielderId in fielderDroppedCatches else 0
                fielderMisfield[fielderId] = fielderMisfield[fielderId] if fielderId in fielderMisfield else 0
                fielderMissedStumping[fielderId] = fielderMissedStumping[fielderId] if fielderId in fielderMissedStumping else 0
                fielderGreatCatch[fielderId] = fielderGreatCatch[fielderId] if fielderId in fielderGreatCatch else 0
                fielderDirectHit[fielderId] = fielderDirectHit[fielderId] if fielderId in fielderDirectHit else 0
                fielderGreatSave[fielderId] = fielderGreatSave[fielderId] if fielderId in fielderGreatSave else 0
                fielderRunsSaved[fielderId] = fielderRunsSaved[fielderId] if fielderId in fielderRunsSaved else 0
                batsmenDropped[fielderId] = batsmenDropped[fielderId] if fielderId in batsmenDropped else 0
                batsmenGreatCatch[fielderId] = batsmenGreatCatch[fielderId] if fielderId in batsmenGreatCatch else 0
                batsmenDirectHit[fielderId] = batsmenDirectHit[fielderId] if fielderId in batsmenDirectHit else 0
                batsmenMissedStumping[fielderId] = batsmenMissedStumping[fielderId] if fielderId in batsmenMissedStumping else 0
                if ("bobbles the chance" in commentaryNoCaps or "has made a meal of it" in commentaryNoCaps or "sitter" in commentaryNoCaps or ("drop" in commentaryNoCaps and "in and out of" in commentaryNoCaps) or ("dolly" in commentaryNoCaps and "dolly on the toes" not in commentaryNoCaps) or "spills" in commentaryNoCaps or "put down" in commentaryNoCaps or "dropping the ball" in commentaryNoCaps or "gets both hands to it but drops it" in commentaryNoCaps or "drops an easy catch" in commentaryNoCaps or "fails to take the catch" in commentaryNoCaps or ("dropped" in commentaryNoCaps and "dropped right" not in commentaryNoCaps and "dropped with" not in commentaryNoCaps and "dropped just" not in commentaryNoCaps and "dropped it short" not in commentaryNoCaps and "dropped short" not in commentaryNoCaps and "dropped well in front" not in commentaryNoCaps and "drops the wrist" not in commentaryNoCaps and "dropped from" not in commentaryNoCaps and "earlier he was dropped" not in commentaryNoCaps and "dropped his" not in commentaryNoCaps and "dropped a touch short" not in commentaryNoCaps and "dropped catches" not in commentaryNoCaps and "dropped behind" not in commentaryNoCaps and "dropped at his feet" not in commentaryNoCaps and "dropped in" not in commentaryNoCaps and "dropped a bit" not in commentaryNoCaps and "dropped into" not in commentaryNoCaps and "dropped softly" not in commentaryNoCaps and "dropped his bat" not in commentaryNoCaps and "dropped catch and" not in commentaryNoCaps and "dropped it into" not in commentaryNoCaps and "dropped to" not in commentaryNoCaps and "dropped him earlier" not in commentaryNoCaps and "dropped far too short" not in commentaryNoCaps and "dropped over" not in commentaryNoCaps) or "shelled" in commentaryNoCaps or "grassed" in commentaryNoCaps) and ("tough chance" not in commentaryNoCaps and "hard chance" not in commentaryNoCaps and "hard to call it dropped" not in commentaryNoCaps and "hard to call that dropped" not in commentaryNoCaps and "like a football goalkeeper" not in commentaryNoCaps and "desperate effort" not in commentaryNoCaps and "difficult chance" not in commentaryNoCaps and "superb attempt" not in commentaryNoCaps and "good effort" not in commentaryNoCaps and "screaming past" not in commentaryNoCaps and "would have been a very good" not in commentaryNoCaps and "terrific effort" not in commentaryNoCaps and "harsh to blame" not in commentaryNoCaps and "great attempt" not in commentaryNoCaps and "what an effort" not in commentaryNoCaps and "would have been a terrific catch" not in commentaryNoCaps and "would have been a wundercatch" not in commentaryNoCaps and "tough one" not in commentaryNoCaps and "fabulous attempt" not in commentaryNoCaps and "tremendous effort" not in commentaryNoCaps and "difficult one" not in commentaryNoCaps and "would have been a stunner" not in commentaryNoCaps and "would have been a superb" not in commentaryNoCaps and "would have been a mind-blowing" not in commentaryNoCaps and "valiant effort" not in commentaryNoCaps and "harsh to call it" not in commentaryNoCaps and "would have been a classic catch" not in commentaryNoCaps and "would have been a cracker" not in commentaryNoCaps) and ("OUT" not in eventSplit[2]):
                    droppedCatch = 1
                if ("fumble" in commentaryNoCaps or "misfield" in commentaryNoCaps or "slip through his legs" in commentaryNoCaps or "poor fielding" in commentaryNoCaps or "poor effort" in commentaryNoCaps or "bad fielding" in commentaryNoCaps or "makes a mess of it" in commentaryNoCaps or "not great fielding" in commentaryNoCaps) and ("OUT" not in eventSplit[2]):
                    misfield = 1
                    if ("1" in eventSplit[2]): runsSaved = -1
                    if ("2" in eventSplit[2]): runsSaved = -1
                    if ("3" in eventSplit[2]): runsSaved = -1
                    if ("FOUR" in eventSplit[2] or "4" in eventSplit[2]): runsSaved = -2
                if ("whattay catch" in commentaryNoCaps or "what a catch" in commentaryNoCaps or "stunning catch" in commentaryNoCaps or "wonderful catch" in commentaryNoCaps or "times his jump perfectly to take this one-handed" in commentaryNoCaps or "pulled this off one-handed" in commentaryNoCaps or "one-handed stunner" in commentaryNoCaps or "plucks it" in commentaryNoCaps or "blinder" in commentaryNoCaps or "top catch" in commentaryNoCaps or "great catch" in commentaryNoCaps or "amazing catch" in commentaryNoCaps or "unbelievable catch" in commentaryNoCaps or "stupendous catch" in commentaryNoCaps or "tough catch" in commentaryNoCaps or "brilliant catch" in commentaryNoCaps or "tremendous catch" in commentaryNoCaps or "fantastic catch" in commentaryNoCaps or "fantastic running catch" in commentaryNoCaps or "flying catch" in commentaryNoCaps) and "OUT" in eventSplit[2]:
                    greatCatch = 1
                if ("fielded!" in commentaryNoCaps) or ("great fielding" in commentaryNoCaps and "not great fielding" not in commentaryNoCaps) or ("good bit of fielding" in commentaryNoCaps)  or ("good piece of fielding" in commentaryNoCaps) or ("excellent fielding" in commentaryNoCaps) or ("saved a boundary" in commentaryNoCaps) or ("saved four runs" in commentaryNoCaps) or ("saves four runs" in commentaryNoCaps) or ("saves three runs" in commentaryNoCaps) or ("saved three runs" in commentaryNoCaps) or ("brilliant work" in commentaryNoCaps) or ("diving stop" in commentaryNoCaps) or ("saves a few runs" in commentaryNoCaps) or ("saved a few runs" in commentaryNoCaps) or ("saves some runs" in commentaryNoCaps) or ("saved some runs" in commentaryNoCaps) or ("massive dive" in commentaryNoCaps):
                    greatSave = 1
                if (("direct hit" in commentaryNoCaps or "accurate with the throw" in commentaryNoCaps or "throw has beaten him" in commentaryNoCaps or "hits the stumps direct" in commentaryNoCaps) and "OUT" in eventSplit[2]):
                    directHit = 1
                if (("missed the stumping" in commentaryNoCaps or "missed stumping" in commentaryNoCaps or "stumping missed" in commentaryNoCaps or "misses a stumping" in commentaryNoCaps) and "OUT" not in eventSplit[2] and fielderId in keeper):
                    missedStumping = 1
                if ("saved a boundary" in commentaryNoCaps) or ("saves three runs" in commentaryNoCaps) or ("saved three runs" in commentaryNoCaps):
                    runsSaved = 3
                elif ("saved four runs" in commentaryNoCaps) or ("saves four runs" in commentaryNoCaps):
                    runsSaved = 4
                elif ("saved two runs" in commentaryNoCaps) or ("saves two runs" in commentaryNoCaps) or ("saves a couple" in commentaryNoCaps) or ("saved a couple" in commentaryNoCaps):
                    runsSaved = 2
                elif ("saved a single" in commentaryNoCaps) or ("saves a single" in commentaryNoCaps) or ("saves a run" in commentaryNoCaps) or ("saved a run" in commentaryNoCaps):
                    runsSaved = 1
                if greatSave == 1 and runsSaved == 0: runsSaved = 2
                if droppedCatch == 1 and fielder == "" and "bowler" in commentaryNoCaps: fielder = eventBowler
                if "substitute" in commentaryNoCaps: fielder = ""
                if eventFound == 0 and fielder != "" and fielder != eventBatsman and (droppedCatch == 1 or misfield == 1 or missedStumping == 1 or greatCatch == 1 or directHit == 1 or greatSave == 1):
                    eventFound = 1
                    print eventSplit
                    if ((inn == 1 or inn == 3) and followOn == 0) or ((inn == 1 or inn == 4) and followOn == 1):
                        c.execute('select rating from battingTestLive where playerId=? and testId<? order by testId desc', (batsman2Id1[eventBatsman], testId))
                    else:
                        c.execute('select rating from battingTestLive where playerId=? and testId<? order by testId desc', (batsman2Id2[eventBatsman], testId))
                    battingLiveRating = c.fetchone()
                    battingLiveRating = 236.36 if battingLiveRating is None else (236.36 + battingLiveRating[0]/5)
                    if droppedCatch == 1: batsmenDropped[fielderId] = batsmenDropped[fielderId] + battingLiveRating
                    if directHit == 1: batsmenDirectHit[fielderId] = batsmenDirectHit[fielderId] + battingLiveRating
                    if greatCatch == 1: batsmenGreatCatch[fielderId] = batsmenGreatCatch[fielderId] + battingLiveRating
                    if missedStumping == 1: batsmenMissedStumping[fielderId] = batsmenMissedStumping[fielderId] + battingLiveRating
                    fielderDroppedCatches[fielderId] += droppedCatch
                    fielderMisfield[fielderId] += misfield
                    fielderMissedStumping[fielderId] += missedStumping
                    fielderGreatCatch[fielderId] += greatCatch
                    fielderDirectHit[fielderId] += directHit
                    fielderGreatSave[fielderId] += greatSave
                    fielderRunsSaved[fielderId] += runsSaved
                    if ((inn == 1 or inn == 3) and followOn == 0) or ((inn == 1 or inn == 4) and followOn == 1):
                        c.execute('insert or ignore into fieldingEventTest (eventId, testId, bowler, batsman, bowlerId, batsmanId, fielder, fielderId, droppedCatch, misfield, missedStumping,'
                                  'greatCatch, directHit, greatFielding, runsSaved, commentary) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (eventId, testId, eventBowler, eventBatsman, bowler2Id1[eventBowler], batsman2Id1[eventBatsman], fielder, fielderId, droppedCatch, misfield, missedStumping,
                                 greatCatch, directHit, greatSave, runsSaved, commentary))
                    else:
                        c.execute('insert or ignore into fieldingEventTest (eventId, testId, bowler, batsman, bowlerId, batsmanId, fielder, fielderId, droppedCatch, misfield, missedStumping,'
                                  'greatCatch, directHit, greatFielding, runsSaved, commentary) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (eventId, testId, eventBowler, eventBatsman, bowler2Id2[eventBowler], batsman2Id2[eventBatsman], fielder, fielderId, droppedCatch, misfield, missedStumping,
                                 greatCatch, directHit, greatSave, runsSaved, commentary))

    if detailedCommentaryCount == 0: continue
    if 0 in fielderCatches: del fielderCatches[0]
    for fielderId in fielderCatches.keys():
        batsmenDropped[fielderId] = 0 if fielderId not in batsmenDropped else batsmenDropped[fielderId]
        batsmenGreatCatch[fielderId] = 0 if fielderId not in batsmenGreatCatch else batsmenGreatCatch[fielderId]
        batsmenDirectHit[fielderId] = 0 if fielderId not in batsmenDirectHit else batsmenDirectHit[fielderId]
        batsmenStumped[fielderId] = 0 if fielderId not in batsmenStumped else batsmenStumped[fielderId]
        batsmenMissedStumping[fielderId] = 0 if fielderId not in batsmenMissedStumping else batsmenMissedStumping[fielderId]
        fielderStumpings[fielderId] = 0 if fielderId not in fielderStumpings else fielderStumpings[fielderId]
        fielderMissedStumping[fielderId] = 0 if fielderId not in fielderMissedStumping else fielderMissedStumping[fielderId]
        fielderGreatCatch[fielderId] = 0 if fielderId not in fielderGreatCatch else fielderGreatCatch[fielderId]
        fielderDirectHit[fielderId] = 0 if fielderId not in fielderDirectHit else fielderDirectHit[fielderId]
        fielderRunsSaved[fielderId] = 0 if fielderId not in fielderRunsSaved else fielderRunsSaved[fielderId]
        fielderDroppedCatches[fielderId] = 0 if fielderId not in fielderDroppedCatches else fielderDroppedCatches[fielderId]
        fielderMisfield[fielderId] = 0 if fielderId not in fielderMisfield else fielderMisfield[fielderId]
        fielderGreatSave[fielderId] = 0 if fielderId not in fielderGreatSave else fielderGreatSave[fielderId]
        if fielderGreatCatch[fielderId] > 0 and fielderCatches[fielderId] < fielderGreatCatch[fielderId]: fielderCatches[fielderId] = fielderGreatCatch[fielderId]
        rating = batsmenCaught[fielderId] * 0.125 + batsmenStumped[fielderId] * 0.125 - batsmenMissedStumping[fielderId] + batsmenGreatCatch[fielderId] + batsmenDirectHit[fielderId] + fielderRunsSaved[fielderId] * 25 - batsmenDropped[fielderId]
        if rating == 0: continue
        print fielderName[fielderId] + " " + `rating`
        matchId = repr(int(testId)) + repr(fielderId)
        c.execute('insert or ignore into fieldingTestMatch (matchId, playerId, player, testId, keeper, catches, droppedCatches, misfields, stumpings, missedStumpings, greatCatches, directHits, greatSaves, runsSaved, '
                  'rating) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (matchId, fielderId, fielderName[fielderId], testId, (1 if fielderId in keeper else 0), fielderCatches[fielderId], fielderDroppedCatches[fielderId], fielderMisfield[fielderId], fielderStumpings[fielderId],
                  fielderMissedStumping[fielderId], fielderGreatCatch[fielderId], fielderDirectHit[fielderId], fielderGreatSave[fielderId], fielderRunsSaved[fielderId], rating))

        c.execute('select matchId, rating from fieldingTestLive where playerId=? order by matchId desc', (fielderId, ))
        fieldingLiveRating[fielderId] = c.fetchone()
        if fieldingLiveRating[fielderId] is None:
            fieldingLiveRating[fielderId] = 0
            fieldingNumCareerMatches[fielderId] = 0
        else:
            fieldingLiveRating[fielderId] = fieldingLiveRating[fielderId][1]
            fieldingNumCareerMatches[fielderId] = len(c.fetchall())+1

        if fieldingNumCareerMatches[fielderId] == 0: # discount live ratings for a player's first 10 innings to avoid them hitting top rankings prematurely
            liveRating = rating * 0.15
        elif fieldingNumCareerMatches[fielderId] < 10:
            liveRating = expSmoothFactor * rating * (0.66 + newPlayerPenaltyFactor*(fieldingNumCareerMatches[fielderId]-1)) + (1 - expSmoothFactor) * fieldingLiveRating[fielderId]
        else:
            liveRating = expSmoothFactor * rating + (1 - expSmoothFactor) * fieldingLiveRating[fielderId]
        c.execute('insert or ignore into fieldingTestLive(matchId, startDate, playerId, testId, player, rating) values (?, ?, ?, ?, ?, ?)',
                    (matchId, startDate, fielderId, testId, fielderName[fielderId], liveRating))

    conn.commit()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print 'Time elapsed: ' + `elapsedMin` + 'min'
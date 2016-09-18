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
c.execute('drop table tossTest')
c.execute('''create table tossTest (testId integer unique, toss text)''')

# get odis info
c.execute('select * from testInfo')
testsInfo = c.fetchall()

# loop through odi matches
tossFile = open("tossTest.csv", "w")
for x in range(startTest, len(testsInfo)):
    testId = testsInfo[x][0]
    team1 = testsInfo[x][3]
    team2 = testsInfo[x][4]
    result = testsInfo[x][8]
    print testId
    scorecardURL = 'http://www.espncricinfo.com' + testsInfo[x][12]
    scorecardPage = requests.get(scorecardURL)
    scoreTree = html.fromstring(scorecardPage.text)
    toss = scoreTree.xpath('(//div[@class="match-information"]/div/span/text())')
    if toss[0] == "4" or toss[0] == "8" or toss[0] == "5" or toss[0] == "6": toss.pop(0)
    toss = toss[0].split(",")[0]
    tossFile.write(str(team1) + "," + str(team2) + "," +str(result) + "," +str(toss) + "\n")
    print str(team1) + "," + str(team2) + "," +str(result) + "," +str(toss) + "\n"
    c.execute('insert or replace into tossTest (testId, toss) values (?, ?)', (testId, toss))
    conn.commit()
tossFile.close()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')
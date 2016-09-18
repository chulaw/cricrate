#!/usr/bin/env python
import time
import lxml.html
from lxml import html
import requests
import sqlite3
start = time.clock()

startODI = int(input('Enter starting ODI #: '))

# connect to db
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()
c.execute('drop table tossODI')
c.execute('''create table tossODI (odiId integer unique, toss text)''')

# get odis info
c.execute('select * from odiInfo')
odisInfo = c.fetchall()

# loop through odi matches
tossFile = open("toss.csv", "w")
for x in range(startODI, len(odisInfo)):
    # load cricinfo scorecard html
    odiId = odisInfo[x][0]
    team1 = odisInfo[x][3]
    team2 = odisInfo[x][4]
    result = odisInfo[x][8]
    print odiId
    scorecardURL = 'http://www.espncricinfo.com' + odisInfo[x][12]
    scorecardPage = requests.get(scorecardURL)
    scoreTree = html.fromstring(scorecardPage.text)
    toss = scoreTree.xpath('(//div[@class="match-information"]/div/span/text())')
    if toss[0] == "8": toss.pop(0)
    toss = toss[0].split(",")[0]
    tossFile.write(str(team1) + "," + str(team2) + "," +str(result) + "," +str(toss) + "\n")
    print str(team1) + "," + str(team2) + "," +str(result) + "," +str(toss) + "\n"
    c.execute('insert or replace into tossODI (odiId, toss) values (?, ?)', (odiId, toss))
    conn.commit()
tossFile.close()
conn.close()
elapsedSec = (time.clock() - start)
elapsedMin =  elapsedSec / 60
print('Time elapsed: ' + repr(elapsedMin) + 'min')
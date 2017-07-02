#!/usr/bin/env python
import lxml.html
from lxml import html
import requests
import sqlite3
conn = sqlite3.connect('ccrODI.db')

c = conn.cursor()
c.execute('drop table retiredPlayers')
c.execute('create table retiredPlayers (playerId integer unique, retireODI integer)')

# for row in c.execute('select playerId, max(odiId) from battingODIInnings group by playerId'):
#       print row

playerMaxODI = {}
c.execute('select playerId, max(odiId) from battingODIInnings group by playerId')
for batsmanLastODI in c.fetchall():
    pid = batsmanLastODI[0]
    lastODIId = batsmanLastODI[1]
    playerMaxODI[pid] = lastODIId

c.execute('select playerId, max(odiId) from bowlingODIInnings group by playerId')
for bowlerLastODI in c.fetchall():
    pid = bowlerLastODI[0]
    lastODIId = bowlerLastODI[1]
    if pid in playerMaxODI:
        if lastODIId > playerMaxODI[pid]:
            playerMaxODI[pid] = lastODIId
    else:
        playerMaxODI[pid] = lastODIId

for playerId in playerMaxODI:
    if playerMaxODI[playerId] < 3572: # 01/08/2015
        print `playerId` + ' ' + `playerMaxODI[playerId]`
        c.execute('insert or replace into retiredPlayers(playerId, retireODI) values (?, ?)',
                (playerId, playerMaxODI[playerId]))

c.execute('insert into retiredPlayers values (111631, 3636)')
c.execute('insert into retiredPlayers values (85281, 3642)')
c.execute('insert into retiredPlayers values (11123, 3645)')
c.execute('insert into retiredPlayers values (77423, 3646)')
c.execute('insert into retiredPlayers values (9159, 3646)')
c.execute('insert into retiredPlayers values (101423, 3640)')
c.execute('insert into retiredPlayers values (98581, 3640)')
c.execute('insert into retiredPlayers values (82759, 3642)')
c.execute('insert into retiredPlayers values (12069, 3646)')
conn.commit()
conn.close()

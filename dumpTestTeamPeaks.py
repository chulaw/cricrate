#!/usr/bin/env python
from datetime import date
import sqlite3
import math

# connect to db
conn = sqlite3.connect('ccr.db')
c = conn.cursor()

c.execute('select distinct team from teamTestLive order by team asc')
for team in c.fetchall():
    c.execute('select startDate, rating from teamTestLive where team="'+team[0]+'" order by rating asc')
    for teamRating in c.fetchall():
        startDate = teamRating[0]
        rating = teamRating[1]
        c.execute('select startDate, rating from teamTestLive where team="'+team[0]+'" and startDate<? order by startDate desc',(startDate, ))
        beforeRating = c.fetchone()
        if beforeRating is None: continue
        beforeRating = beforeRating[1]

        c.execute('select startDate, rating from teamTestLive where team="'+team[0]+'" and startDate>? order by startDate asc',(startDate, ))
        afterRating = c.fetchone()
        if afterRating is None: continue
        afterRating = afterRating[1]

        if rating > beforeRating and rating > afterRating:
            print team[0] + ' ' + startDate + ' ' + `rating`

# conn.commit()
conn.close()

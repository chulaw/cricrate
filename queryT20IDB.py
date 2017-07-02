#!/usr/bin/env python
import time
start = time.clock()
import sqlite3
conn = sqlite3.connect('ccrT20I.db')
c = conn.cursor()
#for row in c.execute('SELECT * FROM groundInfo'):
#    print row
for row in c.execute('SELECT max(t20iId) FROM battingT20IInnings'):
    print row

# for row in c.execute('delete FROM battingT20IInnings where t20iId>0'):
#        print row
# for row in c.execute('delete FROM bowlingT20IInnings where t20iId>0'):
#        print row
# for row in c.execute('delete FROM allRoundT20IMatch where t20iId>0'):
#      print row
# for row in c.execute('delete FROM allRoundT20ILive where t20iId>0'):
#      print row
# for row in c.execute('delete FROM battingT20ILive where t20iId>0'):
#      print row
# for row in c.execute('delete FROM bowlingT20ILive where t20iId>0'):
#      print row
#homeAwayFile = open("homeAwayT20I.csv", "w")
#for row in c.execute('SELECT team1, team2, location, result from t20iInfo'):
#    homeAwayFile.write(str(row[0]) + "," + str(row[1]) + "," +str(row[2]) + "," +str(row[3]) + "," + "\n")
#    print(row)
#homeAwayFile.close()
#for row in c.execute('SELECT * FROM playerInfo where name=?',('Brian Lara',)):
#    print row
#for row in c.execute('SELECT * FROM battingT20IInnings where player=?',('Ricky Ponting',)):
#    print row
#for row in c.execute("select b.playerId, b.player, b.balls, t.ballsPerOver, b.runs, b.wkts, b.rating, p.country, t.team1, t.team2, t.startDate, t.testId, t.scoreLink from bowlingT20IInnings b, testInfo t, playerInfo p where b.testId=t.testId and b.playerId=p.playerId and b.rating > 1000 order by b.rating desc"):
#    print row
#for row in c.execute('SELECT * FROM bowlingT20IInnings'):
#    print row
#for row in c.execute('SELECT * FROM battingT20ILive where player=?',('Brian Lara',)):
#    print row
#for row in c.execute('SELECT * FROM battingT20IInnings where player=?',('Ken Barrington',)):
#    print row
#for row in c.execute('SELECT * FROM bowlingT20IInnings where player=?',('Muttiah Muralitharan',)):
#    print row
#for row in c.execute('SELECT * FROM bowlingT20ILive where testId=?',(1572,)):
#    print row
#for row in c.execute("select b.playerId, b.player, p.country, b.rating from bowlingT20ILive b, playerInfo p inner join(select playerId, max(inningsId) maxInningsId from bowlingT20ILive group by playerId) bb on b.playerId = bb.playerId and b.inningsId = bb.maxInningsId and b.startDate>'20140101' and p.playerId=b.playerId order by b.rating desc"):
    #print row
#for row in c.execute('SELECT * FROM bowlingT20ILive where player=?',('Muttiah Muralitharan',)):
#    print row
#for row in c.execute('SELECT * FROM battingT20ICareer order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM bowlingT20ICareer order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM allRoundT20ICareer order by rating asc'):
#    print row
#for row in c.execute('select startDate, endDate, innings, balls, runs, wickets, average, econRate, strikeRate, threeWkts, fiveWkts, rating from bowlingT20ICareer where playerId=44936'):
#    print row
#for row in c.execute("select b.playerId, t.startDate, p.country, t.team1, t.team2, b.rating from battingT20ILive b, playerInfo p, t20iInfo t inner join (select playerId, max(rating) maxRating from battingT20ILive group by playerId) as bb on bb.playerId=b.playerId and bb.maxRating=b.rating and p.playerId=b.playerId and t.t20iId=b.t20iId order by b.rating asc"):
#    print row
# c.execute('insert into retiredPlayers values (75477)')
# conn.commit()
conn.close()
elapsed = (time.clock() - start)
print elapsed
#
#
#select
#  Name, Top, Total
#from
#  sometable
#  inner join (
#    select max(Total) Total, Name
#    from sometable
#    group by Name
#  ) as max on max.Name = sometable.Name and max.Total = sometable.Total

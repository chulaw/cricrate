#!/usr/bin/env python
import time
start = time.clock()
import sqlite3
conn = sqlite3.connect('ccr.db')
c = conn.cursor()
# for row in c.execute('select b.playerId, b.player, b.notOut, b.runs, b.balls, b.rating, p.country, t.team1, t.team2, t.ground, t.startDate, t.testId from battingTestInnings b, testInfo t, playerInfo p where b.testId=t.testId and b.playerId=p.playerId and b.rating > 1000 order by b.rating desc limit 107'):
#     print(row)
#for row in c.execute("select startDate, rating, opposition, location, result from teamTestLive where team='Australia'"):    
#    print row
# for row in c.execute('DELETE FROM testInfo where testId>2213'):
#       print(row)
#for row in c.execute('select count(testId) FROM testInfo where startDate>=20100101'):
#      print(row)
#for row in c.execute('select ocId, overs, runs, wkts, runsReq, ballsRem, result from overComparisonTest'):
#    print row
# for row in c.execute('SELECT avg(entryRuns) as AvgEntryRuns FROM battingTestInnings GROUP BY entryWkts'):
#     print(row)
# for row in c.execute('SELECT runs, balls, notOut FROM battingTestInnings where playerId=10783 and entryWkts=5'):
#     print(row)

#for row in c.execute('SELECT testId from testInfo where ground=\"Hobart\"'):
#     print(row)
# for row in c.execute('SELECT avg(runs) from detailsTestInnings where testId in (1133, 1236, 1313, 1388, 1469, 1571, 1771, 1847, 1947, 2021, 2067) and innings=1 and wickets=10'):
#      print(row)
# for row in c.execute('SELECT avg(runs) from detailsTestInnings where innings=1 and wickets=10'):
#      print(row)

# import csv
# csvF = open("bowlInn.csv", "a")
# for row in c.execute('SELECT wkts, result from bowlingTestInnings'):
#     csvF.write(str(row[0]) +"," + str(row[1]) + "\n")
# csvF.close()
# for row in c.execute('delete FROM allRoundTestMatch'):
#      print row
# for row in c.execute('delete FROM battingTestLive'):
#      print row
# for row in c.execute('delete FROM bowlingTestLive'):
#      print row
# for row in c.execute('delete FROM allRoundTestLive'):
#      print row
#for row in c.execute('select count(commentary) FROM fieldingEventTest where directHit>0'):
#            print row
#for row in c.execute('select commentary FROM fieldingEventTest where droppedCatch=1 and fielder=?',("Rahul Dravid",)):
#                   print row
# for row in c.execute('select rankDiff, rank, rating, player, country, bestCurrentRating from fieldingTestCurrent order by rating desc limit 100'):
#         print row
# for row in c.execute('select * from fieldingTestMatch order by rating desc limit 100'):
#         print row
# for row in c.execute('select matchId, rating from fieldingTestMatch where player=?',("Monty Panesar",)):
#           print row
# for row in c.execute('select eventId, commentary FROM fieldingEventTest where fielder=?',("Monty Panesar",)):
#                print row
# for row in c.execute('select commentary FROM commentaryEventTest where commentary like \"%misses a stumping%\"'):
#            print row
# for row in c.execute('SELECT player,tests,catches,dropRate,matPerMisfield,rating FROM fieldingTestCareer where player=?',("Matt Prior",)):
#        print row
#for row in c.execute('SELECT max(balls) FROM detailsTestInnings'):
#       print row
# for row in c.execute('SELECT player FROM fieldingTestCareer where droppedCatches>0 and catches=0'):
#        print row
#for row in c.execute('SELECT player,tests,catches,dropRate,matPerMisfield,rating FROM fieldingTestCareer where rating>0 order by rating desc'):
#         print row
# for row in c.execute('SELECT * FROM fieldingTestCareer where missedStumpings>0 order by missedStumpings asc'):
#              print row
#for row in c.execute('SELECT * FROM bowlerFieldingTestCareer where droppedCatches>0 order by droppedCatches desc '):
#       print row
# for row in c.execute('SELECT * FROM batsmanFieldingTestCareer where droppedCatches>0 order by droppedCatches desc '):
#         print row
# for row in c.execute('select sum(droppedCatches) FROM fieldingTestMatch'):
#                print row
#for row in c.execute('select commentary FROM commentaryEventTest where commentary like \"%accurate with the throw%\"'):
#            print row
#for row in c.execute("select b.playerId, b.player, b.balls, t.ballsPerOver, b.runs, b.wkts, b.rating, p.country, t.team1, t.team2, t.startDate, t.testId, t.scoreLink from bowlingTestInnings b, testInfo t, playerInfo p where b.testId=t.testId and b.playerId=p.playerId and b.rating > 1000 order by b.rating desc"):
#    print row    
#for row in c.execute('SELECT * FROM bowlingTestInnings order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM battingTestLive where player=?',('Brian Lara',)):
#    print row
#for row in c.execute('select b.playerId, b.player, p.country, b.startDate, b.endDate, b.tests, b.innings, b.balls, b.runs, b.wickets, b.average, b.econRate, b.strikeRate, b.fiveWkts, b.tenWkts, b.rating from bowlingTestCareer b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>18770101 and ((b.startDate+b.endDate)/2)<=20151231 and p.country= order by b.rating desc limit 100'):
#    print row
#for row in c.execute("SELECT player,avg(runs) as avgRuns FROM battingTestInnings where runs>=50 and notOut=0 group by player order by avgRuns asc"):
#    print row
#for row in c.execute('select tests, runs, wickets from bowlingTestCareer where wickets>99'):
#    print row
# for row in c.execute('select innings, notOuts, runs from battingTestCareer where runs>999'):
#     print row
#for row in c.execute('SELECT * FROM bowlingTestInnings where player=?',('Muttiah Muralitharan',)):
#    print row
#for row in c.execute('SELECT * FROM bowlingTestLive where testId=?',(1572,)):
#    print row
#for row in c.execute("select b.playerId, b.player, p.country, b.rating from bowlingTestLive b, playerInfo p inner join(select playerId, max(inningsId) maxInningsId from bowlingTestLive group by playerId) bb on b.playerId = bb.playerId and b.inningsId = bb.maxInningsId and b.startDate>'20140101' and p.playerId=b.playerId order by b.rating desc"):
    #print row
#for row in c.execute('SELECT * FROM bowlingTestLive where player=?',('Muttiah Muralitharan',)):
#    print row
#for row in c.execute('SELECT count(*) FROM battingTestCareer where average>40 and runs>2750'):
#    print row
#for row in c.execute('SELECT count(*) FROM bowlingTestCareer where average<30.33 and wickets>100'):
#    print row
#for row in c.execute('select b.playerId, b.player, max(b.rating) maxRating from battingTestLive b group by playerId order by maxRating asc'):
#for row in c.execute("select b.playerId, b.player, t.startDate, p.country, t.team1, t.team2, b.rating from battingTestLive b, playerInfo p, testInfo t inner join (select playerId, max(rating) maxRating from battingTestLive group by playerId) as bb on bb.playerId=b.playerId and bb.maxRating=b.rating and p.playerId=b.playerId and t.testId=b.testId order by b.rating asc"):
#    print row
#for row in c.execute("select b.playerId, b.player, p.country, b.startDate, b.endDate, b.tests, b.innings, b.notOuts, b.runs, b.average, b.fifties, b.hundreds, b.dblHundreds, b.tripleHundreds, b.rating from battingTestCareer b, playerInfo p where p.playerId=b.playerId and ((b.startDate+b.endDate)/2)>20000101  and ((b.startDate+b.endDate)/2)<20091231 order by b.rating desc limit 100"):
#    print row    
#for row in c.execute('SELECT * FROM battingTestCareer where runs>1000 order by strikeRate asc'):
    #print row
#for row in c.execute('SELECT * FROM allRoundTestCareer order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM allRoundTestMatch order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM battingTestCurrent order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM bowlingTestCurrent order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM teamTestLive where team=? order by startDate desc',('England',)):
#for row in c.execute('SELECT SUBSTR(l.testTeamId, 1, LENGTH(l.testTeamId)-1) AS l.testId, t.scoreLink FROM teamTestLive l, testInfo t where l.testId=t.testId order by l.rating desc limit 100'):
#for row in c.execute('SELECT l.team, l.rating, m.scoreLink FROM teamTestLive l, teamTestMatch m where l.testTeamId=m.testTeamId order by l.rating desc limit 100'):
#for row in c.execute('select playerId, player from playerInfo where player like \"%Warne%\"'):
#for row in c.execute('select playerId, rankDiff, rank, rating, player, country, bestCurrentRating from battingTestCurrent where playerId not in (98581, 91581) order by rating desc limit 100'):
#for row in c.execute('select * from bowlingTestCareer where player=? order by rating asc',('Dennis Lillee',)):
#for row in c.execute('select * from battingTestInnings where testId=?',(1,)):
##for row in c.execute('select * from detailsTestInnings where testId=?',(1,)):
##for row in c.execute('select t.team, t.startDate, t.rating from teamTestLive t inner join (select team, max(rating) maxRating from teamTestLive group by team) as tt on tt.team=t.team and tt.maxRating=t.rating order by t.rating desc'):
    #print row
#for row in c.execute('SELECT * FROM teamTestMatch where team=?',('England',)):
#for row in c.execute('SELECT * FROM teamTestMatch where team=? order by rating asc',('Pakistan',)):
    #print row
c.execute('insert into retiredPlayers values (12069)')
# for row in c.execute('SELECT * FROM retiredPlayers'):
#     print row

# for row in c.execute("select b.playerId, b.player, sum(b.innings), sum(b.notOut), sum(b.runs) as sumRuns, sum(b.balls), avg(b.rating), p.country from battingTestInnings b, testInfo t, playerInfo p where b.testId=t.testId and b.playerId=p.playerId and t.startDate>=20150101 and t.startDate<=20999999 and p.country in ('Australia','New Zealand','') group by b.playerId order by sumRuns desc"):
#      print(row)

# homeAwayFile = open("homeAwayTest.csv", "w")
# for row in c.execute('SELECT team1, team2, location, result from testInfo'):
#     homeAwayFile.write(str(row[0]) + "," + str(row[1]) + "," +str(row[2]) + "," +str(row[3]) + "," + "\n")
#     print(row)
# homeAwayFile.close()
# tossFile = open("tossTest.csv", "w")
# for row in c.execute('SELECT testId, team1, team2, result from testInfo'):
# #for row in c.execute('SELECT testId, toss from tossTest'):
#     #for rowT in c.execute('SELECT toss from tossTest where testId=?',(row[0],)):
#     #tossFile.write(",,," +str(row[1]) + "\n")
#     tossFile.write(str(row[1]) + "," +str(row[2]) + "," +str(row[3]) + "\n")
# tossFile.close()
conn.commit()
conn.close()
elapsed = (time.clock() - start)
print(elapsed)
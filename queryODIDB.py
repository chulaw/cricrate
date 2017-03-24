#!/usr/bin/env python
import time
start = time.clock()
import sqlite3
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()
# for row in c.execute('SELECT player, runs, wkts, rating FROM bowlingODIInnings where odiId>3598 order by rating desc limit 10'):
#      print(row)
# for row in c.execute('SELECT * from retiredPlayers'):
#      print(row)
# for row in c.execute('delete FROM battingODIInnings where odiId>3481'):
#        print row
# for row in c.execute('delete FROM bowlingODIInnings where odiId>3481'):
#        print row
for row in c.execute('delete FROM allRoundODIMatch where odiId>3777'):
     print row
for row in c.execute('delete FROM battingODILive where odiId>3777'):
     print row
for row in c.execute('delete FROM bowlingODILive where odiId>3777'):
     print row
for row in c.execute('delete FROM allRoundODILive where odiId>3777'):
    print row
#for row in c.execute('delete FROM odiInfo where odiId=3598'):
#     print row
# for row in c.execute('delete FROM fieldingEventODI where odiId>3644'):
#       print row
# for row in c.execute('delete FROM fieldingODIMatch where odiId>3644'):
#      print row
# for row in c.execute('delete FROM fieldingODILive where odiId>3644'):
#      print row
# for row in c.execute('delete FROM winSharesODIMatch where odiId>0'):
#        print row
# for row in c.execute('delete FROM winSharesODILive where odiId>0'):
#         print row
# for row in c.execute('select max(odiId) FROM overComparisonODI'):
#           print row
# for row in c.execute('select overs, wkts FROM overComparisonODI where odiId=1952 and innings=1'):
#           print row
#for row in c.execute('SELECT avg(runs) from detailsTestInnings where testId in (1133, 1236, 1313, 1388, 1469, 1571, 1771, 1847, 1947, 2021, 2067) and innings=1 and wickets=10'):
#     print(row)
#for row in c.execute('SELECT distinct ground from odiInfo'):

# homeAwayFile = open("homeAway.csv", "w")
# for row in c.execute('SELECT team1, team2, location, result from odiInfo'):
#     homeAwayFile.write(str(row[0]) + "," + str(row[1]) + "," +str(row[2]) + "," +str(row[3]) + "," + "\n")
#     print(row)
# homeAwayFile.close()
#for row in c.execute('SELECT odiId from odiInfo where ground=?',("Colombo (SSC)",)):
#for row in c.execute('SELECT runs from detailsODIInnings where innings=1 and balls=300 and odiId in (3092, 3096, 3099)'):
#     print(row)
# for row in c.execute('select avg(runs) from overComparisonODI where innings=1 and odiId>3309 and overs=45'):
#      print(row)

# c.execute('update odiInfo set result=? where odiId=3598', ("New Zealand",))
# for row in c.execute('select count(commentary) FROM fieldingEventODI where droppedCatch>0'):
#            print row
# for row in c.execute('select result, odiId from overComparisonODI where odiId<3000 and innings=1 and overs>=10 and overs<12 and runs<=80 and runs>70 and wkts>=1 and wkts<=3'):
#               print row

# for row in c.execute('select avg(result), teamBat, odiId from overComparisonODI where odiId<3000 and innings=1 and overs>=10 and overs<12 and runs<=80 and runs>70 and wkts>=1 and wkts<=3 group by odiId'):
#              print row

# for row in c.execute('select batsman, bowler, fielder, droppedCatch, commentary FROM fieldingEventODI where droppedCatch=1 and fielder=?',("Suresh Raina",)):
#                    print row
# for row in c.execute('select rankDiff, rank, rating, player, country, bestCurrentRating from fieldingODICurrent order by rating desc limit 100'):
#       print row
# for row in c.execute('select rating from fieldingODILive where player=?',("AB de Villiers",)):
#       print row
#for row in c.execute('select * FROM fieldingODIMatch where player=?',("Ravindra Jadeja",)):
#               print row
# for row in c.execute('select sum(catches), sum(droppedCatches), sum(stumpings), sum(missedStumpings) FROM fieldingODIMatch'):
#                 print row
# for row in c.execute('select commentary FROM commentaryEventODI where commentary like \"%misses a stumping%\"'):
#               print row
#for row in c.execute('SELECT * FROM playerInfo where name=?',('Brian Lara',)):
#    print row
#for row in c.execute('SELECT count(player) FROM fieldingODICareer where droppedCatches>0 and catches=0'):
#       print row
# for row in c.execute('SELECT player,odis,catches,droppedCatches,dropRate,greatCatches,directHits,misfields,runsSaved,missedStumpings,rating FROM fieldingODICareer where player=?',("Tillakaratne Dilshan",)):
#       print row
# for row in c.execute('SELECT player,odis,catches,dropRate,matPerMisfield,rating FROM fieldingODICareer where rating>0 and keeper=0 order by rating asc'):
#         print row
# for row in c.execute('SELECT player, odis, battingAdjWSAvg, battingRating FROM winSharesODICareer where abs(battingRating)>0.02 order by battingRating desc'):
#          print row
# print "\n"
# for row in c.execute('SELECT player, odis, bowlingAdjWSAvg, bowlingRating FROM winSharesODICareer where abs(bowlingRating)>0.02 order by bowlingRating desc'):
#          print row
# print "\n"
# for row in c.execute('SELECT player, odis, totalAdjWSAvg, totalRating FROM winSharesODICareer where abs(totalRating)>0.02 order by totalRating desc'):
#          print row
# for row in c.execute('SELECT player, odiId, battingAdjWS FROM winSharesODIMatch where player=?',("Harbhajan Singh",)):
#           print row
#for row in c.execute('SELECT player,odis,stumpings,missedStumpings,stumpRate,rating FROM fieldingODICareer where keeper=1 order by rating asc'):
#        print row
# for row in c.execute('SELECT * FROM fieldingODICareer where missedStumpings>0 order by missedStumpings asc'):
#             print row
# for row in c.execute('SELECT * FROM bowlerFieldingODICareer where droppedCatches>0 order by droppedCatches desc '):
#       print row
# for row in c.execute('SELECT * FROM batsmanFieldingODICareer where droppedCatches>0 order by droppedCatches desc '):
#        print row
#for row in c.execute("select b.playerId, b.player, b.balls, t.ballsPerOver, b.runs, b.wkts, b.rating, p.country, t.team1, t.team2, t.startDate, t.testId, t.scoreLink from bowlingODIInnings b, testInfo t, playerInfo p where b.testId=t.testId and b.playerId=p.playerId and b.rating > 1000 order by b.rating desc"):
#    print row
#for row in c.execute('SELECT * FROM bowlingODIInnings'):
#    print row
#for row in c.execute('SELECT * FROM battingODILive where player=?',('Brian Lara',)):
#    print row
#for row in c.execute('SELECT * FROM battingODIInnings where player=?',('Ken Barrington',)):
#    print row
# for row in c.execute('SELECT result FROM bowlingODIInnings where player=? and odiId=?',('Chaminda Vaas','921')):
#     print row
#for row in c.execute('SELECT * FROM bowlingODILive where testId=?',(1572,)):
#    print row
#for row in c.execute("select b.playerId, b.player, p.country, b.rating from bowlingODILive b, playerInfo p inner join(select playerId, max(inningsId) maxInningsId from bowlingODILive group by playerId) bb on b.playerId = bb.playerId and b.inningsId = bb.maxInningsId and b.startDate>'20140101' and p.playerId=b.playerId order by b.rating desc"):
    #print row
#for row in c.execute('SELECT * FROM bowlingODILive where player=?',('Muttiah Muralitharan',)):
#    print row
#for row in c.execute('SELECT * FROM battingODICareer order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM bowlingODICareer order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM allRoundODICareer order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM battingODICurrent order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM bowlingODICurrent order by rating asc'):
#    print row
#for row in c.execute('SELECT * FROM allRoundODICurrent order by rating asc'):
#    print row
#c.execute('update odiInfo set team2=?,result=? where odiId=3541', ("Papua New Guinea", "Papua New Guinea"))
#c.execute('update odiInfo set team2=?,result=? where odiId=3542', ("Papua New Guinea", "Papua New Guinea"))
#for row in c.execute('select * from odiInfo where odiId=3541'):
#    print row
#c.execute('''create table odiInfo (odiId integer unique, startDate text, location text, team1 text, team2 text, season text, ground text, ballsPerOver integer, result text, margin text, series text,
#          seriesStatus text, scoreLink text)''')
#for row in c.execute('SELECT max(odiId) FROM odiInfo'):
#    print row
# c.execute('insert into retiredPlayers values (12069)')
conn.commit()
conn.close()
elapsed = (time.clock() - start)
print(elapsed)

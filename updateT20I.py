#!/usr/bin/env python
import sys
import os

t20iId = int(sys.argv[1])
print "Dumping t20iinfo"
os.system("python dumpT20IInfo.py")
print "Scraping t20i scorecards"
os.system("python scrapeT20IScorecard.py " + `t20iId`)
print "Dumping t20i innings"
os.system("python dumpT20IInnings.py " + `t20iId`)
print "Scraping dumping t20i career"
os.system("python dumpT20ICareer.py")
print "Scraping dumping current"
os.system("python dumpCurrent.py")

#!/usr/bin/env python
import sys
import os

testId = int(sys.argv[1])
# print "Dumping test info"
# os.system("python dumpTestInfo.py")
# print "Scraping test scorecards"
# os.system("python scrapeScorecard.py " + `testId`)
print "Dumping test innings"
os.system("python dumpInnings.py " + `testId`)
print "Scraping test fielding"
os.system("python scrapeTestFielding.py " + `testId`)
print "Scraping dumping test fielding career"
os.system("python dumpTestFieldingCareer.py")
print "Scraping dumping test career"
os.system("python dumpCareer.py")
print "Scraping dumping current"
os.system("python dumpCurrent.py")

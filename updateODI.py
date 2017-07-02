#!/usr/bin/env python
import sys
import os

odiId = int(sys.argv[1])
print "Dumping odiinfo"
os.system("python dumpODIInfo.py")
print "Scraping odi scorecards"
os.system("python scrapeODIScorecard.py " + `odiId`)
print "Dumping odi innings"
os.system("python dumpODIInnings.py " + `odiId`)
print "Scraping odi fielding"
os.system("python scrapeODIFielding.py " + `odiId`)
print "Scraping dumping odi fielding career"
os.system("python dumpODIFieldingCareer.py")
print "Scraping odi win shares"
os.system("python scrapeODIWinShares.py " + `odiId`)
print "Scraping dumping odi win shares career"
os.system("python dumpODIWinSharesCareer.py")
print "Scraping dumping odi career"
os.system("python dumpODICareer.py")
print "Scraping dumping current"
os.system("python dumpCurrent.py")

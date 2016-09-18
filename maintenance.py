#!/usr/bin/env python
import time
start = time.clock()
import sqlite3
conn = sqlite3.connect('ccrODI.db')
c = conn.cursor()
c.execute("update bowlingODICurrent set country=? where player=?", ("South Africa", "Dale Steyn"))
c.execute("update bowlingODICurrent set country=? where player=?", ("South Africa", "Morne Morkel"))
c.execute("update bowlingODICurrentAllTime set country=? where player=?", ("South Africa", "Dale Steyn"))
c.execute("update bowlingODICurrentAllTime set country=? where player=?", ("South Africa", "Morne Morkel"))
c.execute("update playerInfo set country=? where player=?", ("South Africa", "Dale Steyn"))
c.execute("update playerInfo set country=? where player=?", ("South Africa", "Morne Morkel"))
c.execute("update playerInfo set country=? where player=?", ("New Zealand", "Luke Ronchi"))
c.execute("update playerInfo set country=? where player=?", ("England", "Eoin Morgan"))
conn.commit()
conn.close()
elapsed = (time.clock() - start)
print(elapsed)
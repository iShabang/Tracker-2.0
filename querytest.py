import sqlite3
import dbfunctions

conn = sqlite3.connect('tracker.db')
c = conn.cursor()
print(dbfunctions.GetTransByName(c, dbfunctions.NameSearchString("ch")))
print(dbfunctions.GetTransByNameDate(c, "che","2018-11-00", "2018-11-31"))
print(dbfunctions.GetTransByCategory(c, 2))
print(dbfunctions.GetTransByCategoryDate(c,2,"2018-11-00", "2018-11-31"))
print(dbfunctions.GetTransByDateInterval(c, "2018-11-00", "2018-11-31"))

conn.close()

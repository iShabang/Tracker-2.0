import sqlite3
import dbfunctions

values = [("chipotle", "2018-11-06", 8, 1),
          ("mcdonolds", "2018-11-04", 5.01, 1),
          ("canes", "2018-10-05", 10.25, 1),
          ("innout", "2018-09-03", 14.30, 1),
          ("chewy", "2018-08-02", 6.45, 1),
          ("phone case", "2018-11-09", 45.43, 2),
          ("headphones", "2018-11-08", 56.99, 2),
          ("Check","2018-12-27", 500.00, 3)]

dbfunctions.AddCategory(name="Food", income=0)
dbfunctions.AddCategory(name="Things", income=0)
dbfunctions.AddCategory(name="Income", income=1)
dbfunctions.AddManyTrans(values=values)
print(dbfunctions.GetTransByDateInterval(lowdate="2018-00-00",highdate="2019-00-00"))

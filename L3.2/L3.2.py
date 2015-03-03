__author__ = 'daniel'
import sqlite3 as lite

cities = (('Las Vegas', 'NV'),('Atlanta', 'GA'))

weather = (('Las Vegas', 2013, 'July', 'December', 55), ('Atlanta', 2013, 'July', 'January'))

con = lite.connect('getting_started.db')

# Inserting rows by passing tuples to `execute()`

with con:
    cur = con.cursor()
    cur.executemany("INSERT INTO cities VALUES (?,?)", cities
    cur.executemany("INSERT INTO weather VALUES (?,?,?,?,?)", weather
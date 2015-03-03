__author__ = 'daniel'

import sqlite3 as lite
import pandas as pd

con = lite.connect('getting_started.db')

# Select all rows and print the result set one row at a time

with con:

    cur = con.cursor()
    cur.execute("select name, state, year, warm_month, cold_month")
    cur.execute("from cities")
    cur.execute("inner join weather")
    cur.execute("on city = name")

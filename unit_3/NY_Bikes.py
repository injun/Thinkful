import requests
from pandas.io.json import json_normalize
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections

# accesses data online and stores it in df
r = requests.get('http://www.citibikenyc.com/stations/json')
df = json_normalize(r.json()['stationBeanList'])

# create city_bike SQL with a table 'citybike_reference' that will store downloaded data
con = lite.connect('city_bike.db')
cur = con.cursor()

with con:
    cur.execute('DROP TABLE IF EXISTS citybike_reference')
    cur.execute('CREATE TABLE citybike_reference (id INT PRIMARY KEY, '
                'totalDocks INT, '
                'city TEXT, '
                'altitude INT, '
                'stAddress2 TEXT, '
                'longitude NUMERIC, '
                'postalCode TEXT, '
                'testStation TEXT, '
                'stAddress1 TEXT, '
                'stationName TEXT, '
                'landMark TEXT, '
                'latitude NUMERIC, '
                'location TEXT )')

# populate table with values:
# a prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citybike_reference (id, " \
      "totalDocks, " \
      "city, " \
      "altitude, " \
      "stAddress2, " \
      "longitude, " \
      "postalCode, " \
      "testStation, " \
      "stAddress1, " \
      "stationName, " \
      "landMark, " \
      "latitude, " \
      "location) " \
      "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

# for loop to populate values in the database
with con:
    for station in r.json()['stationBeanList']:
        # id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql, (
            station['id'],
            station['totalDocks'],
            station['city'],
            station['altitude'],
            station['stAddress2'],
            station['longitude'],
            station['postalCode'],
            station['testStation'],
            station['stAddress1'],
            station['stationName'],
            station['landMark'],
            station['latitude'],
            station['location']))

# extract the all 'id' columns from the dataframe and put them into a list
station_ids = df['id'].tolist()

# add the '_' to the station name (column names cannot start with a numer)
# and also the data type for the SQL
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

# create the table for the available bikes and the time stamp
with con:
    cur.execute('DROP TABLE IF EXISTS available_bikes')
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");")

# populate with values for available bikes
# take the string used as time stamp and parse it into a Python datetime object
exec_time = parse(r.json()['executionTime'])

# create an entry for the execution time by inserting it into the database
with con:
    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%S'),))

id_bikes = collections.defaultdict(int)  # defaultdict to store available bikes by station

# loop through the stations in the station list
for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']

# iterate through the defaultdict to update the values in the database
with con:
    for k, v in id_bikes.iteritems():
        cur.execute(
            "UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime(
                '%S') + ";")
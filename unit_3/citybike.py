import requests
from pandas.io.json import json_normalize
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections
import pandas as pd
import matplotlib.pyplot as plt
import datetime

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

# for loop to request data from online json 60 times, every 60 seconds (during 1 hour every minute)
for i in range(60):
    # accesses data online and stores it in df
    r = requests.get('http://www.citibikenyc.com/stations/json')
    df = json_normalize(r.json()['stationBeanList'])

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

    time.sleep(60)

# Analysing data

# Accessing the database
con = lite.connect('citi_bike.db')
cur = con.cursor()

# transfering data into a pandas dataframe
df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')
print df

# capture the difference between two values in sequence.
# The key is having the values sorted in time in order to make the difference from one minute to the next meaningful.
#
# First process each column and calculate the change each minute:
hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k, v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer

# The enumerate() function returns not only the item in the list but also the index of the item.
# This allows us to find the value (with index of k) just after it in sequence (k + 1).
# We run the loop until k is equal to the index for the second to last element in the list.


# The enumerate() function returns not only the item in the list but also the index of the item.
# This allows us to find the value (with index of k) just after it in sequence (k + 1).
# We run the loop until k is equal to the index for the second to last element in the list.

# At this point, the values are in the dictionary keyed on the station ID. To find the winner:
def keywithmaxval(d):
    # create a list of the dict's keys and values;
    v = list(d.values())
    k = list(d.keys())

    # return the key with the max value
    return k[v.index(max(v))]

# assign the max key to max_station
max_station = keywithmaxval(hour_change)

# From there, you query the reference table for the important information about the most active station:
#query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(hour_change[379]) + " bicycles coming and going in the hour between " \
      + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " \
      + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

# Note that this will just print out the first station in the list that has the max value.
#  to visually inspect the data to make sure this is the case:
plt.bar(hour_change.keys(), hour_change.values())
plt.show()

# coding: utf-8

# In[2]:

import requests
# from pandas.io.json import json_normalize
import sqlite3 as lite
import pandas as pd
import datetime
import collections


# Initialize variables

# In[16]:

# dictionary of the select cities and coordinates
cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }

API_key = '588757ec5c50538fcce65477d8502b22'

url = 'https://api.forecast.io/forecast/' + API_key + '/'

end_date = datetime.datetime.now()
query_date = end_date - datetime.timedelta(days = 30)


# In[17]:

# create sql database weather.db

con = lite.connect('weather.db')
cur = con.cursor()

with con:
    cur.execute('DROP TABLE IF EXISTS daily_temp')
    cur.execute('CREATE TABLE daily_temp (day_of_reading INT, '
                'Atlanta REAL, '
                'Austin, '
                'Boston, '
                'Chicago, '
                'Cleveland)')


# In SQL, a row has to be inserted before it can be updated. In order to keep the code clean, we're going to iterate through the values in the range and insert them into the database without any other values

# In[21]:

with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%D')),))
        query_date += datetime.timedelta(days=1)


# loop through cities list and query the API

# In[ ]:

for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%d'))

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day



# In[ ]:




import sqlite3 as lite
import pandas as pd

# create tuples of tuples to later insert into weather table

weather = (('New York City', 2013, 'July', 'January', 62),
('Boston', 2013, 'July', 'January', 59),
('Chicago', 2013, 'July', 'January', 59),
('Miami', 2013, 'August', 'January', 84),
('Dallas', 2013, 'July', 'January', 77),
('Seattle', 2013, 'July', 'December', 61),
('Portland', 2013, 'July', 'December', 63),
('San Francisco', 2013, 'September', 'December', 64),
('Los Angeles', 2013, 'September', 'December', 75))


con = lite.connect('getting_started.db')


cur = con.cursor()

# delete tables with same names as used for the program
cur.execute("DROP TABLE IF EXISTS weather")
cur.execute("DROP TABLE IF EXISTS cities")

# Create the tables
cur.execute("CREATE TABLE cities (name text, state text)")
cur.execute("CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)")

# Insert data into table "cities", line-by-line
cur.execute("INSERT INTO cities values('New York City', 'NY')")
cur.execute("INSERT INTO cities values('Boston', 'MA')")
cur.execute("INSERT INTO cities values ('Chicago', 'IL')")
cur.execute("INSERT INTO cities values ('Miami', 'FL')")
cur.execute("INSERT INTO cities values ('Dallas', 'TX')")
cur.execute("INSERT INTO cities values ('Seattle', 'WA')")
cur.execute("INSERT INTO cities values ('Portland', 'OR')")
cur.execute("INSERT INTO cities values ('San Francisco', 'CA')")
cur.execute("INSERT INTO cities values ('Los Angeles', 'CA')")

# Insert data into table "weather", using execute all command
cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)

con.commit()

# Join data from both tables and store in "result"
result = cur.execute("SELECT name, state, year, warm_month, cold_month, average_high from cities INNER JOIN weather ON name = city")

# load joined data into panda dataframe
rows = cur.fetchall()
cols = [desc[0] for desc in cur.description]
df = pd.DataFrame(rows, columns=cols)

# select cities where July was the warmest month and print the name of the city and state
index = 0
list_of_cities = []
for month in df['warm_month']:
    if month == 'July':
        list_of_cities.append(df.iloc[index, 0])
        list_of_cities.append(df.iloc[index, 1])
    index += 1
print 'The list of cities is ', ", ".join(list_of_cities)






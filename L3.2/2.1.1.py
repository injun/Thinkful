__author__ = 'daniel'
import pandas as pd

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

# split the string on the (hidden characters that indicate) newlines
data = data.splitlines()

# split each item in this list on the commas
data = [i.split(', ') for i in data]

column_names = data[0] # this is the first row
data_rows = data[1::] # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

# convert Alcohol and Tobacco columns to float.
from scipy.stats import stats

print df['Alcohol'].mean()
# 5.4436363636363634
print df['Alcohol'].median()
# 5.63

# If all numbers occur equally often, stats.mode() will return the smallest number
print stats.mode(df['Alcohol'])
# 4.02

print df['Tobacco'].mean()
# 3.6181818181818186
print df['Tobacco'].median()
# 3.53
print stats.mode(df['Tobacco'])
# 2.71

max(df['Alcohol']) - min(df['Alcohol'])
# range between max and min values in column
print df['Alcohol'].std()
# standard deviation
print df['Alcohol'].var()
# variance

print max(df['Tobacco']) - min(df['Tobacco'])
# 1.8499999999999996
print df['Tobacco'].std()
# 0.59070835751355388
print df['Tobacco'].var()
# 0.3489363636363606
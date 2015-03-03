import pandas as pd
from scipy import stats

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


data = data.splitlines() #or data.split('\n'): splits the string on the (hidden characters that indicate) newlines

data = [i.split(', ') for i in data]    #List comprehension to take each string and split that into a list so that we end up with a list of lists

#insert into pandas dataframe
column_names = data[0] # this is the first row
data_rows = data[1::] # these are all the following rows of data
df = pd.DataFrame(data_rows, columns=column_names)

# convert Alcohol and Tobacco columns to float
df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

# prints the Average, Median and mode for alcohol columns
print 'The average values for the Alcohol and Tobacco datasets are ',df['Alcohol'].mean(), 'and ', df['Tobacco'].mean(), ', respectively.'
print 'The median values for the Alcohol and Tobacco datasets are ',df['Alcohol'].median(), 'and ', df['Tobacco'].median(), ', respectively.'
print 'The mode for the Alcohol and Tobacco datasets are ',stats.mode(df['Alcohol']), 'and ', stats.mode(df['Tobacco']), ', respectively.'
print 'The range of values for the Alcohol and Tobacco datasets are ', max(df['Alcohol']) - min(df['Alcohol']), 'and ', max(df['Tobacco']) - min(df['Tobacco']), ', respectively.'
print 'The standard deviation for the Alcohol and Tobacco datasets are ',df['Alcohol'].std(), 'and ', df['Tobacco'].std(), ', respectively.'
print 'The variance for the Alcohol and Tobacco datasets are ',df['Alcohol'].var(), 'and ', df['Tobacco'].var(), ', respectively.'

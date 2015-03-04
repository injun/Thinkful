import matplotlib.pyplot as plt
from scipy import stats
import collections
import pandas as pd

# load the reduced version of the Lending Club Data
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# Clean null rows
loansData.dropna(inplace='True')

# Determine frequency (counts of observations for each number if credit lines) AND plot it
freq = collections.Counter(loansData['Open.CREDIT.Lines'])
# plt.figure()
# plt.bar(freq.keys(), freq.values(), width = 1)
# plt.show()

# Perform chi-squared test
result = stats.chisquare(freq.values())
print "chi_squared = ", result[0]
print "p > ", result[1]

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData.dropna(inplace=True)

# generates a box plot

loansData.boxplot(column='Amount.Requested')
plt.savefig(boxplot_222.png)

# generates a histogram

loansData.hist(column='Amount.Requested')
plt.savefig(hist222.png)

# tests the data for normal distribution using a QQ plot

plt.figure()
graph1 = stats.probplot(loansData['Amount.Requested'], dist='norm', plot=plt)
plt.savefig(QQ222.png)
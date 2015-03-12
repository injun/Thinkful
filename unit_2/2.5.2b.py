import pandas as pd
import statsmodels.api as sm
import numpy as np

loansData = pd.read_csv("C:\Thinkful\Unit_2\LoanStats3a.csv")
loansData.to_csv('loansData_clean.csv', header=True, index=False)

loansData['int_rate'] = loansData['int_rate'].map(lambda x: x.rstrip('%'))
loansData['int_rate'] = loansData['int_rate'].map(lambda x: [int(n) for n in x])
loansData['int_rate'] = loansData['int_rate'].astype(float)


'''convert the data in FICO.Range into string and split the string and take the lowest value'''
loansData['FICO.Score'] = loansData['FICO.Range']
temp_list = loansData['FICO.Score'].tolist()
FICO = [] #declare an empty array
for i in range(len(temp_list)):
  temp_list_1 = temp_list[i].split("-")
  temp_list_2 = float(temp_list_1[0])        #
  FICO.append(temp_list_2)
loansData['FICO.Score'] = FICO


# model interest rates with monthly income /exercise says annual income?
# model is (interest rates, y) = b + a1 * (monthly income, x1) + a2 * (home ownership, x2)

# strip data from dataframe
intrate = loansData['int_rate']
intrate[np.isnan(intrate)] = 0 # looks for NaN and replaces by '0'
annual_inc = loansData['annual_inc']
annual_inc_inc[np.isnan(annual_inc)] = 0
home_own = loansData['Home.Ownership']
home_own = [4 if x == 'OWN' else 3 if x == 'MORTGAGE' else 2 if x == 'RENT' else 1 if x == 'OTHER' else 0 for x in home_own]

# reshape data
y = np.matrix(intrate)
y = y.transpose()


x1 = np.matrix(annual_inc).transpose()
x2 = np.matrix(home_own).transpose()
x = np.column_stack([x1, x2]) # combines both variables to use in the model

# model

X = sm.add_constant(x)
model = sm.OLS(y, X)
f = model.fit()

# print results
print 'Coefficients: ', f.params
print 'Intercept: ', f.params
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

x = loansData['Interest.Rate'][0:5].values[1] # creates dict x from data in first 5 rows of column 'Interest.Rate' in loansData, and .values[1] gets the first value from that dict

# x = x.rstrip('%') # Removes the % from the end of the data
# x = float(x) # Convert x to a number
# x = x / 100
# x = round(x, 4)

# y = lambda x: round(float(x.rstrip('%'))/100, 4) # nameless function that combines all steps commented out above

# map is a built in function that will go through the data and replace it by the result of the applied command
# cleanInterestRate is the cleaned out version of the original
# Interest.Rate, stripped out of the '%' symbol and with data type as float

cleanInterestRate = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) / 100, 4))
loansData['Interest.Rate'] = cleanInterestRate # replaces values in the original column

# repeat to clean 'months' from the 'Loan.Length' column
cleanLoanLength = loansData['Loan.Length'].map(lambda x: x.strip('months'))
loansData['Loan.Length'] = cleanLoanLength

# convert the data in FICO.Range into string and split the string and take the lowest value
loansData['FICO.Score'] = loansData['FICO.Range']

A =loansData['FICO.Score'].tolist()
#print (A)
FICO=[] #declare an empty array
for j in range(len(A)):   #for j in between 0 to len(A)
  B = A[j].split("-")     #split each sub-array on - and save it to B
  #C = int(B[0], B[1])    #convert the str to int
  #C = np.mean(C)         #finding the mean of B[0] and B[1]
  C = float(B[0])           #convert the string to int, using only the first value
  FICO.append(C)          #append each C to the empty array, using first value
loansData['FICO.Score']=FICO

# generate a histogram

loansData.hist(column='FICO.Score')
plt.show()

# Generate a scatter plot that plots each variable with every other variable in the table;
# to establish potential links between variables
# and determine which can be used as independent variables in a model
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()

# define a linear model with two independent variables: FICO Score and Loan Amount.
# This will help us determine the dependent variable, Interest Rate.
# InterestRate = b + a1(FICOScore) + a2(LoanAmount)
# use statsmodels to find the model coefficients b (which is the y-intercept), a1, and a2

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

# transpose column elements for dependent variable
y = np.matrix(intrate).transpose()

# transpose column elements for independent variables
x1 = np.matrix(loanamt).transpose()
x2 = np.matrix(fico).transpose()

# merge columns into a matrix, with a column for each independent variable
x = np.column_stack([x1, x2])

# linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

# print results
print 'Coefficients: ', f.params[0:2]
print 'Intercept: ', f.params[2]
print 'P-Values: ', f.pvalues
print 'R-Squared: ', f.rsquared

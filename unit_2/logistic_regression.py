import pandas as pd
import statsmodels.api as sm

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: x.rstrip('%'))
loansData['Interest.Rate'] = loansData['Interest.Rate'].astype(float)
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: x.rstrip('months'))

loansData['FICO.Score'] = loansData['FICO.Range']
A = loansData['FICO.Score'].tolist()
#print (A)
FICO=[] #declare an empty array
for j in range(len(A)):   #for j in between 0 to len(A)
  B = A[j].split("-")     #split each sub-array on - and save it to B
  #C = int(B[0], B[1])    #convert the str to int
  #C = np.mean(C)         #finding the mean of B[0] and B[1]
  C = float(B[0])           #convert the string to int, using only the first value
  FICO.append(C)          #append each C to the empty array, using first value
loansData['FICO.Score']=FICO

loansData.to_csv('loansData_clean.csv', header=True, index=False)

intercept = [1] * len(loansData)
loansData['Intercept'] = intercept
# independant variables
ind_vars = ['Intercept', 'Amount.Requested', 'FICO.Score']
ir = loansData['Interest.Rate']
ir = [1 if x < 12 else 0 for x in ir]
loansData['IR_TF'] = ir
X = loansData[ind_vars]
y = loansData['IR_TF']

logit = sm.Logit(y, X)
result = logit.fit()
coeff = result.params
print coeff
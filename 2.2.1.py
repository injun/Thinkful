# import collections
#
# testlist = [1, 4, 5, 6, 9, 9, 9]
#
# c = collections.Counter(testlist)
#
# print c
#
# # calculate the number of instances in the list
# count_sum = sum(c.values())
#
# for k,v in c.iteritems(): # calling both the key,k, and the value, v as indexes
#   print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum)
#
# import matplotlib.pyplot as plt
# x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
# plt.hist(x, histtype='bar')
# plt.show()

import collections
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# generates data to plot in data1

plt.figure()
data1 = np.random.normal(size=1000)

# calculate the number of instances in the list 'test_data'

freq_1 = collections.Counter(data1)
count_sum_1 = sum(freq_1.values())
for k,v in freq_1.iteritems(): # calling both the key,k, and the value, v as indexes
  print "The frequency of number " + str(k) + " is " + str(float(v) / count_sum_1)

# generate and save boxplot on data 1

plt.boxplot(data1)
plt.savefig("boxplot_1.png")

# generate and save histogram on data 1

plt.hist(data1, histtype='bar')
plt.savefig("histogram_1.png")

# plot QQ from data1

graph1 = stats.probplot(data1, dist="norm", plot=plt)
plt.savefig("QQ-plot_1.png")


# Generates data to plot in data2
plt.figure()
data2 = np.random.uniform(size=1000)

# calculate the number of instances in the list 'data2'

freq_2 = collections.Counter(data2)
count_sum_2 = sum(freq_2.values())
for k,v in freq_2.iteritems():
    print 'The frequency of number' + str(k) + ' is ' + str(float(v) / count_sum_2)

# Boxplot on data2
plt.boxplot(data2)
plt.savefig("boxplot_2.png")

# histogram on data 2
plt.hist(data2, histtype='bar')
plt.savefig("histogram_2.png")

# QQ plot on data 2
graph2 = stats.probplot(data2, dist="norm", plot=plt)
plt.save("QQ-plot_2.png")
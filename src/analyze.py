"""
Contains analyze data scripts
author: chris
"""

#Useful Libraries
import numpy as np

#Data Library
import data as dc

#Debug Timer Wrappers
from wrappers import debug

@debug
def FeatureCostRange(d,var, mode, bins = 10):
	"""
	Returns a dictionary {features: dictionary2}
	where dicionary2 is {feature ranges: (cost-ranges, count)}

	These results will show which feature ranges result in the greater number of higher cost ranges

	author: chris
	"""
	cost = []
	#try:
	#Grab the ranges for the feature
	data = d.getColumn(var).astype("float")

	if mode:
		bins = max(data) - min(data) + 1
	ranges = np.linspace(min(data), max(data) + 1, bins) #Unssuport crap
	cost.append(["classification"] if len(set(data)) < 10 else ["continuous"])

	#Loop through the ranges to get the costs
	for i,(low, high) in enumerate(zip(ranges[:-1], ranges[1:])):
		#Grab the costs at those ranges
		costs = d.cost[np.where((low <= data) * (data < high))]
		cost.append((low, high, costs))
	#except:
	#If the data contains non-numeral data, catch the exception
	#print "data is not numeral"
	return cost

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D)
	d.createRefs()
	d.loadData("../data/h144d.dat")

	#Save feature dictionary in dataholder
	d.results["featureCostRange"] = featureCostRange(d)

	#Save the current State of the dataholder (including data)
	d.save("temp.p")

	#Load previously saved state of the dataholder (including data)
	#d.load("temp.p")

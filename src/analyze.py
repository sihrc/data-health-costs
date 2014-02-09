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
def featureCostRange(d):
	"""
	Returns a dictionary {features: dictionary2}
	where dicionary2 is {feature ranges: (cost-ranges, count)}

	These results will show which feature ranges result in the greater number of higher cost ranges

	author: chris
	"""
	#Initiate first Dictionary
	feature_dicts = dict()
	#Loop through the different features
	for i in range(len(d.features)):
		try:
			#Grab the relevant data
			var = "V"+str(i)
			data = d.getColumn(var)

			#Grab the ranges for the feature
			ranges = np.linspace(min(data), max(data), 10)

			#Loop through the ranges to get the costs
			for i,(low, high) in enumerate(zip(ranges[:-1], ranges[1:])):
				#Grab the costs at those ranges
				costs = d.cost[np.where((low < data) * (data < high))]
				feature_dicts[var] = feature_dicts.get(var, []) + [(low, high, costs)]
		except:
			#If the data contains non-numeral data, catch the exception
			print var + " is not numeral"
	return feature_dicts

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

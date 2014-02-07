"""
Contains analyze data scripts
"""

#Useful Libraries
import numpy as np

#Data Library
import data as dc

def featureCostRange(d):
	"""
	Returns a dictionary {features: dictionary2}
	where dicionary2 is {feature ranges: (cost-ranges, count)}

	These results will show which feature ranges result in the greater number of higher cost ranges
	"""
	#Initiate first Dictionary
	feature_dicts = dict()
	#Loop through the different features
	for i in range(len(d.features)):
		try:
			#Create dictionary for this feature
			current_dict = dict()
			
			#Grab the relevant data
			var = "V"+str(i)
			data = d.getColumn(var)

			#Grab the ranges for the feature
			ranges = np.linspace(min(data), max(data), 10)

			#Loop through the ranges to get the costs
			for i,(low, high) in enumerate(zip(ranges[:-1], ranges[1:])):
				#Grab the costs at those ranges
				costs = cost[np.where((low < data) * (data < high))]
				if len(costs) == 0:
					continue
				#Get the cost ranges
				cost_range = np.linspace(min(costs), max(costs),10)
				#Count the costs that lie in each cost range and add it to the dictionary
				for cost_low, cost_high in zip(cost_range[:-1], cost_range[1:]):
					current_dict[(low,high)] = (cost_low, cost_high, len(np.where((cost_low < costs) * (costs < cost_high))[0]))
			#Assign this feature dict into the big dictionary
			feature_dicts[var] = current_dict
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

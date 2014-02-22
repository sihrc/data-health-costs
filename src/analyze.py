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
def FeatureCostRange(d,tag, bins = 0):
	"""
	Takes in the data object, the feature tag, and number of features (automatically fitted if 0)
	Returns a list of (low feature, high feature, cost list)

	author: chris
	"""
	cost = []
	bin_max = 20

	#Grab the ranges for the feature
	try:
		#Feature data is numeral
		data = d.getColumn(tag).astype("float")
	except:
		#Feature data is categorical (we want to decode this into numbers) TODO!
		data = d.getColumn(tag)
		if len(data[0][0]) == 1:
			row,col = data.shape
			new = np.zeros(shape=(row,col))

			for i in xrange(row):
				for j in xrange(col):
					new[i,j] = ord(data[i,j])
			return new
		d.ignored.append(d.getColumn(tag=tag))
		return cost

	#Automation for bin fitting
	if bins == 0:
		bins = int(max(data) - min(data) + 1)
		bins = bin_max if bins > bin_max else bins

	#Loop through the ranges to get the costs
	ranges = list(np.linspace(min(data), max(data), bins))
	ranges.append(ranges[-1]+.01)
	for i in xrange(len(ranges)-1):
		low,high = ranges[i], ranges[i+1]
		costs = d.cost[np.where((low <= data) * (data < high))]
		cost.append((low, high, costs))
	return cost


def reject_outliers(data, m=5):
	"""
	Returns a numpy array with outliers that are further than 
	m * the std of the data away from the mean
	"""
	return data[abs(data - np.mean(data)) < m * np.std(data)]


def createBins(data, bins = 10):
	"""
	CreateBins (data = np.array, bins = int)
	Returns a binned version of the data
	"""
	#Create ranges for data
	ranges = np.linspace(np.min(data), np.max(data), bins)
	#Ranges between ranges
	for low,high in zip(ranges[:1], ranges[1:]):
		data[np.where((data > low) * (data < high))] = (low + high)/2.0
	return data

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

"""
Contains analyze data scripts
author: chris
"""

#Useful Libraries
import numpy as np
import os

#Local Library
import config
from host import client
import data as dc
import visuals as vis

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

@debug
def getData(datafile):
	dataconfig = config.configuration[datafile]
	return dc.Data(codebook = dataconfig[0], datapath = os.path.join("..", "data" , datafile), costId = dataconfig[1])

@debug
def CDF_COST_FOR_FEATURE(datafile):
		dataconfig = config.configuration[datafile]
		d = dc.Data(codebook = dataconfig[0], datapath = os.path.join("..", "data" , datafile), costId = dataconfig[1])
		for row in d.features:
			costRangeData = FeatureCostRange(d, row)
			d = vis.GetCostForBinnedFeature(d,costRangeData, row) #gets cost for feature V24
		# with open(datafile[:-4] + "_ignored.txt", 'wb') as f:
		# 	for line in d.ignored:
		# 		f.write(str(line))
		# 		f.write("\n")
		# d.save(d.datapath[:-4] + ".p")
if __name__ == "__main__":
	CDF_COST_FOR_FEATURE(config.datafiles[-1])
	for datafile in config.datafiles:
		CDF_COST_FOR_FEATURE(datafile)

	# d = getData(config.H144E)
	

"""
Formats the data for training the model

author: chris
"""
#System level modules
import numpy as np

#Local Modules
import data as dc
import config
import data
import lookup

#Wrapper for debug function (timing and debug print statements)
from wrappers import debug

@debug
def filterNegatives(X,Y):
	"""
	Filter out the negative (not provided) feature values

	author: chris
	"""
	positive = np.where(np.prod(X > 0, axis = 1))
	return X[positive], Y[positive]

@debug
def formatData(datafile, features):
	"""
	Get data into numpy array for model to load

	author: chris
	"""
	tags = config.datafiles[datafile]
	d = dc.getData(datafile)
	dataX = np.zeros(shape=(len(d.cost), len(features)))
	for i,feature in enumerate(features):
		dataX[:,i] = d.getColumn(tag = feature).astype("float")
	return dataX, d.cost

@debug
def crossReference(datafile, features):
	"""
	Make sure there are no duplicate features and all features exist in datafile

	author: chris
	"""
	all_features = config.data[datafile][0].keys()
	for feature in features:
		if not (feature in all_features):
			print datafile, feature
	if len(set(features)) != len(features):
		for i,feature in enumerate(features):
			if feature in features[i + 1:] + features[:i]:
				print feature, " is duplicated"
		print datafile, "features has duplicates"

@debug
def lookUpFeatures(datafile, features):
	"""
	HTML Scrapes for the feature and pretty prints it.

	author: chris
	"""
	for feature in feature_dict[datafile]:
	 	lookup.print_variable(lookup.getDetails(datafile, feature))
	 	raw_input() # pause for user to catch up


if __name__ == "__main__":
	for datafile, features in feature_dict.iteritems():
		# crossReference(datafile, features)
		X,Y = formatData(datafile, features)
		np.save(config.path("..","data",datafile, datafile + "_" + "dataX.npy"),X)
		np.save(config.path("..","data",datafile, datafile + "_" + "dataY.npy"), Y)

			

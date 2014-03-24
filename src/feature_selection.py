#Python Modules
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.cross_validation import train_test_split
from sklearn.metrics import explained_variance_score
import pandas as pd
from operator import itemgetter

#Local Modules
from wrappers import debug 
import gc
import data as dc
import config
import random

@debug
def predict(model, trainFeatures, targetFeature):
	predicts = model.predict(trainFeatures)
	return explained_variance_score(targetFeature, targetFeature)

@debug
def train(model, data, test_train_split = .1):
	targetIndex = random.randint(0, len(data.costs))
	num_training = float(test_train_split * data.lines)
	splits = [0] * len(data.paths)
	splits[-1] = num_training/data.tail if num_training < data.tail else 1
	counter = 1
	while num_training > 0:
		counter += 1
		splits[-counter] = num_training/data.limit if num_training < data.limit else 1
		num_training -= data.limit

	import numpy as np
	x_tests, y_tests = None, None
	for i,(path,split) in enumerate(zip(data.paths, splits)):
		print "Training ... %d of %d chunks" % (i+1,len(data.paths))
		print i,path,split
		model, columns, x_test, y_test = chunk_train(model, path, data.costs, targetIndex, split = split)
		x_tests = np.vstack((x_tests, x_test)) if type(x_tests) != np.ndarray else x_test
		y_tests = np.vstack((y_tests, y_test)) if type(y_tests) != np.ndarray else y_test
		gc.collect()

	return model, columns, x_tests, y_tests

@debug
def chunk_train(model, path, costs, targetIndex, split = 0):
	# Reading Data into a Panda Table - Do this in chunks - d.panda -> List of csv files
	raw_panda = pd.read_csv(path, low_memory=False, delimiter = ",")
	panda = raw_panda._get_numeric_data()

	print "Non-numerical Columns\n", set(raw_panda.columns.values) - set(panda.columns.values)

	#Get feature and target data
	dataFeatures = panda[[feature for feature in panda.columns.values if feature not in costs]].as_matrix().astype("float")
	targetFeatures = panda[costs].as_matrix().astype("float")

	#Split the data
	x_train, x_test, y_train, y_test = train_test_split(dataFeatures, targetFeatures[:,targetIndex], test_size= split, random_state=42)

	#Create Models
	model = model.fit(x_train, y_train)
	return model, panda.columns.values, x_test, y_test

@debug
def writeFeatures(features, datafile):
	with open(config.path("..","data",datafile,"feature_importance.txt"),'wb') as f:
		for feature, importance in features:
			write = "%s#%f\n" % (feature, importance)
			f.write(write.replace("#", (24 - len(write)) * " "))

@debug
def main(datafile):
	#Creating the model
	model = GradientBoostingRegressor()

	# Getting Data
	d = dc.Data(datafile = datafile, limit = 2000)
	gc.collect()

	# Training the model
	# train(model, d, test_train_split = .1)
	model, columns, x_tests, y_tests = config.get(config.path("..","data",datafile,"model.p"), train, model = model, data = d, test_train_split = .1)

	#Sorting and Writing Important Features
	sortedFeatures = sorted(zip(columns, model.feature_importances_), key = itemgetter(1))[::-1]
	writeFeatures(sortedFeatures, datafile)

if __name__ == "__main__":
	main("H147")

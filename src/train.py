import format_data as fd
import data as dc
from wrappers import debug
import config
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle as p
import numpy as np
import os 

@debug
def train(trainFeature, trainCost):
	"""
	Creates a model and trains it with the training features and costs
	"""
	model = RandomForestRegressor(n_estimators = 500)
	model.fit(trainFeature, trainCost)
	return model

@debug
def predict(model, testFeature, testCost):
	"""
	Uses a modle and predicts the cost given the test features. 
	Returns the accuracy score
	"""
	predicts = model.predict(testFeature)
	with open("predictions.txt", 'wb') as f:
		p.dump(predicts, f)
	#return metrics.mean_squared_error(testCost, predicts)
	return metrics.explained_variance_score(testCost, predicts)

@debug
def loadData(filename, test = .1):
	"""
	Loads data from .npy binaries representative of our data created by format_data.py
	Takes in filename (i.e. 144d.dat) and a test size (percentage)
	returns trainX, trainY, testX, testY
	"""
	X = np.load(os.path.join("..","data",filename[:-4] + "_dataX.npy"))
	Y = np.load(os.path.join("..","data",filename[:-4] + "_dataY.npy"))
	cut = int(X.shape[0] * test)
	return  X[cut:], Y[cut:], X[:cut], Y[:cut]

if __name__ == "__main__":
	trainFeature, trainCost, testFeature, testCost = loadData(config.H144D, test = .1)

	# print trainFeature.shape
	# print trainCost.shape

	# print testFeature.shape
	# print testCost.shape


if __name__ == "__main__":
	percentTrain = 0.8
	h144aCostData = np.load(os.path.join("..","data", "h144a" + "_" + "dataX" + ".npy"))
	h144aFeatureData = np.load(os.path.join("..","data", "h144a" + "_" + "dataY" + ".npy"))

	end = int(percentTrain*len(h144aFeatureData))
	trainCost = h144aCostData[0:end]
	trainFeature = h144aFeatureData[0:end]
	testCost = h144aCostData[end:len(h144aCostData)]
	testFeature = h144aFeatureData[end:len(h144aFeatureData)]
	model = Train(trainCost, trainFeature)
	# predicts(model, testCost, testFeature)


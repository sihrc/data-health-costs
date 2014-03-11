import data as dc
from wrappers import debug
import config
from lookup import writeFeatureImportance
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics
import pickle as p
import numpy as np

@debug
def train(trainFeature, trainCost):
	"""
	Creates a model and trains it with the training features and costs

	author: Jazmin
	"""
	model = GradientBoostingRegressor()
	model.fit(trainFeature, trainCost)
	return model

@debug
def predict(model, testFeature, testCost):
	"""
	Uses a modle and predicts the cost given the test features. 
	Returns the accuracy score

	author: Jazmin
	"""
	predicts = model.predict(testFeature)
	#return metrics.mean_squared_error(testCost, predicts)
	return metrics.explained_variance_score(testCost, predicts)

@debug
def loadData(filename, test = .1):
	"""
	Loads data from .npy binaries representative of our data created by format_data.py
	Takes in filename (i.e. 144d.dat) and a test size (percentage)
	returns trainX, trainY, testX, testY

	Author: Chris 
	"""
	X = np.load(config.path("..","data",filename, filename + "_dataX.npy"))
	Y = np.load(config.path("..","data",filename, filename + "_dataY.npy"))
	cut = int(X.shape[0] * test)
	return  X[cut:], Y[cut:], X[:cut], Y[:cut]

if __name__ == "__main__":
	trainFeature, trainCost, testFeature, testCost = loadData("H147", test = .1)

	# print trainFeature.shape
	# print trainCost.shape

	# print testFeature.shape
	# print testCost.shape

	model = train(trainFeature, trainCost)
	error = predict(model, testFeature, testCost)

	# importances = zip (range(trainFeature.shape[1]), model.feature_importances_)
	# importances.sort(key = itemgetter(1))
	
	# for featureIndex,importance in importances[::-1]:
	# 		print feature_dict["H147"][featureIndex] , importance
	# 		raw_input()

	writeFeatureImportance(model, trainFeature, "H147")


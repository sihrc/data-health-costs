import data as dc
from wrappers import debug
import config

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics

import pickle as p
import numpy as np
import os

@debug
def one_hot(array):
        """
        [0,1,2,3,4,5,6,7,8,9]
        """
        array = array.flatten()
        output = np.zeros(shape = (len(array),np.max(array) + 1))
        output[np.arange(len(array)),array] = 1
        return output

@debug
def loadData(filename, test = .1):
	"""
	Loads data from .npy binaries representative of our data created by format_data.py
	Takes in filename (i.e. 144d.dat) and a test size (percentage)
	returns trainX, trainY, testX, testY
	"""
	X = np.load(os.path.join("..","data",filename[:-4] + "_dataX.npy"))
	Y = np.load(os.path.join("..","data",filename[:-4] + "_dataY.npy"))
	for line in Y:
		if line < 0:
			print line
	#One Hot the plan options
	Y = one_hot(Y.astype("int"))
	cut = int(X.shape[0] * test)
	return  X[cut:], Y[cut:], X[:cut], Y[:cut]

@debug
def train(trainFeature, trainCost):
	"""
	Creates a model and trains it with the training features and costs
	"""
	model = RandomForestClassifier(n_estimators = 300)
	model.fit(trainFeature, trainCost)
	return model

@debug
def predict(model, testFeature, testCost):
	"""
	Uses a modle and predicts the cost given the test features. 
	Returns the accuracy score
	"""
	predicts = model.predict(testFeature)
	return metrics.accuracy_score(testCost, predicts)


if __name__ == "__main__":
	trainFeature, trainCost, testFeature, testCost = loadData(config.H143, test = .1)

	# print trainFeature.shape
	# print trainCost.shape

	# print testFeature.shape
	# print testCost.shape

	model = train(trainFeature, trainCost)
	error = predict(model, testFeature, testCost)

	print error



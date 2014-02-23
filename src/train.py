import format_data as fd
import data as dc
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle as p
import numpy as np
import os 

def Train(trainCost, trainFeature):
	model = RandomForestRegressor()
	model.fit(trainFeature, trainCost)
	return model

def Predict(model, testCost, testFeature):
	predicts = model.predict(testFeature)
	print metrics.accuracy_score(testCost, predicts)
	with open("predictions.txt", 'wb') as f:
		p.dump(predicts, f)




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

#Python Modules
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
# import numpy as np

#Local Modules
from wrappers import debug
import data as dc
@debug
def train(trainFeatures, targetFeature):
	model = GradientBoostingRegressor()
	model.fit(trainFeatures, targetFeature)
	return model

@debug
def predict(model, testFeatures, targetFeature):
	predicts = model.predict(testFeatures)
	return metrics.explained_variance_score(targetFeature, predictions)

@debug
def main(datafile):
	# Getting Data
	d = dc.getData(datafile)
	# Reading Data into a Panda Table
	panda = pd.read_csv(d.panda, low_memory=False, delimiter = ",")
	# data = panda.as_matrix()

	targetFeatures = panda[d.costs].as_matrix()
	trainFeatures = panda[[feature for feature in d.tags if feature not in d.costs]].as_matrix()

	print targetFeatures.shape
	print trainFeatures.shape

if __name__ == "__main__":
	main("H144D")
	# targetFeatureData = d.data[d.featureIndices[random.choice(d.targetCosts)]]
	# trainX = d.data.copy()
	# trainX.mask[[d.featureIndices[cost] for cost in d.targetCosts]]= True
	# model = config.get(config.path("..","data",datafile,"model.p"), train, trainFeatures = trainX, targetFeature = targetFeatureData)



#with pandas takes 19243.000 ms
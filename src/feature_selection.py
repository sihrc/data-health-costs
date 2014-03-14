from sklearn.ensemble import GradientBoostingRegressor

#Local Modules
from wrappers import debug
import data as dc
import config

def train(trainFeatures, targetFeature):

	model = GradientBoostingRegressor()
	model.fit(trainFeatures, targetFeature)
	return model

def predict(model, testFeatures, targetFeature):

	predicts = model.predict(testFeatures)
	return metrics.explained_variance_score(targetFeature, predictions)

if __name__ == "__main__":
	import shutil
	shutil.rmtree(config.path("..","data"))
	d = dc.getData("H147")
	targetFeatureData = d.data[d.featureIndices[random.choice(d.targetCosts)]]
	trainX = d.data.copy()
	trainX.mask[[d.featureIndices[cost] for cost in d.targetCosts]]= True
	model = config.get(config.path("..","data",datafile,"model.p"), train, trainFeatures = trainX, targetFeature = targetFeatureData)

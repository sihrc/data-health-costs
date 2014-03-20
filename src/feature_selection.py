#Python Modules
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd

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
def readData(path):
	return pd.read_csv(path)

@debug
def main(datafile):
	d = dc.getData(datafilez)
	data = readData(d.panda)

if __name__ == "__main__":
	main("H144D")
	# targetFeatureData = d.data[d.featureIndices[random.choice(d.targetCosts)]]
	# trainX = d.data.copy()
	# trainX.mask[[d.featureIndices[cost] for cost in d.targetCosts]]= True
	# model = config.get(config.path("..","data",datafile,"model.p"), train, trainFeatures = trainX, targetFeature = targetFeatureData)



#with pandas takes 19243.000 ms
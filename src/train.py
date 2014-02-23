import analyze_features as af
import data as dc
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle as p

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
	model = Train(trainCost, trainFeature)
	predicts(model, testCost, testFeature)



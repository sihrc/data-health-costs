#Python Modules
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.cross_validation import train_test_split
from sklearn.metrics import explained_variance_score
import pandas as pd

#Local Modules
from wrappers import debug
import data as dc
import config
import random

@debug
def train(trainFeatures, targetFeature):
	model = GradientBoostingRegressor()
	model.fit(trainFeatures, targetFeature)
	return model

@debug
def predict(model, trainFeatures, targetFeature):
	predicts = model.predict(trainFeatures)
	return explained_variance_score(targetFeature, targetFeature)

@debug
def main(datafile):
	# Getting Data
	d = dc.getData(datafile)
	# Reading Data into a Panda Table
	raw_panda = pd.read_csv(d.panda, low_memory=False, delimiter = ",")
	panda = raw_panda._get_numeric_data()

	print "Non-numerical Columns\n", set(raw_panda.columns.values) - set(panda.columns.values)

	#Get feature and target data
	dataFeatures = panda[[feature for feature in panda.columns.values if feature not in d.costs]].as_matrix().astype("float")
	targetFeatures = panda[d.costs].as_matrix().astype("float")

	#Split the data
	x_train, x_test, y_train, y_test = train_test_split(dataFeatures, targetFeatures[:,random.randint(0,targetFeatures.shape[1])], test_size=0.15, random_state=42)

	#Create Models
	model = train(x_train, y_train)
	# model = config.get(config.path("..","data",datafile,"model.p"), train, trainFeatures = x_train, targetFeature = y_train)

	print predict(model, x_test, y_test)

if __name__ == "__main__":
	main("H144D")

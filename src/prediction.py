from sklearn.linear_model import Ridge
from pandas import read_csv
import random
import numpy as np
from sklearn.cross_validation import train_test_split

from wrappers import debug
import data as dc
import config



@debug
def train(trainFeatures, targetFeature):
	model = Ridge()
	model.fit(trainFeatures, targetFeature)
	return model

@debug
def predict(model, trainFeatures, targetFeature):
	predicts = model.predict(trainFeatures)
	return explained_variance_score(targetFeature, targetFeature)

def normalize(dataFeatures):
	# Normalize the data
	mean = np.mean(dataFeatures)
	return dataFeatures/mean


if __name__ == "__main__":
	d = dc.Data("H144D")

	# Reading Data into a Panda Table
	raw_panda = read_csv(d.panda, delimiter = ",")
	panda = raw_panda._get_numeric_data()

	print "Non-numerical Columns\n", set(raw_panda.columns.values) - set(panda.columns.values)

	#Get feature and target data
	dataFeatures = panda[[feature for feature in panda.columns.values if feature not in d.costs]].as_matrix().astype("float")
	targetFeatures = panda[d.costs].as_matrix().astype("float")
	target = random.randint(0,targetFeatures.shape[1])

	normalFeatuers = normalize(dataFeatures)

	#Split the data
	x_train, x_test, y_train, y_test = train_test_split(dataFeatures, targetFeatures[:,target], test_size=0.15, random_state=42)
	#Create Models
	model = train(x_train, y_train)

	error = predict(model, x_train, x_test)

	print error
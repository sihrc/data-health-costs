from sklearn.ensemble import GradientBoostingRegressor

#Local Modules
from wrappers import debug
import data as dc
import lookup as L
import config
import cPickle

@debug
def getCostFeatures(datafile):
	"""
	Get target cost features from data set
	author: chris
	"""
	exists, path = config.path("..","data",datafile,"costFeatures.p")
	
	if exists:
		with open(path, 'rb') as f:
			costFeatures = p.load(f)
		return costFeatures

	costFeatures = []
	d = dc.getData(datafile)
	for feature in d.codebook.keys():
		featureDetails = L.getDetails(datafile, feature)
		if  "$" in featureDetails["Values"]:
			costFeatures.append(feature)
	with open(path, 'wb') as f:
		p.dump(costFeatures, f)

	return costFeatures


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
	datafile = "H144D"
	print getCostFeatures("H144D")

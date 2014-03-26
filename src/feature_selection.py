#Python Modules
from sklearn.preprocessing import normalize
from sklearn.linear_model import LinearRegression as Model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import explained_variance_score
from pandas import read_csv
from operator import itemgetter
from random import randint

#Local Modules
from wrappers import debug
import data as dc
import config

@debug
def predict(model, trainFeatures, targetFeature):
    predicts = model.predict(trainFeatures)
    return explained_variance_score(targetFeature, targetFeature)

@debug
def train(trainFeatures, targetFeature):
    model = Model()
    model.fit(trainFeatures, targetFeature)
    return model

@debug
def writeFeatures(features, targetName):
    with open(config.path(path,"feature_importance%s.txt" % (targetName)),'wb')as f:
        for feature, importance in features:
            write = "%s#%f\n" % (feature, importance)
            f.write(write.replace("#", (24 - len(write)) * " "))

@debug
def runModel(dataFeatures, targetFeatures, target, panda, d):
    #Split the data
    x_train, x_test, y_train, y_test = train_test_split(dataFeatures, targetFeatures[:,target], test_size=0.15, random_state=42)
    #Create Models
    # model = train(x_train, y_train)
    model = config.get(config.path(path,"model.p"), train, trainFeatures = x_train, targetFeature = y_train)
    #Sorting and Writing Important Features
    sortedFeatures = sorted(zip(panda.columns.values, model.coef_), key = itemgetter(1))[::-1]
    writeFeatures(sortedFeatures, d.costs[target])
    return model, x_test, y_test

@debug
def main():
    # Getting Data
    d = dc.Data(datafile)
    # Reading Data into a Panda Table
    raw_panda = read_csv(d.panda, delimiter = ",")
    panda = raw_panda._get_numeric_data()
    print "Non-numerical Columns\n", set(raw_panda.columns.values) - set(panda.columns.values)
    #Get feature and target data
    dataFeatures = normalize(panda[[feature for feature in panda.columns.values if feature not in d.costs]].as_matrix().astype("float"), axis = 0)
    targetFeatures = normalize(panda[d.costs].as_matrix().astype("float"), axis = 0)

    # runModel on all cost features
    for target in xrange(targetFeatures.shape[1]):
      model, x_test, y_test = runModel(dataFeatures, targetFeatures, target, panda, d)
      print predict(model, x_test, y_test)


    #runModel for one cost feature
    # runModel(dataFeatures, targetFeatures, randint(0,targetFeatures.shape[1] - 1), panda, d)


if __name__ == "__main__":
    datafile = "H147"
    path = config.path("..","data",datafile)
    main()
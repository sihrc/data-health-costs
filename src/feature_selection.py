#Python Modules
from sklearn.preprocessing import normalize
from sklearn.ensemble import GradientBoostingRegressor as Model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error as score
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
    return score(predicts, targetFeature)

@debug
def train(trainFeatures, targetFeature):
    model = Model()
    model.fit(trainFeatures, targetFeature)
    return model

@debug
def writeFeatures(features, costTag):
    with open(config.path(path,"feature_importance_%s.txt" % (costTag)),'wb')as f:
        for feature, importance in features:
            write = "%s#%f\n" % (feature, importance)
            f.write(write.replace("#", (24 - len(write)) * " "))

@debug
def runTrain(x_train, y_train, costTag, columns):
    #Create Models
    # model = train(x_train, y_train)
    model = config.get(config.path(path,"model_%s.p" % costTag), train, trainFeatures = x_train, targetFeature = y_train)
    return model

    #Sorting and Writing Important Features
    try:
        sortedFeatures = sorted(zip(columns, model.coef_), key = itemgetter(1))[::-1]
    except:
        sortedFeatures = sorted(zip(columns, model.feature_importances_), key = itemgetter(1))[::-1]
    writeFeatures(sortedFeatures, costTag)
@debug
def clean(*args):
    import os
    if not os.path.exists(path): return
    for cfile in os.listdir(path):
        if sum([arg in cfile for arg in args]) > 0:
            filepath = config.path(path, cfile)
            os.chmod(filepath, 0777)
            os.remove(filepath)
            print "Cleaning %s" % filepath

@debug
def readData():
    # Reading Data into a Panda Table
    raw_panda = read_csv(d.csv, delimiter = ",")
    panda = raw_panda._get_numeric_data()
    columns = panda.columns.values

    print "Non-numerical Columns\n", set(raw_panda.columns.values) - set(columns)
    #Get feature and target data
    dataFeatures = normalize(panda[[feature for feature in columns if feature not in d.costs]].as_matrix().astype("float"), axis = 0)
    targetFeatures = normalize(panda[d.costs].as_matrix().astype("float"), axis = 0)

    x_train, x_test, y_train, y_test = train_test_split(dataFeatures, targetFeatures, test_size=0.15, random_state=42)
    return  x_train, x_test, y_train, y_test, columns

@debug
def runModel(x_train, x_test, y_train, y_test,columns):            
    # runModel on all cost features
    results = []
    for target in xrange(y_train.shape[1]):
        mask_train = y_train[:,target] > 0
        mask_test = y_test[:,target] > 0
        model = runTrain(x_train[mask_train,:], y_train[mask_train,target], d.costs[target], columns)
        prediction = predict(model, x_test[mask_test,:], y_test[mask_test,target])
        print prediction
        results.append(prediction)
    return results

    #runModel for one cost feature
    # target = randint(0,y_train.shape[1] - 1)
    # model = runModel(x_train, y_train[:,target], d.costs[target], columns)
    # print predict(model, x_test, y_test[:,target])

@debug
def main():
    # Clean Past Data
    clean(\
        # "codebook",\
        # "model",\
        # "csv",\
        # "costs",\
        # "feature",\
        )

    x_train, x_test, y_train, y_test, columns = readData()

    results =  runModel(x_train, x_test, y_train, y_test, columns)

    print results




if __name__ == "__main__":
    datafile = "H147"
     # Getting Data
    d = dc.Data(datafile)
    path = config.path("..","data",datafile)
    main()


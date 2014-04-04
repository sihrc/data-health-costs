#Python Modules
from sklearn.preprocessing import normalize
# from sklearn.ensemble import GradientBoostingRegressor as Model
from sklearn.linear_model import Ridge as Model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error as score
from pandas import read_csv
from operator import itemgetter
from random import randint
from lookup import print_variable
from lookup import getDetails
import numpy as np

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
def filterTop10(sortedFeatures):
    newIgnored = []
    end = 9
    lens = 0
    for feature in sortedFeatures:
        print feature
        print print_variable(getDetails(datafile, feature[0]))
        val = raw_input('Enter y or n:')
        if val == "n":
            newIgnored.append(feature)
        elif val == "y" :
            lens = lens + 1
        if lens == 10:
            break
    with open(config.path(path,"ignoredFeatuers.txt"),'a')as f:
        for feature in newIgnored:
            write = "%s\n" % feature
            f.write(write)

@debug
def writeFeatures(features, costTag):
    with open(config.path(path,"feature_importance_%s.txt" % (costTag)),'wb')as f:
        for feature, importance in features:
            write = "%s#%f\n" % (feature, importance)
            f.write(write.replace("#", (24 - len(write)) * " "))

@debug
def runModel(x_train, y_train, costTag, columns):
    #Create Models
    # model = train(x_train, y_train)
    model = config.get(config.path(path,"model_%s.p" % costTag), train, trainFeatures = x_train, targetFeature = y_train)
    #Sorting and Writing Important Features
    try:
        sortedFeatures = sorted(zip(columns, model.coef_), key = itemgetter(1))[::-1]
    except:
        sortedFeatures = sorted(zip(columns, model.feature_importances_), key = itemgetter(1))[::-1]
    writeFeatures(sortedFeatures, costTag)
    return model

@debug
def filterPanda(panda):
    def nonNumerical(data):
        newTags = data.copy() * -1
        invalid = data < 0
        
        newTags[np.invert(invalid)] = 0
        result = np.zeros((newTags.shape[0],newTags.shape[1],np.max(newTags) + 1))
        for i in xrange(newTags.shape[0]):
            for j in xrange(newTags.shape[1]):
                result[i][j][newTags[i][j]] = 1

        data[invalid] = 0
        mean = np.sum(data, axis = 0)/np.sum(np.invert(invalid), axis = 0)
        data[invalid] = mean[np.where(invalid)[1]]
        return data, newTags
    names = np.array(panda.columns.values)[list(set(np.where(panda.values<0)[1]))]
    data, newData = nonNumerical(panda[names].as_matrix().astype("float")) 
    for i in xrange(len(names)):
        panda[names[i] + "NEGS"] = newData[:,i]
        panda[names[i]] = data[:,i]
    return panda


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
def main():
    # Clean Past Data
    clean(\
        # "codebook",\
        "model",\
        # "csv",\
        # "costs",\
        # "panda",\
        "feature",\
        # "filtered_panda",\
        )

    # Getting Data
    d = dc.Data(datafile)
    # Reading Data into a Panda Table
    raw_panda = read_csv(d.csv, delimiter = ",")
    panda  = config.get(config.path(path,"filtered_panda.p"), filterPanda, panda = (raw_panda._get_numeric_data()))
    columns = [feature for feature in panda.columns.values if feature not in d.costs]

    print "Non-numerical Columns\n", set(raw_panda.columns.values) - set(columns)
    #Get feature and target data
    dataFeatures = normalize(panda[columns].as_matrix().astype("float"), axis = 0)
    targetFeatures = normalize(panda[d.costs].as_matrix().astype("float"), axis = 0)
    x_train, x_test, y_train, y_test = train_test_split(dataFeatures, targetFeatures, test_size=0.15, random_state=42)
    # runModel on all cost features
    results = []
    # for target in xrange(y_train.shape[1]):
    #     mask_train = y_train[:,target] > 0
    #     mask_test = y_test[:,target] > 0
    #     model = runModel(x_train[mask_train,:], y_train[mask_train,target], d.costs[target], columns)
    #     prediction = predict(model, x_test[mask_test,:], y_test[mask_test,target])
    #     print prediction
    #     results.append(prediction)

    #print results


    # runModel for one cost feature
    target = panda["TOTSELF11"].as_matrix().astype("float")
    x_train, x_test, y_train, y_test = train_test_split(dataFeats, target, test_size=0.15, random_state=42)
    model = runModel(x_train, y_train, "TOTSELF11", columns)
    # print predict(model, x_test, y_test[:,target])


if __name__ == "__main__":
    datafile = "H147"
    path = config.path("..","data",datafile)
    main()
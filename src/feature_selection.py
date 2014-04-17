#Python Modules
# from sklearn.ensemble import GradientBoostingRegressor as Model
# from sklearn.linear_model import Ridge as Model
from sklearn.ensemble import RandomForestRegressor as Model
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import normalize
from sklearn.metrics import mean_squared_error as score

from operator import itemgetter
from random import randint
from lookup import print_variable, getDetails
import numpy as np

#Local Modules
from wrappers import debug
import data as dc
import config

@debug
def writeFeatures(costFeature, model):
    try:
        sortedFeatures = sorted(zip([d.tags[index] for index in d.continuous + d.categorical] , model.coef_), key = itemgetter(1))[::-1]
    except:
        sortedFeatures = sorted(zip([d.tags[index] for index in d.continuous + d.categorical] , model.feature_importances_), key = itemgetter(1))[::-1]

    with open(config.path(path,"feature_importance_%s.txt" % (costFeature)),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (feature, importance)
            f.write(write.replace("#", (24 - len(write)) * " "))
@debug
def one_hot(data):
    result = np.zeros((data.shape[0],data.shape[1], np.unique(data).shape[0]))
    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            result[i][j][data[i][j]] = 1
    return result

@debug
def splitContinuous(data):
    if len(data) == 0:
        return np.empty(data.shape[0])
    # newData = (data.copy() * -1).astype("int")
    invalid = data < 0
    
    # newData[np.invert(invalid)] = 0
    # results= one_hot(newData)

    data[invalid] = 0
    mean = np.sum(data, axis = 0)/np.sum(np.invert(invalid), axis = 0)
    cols = np.where(invalid)[1]
    data[invalid] = mean[cols]

    # tags = list()
    # for index in cols:
    #     if index not in tags:
    #         tags.append(index)
    return data#, results, tags

@debug
def costModel(x_test, y_test, x_train, y_train, costIndex = ""):
    #Create Models
    model = Model()
    model.fit(x_train, y_train[:,costIndex])

    return model
    
@debug 
def formatNonNumerical(catData):
    cats = {}
    counter = 0
    for i in xrange(catData.shape[0]):
        for j in xrange(catData.shape[1]):
            if catData[i,j] not in cats:
                cats[str(catData[i,j])] = counter
                counter+= 1
            catData[i,j] = cats[str(catData[i,j])]
    return catData

@debug
def getCosts(data):
    return data[:,d.costs]

@debug
def main():
    #Get feature and target data
    data = np.genfromtxt(config.path(path, datafile.lower() + ".csv"), delimiter=",")
    costs = config.get(config.path(path, "formatCost.p"), getCosts, data = data)
    cat = config.get(config.path(path, "formatCat.p"), formatNonNumerical, catData = data[:,d.categorical])
    cont = config.get(config.path(path, "formatCont.p"), splitContinuous, data = data[:,d.continuous])
    # cont, newCat, newTags = config.get(config.path(path, "splitCont.p"), splitContinuous, data = cont)
    # cat = np.hstack((cat, newCat))
    # hotCats = config.get(config.path(path, "hotConts.p"),one_hot, data = cat)
    costIndex = 0
    training_data = np.hstack((cont,cat))

    x_train, x_test, y_train, y_test = train_test_split(training_data, costs,test_size=0.15, random_state=42)
    model = config.get(config.path(path,"model_%s.p" % d.costs[costIndex]), costModel, x_train = x_train, y_train = y_train, x_test = x_test, y_test = y_test, costIndex = costIndex)

    #Sorting and Writing Important Features
    writeFeatures(d.costs[costIndex], model)
    print x_train.shape
    print x_test.shape
    predictions = model.predict(x_test)
    accuracy = score(predictions, y_test[:,costIndex])
    print accuracy ** .5

if __name__ == "__main__":
    datafile = "H149"
    # Clean Past Data
    config.clean([\
        "codebook",\
        "model",\
        "csv",\
        "panda",\
        "feature",\
        "format",\
        ], datafile = datafile)
    d = dc.Data(datafile)
    path = config.path("..","data",datafile)
    main()
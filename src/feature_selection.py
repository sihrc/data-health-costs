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
def writeFeatures(costFeature):
    try:
        sortedFeatures = sorted(zip([d.tags[index] for index in d.continuous + d.categorical] , model.coef_), key = itemgetter(1))[::-1]
    except:
        sortedFeatures = sorted(zip([d.tags[index] for index in d.continuous + d.categorical] , model.feature_importances_), key = itemgetter(1))[::-1]

    with open(config.path(path,"feature_importance_%s.txt" % (costFeature)),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (feature, importance)
            f.write(write.replace("#", (24 - len(write)) * " "))
@debug
def hotDemDats(data):
    result = np.zeros((data.shape[0],data.shape[1], np.unique(data).shape[0]))
    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            result[i][j][data[i][j]] = 1
    return result
@debug
def splitContinuous(data):
    # newData = (data.copy() * -1).astype("int")
    invalid = data < 0
    
    # newData[np.invert(invalid)] = 0
    # results= hotDemDats(newData)

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
def costModel(x_train, y_train, costIndex = ""):
    #Create Models
    model = Model()
    model.fit(x_train, y_train[:,costIndex])

    #Sorting and Writing Important Features
    writeFeatures(d.costs[costIndex])
    predictions = model.predict(x_test)
    accuracy = score(predictions, y_test[:,costIndex])
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
def main():
    #Get feature and target data
    data = np.genfromtxt(config.path(path, datafile.lower() + ".csv"), delimiter=",")
    cont, cat = data[:,d.continuous], data[:,d.categorical]
    costs = data[:,d.costs]
    cat = config.get(config.path(path, "formatCat.p"), formatNonNumerical, catData = cat)
    cont = config.get(config.path(path, "formatCont.p"), splitContinuous, data = cont)
    # cont, newCat, newTags = config.get(config.path(path, "splitCont.p"), splitContinuous, data = cont)
    # cat = np.hstack((cat, newCat))
    # hotCats = config.get(config.path(path, "hotConts.p"),hotDemDats, data = cat)
    x_train, x_test, y_train, y_test = train_test_split(np.hstack((cont,cat)), costs,test_size=0.15, random_state=42)

    model = config.get(config.path(path,"model_%s.p" % d.costs[0]), costModel, x_train = x_train, y_train = y_train, costIndex = 0)

if __name__ == "__main__":
    datafile = "H149"
    # Clean Past Data
    config.clean([\
        # "codebook",\
        "model",\
        # "csv",\
        # "costs",\
        # "panda",\
        "feature",\
        "format",\
        # "filtered_panda",\
        ], datafile = datafile)
    d = dc.Data(datafile)
    path = config.path("..","data",datafile)
    main()
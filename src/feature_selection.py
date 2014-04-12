#Python Modules
from sklearn.ensemble import GradientBoostingRegressor as Model
# from sklearn.linear_model import Ridge as Model
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
        sortedFeatures = sorted(zip(columns, model.coef_), key = itemgetter(1))[::-1]
    except:
        sortedFeatures = sorted(zip(columns, model.feature_importances_), key = itemgetter(1))[::-1]

    with open(config.path(path,"feature_importance_%s.txt" % (costFeature)),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (feature, importance)
            f.write(write.replace("#", (24 - len(write)) * " "))

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
def costModel(costFeature = ""):
    #Create Models
    target = dh.costs.find(costFeature)
    model = Model()
    model.fit(dh.x_train, dh.y_train[:,target])

    #Sorting and Writing Important Features
    writeFeatures(costFeature)
    predictions = model.predict(x_test)
    accuracy = score(predictions, y_test[:,target])
    dh.accuracy.append((costFeature, accuracy))
    return model

            
@debug
def main():
    #Get feature and target data
    data = np.genfromtxt(config.path(path, datafile.lower() + ".csv"), delimiter=",")
    x_train, x_test, y_train, y_test = train_test_split(data[:,d.continuous],data[:,d.costs], test_size=0.15, random_state=42)

    
    model = config.get(config.path(path,"model_%s.p" % d.costs[0]), costModel, costFeature = 0)

if __name__ == "__main__":
    datafile = "H147"
    # Clean Past Data
    config.clean([\
        # "codebook",\
        "model",\
        # "csv",\
        # "costs",\
        # "panda",\
        "feature",\
        # "filtered_panda",\
        ], datafile = datafile)
    d = dc.Data(datafile)
    path = config.path("..","data",datafile)
    main()
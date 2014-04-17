"""
Feature Selection using sci-kit learn
author:chris
"""

#Python Modules
# from sklearn.ensemble import GradientBoostingRegressor as Model
# from sklearn.linear_model import Ridge as Model
from sklearn.ensemble import RandomForestRegressor as Model
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error as score
import numpy as np

#Local Modules
from wrappers import debug
import format_features as ff
import data as dc
import config


@debug
def writeFeatures(costFeature, model, data, costData, d):
    """
    Writes feature importances to file in order of importance
    Saves to pickle file for use in future modelling

    Takes in costFeature index of d.tags
    Takes in the model

    Returns the costFeature, Sorted list of feature indices based on importance
    """
    try:
        sortedFeatures = sorted(zip(d.continuous + d.categorical , model.coef_), key = (lambda x:x[1]))[::-1]
    except:
        sortedFeatures = sorted(zip(d.continuous + d.categorical , model.feature_importances_),  key = (lambda x:x[1]))[::-1]

    with open(config.path("..","data",d.datafile,"features",  "importances", "feature_importance_%s.txt" % (d.tags[costFeature])),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (d.tags[feature], importance)
            f.write(write.replace("#", (24 - len(write)) * " "))
    tags = d.continuous + d.categorical
    return data[:,[tags.index(tag) for tag, value in sortedFeatures]], costData


@debug
def costModel(x_train, y_train):
    """
    Creates and fits the model based on x_train and y_train
    Returns model as specified in import
    """
    model = Model()
    model.fit(x_train, y_train)

    return model



@debug
def select(costIndices, datafile, d):
    """
    Performs feature selection given datafile
    """
    #Get Data Handler
    path = config.path("..","data",datafile)

    #Get feature and target data
    data = np.genfromtxt(config.path(path, "data", datafile.lower() + ".csv"), delimiter=",")
    cat = config.get(config.path(path, "formatted",  "formatCat.p"), ff.formatNonNumerical, catData = data[:,d.categorical])
    cont = config.get(config.path(path, "formatted", "formatCont.p"), ff.splitContinuous, data = data[:,d.continuous])
    # One hotting categorical data for non decision tree models
    # cont, newCat, newTags = config.get(config.path(path, "splitCont.p"), splitContinuous, data = cont)
    # cat = np.hstack((cat, newCat))
    # hotCats = config.get(config.path(path, "hotConts.p"),one_hot, data = cat)
    training_data = np.hstack((cont,cat))
    x_train, x_test, y_train, y_test = train_test_split(training_data, data[:,d.costs],test_size=0.15, random_state=42)

    # moneyError = []
    #Loops through every cost found in datafile
    for costIndex in costIndices:
        target = d.costs.index(costIndex)
        #Splitting to testing and training datasets
        model = config.get(config.path(path,"models", "model_%s.p" % d.tags[costIndex]), costModel, x_train = x_train, y_train = y_train[:,target])

        #Sorting and Writing Important Features
        feat_indices = config.get(config.path(path,"features", "features%s.p" % d.tags[costIndex]), writeFeatures, costFeature = costIndex, model = model, data = training_data, costData = data[:,costIndex], d = d)

        #Testing model accuracies
        # predictions = model.predict(x_test)
        # accuracy = score(predictions, y_test[:,target])
        # moneyError.append((d.tags[costIndex],accuracy ** .5))
    # print moneyError

if __name__ == "__main__":
    datafile = "H144D"
    # Clean Past Data
    config.clean([\
        # "data",\
        "formatted",\
        "features",\
        "models",\
        ], datafile = datafile)

    d = config.get(config.path("..","data",datafile,"data","dHandler.p"), dc.Data, datafile = datafile, include_costs = False)
    select(d.costs, datafile, d)
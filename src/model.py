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
from sklearn.feature_selection import RFE
import numpy as np

#Local Modules
from wrappers import debug
import format_features as ff
import data_helper as dc
import config


@debug
def writeFeatures(costFeature, importance , d):
    """
    Writes feature importances to file in order of importance
    Saves to pickle file for use in future modelling

    Takes in costFeature index of d.tags
    Takes in the model

    Returns the costFeature, Sorted list of feature indices based on importance
    """
    sortedFeatures = sorted(zip(d.continuous + d.categorical, list(importance)) ,  key = (lambda x:x[1]))
    with open(config.path("..","data",d.datafile,"features",  "importances", "feature_importance_%s.txt" % (d.tags[costFeature])),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (d.tags[feature], importance)
            f.write(write.replace("#", (24 - len(write)) * " "))


@debug
def select_feature(x_train, y_train, show_original):
    """
    Creates and fits the model based on x_train and y_train
    Returns model as specified in import
    """
    model = Model(100)
    tenth = int(xtrain.shape[1]/10)
    selector = RFE(model, tenth, tenth, verbose = 1)
    selector.fit(x_train, y_train)
    return selector



@debug
def main(costIndices, d, include_costs = False, show_original = False):
    """
    Performs feature selection given datafile
    """
    #Get Data Handler
    path = config.path("..","data",d.datafile)

    #Get feature and target data
    data = np.genfromtxt(config.path(path, "data", d.datafile.lower() + ".csv"), delimiter=",")
    cat = config.get(config.path(path, "formatted",  "formatCat.p"), ff.formatCategorical, catData = data[:,d.categorical])
    cont = config.get(config.path(path, "formatted", "formatCont.p"), ff.formatContinuous, data = data[:,d.continuous])
    costs = data[:,d.costs]
    # One hotting categorical data for non decision tree models
    # cont, newCat, newTags = config.get(config.path(path, "splitCont.p"), splitContinuous, data = cont)
    # cat = np.hstack((cat, newCat))
    # hotCats = config.get(config.path(path, "hotConts.p"),one_hot, data = cat)
    training_data = np.hstack((cont,cat))
    x_train, x_test, y_train, y_test = train_test_split(training_data, costs, test_size=0.15, random_state=42)

    # moneyError = []
    #Loops through every cost found in datafile
    for costIndex in [d.costs.index(tag) for tag in costIndices]:
        if include_costs:
            x_train_ = np.hstack((x_train, y_train[:,:costIndex], y_train[:,costIndex + 1:]))
            x_test_ = np.hstack((x_test, y_test[:,:costIndex], y_test[:,costIndex + 1:]))
        else:
            x_train_ = x_train
            x_test_ = x_test
        #Splitting to testing and training datasets
        model = config.get(config.path(path,"models", "model_%s.p" % d.tags[costIndex]), select, x_train = x_train_, y_train = y_train[:,costIndex], show_original = show_original)

        #Sorting and Writing Important Features
        writeFeatures(costFeature = costIndex, importance = model.ranking_, d = d)

        predictions = model.predict(x_test)
        accuracy = score(predictions, y_test[:,costIndex]) ** .5
        config.write(config.path("..","data",d.datafile, "models", "%s_after_accuracy.txt" % d.tags[costIndex]), accuracy)
        print "\nModel accuracy after feature selection for cost:%s\terror:%f\n" % (d.tags[costIndex], accuracy)

if __name__ == "__main__":
    import sys
    datafile = sys.argv[1] 
    # Clean Past Data
    config.clean([\
        "data",\
        "formatted",\
        "features",\
        "models",\
        ], datafile = datafile)

    d = config.get(config.path("..","data",datafile,"data","dHandler.p"), dc.Data, datafile = datafile)
    main(d.costs, d)
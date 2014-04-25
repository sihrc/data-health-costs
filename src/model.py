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
import data_helper as dc
import config


@debug
def writeFeatures(costFeature, importance , d, before = "before"):
    """
    Writes feature importances to file in order of importance
    Saves to pickle file for use in future modelling

    Takes in costFeature index of d.tags
    Takes in the model

    Returns the costFeature, Sorted list of feature indices based on importance
    """
    sortedFeatures = sorted(zip(d.continuous + d.categorical, list(importance)) ,  key = (lambda x:x[1]))
    with open(config.path("..","data",d.datafile,"features",  "importances", before + "_feature_importance_%s.txt" % (d.tags[costFeature])),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (d.tags[feature], importance)
            f.write(write.replace("#", (24 - len(write)) * " "))


@debug
def select_feature(x_train, y_train):
    """
    Creates and fits the model based on x_train and y_train
    Returns model as specified in import
    """
    model = Model(100)
    model.fit(x_train, y_train)
    return model

@debug
def main(costIndices, d, include_costs = False, show_original = False):
    """
    Performs feature selection given datafile
    """
    #Get Data Handler
    path = config.path("..","data",d.datafile)

    #Get feature and target data
    data = np.genfromtxt(config.path(path, "data", d.datafile.lower() + ".csv"), delimiter=",")
    cat = config.getNP(config.path(path, "formatted",  "formatCat.npy"), ff.formatCategorical, catData = data[:,d.categorical])
    cont = config.getNP(config.path(path, "formatted", "formatCont.numpy"), ff.formatContinuous, data = data[:,d.continuous])
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
        before_model = config.get(config.path(path,"models", "before_model_%s.p" % d.tags[costIndex]), select_feature , x_train = x_train_, y_train = y_train[:,costIndex])
        after_model = config.get(config.path(path,"models", "after_model_%s.p" % d.tags[costIndex]), select_feature , x_train = before_model.transform(x_train_), y_train = y_train[:,costIndex])
     
        #Sorting and Writing Important Features
        writeFeatures(costFeature = costIndex, importance = before_model.feature_importances_, d = d, before = "before")
        writeFeatures(costFeature = costIndex, importance = after_model.feature_importances_, d = d, before = "after")
        
        predictions_before = before_model.predict(x_test)
        predictions_after = after_model.predict(before_model.transform(x_test))

        accuracy_before = score(predictions_before, y_test[:,costIndex]) ** .5
        accuracy_after = score(predictions_after, y_test[:,costIndex]) ** .5

        config.write(config.path("..","data",d.datafile, "models", "%s_before_accuracy.txt" % d.tags[costIndex]), accuracy_before)
        config.write(config.path("..","data",d.datafile, "models", "%s_after_accuracy.txt" % d.tags[costIndex]), accuracy_after)
        print "\nModel accuracy before feature selection for cost:%s\terror:%f\n" % (d.tags[costIndex], accuracy_before)
        print "\nModel accuracy after feature selection for cost:%s\terror:%f\n" % (d.tags[costIndex], accuracy_after)

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
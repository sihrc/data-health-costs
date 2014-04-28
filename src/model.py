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
def select_feature(x_train, y_train, trees):
    """
    Creates and fits the model based on x_train and y_train
    Returns model as specified in import
    """
    model =  Model(trees)
    model.fit(x_train, y_train)
    return model

@debug
def load_data(d):
    """
    Loads numpy array from CSV file
    """
    return np.genfromtxt(config.path("..","data",d.datafile, "data", d.datafile.lower() + ".csv"), delimiter=",")

@debug
def parse_features(d, inputs):
    """
    Parsing features from input arguments to a list of tag names
    """
    tags = []
    for tag in inputs:
        if len(tag.strip()) == 1:
            for tag in d.titleMap[tag.strip().upper()]:
                for tag in d.tags:
                    tags.append(d.tags.index(tag))
        else:
            if tag in d.tags:
                tags.append(d.tags.index(tag))
    return tags

@debug
def extract_features(d, featureTags,costTags):
    """
    Extracts Features based on inputted features
    """
    cat_tags = []
    cont_tags = []
    feature_tags = parse_features(d, featureTags)
    if len(featureTags) != 0:
        for tag in featureTags:
            if tag in d.categorical:
                cat_tags.append(tag)
            elif tag in d.continuous:
                cont_tags.append(tag)
    if len(cat_tags) == 0: cat_tags = d.categorical
    if len(cont_tags) == 0: cont_tags = d.continuous

    cost_tags = parse_features(d, costTags)
    cost_tags = d.costs if len(cost_tags) == 0 else parse_features(d, costTags)
    return cat_tags, cont_tags, cost_tags

@debug
def main(featureTags, costTags, d, include_costs = False, trees = 1):
    """
    Performs feature selection given datafile
    """
    #Get Data Handler
    path = config.path("..","data",d.datafile)
    
    #Parsing features
    cat_tags, cont_tags, cost_tags = extract_features(d, featureTags, costTags)

    #Get feature and target data
    data = load_data(d)
    cat = config.getNP(config.path(path, "formatted",  "formatCat.npy"), ff.one_hot, data = data[:,cat_tags].astype("int"))
    cont = config.getNP(config.path(path, "formatted", "formatCont.npy"), ff.formatContinuous, data = data[:,cont_tags])
    costs = data[:,cost_tags]
    training_data = np.hstack((cont,cat))
    x_train, x_test, y_train, y_test = train_test_split(training_data, costs, test_size=0.15, random_state=42)

    #Loops through every cost found in datafile
    for target, costIndex in enumerate(cost_tags):
        costTag =  d.tags[costIndex]
        if include_costs:
            x_train_ = np.hstack((x_train, y_train[:,:target], y_train[:,target + 1:]))
            x_test_ = np.hstack((x_test, y_test[:,:target], y_test[:,target + 1:]))
        else:
            x_train_ = x_train
            x_test_ = x_test
        #Splitting to testing and training datasets
        before_model = config.get(config.path(path,"models", "before_model_%s.p" % costTag), select_feature , x_train = x_train_, y_train = y_train[:,target], trees = trees )
        after_model = config.get(config.path(path,"models", "after_model_%s.p" % costTag), select_feature , x_train = before_model.transform(x_train_), y_train = y_train[:,target], trees = trees)
     
        #Sorting and Writing Important Features
        writeFeatures(costFeature = costIndex, importance = before_model.feature_importances_, d = d, before = "before")
        writeFeatures(costFeature = costIndex, importance = after_model.feature_importances_, d = d, before = "after")
        
        predictions_before = before_model.predict(x_test_)
        predictions_after = after_model.predict(before_model.transform(x_test_))

        accuracy_before = score(predictions_before, y_test[:,target]) ** .5
        accuracy_after = score(predictions_after, y_test[:,target]) ** .5

        config.write(config.path("..","data",d.datafile, "models", "%s_before_accuracy.txt" % costTag), accuracy_before)
        config.write(config.path("..","data",d.datafile, "models", "%s_after_accuracy.txt" % costTag), accuracy_after)
        with open(config.path("..","data",d.datafile,"models", "results.txt"), 'a') as f:
            f.write("\nModel accuracy before feature selection for cost:%s\terror:%f\n" % (costTag, accuracy_before))
            f.write("\nModel accuracy after feature selection for cost:%s\terror:%f\n" % (costTag, accuracy_after))

if __name__ == "__main__":
    import sys
    from optparse import OptionParser

    parse = OptionParser()
    parse.add_option("-f", "--file", dest="datafile",
                      help="name of data set to use. i.e. H144D", metavar="FILE")
    parse.add_option("-s", "--select", dest = "select",
                      help="specify list of data features to use by table name or tag name i.e. [A,B,DUID,PID]", default = "[]")
    parse.add_option("-c", "--costs", dest = "costs", default = "[]",
                        help = "clean cached files of previous runs")
    parse.add_option("-d", "--delete", dest = "clean", default = True, action = "count",
                        help = "removes cached files of previous runs")
    parse.add_option("-i", "--include", dest = "include", default = True, action = "count",
                        help = "includes other target costs in training data")
    parse.add_option("-t", "--trees", dest = "trees", default = 1,
                        help = "number of trees to use for decision tree algorithms")

    (options, args) = parse.parse_args()

    if options.clean:
        config.clean([\
            "data",\
            "formatted",\
            "features",\
            "models",\
            ], datafile = options.datafile)

    d = config.get(config.path("..","data",options.datafile,"data","dHandler.p"), dc.Data, datafile = options.datafile)
    main(options.select.strip()[1:-1].split(","), options.costs.strip()[1:-1].split(","), d, include_costs = options.include, trees = int(options.trees))
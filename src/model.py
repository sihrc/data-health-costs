"""
Feature Selection using sci-kit learn
author:chris
"""

# Python Modules
# from sklearn.ensemble import GradientBoostingRegressor as Model
# from sklearn.linear_model import Ridge as Model
from sklearn.ensemble import RandomForestRegressor as Model
from sklearn.cross_validation import train_test_split
# from sklearn.metrics import mean_squared_error as score
from sklearn.metrics import explained_variance_score as score
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
    with open(config.path("..","data",d.datafile,"features",  "importances", "%s.txt" % (d.tags[costFeature])),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (d.tags[feature], importance)
            f.write(write.replace("#", (24 - len(write)) * " "))


@debug
def create_model(x_train, y_train, trees, catTags, contTags):
    """
    Creates and fits the model based on x_train and y_train
    Returns model as specified in import
    """
    model =  Model(trees)
    model.fit(x_train, y_train)
    return model, catTags, contTags

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
                if tag in d.tags:
                    tags.append(d.tags.index(tag))
                else:
                    print "Feature Selection Warning: feature %s not found %s (will be ignored)" % (tag, d.datafile)
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
def model_score(model, train, test):
    """
    The coefficient R^2 is defined as (1 - u/v), 
     where u is the regression sum of squares ((y_true - y_pred) ** 2).sum()
     and v is the residual sum of squares ((y_true - y_true.mean()) ** 2).sum().
    Best possible score is 1.0, lower values are worse.
    """
    return model.score(train,test)

@debug
def main(featureTags, costTags, d, include_costs = False, trees = 10):
    """
    Performs feature selection given datafile
    """
    #Get Data Handler
    path = config.path("..","data",d.datafile)
    
    #Parsing features
    cat_tags, cont_tags, cost_tags = extract_features(d, featureTags, costTags)

    #Get feature and target data
    data = load_data(d)

    cont, newCats = ff.formatContinuous(data = data[:,cont_tags], d = d)
    cat = ff.one_hot(data = np.hstack((data[:,cat_tags].astype("int"), newCats)))
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
        model = config.get(config.path(path,"models", "model_%s.p" % costTag), create_model , x_train = x_train_, y_train = y_train[:,target], trees = trees, catTags = , contTags = )
     
        #Sorting and Writing Important Features
        writeFeatures(costFeature = costIndex, importance = model.feature_importances_, d = d)
        
        predictions = model.predict(x_test_)
        
        # accuracy = model_score(model, x_train_, y_train[:,target])
        accuracy = score(predictions, y_test[:,target])


        # config.write(config.path("..","data",d.datafile, "models", "%s_accuracy.txt" % costTag), accuracy_)
        results = config.path("..","data",d.datafile,"models", "results.txt")
        print "Results saved in %s" % results
        with open(results, 'a') as f:
            f.write("Model accuracy for cost:%s%saccuracy:%.2f\n" % (costTag, (30 - len(costTag)) * " ", accuracy))

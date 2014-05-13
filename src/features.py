#Python Modules
import numpy as np
from sklearn.preprocessing import OneHotEncoder as Sparse
#Local Modules
from wrappers import debug
import config

@debug
def writeFeatures(costFeature, datafile, importance , tags):
    """
    Writes feature importances to file in order of importance
    Saves to pickle file for use in future modelling

    Takes in costFeature index of d.tags
    Takes in the model

    Returns the costFeature, Sorted list of feature indices based on importance
    """
    sortedFeatures = sorted(zip(tags, list(importance)) ,  key = (lambda x:-x[1]))
    with open(config.path("..","data",datafile,"features",  "importances", "%s.txt" % (costFeature)),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (feature, importance)
            f.write(write.replace("#", (24 - len(write)) * " "))
    return sortedFeatures

@debug
def parse_features(d, inputs):
    """
    Parsing features from input arguments to a list of tag names
    """
    tags = []
    for tag in inputs:
        if len(tag.strip()) == 1:
            for tag in d.titleMap[tag.strip().upper()][1]:                
                if tag in d.tags:
                    tags.append(d.tags.index(tag))
                else:
                    print "Feature Selection Warning: feature %s not found %s (will be ignored)" % (tag, d.datafile)
        else:
            if tag in d.tags:
                tags.append(d.tags.index(tag))

    return tags

@debug
def extract_features(d, featureTags, costTags):
    """
    Extracts Features based on inputted features
    """
    if costTags[0] == "":
        cost_tags = d.costs
    else:
        cost_tags = parse_features(d, costTags)
        if len(cost_tags) == 0:
            print "WARNING:: Cost tags inputted cannot be found!"
            return 

    if featureTags[0] == "": return d.categorical, d.continuous + [tag for tag in d.costs if tag not in cost_tags], cost_tags

    cat_tags = []
    cont_tags = []
    feature_tags = parse_features(d, featureTags)
    
    if len(feature_tags) == 0:
        print "WARNING::Feature tags inputted cannot be found!"
        return
    for tag in feature_tags:
        if tag in d.categorical:
            cat_tags.append(tag)
        elif tag in d.continuous or tag in d.costs:
            cont_tags.append(tag)

    return cat_tags, cont_tags, cost_tags


@debug
def one_hot(data, d):
    """
    Performs binary vectorization of categorical data for non-decision tree models
    Returns one_hotted data
    """
    d.catMapper = {"0":0, "NAN":0}
    for x in xrange(data.shape[0]):
        for y in xrange(data.shape[1]):
            str_val = str(data[x,y])
            if str_val not in d.catMapper:
                new = len(d.catMapper)
                d.catMapper[str_val] = new
                data[x,y] = new
            else:
                data[x,y] = d.catMapper[str_val]

    enc = Sparse(n_values = len(d.catMapper))
    # enc = Sparse()
    enc = enc.fit(data)
    train = enc.transform(data).toarray()
    return enc, train
    # return enc, data

@debug
def formatContinuous(d,data, mean = None):
    """
    Splits continuous data from categorical data (negative values)
    Returns the data with replaced negative values with mean

    TODO - return categorical section of continuous data as well
    """
    if len(data) == 0:
        return np.empty(data.shape)

    invalid = (data < 0)

    newCats = data.copy()
    newCats[np.invert(invalid)] = 0

    if mean == None:
        mean = np.sum(newCats, axis = 0)/np.sum(np.invert(invalid), axis = 0)
    cols = np.where(invalid)[1]
    data[invalid] = mean[cols]


    return data, newCats, mean
    # return data, np.empty(newCats.shape), mean
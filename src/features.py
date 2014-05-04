#Python Modules
import numpy as np
from sklearn.preprocessing import OneHotEncoder as Sparse
#Local Modules
from wrappers import debug
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
    with open(config.path("..","data",d.datafile,"features",  "importances", "%s.txt" % (costFeature)),'wb')as f:
        for feature, importance in sortedFeatures:
            write = "%s#%f\n" % (d.tags[feature], importance)
            f.write(write.replace("#", (24 - len(write)) * " "))

@debug
def parse_features(d, inputs):
    """
    Parsing features from input arguments to a list of tag names
    """
    import string
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
    cost_tags = parse_features(d, costTags)
    cost_tags = d.costs if len(cost_tags) == 0 else parse_features(d, costTags)

    cat_tags = []
    cont_tags = []
    feature_tags = parse_features(d, featureTags)
    if len(featureTags) == 0:
        return d.categorical, d.continuous + d.costs, cost_tags
    
    for tag in featureTags:
        if tag in d.categorical:
            cat_tags.append(tag)
        elif tag in d.continuous:
            cont_tags.append(tag)
    if len(cat_tags) == 0: cat_tags = d.categorical
    if len(cont_tags) == 0: cont_tags = d.continuous + d.costs

    return cat_tags, cont_tags, cost_tags


@debug
def one_hot(data, d):
    """
    Performs binary vectorization of categorical data for non-decision tree models
    Returns one_hotted data
    """
    enc = Sparse(n_values = len(d.catMapper))
    encoder = enc.fit(data)
    train = encoder.transform(data).toarray()
    return encoder, train

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

    for x in xrange(newCats.shape[0]):
        for y in xrange(newCats.shape[1]):
            str_val = str(newCats[x,y])
            if str_val not in d.catMapper:
                new = len(d.catMapper)
                d.catMapper[str_val] = new
                newCats[x,y] = new
            else:
                newCats[x,y] = d.catMapper[str_val]

    if mean == None:
        mean = np.sum(newCats, axis = 0)/np.sum(np.invert(invalid), axis = 0)
    cols = np.where(invalid)[1]
    data[invalid] = mean[cols]


    return data, newCats, mean
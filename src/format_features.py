#Python Modules
import numpy as np
from sklearn.preprocessing import OneHotEncoder as Sparse
#Local Modules
from wrappers import debug
import config
@debug
def one_hot(data):
    """
    Performs binary vectorization of categorical data for non-decision tree models
    Returns one_hotted data
    """
    enc = Sparse()
    import sys
    original = sys.stdout
    sys.stdout = open("file.txt",'wb')
    for line in data:
        print line
    train = enc.fit_transform(data).toarray()
    sys.stdout = original
    return train

@debug
def formatContinuous(d,data):
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
    cat_cols = np.unique((np.where(newCats != 0)[1]))
    newCats = newCats[:,cat_cols]
    for x in xrange(newCats.shape[0]):
        for y in xrange(newCats.shape[1]):
            str_val = str(newCats[x,y])
            if str_val not in d.catMapper:
                new = len(d.catMapper)
                d.catMapper[str_val] = new
                newCats[x,y] = new
            else:
                newCats[x,y] = d.catMapper[str_val]

    mean = np.sum(data, axis = 0)/np.sum(np.invert(invalid), axis = 0)
    cols = np.where(invalid)[1]
    data[invalid] = mean[cols]


    return data, newCats

@debug
def getCosts(data, costs):
    """
    Returns cost data.
    """
    return data[:,costs]

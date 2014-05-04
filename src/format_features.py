#Python Modules
import numpy as np
from sklearn.preprocessing import OneHotEncoder as Sparse
#Local Modules
from wrappers import debug
import config
@debug
def one_hot(data, datafile):
    """
    Performs binary vectorization of categorical data for non-decision tree models
    Returns one_hotted data
    """
    enc = Sparse()
    encoder = enc.fit(data)
    config.save(config.path("..","data",datafile, "encoder.p"), encoder)
    train = encoder.transform(data).toarray()
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

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
def formatContinuous(data):
    """
    Splits continuous data from categorical data (negative values)
    Returns the data with replaced negative values with mean

    TODO - return categorical section of continuous data as well
    """
    if len(data) == 0:
        return np.empty(data.shape[0])
    newData = (data.copy() * -1).astype("int")
    invalid = data < 0
    
    newData[np.invert(invalid)] = 0

    # data[invalid] = 0
    # mean = np.sum(data, axis = 0)/np.sum(np.invert(invalid), axis = 0)
    # cols = np.where(invalid)[1]
    # data[invalid] = mean[cols]

    # tags = list()
    # for index in cols:
    #     if index not in tags:
    #         tags.append(index)
    return newData#, results, tags

@debug
def getCosts(data, costs):
    """
    Returns cost data.
    """
    return data[:,costs]

#Python Modules
import numpy as np

#Local Modules
from wrappers import debug

@debug 
def formatNonNumerical(catData):
    """
    Formats nonumerical data found in categorical data
    Returns new categorical data with refitted values
    """
    cats = {}
    counter = 0
    for i in xrange(catData.shape[0]):
        for j in xrange(catData.shape[1]):
            if catData[i,j] not in cats:
                cats[str(catData[i,j])] = counter
                counter+= 1
            catData[i,j] = cats[str(catData[i,j])]
    return catData

@debug
def one_hot(data):
    """
    Performs binary vectorization of categorical data for non-decision tree models
    Returns one_hotted data
    """
    result = np.zeros((data.shape[0],data.shape[1], np.unique(data).shape[0]))
    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            result[i][j][data[i][j]] = 1
    return result

@debug
def splitContinuous(data):
    """
    Splits continuous data from categorical data (negative values)
    Returns the data with replaced negative values with mean

    TODO - return categorical section of continuous data as well
    """
    if len(data) == 0:
        return np.empty(data.shape[0])
    # newData = (data.copy() * -1).astype("int")
    invalid = data < 0
    
    # newData[np.invert(invalid)] = 0
    # results= one_hot(newData)

    data[invalid] = 0
    mean = np.sum(data, axis = 0)/np.sum(np.invert(invalid), axis = 0)
    cols = np.where(invalid)[1]
    data[invalid] = mean[cols]

    # tags = list()
    # for index in cols:
    #     if index not in tags:
    #         tags.append(index)
    return data#, results, tags

@debug
def getCosts(data, costs):
    """
    Returns cost data.
    """
    return data[:,costs]

#Python Modules
import pandas as p
import numpy as np
#Local Modules
from wrappers import debug
import data as dc
import config
from lookup import getValuesCategories


@debug
def filterPanda(panda):
    def nonNumerical(data):
        newTags = data.copy() * -1
        invalid = data < 0
        
        newTags[np.invert(invalid)] = 0
        result = np.zeros((newTags.shape[0],newTags.shape[1],np.max(newTags) + 1))
        for i in xrange(newTags.shape[0]):
            for j in xrange(newTags.shape[1]):
                result[i][j][newTags[i][j]] = 1

        data[invalid] = 0
        mean = np.sum(data, axis = 0)/np.sum(np.invert(invalid), axis = 0)
        data[invalid] = mean[np.where(invalid)[1]]
        return data, newTags
    names = np.array(panda.columns.values)[list(set(np.where(panda.values<0)[1]))]
    data, newData = nonNumerical(panda[names].as_matrix().astype("float")) 
    for i in xrange(len(names)):
        panda[names[i] + "NEGS"] = newData[:,i]
        panda[names[i]] = data[:,i]
    return panda

@debug
def determineType(panda):
    pass

@debug
def main():
    d = dc.Data(datafile)
    panda = p.read_csv(path)._get_numeric_data()

    columns = panda.columns.values
    data = panda.values.astype("float")
    del panda

    print columns
    print data
    

    return 0


if __name__ == "__main__":
    datafile = "H147"
    path = config.path("..","data",datafile,"%s.csv" % datafile.lower())
    main()
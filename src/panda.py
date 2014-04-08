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
def getRawData(npPath, colPath):
    if config.os.path.exists(npPath):
        data = np.load(npPath)
        columns = np.load(colPath)
    else:
        panda = p.read_csv(path)._get_numeric_data()
        columns = np.array(panda.columns.values)
        data = panda.values.astype("float")
        np.save(npPath, data)
        np.save(colPath, columns)
        del panda

@debug
def clean(*args):
    import os
    path = config.path("..","data",datafile)
    if not os.path.exists(path): return
    for cfile in os.listdir(path):
        if sum([arg in cfile for arg in args]) > 0:
            filepath = config.path(path, cfile)
            os.chmod(filepath, 0777)
            os.remove(filepath)
            print "Cleaning %s" % filepath

@debug
def main():
    npPath = config.path("..","data", datafile, "panda_data.npy")
    colPath = config.path('..',"data", datafile, "panda_col.npy")

    if not config.os.path.exists(config.path("..","data", datafile, "panda_data.npy")):
        getRawData(npPath, colPath)

    data = np.load(npPath)
    columns = np.load(colPath)

    d.categorical
    d.continuous
    d.costs
    # print "\n".join([d.features[tag][1] for tag in d.costs])
    

    return 0


if __name__ == "__main__":
    datafile = "H147"
    # Clean Past Data
    clean(\
        # "codebook",\
        # "model",\
        # "csv",\
        # "costs",\
        # "panda",\
        # "feature",\
        # "filtered_panda",\
        )
    d = dc.Data(datafile)
    path = config.path("..","data",datafile,"%s.csv" % datafile.lower())
    main()
#Python Modules
import matplotlib.pyplot as plt
import pickle as p
from os import listdir
from scipy import stats
import numpy as np

#Local Modules
from wrappers import debug
import config
import data_helper as dc
import model


def correlationGraph(target, inputFeature, featureName):
    plt.clf()
    plt.plot(inputFeature, target, "ro")
    plt.axis([0,np.max(inputFeature),0,100000])
    plt.savefig(config.path("..", "visual", datafile, cost + "_" + featureName + ".png"))

def normalCorrGraph(target, inputFeature, featureName):
    plt.clf()
    normalTarget = target/target.max()
    if inputFeature.max() == 0:
        normalFeature = inputFeature
    else:
        normalFeature = inputFeature/inputFeature.max()
    plt.plot(normalFeature, normalTarget, "ro")
    plt.savefig(config.path("..", "visual", datafile, "normal" + cost + "_" + featureName + ".png"))

def CDF(panda, feature):
    data = panda[feature].as_matrix().astype('float')
    data /= np.linalg.norm(data)

    plt.clf()
    plt.plot(data)
    plt.savefig(path("..","visual",datafile, "CDF_%s.png" % feature))

def PMF(panda, feature):
    data = panda[feature].as_matrix().astype("float")

    plt.clf()
    plt.plot(stats.rv_discrete.pmf(data))
    plt.savefig(path("..","visual", datafile, "PMF_%s.png") % feature)


def clean():
    from shutil import rmtree
    path = config.path("..","visual",datafile)
    if config.os.path.exists(path):
        rmtree(path)

if __name__ == "__main__":
    import sys
    datafile =  sys.argv[1]
    clean()
    # Clean Past Data
    config.clean([\
        # "data",\
        # "features",\
        # "formatted",\
        ], datafile = datafile)
    d = dc.Data(datafile = datafile)
    d.printTargetTags()
    cost  = raw_input("Pick a cost\n")
    importance = 10
    model.loadData(datafile, cost, d, True)
    featureData = config.load(config.path("..", "data", datafile,  "features", "features" + cost + ".p"))
    for i, name in enumerate(featureData[0][:11]):
        correlationGraph(featureData[2], featureData[1][:,i], name)
        normalCorrGraph(featureData[2], featureData[1][:,i], name)
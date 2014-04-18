import matplotlib.pyplot as plt
import pickle as p
import config
from wrappers import debug
from os import listdir
from scipy import stats



def correlationGraph(target, inputFeature, featureName):
    plt.clf()
    plt.plot(inputFeature, target, "ro")
    plt.savefig(config.path("..", "visual", dataFile, cost + "_" + featureName + ".png"))

def normalCorrGraph(target, inputFeature, featureName):
    plt.clf()
    normalTarget = target/target.max()
    if inputFeature.max() == 0:
        normalFeature = inputFeature
    else:
        normalFeature = inputFeature/inputFeature.max()
    plt.plot(normalFeature, normalTarget, "ro")
    plt.savefig(config.path("..", "visual", dataFile, "normal" + cost + "_" + featureName + ".png"))

def CDF(panda, feature):
    data = panda[feature].as_matrix().astype('float')
    data /= np.linalg.norm(data)

    plt.clf()
    plt.plot(data)
    plt.savefig(path("..","visual",dataFile, "CDF_%s.png" % feature))

def PMF(panda, feature):
    data = panda[feature].as_matrix().astype("float")

    plt.clf()
    plt.plot(stats.rv_discrete.pmf(data))
    plt.savefig(path("..","visual", dataFile, "PMF_%s.png") % feature)


def clean():
    from shutil import rmtree
    rmtree(path("..","visual",dataFile))

if __name__ == "__main__":
    dataFile = "H144D"
    cost  = "IPFTC11X"
    myPath = config.path("..", "data", dataFile,  "features", "features" + cost + ".p")
    featureData = config.load(myPath)
    for i, name in enumerate(featureData[0][:11]):
        correlationGraph(featureData[2], featureData[1][:,i], name)
        normalCorrGraph(featureData[2], featureData[1][:,i], name)
        # CDF(raw_panda, feature)
        # PMF(raw_panda, feature)       


    # for feature in features_to_plot:
    #     correlationGraph(feature, cost_feature)
    #     CDF(raw_panda, feature)
    #     PMF(raw_panda, feature)


    # for fileName in listdir(pathD):
    #     if "feature_importance" in  fileName:
    #         with open(path(pathD, fileName), 'rb') as f:
    #             for i,line in enumerate(f):
    #                 if i == 10:
    #                     break
    #                 correlationGraph(fileName[19:-4], line.split()[0])

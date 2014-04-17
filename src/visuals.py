import matplotlib.pyplot as plt
import pickle as p
from config import path
from wrappers import debug
from os import listdir
from scipy import stats


@debug
def correlationGraph(target, inputFeature):
    plt.clf()
    plt.plot(raw_panda[inputFeature], raw_panda[target], "ro")
    plt.savefig(path("..", "visual", dataFile, target + "_" + inputFeature + ".png"))

@debug
def normalCorrGraph(target, inputFeature):
    plt.clf()
    normalTarget = raw_panda[target]/raw_panda[target].max()
    normalFeature = raw_panda[inputFeature]/raw_panda[inputFeature].max()
    plt.plot(normalFeature, normalTarget, "ro")
    plt.savefig(path("..", "visual", dataFile, "normal" + target + "_" + inputFeature + ".png"))

@debug
def CDF(panda, feature):
    data = panda[feature].as_matrix().astype('float')
    data /= np.linalg.norm(data)

    plt.clf()
    plt.plot(data)
    plt.savefig(path("..","visual",dataFile, "CDF_%s.png" % feature))

@debug
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
    pathD = path("..", "data", dataFile)
    clean()
    raw_panda = p.load(open(path(pathD, "filtered_panda.p"), 'rb'))
    features_to_plot = ["RXSLF11" ,"IPTSLF11","IPFSLF11","HHNSLF11","DVTSLF11","HHNEXP11","HHNTCH11","OBVSLF11","OBDSLF11","DVGSLF11"]
    cost_feature = "TOTSLF11"

    for feature in features_to_plot:
        correlationGraph(feature, cost_feature)
        CDF(raw_panda, feature)
        PMF(raw_panda, feature)


    # for fileName in listdir(pathD):
    #     if "feature_importance" in  fileName:
    #         with open(path(pathD, fileName), 'rb') as f:
    #             for i,line in enumerate(f):
    #                 if i == 10:
    #                     break
    #                 correlationGraph(fileName[19:-4], line.split()[0])

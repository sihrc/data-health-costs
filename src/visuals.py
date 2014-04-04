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

def CDF(panda, feature):
    data = panda[feature].as_matrix.astype('float')
    data /= np.linalg.norm(data)

    plt.clf()
    plt.plot(data)
    plt.savefig(path("..","visual",dataFile, "CDF_%s.png" % feature))

def PMF(panda, feature):
    data = panda[feature].as_matrix.astype("float")

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
    # for fileName in listdir(pathD):
    #     if "feature_importance" in  fileName:
    #         with open(path(pathD, fileName), 'rb') as f:
    #             for i,line in enumerate(f):
    #                 if i == 10:
    #                     break
    #                 correlationGraph(fileName[19:-4], line.split()[0])
    features_to_plot = []
    cost_features = []
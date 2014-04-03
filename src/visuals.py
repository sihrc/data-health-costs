import matplotlib.pyplot as plt
import pickle as p
from config import path
from wrappers import debug
from os import listdir


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
def clean():
    from shutil import rmtree
    rmtree(path("..","visual",dataFile))

if __name__ == "__main__":
    dataFile = "H144D"
    pathD = path("..", "data", dataFile)
    clean()
    raw_panda = p.load(open(path(pathD, "filtered_panda.p"), 'rb'))
    for fileName in listdir(pathD):
        if "feature_importance" in  fileName:
            with open(path(pathD, fileName), 'rb') as f:
                for i,line in enumerate(f):
                    if i == 10:
                        break
                    correlationGraph(fileName[19:-4], line.split()[0])
                    normalCorrGraph(fileName[19:-4], line.split()[0])
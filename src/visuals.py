import matplotlib.pyplot as plt
# import pickle as p
import pandas as p
from config import path
from wrappers import debug
from os import listdir
from scipy import stats
import numpy as np
import thinkplot as tp
import thinkstats2 as ts2

@debug
def correlationGraph(target, inputFeature):
    plt.clf()
    plt.plot(raw_panda[inputFeature], raw_panda[target], "ro")
    plt.xlabel(inputFeature)
    plt.ylabel(target)
    plt.savefig(path("..", "visual", dataFile, target + "_" + inputFeature + ".png"))

@debug
def normalCorrGraph(target, inputFeature):
    plt.clf()
    normalTarget = raw_panda[target]/raw_panda[target].max()
    normalFeature = raw_panda[inputFeature]/raw_panda[inputFeature].max()
    plt.xlabel(inputFeature)
    plt.ylabel(target)
    plt.plot(normalFeature, normalTarget, "ro")
    plt.savefig(path("..", "visual", dataFile, "normal" + target + "_" + inputFeature + ".png"))

@debug    
def BinData(data, low, high, n):
    """Rounds data off into bins.

    data: sequence of numbers
    low: low value
    high: high value
    n: number of bins

    returns: sequence of numbers
    """
    bins = np.linspace(low, high, n)
    data = (np.array(data) - low) / (high - low) * n
    data = np.round(data) * (high - low) / n + low
    return data

@debug
def CDF(panda, feature):
    data = panda[feature].values.astype('float')
    # data /= np.linalg.norm(data)
    cdf = ts2.MakeCdfFromList(data)

    plt.clf()
    tp.Cdf(cdf)
    tp.Config(title='CDF')
    plt.savefig(path("..","visual",dataFile, "CDF_%s.png" % feature))

@debug
def PMF(panda, feature):
    data = panda[feature].values.astype("float")

    pmf = ts2.MakePmfFromList(data)

    pdf = ts2.EstimatedPdf(data)
    low, high = min(data), max(data)
    xs = np.linspace(low, high, 101)
    kde_pmf = pdf.MakePmf(xs)

    bin_data = BinData(data, low, high, 51)
    bin_pmf = ts2.MakePmfFromList(bin_data)

    plt.clf()
    tp.SubPlot(3, 1, 1)
    tp.Hist(pmf, width=0.1)
    tp.Config(title='Naive Pmf')

    tp.SubPlot(3, 1, 2)
    tp.Hist(bin_pmf)
    tp.Config(title='Binned Hist')

    tp.SubPlot(3, 1, 3)
    tp.Pmf(kde_pmf)
    tp.Config(title='KDE PDF')

    plt.savefig(path("..","visual", dataFile, "PMF_%s.png") % feature)

@debug
def clean():
    from shutil import rmtree
    rmtree(path("..","visual",dataFile))

if __name__ == "__main__":
    dataFile = "H147"
    pathD = path("..", "data", dataFile)
    # raw_panda = p.load(open(path(pathD, "filtered_panda.p"), 'rb'))
    raw_panda = p.read_csv(path(pathD, dataFile.lower() + ".csv"))
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

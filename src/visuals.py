"""
Contains visualization data scripts
"""

#To-DO Create a Visuals module that holds all the visualization TASKS
import matplotlib.pyplot as plt
from stats import *
import numpy as np

def FeatureVsCost(data, var):
		try:
			new_data = data.getColumn(var)
			plt.scatter(new_data, data.cost)
			print "Plotting " + var + " vs cost plot"
			plt.xlabel(data.lookUp(var = var)[0])
			plt.ylabel("Cost in dollars")
			plt.savefig("../visuals/feature_v_cost/" + data.lookUp(var = var)[0].replace(" ", "_") + ".png")
		except:
			print "Plotting " + var + " failed"

def AllFeatureVsCost(data):
	for i in range (len(data.features)):
		FeatureVsCost(data,"V" + str(i))

def GraphCostPmf(subCost):
	pmf = ts2.MakePmfFromList(subCost)
	cdf = ts2.MakeCdfFromPmf(pmf)

	new_dats = ts2.BinData(subCost, min(subCost), max(subCost), 100)
	bin_pmf = ts2.MakePmfFromList(list(new_dats))

	pdf = thinkstats2.EstimatedPdf(subCost)
	xs = np.linspace(min(subCost), max(subCost), 101)
	kde_pmf = pdf.MakePmf(xs)

	tp.SubPlot(2, 2, 1)
	tp.Hist(pmf, width=0.1)
	tp.Config(title='Naive Pmf')

	tp.SubPlot(2, 2, 2)
	tp.Hist(bin_pmf)
	tp.Config(title='Binned Hist')

	tp.SubPlot(2, 2, 3)
	tp.Pmf(kde_pmf)
	tp.Config(title='KDE PDF')

	tp.SubPlot(2, 2, 4)
	tp.Cdf(cdf)
	tp.Config(title='CDF')

	tp.Show()

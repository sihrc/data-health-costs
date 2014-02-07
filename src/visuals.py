"""
Contains visualization data scripts
"""

#To-DO Create a Visuals module that holds all the visualization TASKS
import matplotlib.pyplot as plt
from stats import *
import numpy as np

def FeatureVsCost(data, cost, var):
		try:
			data = data.getColumn(var)
			plt.scatter(data, cost)
			print "Plotting " + var + " vs cost plot"
			plt.xlabel(data.lookUp(var = var)[0])
			plt.ylabel("Cost in dollars")
			plt.savefig("../visuals/feature_v_cost/" + data.lookUp(var = var)[0].replace(" ", "_") + ".png")
		except:
			print "Plotting " + var + " failed"

def AllFeatureVsCost(data):
	for i in range (len(data.features)):
		try:
			FeatureVsCost("V" + str(i))
		except:
			print "Plotting " + str(i) + " failed"

def GraphCostPmf(d):
	pmf = ts2.MakePmfFromList(d.cost)
	cdf = ts2.MakeCdfFromPmf(pmf)

	new_dats = ts2.BinData(d.cost, min(d.cost), max(d.cost), 100)
	bin_pmf = ts2.MakePmfFromList(list(new_dats))

	pdf = thinkstats2.EstimatedPdf(d.cost)
	xs = np.linspace(min(d.cost), max(d.cost), 101)
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

"""
Contains visualization data scripts
"""

#To-DO Create a Visuals module that holds all the visualization TASKS
import matplotlib.pyplot as plt
from stats import *

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

def GraphCostPmf(cost):
	new_dats = ts2.BinData(cost, min(list(cost)), max(list(cost)), 100)
	pmf = ts2.MakePmfFromList(list(cost))
	print pmf.d
	cdf = ts2.MakeCdfFromPmf(pmf)
	#pmf = ts2.MakePmfFromList(cost)
	tp.Hist(pmf)
	#tp.Clf()
	#tp.Cdf(cdf)
	tp.Show(title='PMF of Cost',
               xlabel='Money (Dollars)',
               ylabel='probability')

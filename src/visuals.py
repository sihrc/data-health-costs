"""
Contains visualization data scripts

author: jazmin
"""

#To-DO Create a Visuals module that holds all the visualization TASKS
import matplotlib.pyplot as plt
from stats import *
import numpy as np
import os
import re

#Debug Timer Wrappers
from wrappers import debug

@debug
def FeatureVsCost(d, data, tag):
		try:
			new_data = data.getColumn(tag) #gets the data
			plt.scatter(new_data, data.cost) #creates a scatterplot of the data vs the cost
			print "Plotting " + tag + " vs cost plot"
			plt.xlabel(data.lookUp(tag = tag)[0]) #labels the x axis
			plt.ylabel("Cost in dollars")
			plt.savefig("../visuals/feature_v_cost/" + data.lookUp(tag = tag)[0].replace(" ", "_") + ".png") #saves the scatter plot
		except:
			d.ignored.append(tag)

@debug
def AllFeatureVsCost(data):
	for tag in data.features:
		FeatureVsCost(data, tag) #runs featurevscost for all features

@debug
def GraphPmf(data, save, bins, show = True):
	if len(set(data)) == 1: #makes sure there's enough data to graph
		print "Only one Bin Found"
		return	
	
	pmf = ts2.MakePmfFromList(data)

	new_dats = ts2.BinData(data, min(data), max(data), bins)
	bin_pmf = ts2.MakePmfFromList(list(new_dats))

	tp.SubPlot(2, 1, 1)
	tp.Hist(pmf) #makes a histogram from pmf
	tp.Config(title='Naive Pmf')

	tp.SubPlot(2, 1, 2)
	tp.Hist(bin_pmf) #makes a binned histogram from pmf
	tp.Config(title='Binned Hist')

	if show:
		tp.Show()
	# tp.Save(filename = save, formats = "png")
	tp.Save(filename = save)
	tp.Clf()

def GraphCdf(data, name, show = False):
	pmf = ts2.MakePmfFromList(data) #makes pmf from data
	cdf = ts2.MakeCdfFromPmf(pmf) #makes cdf from the pdf
	tp.Cdf(cdf, label = name) #plots the cdf
	tp.Config(title='CDF')
	if show:	
		tp.Show()

def GraphPdf(data, show = False):
	pdf = thinkstats2.EstimatedPdf(data)
	xs = np.linspace(min(data), max(data), 101)
	kde_pmf = pdf.MakePmf(xs)
	tp.Pmf(kde_pmf)
	tp.Config(title='KDE PMF')
	if show:
		tp.Show()

def GetCostForBinnedFeature(d, data, tag):
	for low,high,data in data[1:]:
		ranges = "_" + str(low) + "-" + str(high)
		name = d.lookUp(tag = tag)[0]
		name = re.sub(r'([^\s\w]|_)+', '', name).replace(" ","_") #only retains alphanumeric characters and whitespace
		#name.replace(" ","_").replace(":","").replace("/","") 
		if len(data) <= 2: #if the data doesn't have multiple data points
			d.ignored.append((d.datafile,(name, ranges)))
			continue
		path = os.path.join("..","visuals","feature_bin_costs",d.datafile[:-4])
		if not os.path.exists(path):
			os.makedirs(path)
		#GraphPmf(data, False)
		GraphCdf(data, str(low)) #creates cdf
	tp.Save(filename = os.path.join(path, name + ".jpg"))
	tp.Clf()
	return d

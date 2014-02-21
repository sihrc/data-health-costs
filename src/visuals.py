"""
Contains visualization data scripts
"""

#To-DO Create a Visuals module that holds all the visualization TASKS
import matplotlib.pyplot as plt
import numpy as np
import re,os

#Local Modules
import analyze as an
import config
from stats import *

#Debug Timer Wrappers
from wrappers import debug

@debug
def FeatureVsCost(d, tag):
	"""
	FeatureVsCost 
	Takes in the data manager object and a feature tag.
	Returns a visual of the scatter plot between feature and cost

	author: chris
	"""
	try:
		new_data = data.getColumn(tag) #gets the data
		plt.scatter(new_data, data.cost) #creates a scatterplot of the data vs the cost
		print "Plotting " + tag + " vs cost plot"
		plt.xlabel(data.lookUp(tag = tag)[0]) #labels the x axis
		plt.ylabel("Cost in dollars")
		plt.savefig("../visuals/feature_v_cost/" + data.lookUp(tag = tag)[0].replace(" ", "_") + ".png") #saves the scatter plot
	except:
		d.ignored.append(tag, data.getColumn(tag))

@debug
def GraphPmf(data, save, bins, show = True):
	"""
	Given the a numpy array, a filepath to save, the number of bins to create, and whether or not to display the PMF
	Returns a saved PMF plot

	author: Jazmin
	"""
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

def GraphCdf(data, name):
	"""
	Given a numpy array, a legend label for the graph
	Plots a CDF plot

	author: Jazmin
	"""
	pmf = ts2.MakePmfFromList(data) #makes pmf from data
	cdf = ts2.MakeCdfFromPmf(pmf) #makes cdf from the pdf
	tp.Cdf(cdf,label = name) #plots the cdf

def GraphPdf(data, name):
	"""
	Given numpy array, plots a PDF graph
	author: Jazmin/Chris
	"""
	pdf = thinkstats2.EstimatedPdf(data)
	xs = np.linspace(min(data), max(data), 101)
	kde_pmf = pdf.MakePmf(xs)
	tp.Pmf(kde_pmf, label = name)

def GetCostForBinnedFeature(d, data, tag):
	"""
	Inputs:
		Cost: Cost for binned Feature Data (low,high,actualData)
		d: data object
		tag: feature tag
	Outputs:
		d: modified data object
	"""
	for low,high,data in data: #Grab the split ranges in data
		data = an.reject_outliers(data)
		if len(data) <= 2: #if the data doesn't have multiple data points
			d.ignored.append((d.datafile,(tag, str(low,high))))
			continue
		GraphCdf(data, str(low)) #creates cdf
	path = config.makedirs("..","visuals","feature_bin_costs",d.datafile[:-4], tag + ".jpg")
	tp.Config(title = tag)
	tp.Save(filename = path)
	tp.Clf()
	return d

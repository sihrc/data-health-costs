"""
Contains data holder class
author:chris
"""
#Local Modules
import config
import lookup
from wrappers import debug

#Python Modules
from os import path as os
from re import search

class Data():
	"""
	Data Handler object that has methods for handling references 
	for our variables, such as looking up variables,
	getting data for features as well as loading data, 
	saving and loading temporary sessions
	"""
	@debug
	def __init__ (self, datafile = ""):
		self.datafile = datafile
		self.codebook, self.lookup, self.costs, self.tags = config.get(config.path("..","data",datafile,"codebook.p"), self.downloadCodebook)
		self.costs = config.get(config.path("..","data",datafile,"target_costs.p"), self.filterTargetCosts)
		self.csv = config.get(config.path("..","data",datafile,"csv.p"), self.downloadData)

	@debug
	def downloadCodebook(self):
		"""
		Given the datafile name, returns the codebook needed
		author: chris
		"""
		import urllib2, unicodedata
		from bs4 import BeautifulSoup

		page = urllib2.urlopen(config.datafiles[self.datafile][-1])
		soup = BeautifulSoup(page.read())

		tags = []
		codebook = []
		lookup = {}
		costs = []

		for found in soup.find_all("tr",{"id":"faqRoll_neoTD3"}):
			text = unicodedata.normalize('NFKD',found.text).encode("ascii",'ignore')
			details = text.strip().replace("   ","").split("\n")
			codebook.append((int(details[1]), int(details[2])))
			tags.append(details[0])
			lookup[details[0]] = details[3]
			if sum([type(search("\W+%s[\WS]+" % x, details[3])) != type(None) for x in ["PAYMENT", "COST", "CHG", "CHARGE", "FEE", "EXP", "EXPENSE", "PD","PAID"]]) > 0:
				costs.append(details[0])
 		return codebook, lookup, costs, tags

	@debug
	def downloadData(self):
		"""
		Download data
		"""
		def download(self):
			import zipfile
			import urllib
			dfile = config.path("..","data",self.datafile.upper() + ".zip")
			urllib.urlretrieve(config.download % self.datafile.lower(), dfile)
			with zipfile.ZipFile(dfile) as zf:
				zf.extractall(config.path("..","data",self.datafile.upper()))

		import pandas as pd

		path = config.path("..","data",self.datafile, self.datafile.lower())

		if not os.exists(path + ".dat"):	download(self)

		printFormat = "".join(["%s" * (high - low + 1) + "," for low,high in self.codebook])[:-1]
		with open(path+".csv", 'wb') as g:
			g.write(",".join(self.tags) + "\n")
			with open(path + ".dat", 'rb') as f:
				for line in f:
					g.write(printFormat % tuple(line.strip()) + "\n")
		return path + ".csv"

	@debug
	def filterTargetCosts(self):
		"""
		Get target cost features from data set
		author: chris
		"""
		costFeatures = []
		for i,feature in enumerate(self.costs):
			values = lookup.getValues(self.datafile, feature)
			if "$" in values:
				print "Looking up values for %s %d of %d..." % (feature, i, len(self.costs))
				costFeatures.append(feature)
		print "\nFound %d cost features of %d potential cost features\n" % (len(costFeatures), len(self.costs))
		return costFeatures


	"""
	Class native methods
	"""
	def __repr__(self):
		return "Data Handler Object"

	def __str__(self):
		return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary\n\npandas data file at %s" % self.csv

if __name__ == "__main__":
	data = getData("H144D")
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
		self.codebook, self.lookup, self.tags = config.get(config.path("..","data",datafile,"codebook.p"), self.downloadCodebook)
		self.costs = config.get(config.path("..","data",datafile,"target_costs.p"), self.getTargetCosts)
		self.panda = config.get(config.path("..","data",datafile,"panda.p"), self.downloadData)

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

		for found in soup.find_all("tr",{"id":"faqRoll_neoTD3"}):
			text = unicodedata.normalize('NFKD',found.text).encode("ascii",'ignore')
			details = text.strip().replace("   ","").split("\n")
			codebook.append((int(details[1]), int(details[2])))
			tags.append(details[0])
			lookup[details[0]] = details[3]

 		return codebook, lookup, tags

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
	def getTargetCosts(self):
		"""
		Get target cost features from data set
		author: chris
		"""
		costFeatures = []
		for feature in self.tags:
			featureDetails = lookup.getDetails(self.datafile, feature)
			if sum([x in featureDetails["Description"].lower() for x in ["payment", "cost", "chg", "fee"]]) > 0:
				costFeatures.append(feature)
		return costFeatures


	"""
	Class native methods
	"""
	def __repr__(self):
		return "Data Handler Object"

	def __str__(self):
		return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary\n\npandas data file at %s" % self.panda

if __name__ == "__main__":
	data = getData("H144D")


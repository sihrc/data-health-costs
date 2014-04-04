"""
Data Acquisition 
author:chris
"""

import config
from wrappers import debug

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
		print self.downloadCodebook()

	@debug
	def downloadCodebook(self):
		"""
		Given the datafile name, returns the codebook needed
		author: chris
		"""
		import urllib2, unicodedata
		from bs4 import BeautifulSoup
		def download(path):
			page = urllib2.urlopen(config.codebook.format(self.datafile.lower())).read()
			with open(path, 'wb') as f:
				f.write(page)
			return page
		path = config.path("..","data",self.datafile,"codebook.txt")

		if not config.os.path.exists(path):
			page = download(path)
		else:
			with open(path, 'rb') as f:
				page = f.read()

		_input = page.find("INPUT STATEMENTS")
		_label = page[_input:].find("LABEL STATEMENTS")
		_value = page[_label:].find("VALUE STATEMENTS")

		indices = page[_input:_input + _label]
		desc = page[_input + _label:_input + _label + _value]
		values = page[_input + _label + _value:]

		# self.indices = []
		# for line in indices.split("\n")[3:]:
		# 	split = line.split()
		# 	self.indices.append(tag, index)	

		self.descriptions = []
		for line in desc.split("\n"):
			print line
			raw_input()

		return 		

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
	import sys
	data = Data("H147")


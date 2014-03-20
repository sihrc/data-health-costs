"""
Contains data holder class
author:chris
"""
#Local Modules
import numpy as np
import config
from wrappers import debug

#Python Modules
import os

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
		
		if not os.path.exists(path + ".dat"):	download(self)
		
		printFormat = "".join(["%s" * (high - low + 1) + "," for low,high in self.codebook])[:-1]
		with open(path+".csv", 'wb') as g:
			g.write(",".join(self.tags) + "\n")
			with open(path + ".dat", 'rb') as f:
				for line in f:
					g.write(printFormat % tuple(line.strip()))
		return path + ".csv"

	# @debug
	# def getTargetCosts(self):
	# 	"""
	# 	Get target cost features from data set
	# 	author: chris
	# 	"""
	# 	costFeatures = []
	# 	for feature in self.codebook:
	# 		featureDetails = L.getDetails(self.datafile, feature[0])
	# 		if  "$" in featureDetails["Values"]:
	# 			costFeatures.append(feature[0])
	# 	return costFeatures


	# @debug
	# def getColumn(self, tag):
	# 	"""
	# 	Gets the column of data given by tag
	# 	"""
	# 	ranges = self.lookUp(tag = tag)[1][1]
	# 	rawData = self.data[:,ranges[0] - 1:ranges[1]]
	# 	newFormat = np.zeros(shape = (rawData.shape[0]))
	# 	for i in range(len(rawData)):
	# 		try:
	# 			newFormat[i] = "".join(rawData[i]).strip()
	# 		except:
	# 			print "data is not a number"
	# 			break
	# 	return newFormat

	"""
	Class native methods
	"""
	def __repr__(self):
		return "Data Handler Object"

	def __str__(self):
		return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary\n\npandas data file at %s" % self.panda

def getData(datafile):
	return Data(datafile)


if __name__ == "__main__":
	data = getData("H144D")




"""
Contains data holder class
author:chris
"""
#Local Modules
import datasets
import numpy as np
import config
import lookup as L
from wrappers import debug

#Python Modules
import os
from bs4 import BeautifulSoup
from operator import itemgetter
import urllib2, urllib, zipfile

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
		self.codebook = config.get(config.path("..","data",datafile,"codebook.p"), self.downloadCodebook)
		self.featureIndices = dict([(tag[1],i) for i,tag in enumerate(sorted([(feature[1][1],feature[0]) for feature in self.codebook]))])
		self.data = config.get(config.path("..","data",datafile,"data.p"), self.downloadData)
		self.targetCosts = config.get(config.path("..","data",datafile,"targetCost.p"), self.getTargetCosts)

	@debug
	def downloadCodebook(self):
		"""
		Given the datafile name, returns the codebook needed
		author: chris
		"""
		page = urllib2.urlopen(config.datafiles[self.datafile][-1])
		soup = BeautifulSoup(page.read())
		details = []	
		tags = []

		found = soup.findAll('font', {'class':"smallBlack"})[3:]
		for i in xrange(0,len(found),3):
			low = found[i].text.encode('utf8').strip()
			low = int(repr(low)[1:repr(low).find("\\")])
			high = found[i + 1].text.encode('utf8').strip()
			high = int(repr(high)[1:repr(high).find("\\")])
			desc = found[i + 2].text.encode('utf8').strip()
			details.append((desc, (low,high)))

		for line in soup.findAll('a', href = True):
			if "download_data_files_codebook.jsp?" in line['href']:
				tags.append(line.text.encode('utf8').strip())

		return zip(tags[5:], details)

	@debug
	def downloadData(self):
		"""
		Download data
		"""
		def download(self):
			dfile = config.path("..","data",self.datafile.upper() + ".zip")
			urllib.urlretrieve(config.download % self.datafile.lower(), dfile)
			with zipfile.ZipFile(dfile) as zf:
				zf.extractall(config.path("..","data",self.datafile.upper()))

		path = config.path("..","data",self.datafile, self.datafile.lower() + ".dat")
		
		if not os.path.exists(path):
			download(self)

		data = []
		with open(path, 'rb') as f:
			for line in f:
				data.append(list(line.strip()))
		data = np.ma.array(data, mask = False)
		return data

	@debug
	def getTargetCosts(self):
		"""
		Get target cost features from data set
		author: chris
		"""
		costFeatures = []
		for feature in self.codebook:
			featureDetails = L.getDetails(self.datafile, feature[0])
			if  "$" in featureDetails["Values"]:
				costFeatures.append(feature[0])
		return costFeatures

	"""
	Class native methods
	"""
	def __repr__(self):
		return "Data Handler Object"

	def __str__(self):
		return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary"

def getData(datafile):
	def makeDataObject(datafile):
		return Data(datafile)
	return config.get(config.path("..","data",datafile,"object.p"), makeDataObject, datafile = datafile)


if __name__ == "__main__":
	import shutil
	shutil.rmtree(config.path("..","data"))
	data = getData("H144D")




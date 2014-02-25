"""
Contains data holder class
author:chris
"""
import pickle as p
import numpy as np
import config

#Debug Timer Wrappers
from wrappers import debug

class Data():
	"""
	Data Handler object that has methods for handling references 
	for our variables, such as looking up variables,
	getting data for features as well as loading data, 
	saving and loading temporary sessions
	"""
	@debug
	def __init__ (self, data = False, codebook = "", datafile = "", costId = "", timeTags = []):
		self.timeTags = timeTags
		self.datafile = datafile
		self.codebook = codebook
		self.createRefs()
		self.results = dict()
		self.ignored = []
		self.data = self.loadData(data)
		self.costId = costId
		self.cost = self.getColumn(self.costId)
		self.filterData()
		
	
	def filterData(self):
		applicable = np.where(self.cost > 0)
		self.data = self.data[applicable]
		self.cost = self.cost[applicable]

	
	def createRefs(self):
		"""
		Create Reference Dicts
		Feature - Tag:(Description, Index)
		"""
		count = 0
		self.features = dict()
		for key,item in self.codebook.iteritems():
			self.features[key.split()[0]] = [key, item]
			count += 1

	def lookUp(self, tag = None):
		"""
		Look up a feature using the tag name or a description
		returns acroynym-description, indices
		"""
		return self.features[tag]

	def loadData(self, data):
		"""
		Loads the Data Set from filename as numpy array
		"""
		if type(data) == bool:
			data = []
			with open(config.path("..","data",self.datafile, self.datafile + ".dat"), 'rb') as f:
				for line in f:
					data.append(list(line.strip()))
			data = np.array(data)
		return data
		

	def getColumn(self, tag):
		"""
		Gets the column of data given by tag
		"""
		ranges = self.lookUp(tag = tag)[1][1]
		rawData = self.data[:,ranges[0] - 1:ranges[1]]
		newFormat = np.zeros(shape = (rawData.shape[0]))
		for i in range(len(rawData)):
			try:
				newFormat[i] = "".join(rawData[i]).strip()
			except:
				print "data is not a number"
				break
		return newFormat

	def save(self, filename):
		with open(filename, 'wb') as f:
			p.dump(self, f)
			print filename + " Saved Successfully"
	
	def load(self, filename):
		"""
		Saves this object as a pickle file for access later
		"""
		with open(filename, 'rb') as f:
			self = p.load(f)
			print filename + " Loaded Successfully"

	"""
	Class native methods
	"""
	def __repr__(self):
		return "Data Handler Object"

	def __str__(self):
		return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary"

@debug
def getData(datafile):
	tags = config.datafiles[datafile]
	return Data(codebook = config.data[datafile][0], datafile = datafile, costId = tags[0] , timeTags = tags[1])

if __name__ == "__main__":
	d = getData("H144D")
	print d.getColumn("IPBEGMM")
	print "See Documentation"
	
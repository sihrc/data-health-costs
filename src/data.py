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
		self.tags = []
		self.indices = []
		self.costs = []
		self.descriptions = {}
		self.values = {} 

		self.parseCodebook()
		self.writeDataCSV()
		self.getCostFeatures()

	@debug
	def writeDataCSV(self):
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

		path = config.path("..","data",self.datafile, self.datafile.lower())

		if not config.os.path.exists(path + ".dat"):	download(self)
		if config.os.path.exists(path + ".csv"): return
		printFormat = "".join(["%s" * (high - low) + "," for low,high in zip(self.indices, self.indices[1:])])
		# print printFormat
		with open(path+".csv", 'wb') as g:
			g.write(",".join(self.tags) + "\n")
			with open(path + ".dat", 'rb') as f:
				format_ = printFormat + "%s" * (len(f.readline().strip()) - self.indices[-1] + 1)
				for line in f:
					g.write(format_ % tuple(line.strip()) + "\n")
		return

	@debug
	def getCostFeatures(self):
		"""
		Get target cost features from data set
		author: chris
		"""
		self.costs = []
		for feature in self.tags:
			if "$" in self.values[feature][-1]:
				if sum([type(search("\W+%s[\WS]+" % x, self.descriptions[feature])) != type(None) for x in ["PAYMENT", "COST", "CHG", "CHARGE", "FEE", "EXP", "EXPENSE", "PD","PAID"]]) > 0:		
					self.costs.append(feature)
		

	@debug
	def parseCodebook(self):
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

		_input  = page.find("* INPUT STATEMENTS;")
		_label  = page.find("* LABEL STATEMENTS;")
		_format = page.find("* FORMAT STATEMENTS;")
		_value  = page.find("* VALUE STATEMENTS;")

		indices = page[_input:_label]
		desc = page[_label:_format]
		mapping = page[_format: _value]
		values = page[_value:]

		for line in indices.split("\n")[3:]:
			if line.strip() == ";":
				break
			split = line.split()
			self.tags.append(split[-2].strip())
			self.indices.append(int(split[-3].strip()[1:]))
		
		for line in desc.split("\n")[1:]:
			if line.strip() == ";":
				break
			split = line.split("=")
			self.descriptions[split[0].strip().split()[-1]] = split[1].strip()
		
		mapper = {}
		for line in mapping.split("\n")[1:]:
			if line.strip() == ";":
				break
			split = line.split()
			mapper[split[-1].strip()[:-1]] = split[-2].strip()


		tag = ""
		value_list = []
		for line in values.split("\n")[1:]:
			if line.strip() == "":
				continue
			if "VALUE" in line[:6]:
				tag = mapper[line.split()[1].strip()]
				continue
			if "=" in line:
				split = line.split("=")
				value_list.append((split[0].strip(), split[1].strip()))
			if ";" == line.strip()[0]	:
				self.values[tag] = value_list
				value_list = []
				continue
		return
	
	"""
	Class native methods
	"""
	def __repr__(self):
		return "Data Handler Object"

	def __str__(self):
		return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary\n\npandas data file at [].csv"

if __name__ == "__main__":
	import sys
	data = Data("H147")


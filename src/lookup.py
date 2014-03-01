"""
Looks up Variables off the online MEPS database

author: chris @ sihrc
"""

import config
from bs4 import BeautifulSoup
import urllib2
import datasets as ds

def threeColumnString(line):
	"""
	Formats the table of values into 3 columns 
	"""
	colLengths = [[],[],[]]
	[[colLengths[i].append(len(cols[i])) for i in xrange(3)] for cols in line]
	maxLengths = [max(col) for col in colLengths]
	
	body = ["\t".join([(maxLengths[x] - len(cols[x])) * " " + cols[x] for x in xrange(3)]) for cols in line]
	return "\n".join(body[:-1]) + "\n\n" + body[-1]

def writeFeatureList(datafile):
	"""
	Function that creates a file that lists out all variable names 
	author: Jazmin @ JazminGonzalez-Rivero
	"""
	features = ds.getData(datafile)[0].keys()
	with open(config.path("..", "data", datafile, "features.txt"), "wb") as f:
		for feature in features:
			f.write(feature + "\n")

	

def getDetails(dataset, variable):
	"""
	Takes in the dataset filename and the variable name 
	Performs the HTTP GET Request and returns a list of decoded values
	"""

	url = "http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId=%s&varName=%s" % (dataset, variable)
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page.read())
	details = []
	for line in soup.findAll('font', {'class':"smallBlack"}):
		details.append(line.text.encode('utf8').strip())
	return [("Title", "\n".join(details[:3])), ("Name", details[4]), ("Description", details[6]), ("Format", details[8]), ("Type", details[10]), ("Range", details[12] + "~" + details[14]), ("Values", threeColumnString([details[n:n+3] for n in xrange(15,len(details),3)]))]


def print_variable(decoded):
	"""
	Format prints decoded values for getDetails
	"""
	for head,body in decoded:
		print head
		print "================================================="
		print body
		print "\n"	

if __name__ == "__main__":
	datafile = "H147"
	writeFeatureList(datafile)
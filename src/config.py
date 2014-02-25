"""
Config.py contains configuration data like constants
Also contains notes on the data sets

author: chris
"""
import os
import pickle as p
import urllib2

from wrappers import debug
from bs4 import BeautifulSoup


def path(*path):
	"""
	Replacement for os.path.join
	It performs makedirs on paths that don't exists
	Returns the os.path.join() result
	author:chris
	"""
	if len(path) == 0:
		return ""
		
	targetpath = os.path.join(*path)
	if "." in path[-1]:
		path = path[:-1]
	targetdirs = os.path.join(*path)
	
	if not os.path.exists(targetdirs):
		os.makedirs(targetdirs)
	return targetpath

@debug
def getCodebook(url):
	"""
	Given the datafile name, returns the codebook needed
	author: chris
	"""
	page = urllib2.urlopen(url)
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

	return dict(zip(tags[5:], details))

@debug
def saveCodebooks(datafile, codebook):
	"""
	Saves the codebook dictionary as a pickle
	author: chris
	"""
	with open(path("..","data",datafile,datafile + ".p"), 'wb') as f:
		p.dump(codebook, f)

@debug
def loadCodebooks(datafile):
	"""
	Loads pickled codebook
	author: chris
	"""
	with open(path("..","data",datafile,datafile + ".p"), 'rb') as f:
		d = p.load(f)
	return d

@debug
def getData(datafiles):
	"""
	Gets the data from pickled files for use in other scripts
	author: chris
	"""
	data = dict()
	for datafile, cost in datafiles:
		data[datafile] = (loadCodebooks(datafile),cost)
	return data


if __name__ == "__main__":
	datasets = {"H144D":"http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId=H144D", "H144A":"http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId=H144A", "H144E":"http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId=H144E", "H143":"http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId=H143"}
	for datafile, url in datasets.iteritems():
		saveCodebooks(datafile, getCodebook(url))
else:
	datafiles = [("H144D", "IPTC11X"), ("H144E","ERTC11X"),("H144A","RXMD11X"),("H143","RTHLTH13")]
	data = getData(datafiles)
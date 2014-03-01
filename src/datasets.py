"""
Datasets.py 
Handles downloading datasets and codebook

author:chris
"""

from wrappers import debug
import config

from bs4 import BeautifulSoup
import pickle as p
import urllib2, urllib
import os, zipfile


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
	with open(config.path("..","data",datafile,datafile + ".p"), 'wb') as f:
		p.dump(codebook, f)


@debug
def loadCodebooks(datafile):
	"""
	Loads pickled codebook
	author: chris
	"""
	with open(config.path("..","data",datafile,datafile + ".p"), 'rb') as f:
		d = p.load(f)
	return d

@debug
def downloadData(datafile):
	"""
	Download data
	"""
	dfile = config.path("..","data",datafile.upper(),  + ".zip")
	urllib.urlretrieve(config.download % datafile.lower(), dfile)
	with zipfile.ZipFile(dfile) as zf:
		zf.extractall(config.path("..","data",datafile.upper()))

@debug
def getData(datafile):
	"""
	Gets the data from pickled files for use in other scripts
	author: chris
	"""
	tags = config.datafiles[datafile]
	return loadCodebooks(datafile),tags[0], tags[1]

if __name__ == "__main__":
	for datafile, configs in config.datafiles.iteritems():
		if not os.path.exists(config.path("..","data",datafile.upper(), datafile + ".dat")):
			downloadData(datafile)
			saveCodebooks(datafile, getCodebook(configs[-1]))
"""Looks up Variables off the online MEPS database

author: chris @ sihrc
"""
#Python Modules
from bs4 import BeautifulSoup
from operator import itemgetter
from urllib2 import urlopen 

#Local Modules
import config
from wrappers import debug

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
	features = dc.getData(datafile)[0].keys()
	with open(config.path("..", "data", datafile, "features.py"), "wb") as f:
		f.write("features = [")
		for feature in features:
			f.write('"' + feature + '", ')
		f.write("]")

def writeChosenFeatures(datafile):
	"""
	Function that looks for CDF graphs remaining (ones that have not been deleted)

	author: chris
	"""
	with open(config.path("..","data",datafile,"chosen_features.py"), 'wb') as f:
		f.write("features = [")
		for dfile in config.os.listdir(config.path("..","visuals","feature_bin_costs",datafile)):
			f.write('"' + dfile[:-4] + '", ')
		f.write("]")


def getDetails(dataset, variable):
	"""
	Takes in the dataset filename and the variable name 
	Performs the HTTP GET Request and returns a list of decoded values
	"""

	url = "http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId=%s&varName=%s" % (dataset, variable)
	page = urlopen(url)
	soup = BeautifulSoup(page.read())
	details = []
	for line in soup.findAll('font', {'class':"smallBlack"}):
		details.append(line.text.encode('utf8').strip())
	return dict([("Title", "\n".join(details[:3])), ("Name", details[4]), ("Description", details[6]), ("Format", details[8]), ("Type", details[10]), ("Range", details[12] + "~" + details[14]), ("Values", threeColumnString([details[n:n+3] for n in xrange(15,len(details),3)]))])

def print_variable(decoded):
	"""
	Format prints decoded values for getDetails
	"""
	for head,body in decoded.iteritems():
		print head
		print "================================================="
		print body
		print "\n"	
@debug
def writeFeatureImportance(model, trainFeature, datafile):
	"""
	Formats and prints the importance of each feature
	author: Jazmin 
	TODO: right now it gets the actual name of the features in a HORRIBLE NOT EFFICIENT WAY make it better
	"""
	importances = zip(range(trainFeature.shape[1]), model.feature_importances_)
	importances.sort(key = itemgetter(1))
	with open(config.path("..", "data", datafile, "featureImportance.py"), "wb") as f:
		f.write("importance = ")
		for featureIndex,importance in importances[::-1]:
			variable = config.feature_dict["H147"][featureIndex]
			f.write(" " + str(variable) + " " + str(importance) + " " + str(dc.getData(datafile)[0][variable][0]) + " \n")


if __name__ == "__main__":
	datafile = "H147"
	writeFeatureList(datafile)
	writeChosenFeatures(datafile)
"""
Config.py contains configuration data like constants
Also contains notes on the data sets

author: chris @ sihrc
"""
import os
import pickle as p


"""
Data sets
"""
baseA = "http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId="
baseB = "http://meps.ahrq.gov/mepsweb/data_stats/download_data_files_codebook.jsp?PUFId="

download = "http://meps.ahrq.gov/data_files/pufs/%sdat.zip"

datafiles = {}
datafiles["H144D"] = ("IPTC11X",["IPBEGYR","IPBEGMM","IPBEGDD"], baseA + "H144D")
datafiles["H144E"] = ("ERTC11X",["ERDATEYR","ERDATEMM","ERDATEDD"], baseA + "H144E")
datafiles["H144A"] = ("RXMD11X",["RXBEGYXR", "RXBEGMM","RXBEGDD"], baseA + "H144A")
datafiles["H143"]  = ("RTHLTH13",["BEGRFY13","BEGRFM13","BEGRFD13"], baseA + "H143")
datafiles["H147"] = ("TOTTCH11",[], baseA + "H147")
datafiles["PROJYR02"]  = (None,[], baseB + "PROJYR02")

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

def get(fpath, func, **kwargs):
	if os.path.exists(fpath):
		return p.load(open(fpath, 'rb'))
	res = func(**kwargs)
	try:
		with open(fpath, 'wb') as f:
			pickle = p.Pickler(f)
			p.dump(res)
	except:
		print "Data file too large."
	return res
	

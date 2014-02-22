"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc
import config
import os
from wrappers import debug
from host import client

@debug
def getData(datafile):
	print datafile
	dataconfig = config.configuration[datafile]
	return dc.Data(codebook = dataconfig[0], datapath = os.path.join("..", "data" , datafile), costId = dataconfig[1])

@debug
def CDF_COST_FOR_FEATURE(datafile):
		dataconfig = config.configuration[datafile]
		d = dc.Data(codebook = dataconfig[0], datapath = os.path.join("..", "data" , datafile), costId = dataconfig[1])
		for row in d.features:
			costRangeData = an.FeatureCostRange(d, row)
			d = vis.GetCostForBinnedFeature(d,costRangeData, row) #gets cost for feature V24
		# with open(datafile[:-4] + "_ignored.txt", 'wb') as f:
		# 	for line in d.ignored:
		# 		f.write(str(line))
		# 		f.write("\n")
		d.save(d.datapath[:-4] + ".p")

if __name__ == "__main__":
	# CDF_COST_FOR_FEATURE(config.datafiles[-1])
	# for datafile in config.datafiles:
	# 	CDF_COST_FOR_FEATURE(datafile)

	d = getData(config.H144E)
	


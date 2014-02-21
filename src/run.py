"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc
import config
import os
from wrappers import debug
import client


@debug
def CDF_COST_FOR_FEATURE():
	for dataset, datafile in config.datasets.iteritems():
		d = dc.Data(codebook = datafile[1], datapath = os.path.join("..", "data" , datafile[0]), data = client.receiveData(datafile[3]), costId = datafile[2])
		for row in d.features:
			costRangeData = an.FeatureCostRange(d, row)
			d = vis.GetCostForBinnedFeature(d,costRangeData, row) #gets cost for feature V24
		with open(datafile[0] + "_ignored.txt", 'wb') as f:
			for line in d.ignored:
				f.write(str(line))
				f.write("\n")
		d.save(d.datapath[:-4] + ".p")
class Config: pass
if __name__ == "__main__":
	CDF_COST_FOR_FEATURE()






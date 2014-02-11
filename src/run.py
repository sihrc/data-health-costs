"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc

import os


def GetCostForBinnedFeature(dataL, var):
	graphData = []
	print dataL
	raw_input()
	for low,high,data in dataL[1:]:
		an.reject_outliers(data,m=10)
		ranges = "_" + str(low) + "-" + str(high)
		name = d.lookUp(var = var)[0] + ranges + ".jpg"
		name = name.replace(" ","").replace(":","")
		print data
		raw_input()
		if len(data) <= 2:
			print var + ranges, " does not have multiple data points!"
			with open(os.path.join("..","visuals","feature_bin_costs", name[:-3] + ".txt"), 'wb') as f:
				f.write(var + "\n")
				f.write(ranges + "\n")
				f.write(data)
			continue
		graphData.append((low,high,data))
		path = os.path.join("..","visuals","feature_bin_costs")
		if not os.path.exists(path):
			os.makedirs(path)
		vis.GraphPmf(data, os.path.join(path, name.replace("/", "")),100, False)



if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D, filename = "h144d.dat")
	GetCostForBinnedFeature(an.FeatureCostRange(d, "V24", True), "V24")
	#print data
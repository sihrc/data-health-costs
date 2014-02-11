"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc
import outliers as out
import os

if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D, filename = "h144d.dat")

	"""
	Extracting and Plotting data from featureCostRange for cost data in each bin of each feature
	"""
	for feature, data in an.AllFeatureCostRange(d).iteritems():
		data = out.rejectoutliers(data, 1)
		type_ = data[0]
		for low,high,data in data[1:]:
			ranges = "_" + str(low) + "-" + str(high)
			name = d.lookUp(var = feature)[0] + ranges + ".jpg"
			if len(data) <= 2:
				print feature + ranges, " does not have multiple data points!"
				with open(os.path.join("..","visuals","feature_bin_costs", name), 'wb') as f:
					f.write(feature + "\n")
					f.write(ranges + "\n")
					f.write(data)
				continue
			vis.GraphCostPmf(data, os.path.join("..","visuals","feature_bin_costs", name.replace("/", "")), False)

	#print d.getColumn("V2")
	#vis.AllFeatureVsCost(d)
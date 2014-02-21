"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc
import os


class Config: pass
if __name__ == "__main__":
	global d
	ignored = []
	datasets = {"Hospital Inpatient Stays":("h144d.dat",dc.H144D), "Emergency Room Visits":("h144e.dat", dc.H144E), "Prescribed Medicines":("h144a.dat", dc.H144A), "General Demographics":("h143.dat", dc.H143)}
	#datafile = datasets["Hospital Inpatient Stays"] #using hospital inpatient stay data
	#datafile, codebook = datasets["Emergency Room Visits"]
	#datafile = datasets["Prescribed Medicines"]
	#datafile = datasets["General Demographics"]
	for dataset, datafile in datasets.iteritems():
		d = dc.Data(codebook = datafile[1], filename = datafile[0])
		for row in d.features:
			costRangeData = an.FeatureCostRange(d, row)
			d = vis.GetCostForBinnedFeature(d,costRangeData, row, ignored) #gets cost for feature V24
		with open(datafile[1] + "_ignored.txt", 'wb') as f:
			for line in d.ignored:
				f.write(line)
				f.write("\n")
	


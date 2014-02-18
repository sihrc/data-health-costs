"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc
import os


class Config: pass

<<<<<<< HEAD
if __name__ == "__main__":
	global d
	
	datasets = {"Hospital Inpatient Stays":("h144d.dat",dc.H144D), "Emergency Room Visits":("h144e.dat", dc.H144E), "Prescribed Medicines":("h144a.dat", dc.H144A), "General Demographics":("h143.dat", dc.H143)}
	#datafile = datasets["Hospital Inpatient Stays"] #using hospital inpatient stay data
	#datafile, codebook = datasets["Emergency Room Visits"]
	#datafile = datasets["Prescribed Medicines"]
	#datafile = datasets["General Demographics"]
	for datafile, codebook in datasets:
		d = dc.Data(codebook = codebook, filename = datafile)
		for row in d.features:
			if row in ["V43","V49"]:
				continue
			costRangeData = an.FeatureCostRange(d, row)
			vis.GetCostForBinnedFeature(d,costRangeData, row) #gets cost for feature V24
=======
	d = dc.Data(codebook = dc.H144D, filename = dataset)
	GetCostForBinnedFeature(an.FeatureCostRange(d, "V24", True), "V24") #gets cost for feature V24
	
	"""What is V24? -CJ """
	#print data
>>>>>>> 09553cac2a873b3ccf576887619af9f3456e4e5d

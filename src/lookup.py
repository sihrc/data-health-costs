"""
Look Up script for data
"""
import analyze as an
import visuals as vis
import data as dc
import os


if __name__ == "__main__":
	datasets = {"Hospital Inpatient Stays":("h144d.dat",dc.H144D), "Emergency Room Visits":("h144e.dat", dc.H144E), "Prescribed Medicines":("h144a.dat", dc.H144A)}#, "General Demographics":("h143.dat", dc.H143)}

	datafile = datasets["Hospital Inpatient Stays"] #using hospital inpatient stay data
	#datafile, codebook = datasets["Emergency Room Visits"]
	#datafile = datasets["Prescribed Medicines"]
	#datafile = datasets["General Demographics"]
	
	d = dc.Data(codebook = datafile[1], filename = datafile[0])
	print d.lookUp(var = "V42")


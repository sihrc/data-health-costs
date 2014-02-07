"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc

if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D, filename = "h144d.dat")
	for line in d.createBins(d.cost, bins = 30):
		print line
	#vis.GraphCostPmf(d.cost)
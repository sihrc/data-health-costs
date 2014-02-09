"""
Main Script for data
"""
import analyze as an
import visuals as vis
import data as dc

if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D, filename = "h144d.dat")
	#print d.getColumn("V2")
	#vis.AllFeatureVsCost(d)
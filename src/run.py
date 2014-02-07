"""
Main Script for data
"""
import analyze as an
import visuals as vis
import datacode.feature_dict as dc

if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D)
	d.createRefs()
	d.loadData("../data/h144d.dat")

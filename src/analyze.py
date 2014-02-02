#Useful Libraries
import numpy as np
import pickle as p
import matplotlib.pyplot as plt

#Data Library
import datacode.feature_dict as dc

if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D)
	d.createRefs()
	d.loadData("../h144d.dat")

	print d.getColumn("V1")
	# for i in range (len(dataHolder.data)) :
	# 	plt.plot( dataHolder.getColumn("V" + str(i)))
	# 	plt.ylabel(dataHolder.lookUp("V" + str(i)))
	# 	plt.show()
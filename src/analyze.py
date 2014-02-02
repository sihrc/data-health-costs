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

	#print d.getColumn("V1")
	costId = d.lookUp(desc = "CHG")[0][0] # V49
	cost = d.getColumn(costId)

	for i in range (len(d.data)) :
		data = d.getColumn("V" + str(i))
		print data
		raw_input()
	 	plt.plot(data, cost)
	 	plt.ylabel(d.lookUp(var = "V" + str(i))[1])
	 	plt.show()
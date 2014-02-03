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

	for i in range (len(d.features)):
		try:
			data = d.getColumn("V" + str(i))
		 	plt.scatter(data, cost)
		 	print "Plotting " + str(i) + " variable vs cost plot"
		 	plt.xlabel(d.lookUp(var = "V" + str(i))[0])
		 	plt.ylabel("Cost in dollars")
		 	plt.savefig("../visuals/feature_v_cost/" + d.lookUp(var = "V" + str(i))[0].replace(" ", "_") + ".png")
		except:
			print "Plotting " + str(i) + " failed"

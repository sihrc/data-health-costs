#To-DO Create a Visuals module that holds all the visualization TASKS
import matplotlib.pyplot as plt


def FeatureVsCost(data, cost, var):
		try:
			data = data.getColumn(var)
	 		plt.scatter(data, cost)
	 		print "Plotting " + var + " vs cost plot"
	 		plt.xlabel(data.lookUp(var = var)[0])
	 		plt.ylabel("Cost in dollars")
	 		plt.savefig("../visuals/feature_v_cost/" + data.lookUp(var = var)[0].replace(" ", "_") + ".png")
		except:
		 	print "Plotting " + var + " failed"

def AllFeatureVsCost(data):
	for i in range (len(data.features)):
		try:
			FeatureVsCost("V" + str(i))
		except:
			print "Plotting " + str(i) + " failed"

def graphCostPmf(data):
	return "what"
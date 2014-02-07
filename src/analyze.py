#Useful Libraries
import numpy as np
import pickle as p
import matplotlib.pyplot as plt
from stats import *

#Data Library
import datacode.feature_dict as dc

def featureCostRange(dataHandler):
	feature_dicts = dict()
	for i in range(len(d.features)):
		try:
			var = "V"+str(i)
			current_dict = dict()
			data = d.getColumn(var)
			ranges = np.linspace(min(data), max(data), 10)
			colors = ['b','g','k','m','y','p','r','c','k-','k*']
			for i,(low, high) in enumerate(zip(ranges[:-1], ranges[1:])):
				costs = cost[np.where((low < data) * (data < high))]
				if len(costs) == 0:
					continue
				cost_range = np.linspace(min(costs), max(costs),10)
				for cost_low, cost_high in zip(cost_range[:-1], cost_range[1:]):
					current_dict[(low,high)] = (cost_low, cost_high, len(np.where((cost_low < costs) * (costs < cost_high))[0]))
			feature_dicts[var] = current_dict
		except:
			print var + " is not numeral"
	return feature_dicts

if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D)
	# d.createRefs()
	# d.loadData("../data/h144d.dat")

	d.load("temp.p")






	# try:
	# 	pmf = ts2.MakePmfFromList(list(costs))
	# 	tp.Hist(pmf, color = colors[i])
	# 	tp.show()
	# 	raw_input()
	# except ValueError:
	# 	print "divide by 0 sadness"
	

	# new_dats = ts2.BinData(cost, min(cost), max(cost),10)
	# print "Plotting " + str(i) + " variable vs cost plot"
	# print cost
	# pmf = ts2.MakePmfFromList(cost, "Cost")
	# tp.Hist(pmf)
	# thinkplot.Show(title=d.lookUp(var = "V" + str(i))[0],
 #           xlabel='Cost in dollars',
 #           ylabel='Count')
	#tp.Show()

	# for i in range (len(d.features)):
	# 	try:
	# 		data = d.getColumn("V" + str(i))
	# 	 	plt.scatter(data, cost)
	# 	 	print "Plotting " + str(i) + " variable vs cost plot"
	# 	 	plt.xlabel(d.lookUp(var = "V" + str(i))[0])
	# 	 	plt.ylabel("Cost in dollars")
	# 	 	plt.savefig("../visuals/feature_v_cost/" + d.lookUp(var = "V" + str(i))[0].replace(" ", "_") + ".png")
	# 	except:
	# 		print "Plotting " + str(i) + " failed"

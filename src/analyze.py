#Useful Libraries
import numpy as np
import pickle as p
import matplotlib.pyplot as plt
from stats import *

#Data Library
import datacode.feature_dict as dc
import visuals as vis

if __name__ == "__main__":
	d = dc.Data(codebook = dc.HC144D)
	d.createRefs()
	d.loadData("../data/h144d.dat")


	#print d.getColumn("V1")
	costId = d.lookUp(desc = "CHG")[0][0] # V49
	cost = d.getColumn(costId)

	vis.FeatureVsCost(d, cost, "V1")
	vis.graphCostPmf(cost)
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

	print feature_dicts['V2']


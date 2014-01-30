# import pandas as pd
import numpy as np
import re
import matplotlib.pyplot

def loadData(filename):
	data = dict()
	with open(filename, 'rb') as f:
		for line in f:
			decomp = decompose(line)
			for i in range(len(decomp)):
				data[i] = data.get(i, []) + [decomp[i]]
	return data

def decompose(line):
	return re.findall(r"[0-9]+", line)
	


if __name__ == "__main__":
#	printpd.load_csv("../h144d.dat", "label")
	data = loadData("../h144d.dat")
	print data

	"""
	TO-DO 
	"""
	#make graph of keys of data with dictionary values.
	
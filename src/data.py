# import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

import stats
import pickle as p
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

def substractStrings(a,b):
	"""
	Subtracts two very long strings
	"""
	lineUp = zip(map(int, a), map(int, b))
	lineUp.reverse()
	difference = []
	substract = []
	carry = 0
	for charA, charB in lineUp:
		if charA != charB:
			difference.append("1")
		else:
			difference.append("0")
		charA -= carry
		if charA >= charB:
			substract.append(charA - charB)
			carry = 0
		else:
			substract.append(10 + charA - charB)
			carry = 1
	if carry == 1:
		subtract.append(-1)
	difference.reverse()
	substract.reverse()
	return "".join(difference), "".join(map(str,substract))


def stringDifference(strings):
	"""
	Finds the difference between very long longs as strings (difference and subtractions)
	"""
	first = strings[0]
	differences = []
	subtractions = []
	for string in strings:
		# print "===================================="
		# print "original:\t", string
		# print "compare: \t", first
		diff, subs = substractStrings(string, first)
		differences.append(diff)
		subtractions.append(subs)
		# print "difference:\t", diff
		# print "substracted:\t", subtract
		first = string
	return differences, subtractions

def stringDiffFreq(stringList):
	"""
	For Use with the Differences from stringDifference
	"""
	diffDict = dict()
	for diff in stringList:
		for i in range(len(diff)):
			diffDict[i] = diffDict.get(i, 0) + int(diff[i])
	return diffDict

def tempSave(data):
	with open("temp.p", 'wb') as f:
		p.dump(data, f)

def tempLoad():
	with open("temp.p", 'rb') as f:
		return p.load(f)

if __name__ == "__main__":
	#data = loadData("../h144d.dat")
	
	"""
	The first item in each row (data[0]) differ each iteration like so:
	00000000000000000000000000100
	00011001000110010001100100100
	00011001000110010001100101101
	00010001000100010001000101100
	00000000000000000000000000100
	00011001000110010001100101101

	etc..
	"""
	#diffs, subs = stringDifference(data[0])
	# diffDict = stringDiffFreq(diffs)
	
	diffs, subs, data, diffDict = tempLoad()

	scalars = []
	for x in xrange(len(diffDict)):
		scalars.append(diffDict[x])
	plt.bar(xrange(len(scalars)), scalars)
	plt.show()


	

	
	
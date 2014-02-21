"""
Server that hosts the data
Use template to access data
Chris Lee
"""

import csv, sys
import numpy as np
from multiprocessing.connection import Listener
from timer import print_timing
#Import data from csv file
@print_timing
def importData(filename):
	with open(filename + ".csv", "rb") as f:
		print "Importing Data ..."
		reader = csv.reader(f)
		trainX, trainY = [], []
		count = 0
		for line in reader:
			trainY.append(line[0])
			trainX.append(line[1:])
			count += 1
		print "Loaded ", count, "records"
		return np.array(trainX).astype('int'), np.array(trainY).astype('int'), count

#Main program loop to listener for commands
def loopListener(old):
	while True:
		program = raw_input("Which script do you want to run?")
		try:
			sys.modules = old
			exec("import " + program)
			exec(program + ".run()")
		except:
			print "Make sure that script exists and has a run() function!"

#Server Listener
def hostServer(features, targets, records):
	print "Hosting data on localhost:5000"
	serv = Listener(('',5000))
	while True:
		client = serv.accept()
		client.send((features, targets, records))

if __name__ == "__main__":
	filename = sys.argv[1]
	#Grabbing Data from CSV
	trainX, trainY, m = importData(filename)
	print "Finished loading data \n ==================================="

	hostServer(trainX, trainY, m)
	print "Server started!"
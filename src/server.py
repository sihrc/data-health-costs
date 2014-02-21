"""
Server that hosts the data
Use template to access data
Chris Lee
"""

import numpy as np
from multiprocessing.connection import Listener
import os

#Import data from csv file
def importData(filename):
	data = []
	with open(os.path.join("..","data",filename), 'rb') as f:
		for line in f:
			data.append(list(line.strip()))
	return np.array(data)

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
def hostServer(data):
	print "Hosting data on localhost:5000"
	serv = Listener(('',5000))
	while True:
		client = serv.accept()
		client.send(data)

if __name__ == "__main__":
	#Grabbing Data from CSV
	data = dict()
	filenames = ["h143.dat", "h144a.dat", "h144e.dat", "h144d.dat"]
	for datafile in filenames:
		print "Importing " + datafile
		data[datafile] = importData(os.path.join("..","data",datafile))
	print "Finished loading data \n ==================================="
	hostServer(data)
	print "Server started!"
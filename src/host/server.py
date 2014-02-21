"""
Server that hosts the data
Use template to access data
Chris Lee
"""

import numpy as np
from multiprocessing.connection import Listener
import os, sys
sys.path.append("..")
import config, threading
from subprocess import call

#Import data from csv file
def importData(filename):
	data = []
	with open(filename, 'rb') as f:
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
def hostServer(datafile, dataset):
	print "Hosting data on localhost:" + config.datasets[datafile][-1]
	serv = Listener(('',int(config.datasets[datafile][-1])))
	while True:
		client = serv.accept()
		client.send(dataset)

def main(datafile):
	#Grabbing Data from CS
	print "Importing " + datafile
	data = importData(os.path.join("..","..","data",datafile))
	print "Finished loading data \n ==================================="
	hostServer(datafile, data)
	print "Server started!"

if __name__ == "__main__":
	for datafile in config.datafiles:
		t = threading.Thread(target=main,args=datafile)
		t.daemon = False
		t.start()
"""
Template for reading data from load_data_server.py
Chris Lee
"""

from multiprocessing.connection import Client
from wrappers import debug
import pickle as p

@debug
def receiveData(port):
	c = Client(('127.0.0.1', port))
	c.send('data')
	return c.recv()

def loadData(filepath):
	with open(filepath, 'rb') as f:
		data = p.load(f)
	return data

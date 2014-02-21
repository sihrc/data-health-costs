"""
Template for reading data from load_data_server.py
Chris Lee
"""

from multiprocessing.connection import Client
from wrappers import debug
@debug
def receiveData(port):
	c = Client(('127.0.0.1', port))
	c.send('data')
	return c.recv()
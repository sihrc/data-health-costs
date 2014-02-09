import time
import data as d

"""
Debug/Timer Wrapper
prints debug statements
prints the timing of a function

author: chris
"""
def debug(func):
	def wrapper(*arg):
		print "Currently Running:",func.func_name
		print "======================================="
		t1 = time.time()
		res = func(*arg)
		t2 = time.time()
		print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
		print "Finished Running: ", func.func_name
		return res
	return wrapper

"""
Session Saving Wrapper for Data Dict
loads previous session of data holder
runs function
saves previous session of data holder
author: chris
"""
def develop(func):
	def wrapper(*arg):
		dc = d.Data()
		print "Loading previous data session"
		dc = dc.load()
		res = func(dc, *arg)
		print "Saving new data session"
		dc.save()
		return res
	return wrapper
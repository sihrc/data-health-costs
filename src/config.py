"""
Config.py contains configuration data like constants
Also contains notes on the data sets
"""
import data as dc
import os

datafiles = ["h144d.dat","h144e.dat","h144a.dat","h143.dat"]
configuration = {"h144d.dat":(dc.H144D, "IPTC11X", "1000"), "h144e.dat": (dc.H144E,"ERTC11X","2000"), "h144a.dat":(dc.H144A,"RXMD11X","3000"), "h143.dat": (dc.H143,"RTHLTH13","4000")}
	
def makedirs(*path):
	"""
	Header for makedirs
	author:chris
	"""
	if len(path) == 0:
		return ""
		
	targetpath = os.path.join(*path)
	if "." in path[-1]:
		path = path[:-1]
	targetdirs = os.path.join(*path)

	if not os.path.exists(targetdirs):
		os.makedirs(targetdirs)
	return targetpath

"""
HOSPITAL INPATIENT STAYS h144d
------------------------------
*CHG (charge) - total faculty charge + total doctor charge
	Actual sum of money for treatment covered by other things (that we are not going to plot because it's part of the hospital funds provided by government, too)
EXP (expense) - doctor amount paid by family + doctor amount paid by other isurance + faculty amount paid by family insurace + faculty amount paid by other insurance
	How much is paid by insurance
 
EMERGENCY ROOM STAYS h144e
-------------------------------


GENERAL DEMOGRAPHICS STAYS h143
-------------------------------
RTHLTH13 - health condition
1 - 5 poor to excellent

PRESCRIBED MEDICATION h144a
-------------------------------

"""



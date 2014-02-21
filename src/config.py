"""
Config.py contains configuration data like constants
Also contains notes on the data sets
"""
import data as dc
import os

datasets = {"Hospital Inpatient Stays":("h144d.dat",dc.H144D, "IPTC11X"), "Emergency Room Visits":("h144e.dat", dc.H144E,"ERTC11X"), "Prescribed Medicines":("h144a.dat", dc.H144A,"RXMD11X"), "General Demographics":("h143.dat", dc.H143,"RTHLTH13")}

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


GENERAL DEMOGRAPHICS STAYS h143
-------------------------------
RTHLTH13 - health condition
1 - 5 poor to excellent
"""



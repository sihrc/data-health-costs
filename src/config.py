"""
Config.py contains configuration data like constants
Also contains notes on the data sets
"""
import data as dc

datasets = {"Hospital Inpatient Stays":("h144d.dat",dc.H144D), "Emergency Room Visits":("h144e.dat", dc.H144E), "Prescribed Medicines":("h144a.dat", dc.H144A)}#, "General Demographics":("h143.dat", dc.H143)}


"""
HOSPITAL INPATIENT STAYS h144d
------------------------------
*CHG (charge) - total faculty charge + total doctor charge
	Actual sum of money for treatment covered by other things (that we are not going to plot because it's part of the hospital funds provided by government, too)
EXP (expense) - doctor amount paid by family + doctor amount paid by other isurance + faculty amount paid by family insurace + faculty amount paid by other insurance
	How much is paid by insurance

"""



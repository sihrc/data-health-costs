"""
Contains data holder class
author:chris 
"""

import pickle as p
import numpy as np
import os

#Debug Timer Wrappers
from wrappers import debug

HC144D = {"DUID: DWELLING UNIT ID":(1, 5),"PID: PERSON NUMBER":(6, 8),"DUPERSID: PERSON ID (DUID + PID)":(9, 16),"EVNTIDX: EVENT ID":(17, 28),"EVENTRN: EVENT ROUND NUMBER":(29, 29),"ERHEVIDX: EVENT ID FOR CORRESPONDING EMER RM VISIT":(30, 41),"FFEEIDX: FLAT FEE ID":(42, 53),"PANEL: PANEL NUMBER":(54, 55),"MPCDATA: MPC DATA FLAG":(56, 56),"IPBEGYR: EVENT START DATE - YEAR":(57, 60),"IPBEGMM: EVENT START DATE - MONTH":(61, 62),"IPBEGDD: EVENT START DATE - DAY":(63, 64),"IPENDYR: EVENT END DATE - YEAR":(65, 68),"IPENDMM: EVENT END DATE - MONTH":(69, 70),"IPENDDD: EVENT END DATE - DAY":(71, 72),"NUMNIGHX: NUM OF NIGHTS IN HOSPITAL - EDITED/IMPUTED":(73, 75),"NUMNIGHT: NUMBER OF NIGHTS STAYED AT PROVIDER":(76, 77),"EMERROOM: DID STAY BEGIN WITH EMERGENCY ROOM VISIT":(78, 79),"SPECCOND: HOSPITAL STAY RELATED TO CONDITION":(80, 81),"RSNINHOS: REASON ENTERED HOSPITAL":(82, 83),"DLVRTYPE: VAGINAL OR CAESAREAN DELIVERY":(84, 85),"EPIDURAL: RECEIVE AN EPIDURAL OR SPINAL FOR PAIN":(86, 87),"ANYOPER: ANY OPERATIONS OR SURGERIES PERFORMED":(88, 89),"IPICD1X: 3-DIGIT ICD-9-CM CONDITION CODE":(90, 92),"IPICD2X: 3-DIGIT ICD-9-CM CONDITION CODE":(93, 95),"IPICD3X: 3-DIGIT ICD-9-CM CONDITION CODE":(96, 98),"IPICD4X: 3-DIGIT ICD-9-CM CONDITION CODE":(99, 101),"IPPRO1X: 2-DIGIT ICD-9-CM PROCEDURE CODE":(102, 103),"IPPRO2X: 2-DIGIT ICD-9-CM PROCEDURE CODE":(104, 105),"IPCCC1X: MODIFIED CLINICAL CLASSIFICATION CODE":(106, 108),"IPCCC2X: MODIFIED CLINICAL CLASSIFICATION CODE":(109, 111),"IPCCC3X: MODIFIED CLINICAL CLASSIFICATION CODE":(112, 114),"IPCCC4X: MODIFIED CLINICAL CLASSIFICATION CODE":(115, 117),"DSCHPMED: MEDICINES PRESCRIBED AT DISCHARGE":(118, 119),"FFIPTYPE: FLAT FEE BUNDLE":(120, 121),"IPXP11X: TOT EXP FOR EVENT (IPFXP11X+IPDXP11X)":(122, 130),"IPTC11X: TOTAL CHG FOR EVENT (IPFTC11X+IPDTC11X)":(131, 140),"IPFSF11X: FACILITY AMT PD, FAMILY (IMPUTED)":(141, 148),"IPFMR11X: FACILITY AMT PD, MEDICARE (IMPUTED)":(149, 157),"IPFMD11X: FACILITY AMT PD, MEDICAID (IMPUTED)":(158, 166),"IPFPV11X: FACILITY AMT PD, PRIV INSUR (IMPUTED)":(167, 175),"IPFVA11X: FAC AMT PD,VETERANS/CHAMPVA(IMPUTED)":(176, 183),"IPFTR11X: FACILITY AMT PD,TRICARE(IMPUTED)":(184, 191),"IPFOF11X: FACILITY AMT PD, OTH FEDERAL (IMPUTED)":(192, 199),"IPFSL11X FACILITY AMT PD, STATE/LOC GOV (IMPUTED)":(200, 207), "IPFWC11X FACILITY AMT PD, WORKERS COMP (IMPUTED)":(208, 216), "IPFOR11X FACILITY AMT PD, OTH PRIV (IMPUTED)":(217, 225), "IPFOU11X FACILITY AMT PD, OTH PUB (IMPUTED)":(226, 233), "IPFOT11X FACILITY AMT PD, OTH INSUR (IMPUTED)":(234, 241), "IPFXP11X FACILITY SUM PAYMENTS IPFSF11X-IPFOT11X":(242, 250), "IPFTC11X TOTAL FACILITY CHARGE (IMPUTED)":(251, 260), "IPDSF11X DOCTOR AMOUNT PD, FAMILY (IMPUTED)":(261, 268), "IPDMR11X DOCTOR AMOUNT PD, MEDICARE (IMPUTED)":(269, 276), "IPDMD11X DOCTOR AMOUNT PAID, MEDICAID (IMPUTED)":(277, 284), "IPDPV11X DOCTOR AMT PD, PRIV INSUR (IMPUTED)":(285, 292), "IPDVA11X DR AMT PD,VETERANS/CHAMPVA(IMPUTED)":(293, 299), "IPDTR11X DOCTOR AMT PD,TRICARE(IMPUTED)":(300, 307), "IPDOF11X DOCTOR AMT PD, OTH FEDERAL (IMPUTED)":(308, 311), "IPDSL11X DOCTOR AMT PD, STATE/LOC GOV (IMPUTED)":(312, 318), "IPDWC11X DOCTOR AMOUNT PD, WORKERS COMP (IMPUTED)":(319, 326), "IPDOR11X DOCTOR AMT PD, OTH PRIVATE (IMPUTED)":(327, 334), "IPDOU11X DOCTOR AMT PD, OTH PUB (IMPUTED)":(335, 341), "IPDOT11X DOCTOR AMT PD, OTH INSUR (IMPUTED)":(342, 348), "IPDXP11X DOCTOR SUM PAYMENTS IPDSF11X-IPDOT11X":(349, 356), "IPDTC11X TOTAL DOCTOR CHARGE (IMPUTED)":(357, 365), "IMPFLAG IMPUTATION STATUS":(366, 366), "PERWT11F EXPENDITURE FILE PERSON WEIGHT, 2011":(367, 378), "VARSTR VARIANCE ESTIMATION STRATUM, 2011":(379, 382), "VARPSU VARIANCE ESTIMATION PSU, 2011":(383, 383)}
H144E = {"DUID DWELLING UNIT ID ":(1, 5),  "PID PERSON NUMBER ":(6, 8),  "DUPERSID PERSON ID (DUID + PID) ":(9, 16),  "EVNTIDX EVENT ID ":(17, 28),  "EVENTRN EVENT ROUND NUMBER ":(29, 29),  "ERHEVIDX EVENT ID FOR CORRESPONDING HOSPITAL STAY ":(30, 41),  "FFEEIDX FLAT FEE ID ":(42, 53),  "PANEL PANEL NUMBER ":(54, 55),  "MPCDATA MPC DATA FLAG ":(56, 56),  "ERDATEYR EVENT DATE - YEAR ":(57, 60),  "ERDATEMM EVENT DATE - MONTH ":(61, 62),  "ERDATEDD EVENT DATE - DAY ":(63, 64),  "SEEDOC DID P TALK TO MD THIS VISIT ":(65, 66),  "VSTCTGRY BEST CATEGORY FOR CARE P RECV ON VST DT ":(67, 68),  "VSTRELCN THIS VST RELATED TO SPEC CONDITION ":(69, 70),  "LABTEST THIS VISIT DID P HAVE LAB TESTS ":(71, 72),  "SONOGRAM THIS VISIT DID P HAVE SONOGRAM OR ULTRSD ":(73, 74),  "XRAYS THIS VISIT DID P HAVE X-RAYS ":(75, 76),  "MAMMOG THIS VISIT DID P HAVE A MAMMOGRAM ":(77, 78),  "MRI THIS VISIT DID P HAVE AN MRI/CATSCAN ":(79, 80),  "EKG THIS VISIT DID P HAVE AN EKG OR ECG ":(81, 82),  "EEG THIS VISIT DID P HAVE AN EEG ":(83, 84),  "RCVVAC THIS VISIT DID P RECEIVE A VACCINATION ":(85, 86),  "ANESTH THIS VISIT DID P RECEIVE ANESTHESIA ":(87, 88),  "THRTSWAB THIS VISIT DID P HAVE A THROAT SWAB ":(89, 90),  "OTHSVCE THIS VISIT DID P HAVE OTH DIAG TEST/EXAM ":(91, 92),  "SURGPROC WAS SURG PROC PERFORMED ON P THIS VISIT ":(93, 94),  "MEDPRESC ANY MEDICINE PRESCRIBED FOR P THIS VISIT ":(95, 96),  "ERICD1X 3-DIGIT ICD-9-CM CONDITION CODE ":(97, 99),  "ERICD2X 3-DIGIT ICD-9-CM CONDITION CODE ":(100, 102),  "ERICD3X 3-DIGIT ICD-9-CM CONDITION CODE ":(103, 105),  "ERPRO1X 2-DIGIT ICD-9-CM PROCEDURE CODE ":(106, 107),  "ERPRO2X 2-DIGIT ICD-9-CM PROCEDURE CODE ":(108, 109),  "ERCCC1X MODIFIED CLINICAL CLASSIFICATION CODE ":(110, 112),  "ERCCC2X MODIFIED CLINICAL CLASSIFICATION CODE ":(113, 115),  "ERCCC3X MODIFIED CLINICAL CLASSIFICATION CODE ":(116, 118),  "FFERTYPE FLAT FEE BUNDLE ":(119, 120),  "ERXP11X TOT EXP FOR EVENT (ERFXP11X + ERDXP11X) ":(121, 128),  "ERTC11X TOTAL CHG FOR EVENT (ERFTC11X+ERDTC11X) ":(129, 137),  "ERFSF11X FACILITY AMT PD, FAMILY (IMPUTED) ":(138, 145),  "ERFMR11X FACILITY AMT PD, MEDICARE (IMPUTED) ":(146, 153),  "ERFMD11X FACILITY AMT PD, MEDICAID (IMPUTED) ":(154, 161),  "ERFPV11X FACILITY AMT PD, PRIV INSUR (IMPUTED) ":(162, 169),  "ERFVA11X FAC AMT PD,VETERANS/CHAMPVA(IMPUTED)":(170, 176),  "ERFTR11X FACILITY AMT PD,TRICARE(IMPUTED) ":(177, 183),  "ERFOF11X FACILITY AMT PD, OTH FEDERAL (IMPUTED) ":(184, 190),  "ERFSL11X FACILITY AMT PD, STATE/LOC GOV (IMPUTED) ":(191, 197),  "ERFWC11X FACILITY AMT PD, WORKERS COMP (IMPUTED) ":(198, 205),  "ERFOR11X FACILITY AMT PD, OTH PRIV (IMPUTED) ":(206, 213),  "ERFOU11X FACILITY AMT PD, OTH PUB (IMPUTED) ":(214, 221),  "ERFOT11X FACILITY AMT PD, OTH INSUR (IMPUTED) ":(222, 229),  "ERFXP11X FACILITY SUM PAYMENTS ERFSF11X-ERFOT11X ":(230, 237),  "ERFTC11X TOTAL FACILITY CHARGE (IMPUTED) ":(238, 246),  "ERDSF11X DOCTOR AMOUNT PAID, FAMILY (IMPUTED) ":(247, 253),  "ERDMR11X DOCTOR AMOUNT PD, MEDICARE (IMPUTED) ":(254, 260),  "ERDMD11X DOCTOR AMOUNT PAID, MEDICAID (IMPUTED) ":(261, 267),  "ERDPV11X DOCTOR AMT PD, PRIV INSUR (IMPUTED) ":(268, 274),  "ERDVA11X DR AMT PD,VETERANS/CHAMPVA(IMPUTED) ":(275, 280),  "ERDTR11X DOCTOR AMT PD,TRICARE(IMPUTED) ":(281, 286),  "ERDOF11X DOCTOR AMT PAID, OTH FEDERAL (IMPUTED) ":(287, 290),  "ERDSL11X DOCTOR AMT PD, STATE/LOC GOV (IMPUTED) ":(291, 297),  "ERDWC11X DOCTOR AMOUNT PD, WORKERS COMP (IMPUTED) ":(298, 303),  "ERDOR11X DOCTOR AMT PD, OTH PRIVATE (IMPUTED) ":(304, 310),  "ERDOU11X DOCTOR AMT PD, OTH PUB (IMPUTED) ":(311, 316),  "ERDOT11X DOCTOR AMT PD, OTH INSUR (IMPUTED) ":(317, 323),  "ERDXP11X DOCTOR SUM PAYMENTS ERDSF11X - ERDOT11X ":(324, 330),  "ERDTC11X TOTAL DOCTOR CHARGE (IMPUTED) ":(331, 338),  "IMPFLAG IMPUTATION STATUS ":(339, 339),  "PERWT11F EXPENDITURE FILE PERSON WEIGHT, 2011 ":(340, 351),  "VARSTR VARIANCE ESTIMATION STRATUM, 2011 ":(352, 355),  "VARPSU VARIANCE ESTIMATION PSU, 2011":(356, 356)}
class Data():
	def __init__ (self, data = dict(), codebook = HC144D, filename = os.path.join("..","data","h144d.dat")):
		self.codebook = codebook
		self.createRefs()
		self.results = dict()
		self.data = self.loadData(os.path.join("..","data",filename))
	
	def createBins(self, data, bins = 10):
		#Create ranges for data
		ranges = np.linspace(np.min(data), np.max(data), bins)
		#Ranges between ranges
		for low,high in zip(ranges[:1], ranges[1:]):
			data[np.where((data > low) * (data < high))] = (low + high)/2.0
		return data

	def createRefs(self):
		"""
		Create Reference Dicts
		Feature - Var:Description
		Index - Var:Indicies
		"""
		count = 0
		self.features = dict()
		for key,item in self.codebook.iteritems():
			self.features["V" + str(count)] = [key, item]
			count += 1
	def lookUp(self, var = None, desc = None):
		"""
		Look up a feature using the variable name or a description
		returns acroynym-description, indices
		"""
		if var:
			return self.features[var]
		elif desc:
			results = []
			for key,item in self.features.iteritems():
				if desc.lower() in item[0].lower():
					results.append((key,item))
			return results
		else:
			return list
	def loadData(self,filename):
		"""
		Loads the Data Set from filename as numpy array
		"""
		data = []
		with open(filename, 'rb') as f:
			for line in f:
				data.append(list(line.strip()))
		self.data = np.array(data)
		self.costId = self.lookUp(desc = "CHG")[0][0] # V49
		self.cost = self.getColumn(self.costId)
		return self.data
	def getColumn(self, var):
		"""
		Gets the column of data given by var
		"""
		ranges = self.lookUp(var = var)[1]
		rawData = self.data[:,ranges[0] - 1:ranges[1]]
		newFormat = np.zeros(shape = (rawData.shape[0]))
		for i in range(len(rawData)):
			newFormat[i] = "".join(rawData[i]).strip()
		return newFormat
	def save(self, filename):
		with open(filename, 'wb') as f:
			p.dump(self, f)
			print filename + " Saved Successfully"

	def load(self, filename):
		"""
		Saves this object as a pickle file for access later
		"""
		with open(filename, 'rb') as f:
			self = p.load(f)
			print filename + " Loaded Successfully"

	"""
	Class native methods
	"""
	def __repr__(self):
		return "Data Handler Object"

	def __str__(self):
		return "Attributes: \ndata\t\t - contains dataset as a numpy array\nindicies\t - contains variables:indicies dictionary\nfeatures\t - contains variables:feature descriptions as dictionary"

if __name__ == "__main__":
	print "See Documentation"
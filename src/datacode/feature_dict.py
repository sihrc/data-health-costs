import pickle as p
import numpy as np

HC144D = {"DUID: DWELLING UNIT ID":(1, 5),"PID: PERSON NUMBER":(6, 8),"DUPERSID: PERSON ID (DUID + PID)":(9, 16),"EVNTIDX: EVENT ID":(17, 28),"EVENTRN: EVENT ROUND NUMBER":(29, 29),"ERHEVIDX: EVENT ID FOR CORRESPONDING EMER RM VISIT":(30, 41),"FFEEIDX: FLAT FEE ID":(42, 53),"PANEL: PANEL NUMBER":(54, 55),"MPCDATA: MPC DATA FLAG":(56, 56),"IPBEGYR: EVENT START DATE - YEAR":(57, 60),"IPBEGMM: EVENT START DATE - MONTH":(61, 62),"IPBEGDD: EVENT START DATE - DAY":(63, 64),"IPENDYR: EVENT END DATE - YEAR":(65, 68),"IPENDMM: EVENT END DATE - MONTH":(69, 70),"IPENDDD: EVENT END DATE - DAY":(71, 72),"NUMNIGHX: NUM OF NIGHTS IN HOSPITAL - EDITED/IMPUTED":(73, 75),"NUMNIGHT: NUMBER OF NIGHTS STAYED AT PROVIDER":(76, 77),"EMERROOM: DID STAY BEGIN WITH EMERGENCY ROOM VISIT":(78, 79),"SPECCOND: HOSPITAL STAY RELATED TO CONDITION":(80, 81),"RSNINHOS: REASON ENTERED HOSPITAL":(82, 83),"DLVRTYPE: VAGINAL OR CAESAREAN DELIVERY":(84, 85),"EPIDURAL: RECEIVE AN EPIDURAL OR SPINAL FOR PAIN":(86, 87),"ANYOPER: ANY OPERATIONS OR SURGERIES PERFORMED":(88, 89),"IPICD1X: 3-DIGIT ICD-9-CM CONDITION CODE":(90, 92),"IPICD2X: 3-DIGIT ICD-9-CM CONDITION CODE":(93, 95),"IPICD3X: 3-DIGIT ICD-9-CM CONDITION CODE":(96, 98),"IPICD4X: 3-DIGIT ICD-9-CM CONDITION CODE":(99, 101),"IPPRO1X: 2-DIGIT ICD-9-CM PROCEDURE CODE":(102, 103),"IPPRO2X: 2-DIGIT ICD-9-CM PROCEDURE CODE":(104, 105),"IPCCC1X: MODIFIED CLINICAL CLASSIFICATION CODE":(106, 108),"IPCCC2X: MODIFIED CLINICAL CLASSIFICATION CODE":(109, 111),"IPCCC3X: MODIFIED CLINICAL CLASSIFICATION CODE":(112, 114),"IPCCC4X: MODIFIED CLINICAL CLASSIFICATION CODE":(115, 117),"DSCHPMED: MEDICINES PRESCRIBED AT DISCHARGE":(118, 119),"FFIPTYPE: FLAT FEE BUNDLE":(120, 121),"IPXP11X: TOT EXP FOR EVENT (IPFXP11X+IPDXP11X)":(122, 130),"IPTC11X: TOTAL CHG FOR EVENT (IPFTC11X+IPDTC11X)":(131, 140),"IPFSF11X: FACILITY AMT PD, FAMILY (IMPUTED)":(141, 148),"IPFMR11X: FACILITY AMT PD, MEDICARE (IMPUTED)":(149, 157),"IPFMD11X: FACILITY AMT PD, MEDICAID (IMPUTED)":(158, 166),"IPFPV11X: FACILITY AMT PD, PRIV INSUR (IMPUTED)":(167, 175),"IPFVA11X: FAC AMT PD,VETERANS/CHAMPVA(IMPUTED)":(176, 183),"IPFTR11X: FACILITY AMT PD,TRICARE(IMPUTED)":(184, 191),"IPFOF11X: FACILITY AMT PD, OTH FEDERAL (IMPUTED)":(192, 199),"IPFSL11X FACILITY AMT PD, STATE/LOC GOV (IMPUTED)":(200, 207), "IPFWC11X FACILITY AMT PD, WORKERS COMP (IMPUTED)":(208, 216), "IPFOR11X FACILITY AMT PD, OTH PRIV (IMPUTED)":(217, 225), "IPFOU11X FACILITY AMT PD, OTH PUB (IMPUTED)":(226, 233), "IPFOT11X FACILITY AMT PD, OTH INSUR (IMPUTED)":(234, 241), "IPFXP11X FACILITY SUM PAYMENTS IPFSF11X-IPFOT11X":(242, 250), "IPFTC11X TOTAL FACILITY CHARGE (IMPUTED)":(251, 260), "IPDSF11X DOCTOR AMOUNT PD, FAMILY (IMPUTED)":(261, 268), "IPDMR11X DOCTOR AMOUNT PD, MEDICARE (IMPUTED)":(269, 276), "IPDMD11X DOCTOR AMOUNT PAID, MEDICAID (IMPUTED)":(277, 284), "IPDPV11X DOCTOR AMT PD, PRIV INSUR (IMPUTED)":(285, 292), "IPDVA11X DR AMT PD,VETERANS/CHAMPVA(IMPUTED)":(293, 299), "IPDTR11X DOCTOR AMT PD,TRICARE(IMPUTED)":(300, 307), "IPDOF11X DOCTOR AMT PD, OTH FEDERAL (IMPUTED)":(308, 311), "IPDSL11X DOCTOR AMT PD, STATE/LOC GOV (IMPUTED)":(312, 318), "IPDWC11X DOCTOR AMOUNT PD, WORKERS COMP (IMPUTED)":(319, 326), "IPDOR11X DOCTOR AMT PD, OTH PRIVATE (IMPUTED)":(327, 334), "IPDOU11X DOCTOR AMT PD, OTH PUB (IMPUTED)":(335, 341), "IPDOT11X DOCTOR AMT PD, OTH INSUR (IMPUTED)":(342, 348), "IPDXP11X DOCTOR SUM PAYMENTS IPDSF11X-IPDOT11X":(349, 356), "IPDTC11X TOTAL DOCTOR CHARGE (IMPUTED)":(357, 365), "IMPFLAG IMPUTATION STATUS":(366, 366), "PERWT11F EXPENDITURE FILE PERSON WEIGHT, 2011":(367, 378), "VARSTR VARIANCE ESTIMATION STRATUM, 2011":(379, 382), "VARPSU VARIANCE ESTIMATION PSU, 2011":(383, 383)}

class Data():
	def __init__ (self, data = dict(), codebook = HC144D):
		self.codebook = codebook
		self.features = dict()
		self.temporary = dict()
		self.data = None
		costId = d.lookUp(desc = "CHG")[0][0] # V49
		cost = d.getColumn(costId)
	
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

	def getColumn(self, var):
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
	with open("../feature_dict.p",'wb') as f:
		print "Dumping Data in feature_dict.p ..."
		p.dump(data, f)
		print "Finished Dumping Data"
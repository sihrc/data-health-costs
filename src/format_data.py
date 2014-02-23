"""
Formats the data for training the model
"""
#System level modules
import os
import numpy as np

#Local Modules
import data as dc
import config
import data

#Wrapper for debug function (timing and debug print statements)
from wrappers import debug


@debug
def getData(datafile):
	dataconfig = config.configuration[datafile]
	return dc.Data(codebook = dataconfig[0], datapath = os.path.join("..", "data" , datafile), costId = dataconfig[1])

def formatData(datafile, features):
	d = getData(datafile)
	dataX = np.zeros(shape=(len(d.cost), len(features)))
	for i,feature in enumerate(features):
		dataX[:,i] = d.getColumn(tag = feature).astype("float")
	return dataX, d.cost


def crossReference(datafile, features):
	all_features = [key.split()[0] for key in config.configuration[datafile][0].keys()]
	for feature in features:
		if not (feature in all_features):
			print datafile, feature
	if len(set(features)) != len(features):
		for i,feature in enumerate(features):
			if feature in features[i + 1:] + features[:i]:
				print feature, " is duplicated"
		print datafile, "features has duplicates"

if __name__ == "__main__":
	feature_dict = {}
	feature_dict[config.H144A] = ["PERWT11F", "PHARTP1", "PHARTP2", "PHARTP4", "PHARTP6", "PHARTP7", "RXCCC1X", "RXCCC2X", "RXCCC3X", "RXDAYSUP", "RXICD1X", "RXICD2X", "RXICD3X", "RXMD11X", "RXQUANTY", "RXSF11X", "RXSL11X", "RXSTRENG", "RXSTRUNT", "RXXP11X", "TC1", "TC1S1", "TC2", "TC2S1", ]
	feature_dict[config.H144D] = ["ANYOPER", "DLVRTYPE", "DSCHPMED", "EMERROOM", "EPIDURAL", "ERHEVIDX", "EVNTIDX", "IPBEGDD", "IPBEGMM", "IPCCC1X", "IPCCC2X", "IPCCC3X", "IPCCC4X", "IPDMD11X", "IPDMR11X", "IPDOR11X", "IPDOT11X", "IPDOU11X", "IPDPV11X", "IPDSF11X", "IPDSL11X", "IPDTC11X", "IPDTR11X", "IPDXP11X", "IPENDDD", "IPFMD11X", "IPFMR11X", "IPFOR11X", "IPFOT11X", "IPFOU11X", "IPFPV11X", "IPFSF11X", "IPFSL11X", "IPFTC11X", "IPFTR11X", "IPFVA11X", "IPFXP11X", "IPICD2X", "IPICD3X", "IPICD4X", "IPPRO1X", "IPPRO2X", "IPXP11X", "NUMNIGHT", "NUMNIGHX", "PERWT11F", "RSNINHOS", "VARSTR", "SPECCOND"]
	feature_dict[config.H144E] = ["ANESTH", "EEG", "EKG", "ERDMD11X", "ERDMR11X", "ERDOR11X", "ERDOT11X", "ERDOU11X", "ERDPV11X", "ERDSF11X", "ERDSL11X", "ERDTC11X", "ERDTR11X", "ERDVA11X", "ERDWC11X", "ERDXP11X", "ERFMD11X", "ERFMR11X", "ERFOF11X", "ERFOR11X", "ERFOT11X", "ERFOU11X", "ERFPV11X", "ERFSF11X", "ERFSL11X", "ERFTC11X", "ERFTR11X", "ERFVA11X", "ERFWC11X", "ERFXP11X", "ERHEVIDX", "ERICD1X", "ERICD2X", "ERICD3X", "ERPRO1X", "ERPRO2X", "ERTC11X", "ERXP11X", "FFERTYPE", "LABTEST", "MAMMOG", "MEDPRESC", "MPCDATA", "MRI", "OTHSVCE", "PANEL", "PERWT11F", "RCVVAC", "SEEDOC", "SONOGRAM", "SURGPROC", "THRTSWAB", "VSTCTGRY", "VSTRELCN", "XRAYS"]
	feature_dict[config.H143]  = ["ACTDTY13", "ACTLIM13", "ADLHLP13", "AGE13X", "AIDHLP13", "BEGRFD13", "BEGRFM13", "BENDIF13", "COGLIM13", "DOBYY", "EDRECODE", "EDUCYR", "EDUYRDEG", "EMPST13", "ENDRFD13", "ENDRFM13", "FAMSIZ13", "FNGRDF13", "FTSTD13X", "HELD13X", "HIDEG", "HISPANX", "HISPCAT", "HONRDC13", "HOUR13", "HRWAG13X", "HRWAY13", "HRWGRD13", "HSELIM13", "IADLHP13", "INSCOP13", "KEYNESS", "LFTDIF13", "MARRY13X", "MCAID13", "MCAID13X", "MCARE13", "MCARE13X", "MILDIF13", "MNHLTH13", "MSA13", "NUMEMP13", "OFFER13X", "OTPUBA13", "OTPUBB13", "PROXY13", "PSTAT13", "PUB13X", "RACEAX", "RACEBX", "RACETHNX", "RACEWX", "RACEX", "RCHDIF13", "RDRESP13", "REGION13", "RFREL13X", "RNDREF13", "RUCLAS13", "RUENDM13", "RURSLT13", "RUSIZE13", "SCHLIM13", "SELFCM13", "SEX", "SOCLIM13", "SPOUID13", "SPOUIN13", "STNDIF13", "STPDIF13", "STPRG13", "TRINW13X", "UNABLE13", "WLKDIF13", "WLKLIM13", "WRKLIM13"]

	for datafile, features in feature_dict.iteritems():
		# crossReference(datafile, features)
		X,Y = formatData(datafile, features)
		np.save(os.path.join("..","data",datafile[:-4] + "_" + "dataX"),X)
		np.save(os.path.join("..","data",datafile[:-4] + "_" + "dataY"), Y)

			
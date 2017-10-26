import pandas as pd
import numpy as np
from collections import defaultdict as dd
#pathdict is global for easy access throughout the entire file
pathdict = {'cardiologie':'/home/kerkt02/patdata/DM_CARDIOLOGIE.csv', 'subtraject':'/home/kerkt02/patdata/QUERY_FOR_DM_SUBTRAJECTEN.csv','opname':'/home/kerkt02/patdata/QUERY_FOR_DM_LGS_OPNAME.csv'}

def cdb(df):
	

def databuilder():
	labelP = 'PATNR'
	labelZ = 'ZIEKTEGEVALNUMMER'
	labelZa = 'OpnameZiektegeval'
	#convert dictionary to something that takes lists
	patientIDs = dd(list)
	patientIDs = {'Patnr':[],'opname_dt':[],'ontslag_dt':[],'zorgtrajectnr':[]}
	#reading all csv files using the global dictionary for pathnames
	dfcardio = pd.read_csv(pathdict['cardiologie'],header=0,low_memory=False,encoding='ISO-8859-1')
	dfsub = pd.read_csv(pathdict['subtraject'],header=0,low_memory=False,encoding='ISO-8859-1')
	dfadmission = pd.read_csv(pathdict['opname'],header=0,low_memory=False,encoding='ISO-8859-1')

	cardioPatients = set(dfcardio['PATNR'])
	#print(cardioPatients)
	subZ = set(dfsub[labelZ])
	subA = set(dfadmission[labelZa])
	#print(subA, subZ)
	diseaseIDs = set(subZ & subA)

	for i in diseaseIDs:
		for index,row in dfadmission.loc[dfadmission['OpnameZiektegeval'] == i].iterrows():
			patientIDs['Patnr'].append(row['PATNR'])
			patientIDs['opname_dt'].append(row['opname_dt'])
			patientIDs['ontslag_dt'].append(row['ontslag_dt'])
			#insert code for determination of zorgtrajectnr
			#print(row['PATNR'])
			#print(row['opname_dt'])
			uniquenr = set()
			uniquenr.clear()
			for indexx,roww in dfsub.loc[dfsub['ZIEKTEGEVALNUMMER'] == i].iterrows():
				uniquenr.add(roww['ZORGTRAJECTNR'])
			if(len(uniquenr) > 1):
				patientIDs['zorgtrajectnr'].append(list(uniquenr)[1])
			else:
				patientIDs['zorgtrajectnr'].append(list(uniquenr)[0])

	readdf = pd.DataFrame.from_dict(patientIDs)
	readdf = readdf.sort_values(by=['Patnr','zorgtrajectnr'])
	return readdf
def main():
	databuilder()

main()

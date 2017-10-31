import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import sklearn as sk
import datetime as dt
from collections import defaultdict as dd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Imputer

#Headerlist that defines categorical, and continuous variables
headerlistcat = ['Geslacht','DiagnoseCode', 'OpnameUitvoerder','OpnameBewegingVolgnr','OpnameBehandelaar','vrgeschiedenis_myochardinfarct','vrgeschiedenis_PCI','vrgeschiedenis_CABG','vrgeschiedenis_CVA_TIA','vrgeschiedenis_vaatlijden','vrgeschiedenis_hartfalen','vrgeschiedenis_maligniteit','vrgeschiedenis_COPD','vrgeschiedenis_atriumfibrilleren','TIA','CVA_Niet_Bloedig','CVA_Bloedig','LV_Functie','dialyse','riscf_roken','riscf_familieanamnese','riscf_hypertensie','riscf_hypercholesterolemie','riscf_diabetes','roken','Radialis','Femoralis','Brachialis','vd_1','vd_2','vd_3','graftdysfunctie']
headerlistcon = ['Geboortedatum','lengte','gewicht','bloeddruk','HB','HT','INR','Glucose','Kreat','Trombocyten','Leukocyten','Cholesterol_totaal','Cholesterol_ldl']


#COPIED STRING FOR PRESERVATION
#HEADERS = ['DiagnoseCode','lengte','gewicht','bloeddruk','HB','HT','Glucose','Kreat','Trombocyten','Leukocyten','Cholesterol_otaal','Cholesterol_ldl']
HEADERS = ['DiagnoseCode', 'OpnameUitvoerder','OpnameBewegingVolgnr','OpnameBehandelaar','vrgeschiedenis_myochardinfarct','vrgeschiedenis_PCI','vrgeschiedenis_CABG','vrgeschiedenis_CVA_TIA','vrgeschiedenis_vaatlijden','vrgeschiedenis_hartfalen','vrgeschiedenis_maligniteit','vrgeschiedenis_COPD','vrgeschiedenis_atriumfibrilleren','TIA','CVA_Niet_Bloedig','CVA_Bloedig','LV_Functie','dialyse','riscf_roken','riscf_familieanamnese','riscf_hypertensie','riscf_hypercholesterolemie','riscf_diabetes','roken','Radialis','Femoralis','Brachialis','vd_1','vd_2','vd_3','graftdysfunctie', 'Geboortedatum','lengte','gewicht','bloeddruk','HB','HT','INR','Glucose','Kreat','Trombocyten','Leukocyten','Cholesterol_totaal','Cholesterol_ldl']
LHEADERS = ['DiagnoseCode','lengte','gewicht','bloeddruk','HB','HT','Glucose','Kreat','Trombocyten','Leukocyten','Cholesterol_totaal','Cholesterol_ldl','lbl']
LABEL = ['lbl']

#pathdict is global for easy access throughout the entire file
pathdict = {'cardiologie':'/home/kerkt02/patdata/DM_CARDIOLOGIE.csv', 'subtraject':'/home/kerkt02/patdata/QUERY_FOR_DM_SUBTRAJECTEN.csv','opname':'/home/kerkt02/patdata/QUERY_FOR_DM_LGS_OPNAME.csv'}
labelDict = {'opname':'opname_dt','ontslag':'ontslag_dt','code':'zorgtrajectnr'}
dfcardio = pd.read_csv(pathdict['cardiologie'],header=0,low_memory=False,encoding='ISO-8859-1')
dfsub = pd.read_csv(pathdict['subtraject'],header=0,low_memory=False,encoding='ISO-8859-1')
dfadmission = pd.read_csv(pathdict['opname'],header=0,low_memory=False,encoding='ISO-8859-1')

def cdb(df):
	readm = False
	counter = 0
	patnr = 1
	zCode = 0
	patchecker = True
	z = False
	readTrue = []
	prevzCode = 0
	prevdischarge = dt.datetime(1000, 10, 10).date()
	prevadmission = prevdischarge
	#set prevdischarge & prevadmission to impossible date to prevent errors
	for i in df['Patnr']:
		#get date of admission & convert to workable format
		admission = df.loc[counter,labelDict['opname']][0:-9]
		admission = dt.datetime.strptime(admission, '%d%b%y').date()
		#get date of discharge & convert to workable format, save copy for later use in logic
		discharge = df.loc[counter,labelDict['ontslag']][0:-9]
		discharge = dt.datetime.strptime(discharge, '%d%b%y').date()
		#get znosis code
		zCode = df.loc[counter,labelDict['code']]
		#when it's a different patient, check again for possible readmission
		if patnr != i:
			patchecker = True
			if patnr == 1:
				print('running cdb...')
			elif readm:
				readTrue.append(patnr)
				readm = False
			elif not readm:
				readm = False
			patnr = i


		#when it's a different admission date, check again for possible readmission
		if admission != prevadmission:
			patchecker = True

		#patchecker determines whether the patient has been checked, if not, check for readmission
		if patchecker:
			#check if it's a readmission based on date
	#		print(abs(prevdischarge - admission).days)
			if(abs(prevdischarge - admission).days) < 30 and z:
				readm = True
			#dates and booleans for further logic
			prevdischarge = discharge
			prevadmission = admission
			patchecker = False

		#print(prevdischarge)
		counter += 1
		#print(admission, discharge)
		z = False
		if zCode == prevzCode:
			z = True
		prevzCode = zCode

	if readm:
		readTrue.append(patnr)
	#print("patients that got readmitted: ", patlistTrue)
	#print("patients that didn't get readmitted: ", patlistFalse)
	#print("Total amount of ids:", len(readTrue))
	return readTrue
def databuilder():
	print('Running databuilder...')
	labelP = 'PATNR'
	labelZ = 'ZIEKTEGEVALNUMMER'
	labelZa = 'OpnameZiektegeval'
	#convert dictionary to something that takes lists
	patientIDs = dd(list)
	patientIDs = {'Patnr':[],'opname_dt':[],'ontslag_dt':[],'zorgtrajectnr':[]}

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

def datainit(patList):
	print('Running datainit...')
	lbl = pd.Series()
	counter = 0
	for i in dfcardio['PATNR'].values:
		if i in patList:
			lbl = lbl.set_value(counter, True)
		else:
			lbl = lbl.set_value(counter, False)
		counter += 1
	dfcardio['lbl'] = lbl.values
	print('succesfully added a column!')


def dataimputer(t):
	imputer = Imputer(missing_values=np.nan, strategy='mean', axis=0)
	c = imputer.fit_transform(dfcardio[[t]]).ravel()
	return c
def split_dataset(dataset, train_percentage, feature_headers, target_header):
	print("splitting the dataset...")
	check = dataset[target_header]
	dataset = dataset[feature_headers]
	train_x, test_x, train_y, test_y = train_test_split(dataset, check, train_size=train_percentage)
	return train_x, test_x, train_y, test_y

def rfc(features, target):
	print("creating the classifier...")
	cl = RandomForestClassifier()
	cl.fit(features,target)
	return cl

def onehotdummy(d):
	le = LabelEncoder()
	for feature in d:
		dfcardio[feature] = le.fit_transform(dfcardio[feature].astype(str))

def dobconverter(l):
	now = pd.Timestamp(dt.datetime.now())
	dfcardio[l] = pd.to_datetime(dfcardio[l], format='%Y-%m-%d')
	dfcardio[l] = dfcardio[l].where(dfcardio[l] < now, dfcardio[l] - np.timedelta64(100, 'Y'))
	dfcardio[l] = (now - dfcardio[l]).astype('<m8[Y]')

def dataimputer(t):
	imputer = Imputer(missing_values=np.nan, strategy='mean', axis=0)
	c=imputer.fit_transform(dfcardio[[t]]).ravel()
	return c

def vistree(t,features):
	print("visualizing important branches with numpy and exporting...")
	importances = []
	importances = t.feature_importances_
	indices = np.argsort(importances)
	headerorder = []
	for i in indices:
		headerorder.append(HEADERS[i])
	plt.title('Feature Importance')
	plt.barh(range(len(indices)), importances[indices], color='b', align='center')
	plt.yticks(range(len(indices)), features[headerorder])
	plt.xlabel('Relative Importance')
	plt.savefig('treegraph.png')

def main():
	dobconverter('Geboortedatum')
	onehotdummy(headerlistcat)
	for con in headerlistcon:
		dfcardio[con] = dataimputer(con)

	dbdf = databuilder()
	ListTrue = cdb(dbdf)
	datainit(ListTrue)
	train_x, test_x, train_y, test_y = split_dataset(dfcardio, 0.7, HEADERS, LABEL)
	trained_model = rfc(train_x, train_y)
	predictions = trained_model.predict(test_x)
	print("train accuracy: ",accuracy_score(train_y, trained_model.predict(train_x)))
	print("test accuracy: ",accuracy_score(test_y, predictions))
	vistree(trained_model, train_x)
	#print(dfcardio)

main()


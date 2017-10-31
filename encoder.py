from sklearn.preprocessing import LabelBinarizer
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import Imputer
data = pd.read_csv('/home/kerkt02/patdata/DM_CARDIOLOGIE.csv',header=0,low_memory=False,encoding='ISO-8859-1')

def main():
	headerlistcat = ['DiagnoseCode', 'OpnameUitvoerder','OpnameBewegingVolgnr','OpnameBehandelaar','vrgeschiedenis_myochardinfarct','vrgeschiedenis_PCI','vrgeschiedenis_CABG','vrgeschiedenis_CVA_TIA','vrgeschiedenis_vaatlijden','vrgeschiedenis_hartfalen','vrgeschiedenis_maligniteit','vrgeschiedenis_COPD','vrgeschiedenis_atriumfibrilleren','TIA','CVA_Niet_Bloedig','CVA_Bloedig','LV_Functie','dialyse','riscf_roken','riscf_familieanamnese','riscf_hypertensie','riscf_hypercholesterolemie','riscf_diabetes','roken','Radialis','Femoralis','Brachialis','vd_1','vd_2','vd_3','graftdysfunctie']
	headerlistcon = ['Geboortedatum','lengte','gewicht','bloeddruk','HB','HT','INR','Glucose','Kreat','Trombocyten','Leukocyten','Cholesterol_totaal','Cholesterol_ldl']
	headerlistdat = ['Geboortedatum'] #also a continuous variable, just needs to be transformed into actual integers first
	print(len(headerlistcat)+len(headerlistcon)+len(headerlistdat))
	trainerdict = {}
	#onehotencode all categorical variables
	for cat in headerlistcat:
		trainerdict[cat] = makeonehot(data[cat])

	#convert DoB into age
	dobconverter('Geboortedatum')

	for con in headerlistcon:
		trainerdict[con] = dataimputer(con)

	for cat in headerlistcat:
		makedummies(cat)
	print(trainerdict)

def makeonehot(s):
	encoder = LabelBinarizer()
	s[pd.isnull(s)] = 'NaN'
	o = encoder.fit_transform(s)
	return o
def makedummies(d):
	print(pd.get_dummies(data[d]))

def dobconverter(l):
	now = pd.Timestamp(dt.datetime.now())
	data[l] = pd.to_datetime(data[l], format='%Y-%m-%d')
	data[l] = data[l].where(data[l] < now, data[l] - np.timedelta64(100, 'Y'))
	data[l] = (now - data[l]).astype('<m8[Y]')
	#print(data[l])
def dataimputer(t):
	imputer = Imputer(missing_values=np.nan, strategy='mean', axis=0)
	c=imputer.fit_transform(data[[t]]).ravel()
	return c
main()

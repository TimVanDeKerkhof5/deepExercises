from sklearn.preprocessing import LabelBinarizer
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import Imputer

def main():
	data = pd.read_csv('/home/kerkt02/patdata/DM_CARDIOLOGIE.csv',header=0,low_memory=False,encoding='ISO-8859-1')
	headerlist = ['DiagnoseCode', 'OpnameUitvoerder','vrgeschiedenis_maligniteit','roken']
	for i in headerlist:
		print(makeonehot(data[i]))
	print(findAge(dt.datetime(1990,10,10)))
	tsk = data['gewicht']
	tsk[pd.isnull(tsk)] = 0
	print(dataimputer(tsk))

def makeonehot(s):
	encoder = LabelBinarizer()
	s[pd.isnull(s)] = 'NaN'
	o = encoder.fit_transform(s)
	return o

def findAge(born):
	today = dt.date.today()
	return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
def dataimputer(t):
	imputer = Imputer(missing_values=0, strategy='mean', axis=0)
	imputer.fit_transform(t)
	return t

main()

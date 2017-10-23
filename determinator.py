import pandas as pd
import datetime

patdf = pd.read_csv("/home/kerkt02/patdata/QUERY_FOR_DM_LGS_OPNAME.csv", header=0, low_memory=False, encoding="ISO-8859-1")

counter = 0
labelDict = {'opname':'opname_dt', 'ontslag':'ontslag_dt','code':'OpnameDiagnoseCode'}
patnr = 1
diagCode = 0
patchecker = True
diag = False
patlistTrue = []
patlistFalse = []
prevdiagCode = 0
prevdischarge = datetime.datetime(1000, 10, 10).date()
prevadmission = prevdischarge
#set prevdischarge & prevadmission to impossible date to prevent errors
for i in patdf['PATNR']:
	
	#get date of admission & convert to workable format
	admission = patdf.loc[counter,labelDict['opname']][0:-9]
	admission = datetime.datetime.strptime(admission, '%d%b%y').date()
	#get date of discharge & convert to workable format, save copy for later use in logic
	discharge = patdf.loc[counter,labelDict['ontslag']][0:-9]
	discharge = datetime.datetime.strptime(discharge, '%d%b%y').date()
	#get diagnosis code
	diagCode = patdf.loc[counter,labelDict['code']]
	#when it's a different patient, check again for possible readmission
	if patnr != i:
		patchecker = True
		if patnr == 1:
			print('running code...')
		elif readm:
			patlistTrue.append(patnr)
			readm = False
		elif not readm:
			patlistFalse.append(patnr)
			readm = False
		patnr = i


	#when it's a different admission date, check again for possible readmission
	if admission != prevadmission:
		patchecker = True

	#patchecker determines whether the patient has been checked, if not, check for readmission
	if patchecker:
		#check if it's a readmission based on date
#		print(abs(prevdischarge - admission).days)
		if(abs(prevdischarge - admission).days) < 30 and diag:
			readm = True
		#dates and booleans for further logic
		prevdischarge = discharge
		prevadmission = admission
		patchecker = False



	#print(prevdischarge)
	counter += 1
	#print(admission, discharge)
	diag = False
	if diagCode == prevdiagCode:
		diag = True
	prevdiagCode = diagCode

if readm:
	patlistTrue.append(patnr)
else:
	patlistFalse.append(patnr)

#print("patients that got readmitted: ", patlistTrue)
#print("patients that didn't get readmitted: ", patlistFalse)
print("Total amount of ids:", len(patlistTrue), len(patlistFalse))

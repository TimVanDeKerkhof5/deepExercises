#imports
import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
#get data from file
data = pd.read_csv("classtest.csv", header=0,sep=';')


#create label column
def datainit():

	lbl = pd.Series()
	counter = 0
	for i in data['det'].values:
		if i > 0.5:
			lbl = lbl.set_value(counter, True) 
		else:
			lbl = lbl.set_value(counter, False)
		counter += 1

	data['lbl'] = lbl.values


def split_dataset(dataset, train_percentage, feature_headers, target_header):
	train_x, test_x, train_y, test_y = train_test_split(dataset[feature_headers], dataset[target_header], train_size=train_percentage)
	return train_x, test_x, train_y, test_y

def rfc(features, target):
	cl = RandomForestClassifier()
	cl.fit(features, target)
	return cl

def main():
	datainit()
	train_x, test_x, train_y, test_y = split_dataset(data, 0.7, ['test1' , 'chikin', 'det'], ['lbl'])
	
	trained_model = rfc(train_x, train_y)
	print(trained_model)
	predictions = trained_model.predict(test_x)
	print("train accuracy:",accuracy_score(train_y, trained_model.predict(train_x)))
	print("test accuracy:", accuracy_score(test_y, predictions))
	print("confusion matrix:", confusion_matrix(test_y, predictions))
if __name__ == "__main__":
	main()


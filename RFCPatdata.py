import pandas as pd
import sklearn as sk
import numpy as np

def filereader(path):
	file = pd.read_csv(path, low_memory=False, encoding="ISO-8859-1",header=0) 
	print(file)

Class rfcHandler:
	def __init__(self, filedf)

def main():
	filereader("/home/kerkt02/patdata/QUERY_FOR_DM_ZORGACTIVITEITEN.csv")

main()

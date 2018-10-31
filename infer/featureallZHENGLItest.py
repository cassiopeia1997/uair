# #coding:utf-8  
from math import radians, cos, sin, asin, sqrt
import numpy as np
import random
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from scipy import stats

grid=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,2218,811,4166,2603,4331,3992]
grid_x=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,0,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,0,2218,811,4166,0,0,2603,4331,3992,0,0,0,0,0]
#grid=[3862,3198,3056,2762,2462,2124,1999,1061,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,2218,811,4166,2603,4331,3992]

grid_dict={}
index=0
for i in grid_x:
	grid_dict[i]=index
	index+=1
#print grid_dict
with open("grid_choice.txt","r") as f:
	allgrids=f.readlines()
with open("grid_infer.txt","r") as f:
	allinfergrids=f.readlines()
#print allinfergrids
#with open("grid_test.txt","r") as f:
#	alltestgrids=f.readlines()
with open("spatial_features_infer.txt","r") as f:
	alltrainfeatures=f.readlines()
dates=["0226"]
dates_hours={}
totalhours=0
tts=["0226_1630"]
allline=[]
for date in dates:
	for item in tts:
		filename=os.path.join(os.path.join("data",date),"aqi_"+item+".txt")
		with open(filename,"r")as f:
			allline=f.readlines()
with open(os.path.join("data","weather.txt"),"r") as f:
	weather=f.readlines()
featuresTest=[]
y_test=[]
allfeature=[]
label_dict={"G":"[1,0,0,0,0]","M":"[0,1,0,0,0]","US":"[0,0,1,0,0]","U":"[0,0,0,1,0]","VU-H":"[0,0,0,0,1]"}
for i in range(len(allline)):
	featureline=[]
	labels=[]
	
	#print int(allinfergrids[i].strip("\n"))
	infotest=allline[i]
	for cri in infotest.split(" "):
		infos=cri.split("_")
		if infos[0]=="PM10":
			break
	label=""
	if not (infos[1]=="None"):
		temp=infos[1]
		#print infos[1]
		pm10=int(infos[1])
		if pm10<=50:
			label="G" 
		else:
			if pm10<=100:
				label="M"
			else:
				if pm10<=150:
					label="US"
				else:
					if pm10<=200:
						label="U"
					else:
						if pm10<=300:
							label="VU-H"
						else:
							if pm10<=500:
								label="VU-H"
	else:
		label="None"
	y_test.append(label)
	label=""
	for item in allgrids[i].strip("\n").split(" "):
		label=""
		info= allline[int(item)-1].split(" ")
		for cri in info:
			infos=cri.split("_")
			if infos[0]=="PM10":
				break
		#print infos[1]
		if not (infos[1]=="None"):
			temp=infos[1]
			#print infos[1]
			pm10=int(infos[1])
			featureline.append(alltrainfeatures[int(item)-1].strip("\n"))
			if pm10<=50:
				label="G" 
			else:
				if pm10<=100:
					label="M"
				else:
					if pm10<=150:
						label="US"
					else:
						if pm10<=200:
							label="U"
						else:
							if pm10<=300:
								label="VU-H"
							else:
								if pm10<=500:
									label="VU-H"
			featureline.append(label_dict[label])
			
			
		else:
			
			featureline=[]
			break
	allfeature.append(featureline)
		#print featureline
#print allfeature
with open(os.path.join("result","featuresTest.txt"),"a+") as f:
	for k in range(len(allfeature)):
		for item in allfeature[k]:
			f.write(item+" ")
		f.write("\n")
with open(os.path.join("result","LabelsTest.txt"),"a+") as f:
	for item in y_test:
		if not item=="None":
			f.write(label_dict[item]+"\n")
		else:
			f.write("null"+"\n")
		
			
	
	



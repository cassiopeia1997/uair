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
with open("spatial_features.txt","r") as f:
	alltrainfeatures=f.readlines()
dates=["0225","0226","0227","0228","0302","0303","0323","0324","0326","0327","0328","0331","0401","0402","0403","0404","0405","0406","0407","0408","0409","0410","0411","0412","0413"]
dates_hours={}
totalhours=0

for date in dates:
	filename=os.path.join(os.path.join("crawl",date),"station.txt")
	with open(filename,"r")as f:
		allline=f.readlines()
	hours=len(allline)/36
	dates_hours[date]=hours
	totalhours+=hours
print dates_hours
print totalhours

featuresTrain=[]
y_train=[]
featuresTest=[]
y_test=[]

count_hour=0
count_date=0
countline=0
check=0
for i in range(len(allinfergrids)):
	check=0
	times=0
	count=0
	grids_choice=allgrids[i].strip("\n").split(" ")
	feaure_line=[]
	while(count<3):
		file_date=os.path.join(os.path.join("crawl",dates[count_date]),"station.txt")
		times+=1
		
		for item in grids_choice:
			
			#countline+=1
			#print (i,count_date,count_hour,count,times)
			index=grid_dict[int(item)]
			#file_date=os.path.join(os.path.join("crawl",dates[count_date]),"station.txt")
			with open (file_date,"r") as f:
					allline=f.readlines()
			info=allline[index+count_hour*36].split(" ")
			for cri in info:
				infos=cri.split("_")
				if infos[0]=="PM10":
					break
			if not (infos[1]=="None"):
				temp=infos[1]
				count+=1
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
				feaure_line.append(label)
				if count==3:
					index_infer=grid_dict[int(allinfergrids[i].strip("\n"))]
					infer_info=allline[index_infer+count_hour*36].split(" ")
					for cri in infer_info:
						infer_infos=cri.split("_")
						if infer_infos[0]=="PM10":
							temp=infer_infos[1]
							break
					if not (infer_infos[1]=="None"):
						#print infer_infos[1]
						pm10_infer=int(infer_infos[1])
						if pm10_infer<=50:
							label_infer="G" 
						else:
							if pm10_infer<=100:
								label_infer="M"
							else:
								if pm10_infer<=150:
									label_infer="US"
								else:
									if pm10_infer<=200:
										label_infer="U"
									else:
										if pm10_infer<=300:
											label_infer="VU-H"
										else:
											if pm10_infer<=500:
												label_infer="VU-H"
						#y_train.append(label_infer)
						label_line=label_infer
					else:
						feaure_line=[]
						label_line=""
						print "no"
					count_hour+=1
					if count_hour>=dates_hours[dates[count_date]] and count_date<len(dates):
						count_hour=0
						count_date+=1
					if count_date >=len(dates):
						count_date=0
						count_hour=0
					
			else:
				#print ("ok")
				count_hour+=1
				count=0
				#times+=1
				feaure_line=[]
				label_line=""
				if count_hour>=dates_hours[dates[count_date]] and count_date<len(dates):
					count_hour=0
					count_date+=1
				if count_date >=len(dates):
					count_date=0
					count_hour=0
				if times>15:
					count=3
					#y_train.append("")
				break
	#print feaure_line
	featuresTrain.append(feaure_line)
	y_train.append(label_line)
print len(featuresTrain)
#print featuresTrain
print len(y_train)
#print featuresTrain
m=0
label_dict={"G":[1,0,0,0,0],"M":[0,1,0,0,0],"US":[0,0,1,0,0],"U":[0,0,0,1,0],"VU-H":[0,0,0,0,1]}
with open(os.path.join("spatialmodel","featuresTrain.txt"),"a+") as f:
	for i in range(len(featuresTrain)):
		if not featuresTrain[i]==[]:
			
			f.write(alltrainfeatures[m].strip("\n")+" "+str(label_dict[featuresTrain[i][0]])+" ")
			f.write(alltrainfeatures[m+1].strip("\n")+" "+str(label_dict[featuresTrain[i][1]])+" ")
			f.write(alltrainfeatures[m+2].strip("\n")+" "+str(label_dict[featuresTrain[i][2]])+"\n")
		else:
			f.write(""+"\n")
		m+=3

with open(os.path.join("spatialmodel","LabelTrain.txt"),"a+") as f:
	for i in range(len(y_train)):
		if not y_train[i]=="":
			f.write(str(label_dict[y_train[i]])+"\n")
		else:
			f.write(""+"\n")
'''	
if count_hour>=dates_hours[dates[count_date]] and count_date<len(dates):
					count_hour=0
					count_date+=1
				if count_date >=len(dates):
					count_date=0
					count_hour=0
'''
#clf = MLPClassifier(solver='lbfgs', activation='logistic',alpha=0.001,learning_rate_init=0.001,max_iter=200,hidden_layer_size=())
#clf.fit(X, y)


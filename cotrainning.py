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
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
from itertools import chain
import string

with open(os.path.join(os.path.join("spatialmodel","result"),"empty_crf.txt"),"r") as f:
	empty_crf=f.readlines()
with open(os.path.join(os.path.join("spatialmodel","result"),"probability_ann.txt"),"r") as f:
	ann=f.readlines()
with open(os.path.join(os.path.join("spatialmodel","result"),"crf.txt"),"r") as f:
	crf=f.readlines()
with open(os.path.join("spatialmodel","LabelTest.txt"),"r") as f:
	ytest=f.readlines()
dates=["0225","0226","0227","0228","0302","0303","0323","0324","0326","0327","0328","0331","0401","0402","0403","0404","0405","0406","0407","0408","0409","0410","0411","0412","0413"]
#dates=["0225","0226","0227","0228","0302","0303"]
#dates=["0225"]
#grid=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,0,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,0,2218,811,4166,0,0,2603,4331,3992,0,0,0,0,0]
#print len(grid)
date_hours={}
totalhours=0
for date in dates:
	print date
	#filename=os.path.join(os.path.join("crawl",date),"station.txt")
	filelist=[]
	for root, dirs, files in os.walk(os.path.join("crawl",date)):  
		filelist=files
	date_hours[date]=len(filelist)-1
	totalhours+=date_hours[date]
print date_hours
date_order={}
order=0
for item in dates:
	date_order[item]=order
	order+=1
print date_order
empty_5={}
empty_8={}
for item in empty_crf:
	ls=item.strip("\n").split(" ")
	if ls[0]=="5":
		if not ls[1] in empty_5:
			empty_5[ls[1]]=[]
			empty_5[ls[1]].append(int(ls[2]))
		else:
			empty_5[ls[1]].append(int(ls[2]))
	if ls[0]=="8":
		if not ls[1] in empty_8:
			empty_8[ls[1]]=[]
			empty_8[ls[1]].append(int(ls[2]))
		else:
			empty_8[ls[1]].append(int(ls[2]))
lim_data=len(dates)
ann_final=[]
crf_final_5=[["None"]*date_hours[i] for i in dates]
crf_final_8=[["None"]*date_hours[i] for i in dates]
count_date=0
count_time=0
m=0
for item in empty_5:
	for i in range(len(empty_5[item])):
		crf_final_5[date_order[item]][empty_5[item][i]]="null"
for item in empty_8:
	for i in range(len(empty_8[item])):
		crf_final_8[date_order[item]][empty_8[item][i]]="null"
#print crf_final_5
#print empty_5
crf_5=[]
crf_8=[]
temp_5=[]
temp_8=[]
for item in crf:
	if item.strip("\n")=="":
		count_date+=1
		count_time+=1
		
		if count_time>=2:
			crf_5.append(temp_5)
			crf_8.append(temp_8)
			count_time=0
			temp_5=[]
			temp_8=[]
	else:
		if count_time==0:
			temp_5.append(item.strip("\n"))
		if count_time==1:
			temp_8.append(item.strip("\n"))

k=0
#print [len(crf_5[i]) for i in range(len(crf_5))]
count_date=0
count_time=0
for i in range(len(crf_final_5)):
	#print i
	for j in range(len(crf_final_5[i])):
		#print (i,count_date,count_time)
		if not crf_final_5[i][j]=="null":
			crf_final_5[i][j]=crf_5[count_date][count_time]
			count_time+=1
			if count_time==len(crf_5[count_date]):
				count_date+=1
				count_time=0
count_date=0
count_time=0
for i in range(len(crf_final_8)):
	#print i
	for j in range(len(crf_final_8[i])):
		#print (i,count_date,count_time)
		if not crf_final_8[i][j]=="null":
			crf_final_8[i][j]=crf_8[count_date][count_time]
			count_time+=1
			if count_time==len(crf_8[count_date]):
				count_date+=1
				count_time=0
				
ann_final_5=[["None"]*date_hours[i] for i in dates]
ann_final_8=[["None"]*date_hours[i] for i in dates]
y_test_5=[["None"]*date_hours[i] for i in dates]
y_test_8=[["None"]*date_hours[i] for i in dates]
with open(os.path.join("spatialmodel","featuresTest.txt"),"r") as f:
	featuresTest=f.readlines()
count_date=0
count_hour=0
for ind in range(len(featuresTest[0:1000])):
	if not featuresTest[ind].strip("\n")=="":
		if not featuresTest[ind].strip("\n")[0]=="n":
			ann_final_5[count_date][count_hour]=ann[ind].strip("\n")
			y_test_5[count_date][count_hour]=ytest[ind].strip("\n")
			count_hour+=1
			if count_hour>=date_hours[dates[count_date]]:
				count_date+=1
				count_hour=0
			if count_date>=len(dates):
				break
		else:
			ls=featuresTest[ind].strip("\n").split(" ")
			ann_final_5[count_date][count_hour]="null"
			y_test_5[count_date][count_hour]=ytest[ind].strip("\n")
			#print(count_date,count_hour,ls[1],ls[2])
			count_hour+=1
			if count_hour>=date_hours[dates[count_date]]:
				count_date+=1
				count_hour=0
			if count_date>=len(dates):
				break

featuresTest2=featuresTest[1000:]
count_date=0
count_hour=0
#print("\n")
#print count_date,count_hour
for ind in range(len(featuresTest2)):
	if not featuresTest2[ind].strip("\n")=="":
		if not featuresTest2[ind].strip("\n")[0]=="n":
			ann_final_8[count_date][count_hour]=ann[ind+1000].strip("\n")
			y_test_8[count_date][count_hour]=ytest[ind+1000].strip("\n")
			count_hour+=1
			if count_hour>=date_hours[dates[count_date]]:
				count_date+=1
				count_hour=0
			if count_date>=len(dates):
				break
		else:
			ls=featuresTest2[ind].strip("\n").split(" ")
			ann_final_8[count_date][count_hour]="null"
			y_test_8[count_date][count_hour]=ytest[ind+500].strip("\n")
			#print(count_date,count_hour,ls[1],ls[2])
			count_hour+=1
			if count_hour>=date_hours[dates[count_date]]:
				count_date+=1
				count_hour=0
			if count_date>=len(dates):
				break
#print ann_final_5,ann_final_8,crf_final_5,crf_final_8,y_test_5,y_test_8
'''
print ann_final_8
print "\n"
print y_test_8
'''
#print crf_final_5
#print "\n"
#print ann_final_5
for i in range(len(ann_final_5)):
	for j in range(len(ann_final_5[i])):
		if crf_final_5[i][j]=="null":
			ann_final_5[i][j]="null"
			y_test_5[i][j]="null"
for i in range(len(ann_final_8)):
	for j in range(len(ann_final_8[i])):
		if crf_final_8[i][j]=="null":
			ann_final_8[i][j]="null"
			y_test_8[i][j]="null"
# use ann as final feature contains two info ,ann ,crf
# use y_test_ as true label
y_pred=[]
y_true=[]

for i in range(len(ann_final_5)):
	for j in range(len(ann_final_5[i])):
		if not ann_final_5[i][j]=="null":
			#print (i,j)
			ls1=ann_final_5[i][j].strip("[").strip("]").split(",")
			#print ls1
			lst1=[float(item) for item in ls1]
			ls2=crf_final_5[i][j].strip("[").strip("]").split(",")
			#print ls1,ls2
			lst2=[float(item) for item in ls2]
			lst=[lst2[k] for k in range(len(lst1))]  #*1
			maxnum=max(lst)
			lst=[int(item/maxnum) for item in lst]
			y_pred.append(lst)
			#print lst
			#print (i,j)
			yt=y_test_5[i][j].strip("[").strip("]").split(",")
			yt1=[int(item) for item in yt]
			y_true.append(yt1)
			#print yt1
for i in range(len(ann_final_8)):
	for j in range(len(ann_final_8[i])):
		if not ann_final_8[i][j]=="null":
			ls1=ann_final_8[i][j].strip("[").strip("]").split(",")
			lst1=[float(item) for item in ls1]
			ls2=crf_final_8[i][j].strip("[").strip("]").split(",")
			#print ls1,ls2
			lst2=[float(item) for item in ls2]
			lst=[lst2[k] for k in range(len(lst1))] #*1
			maxnum=max(lst)
			lst=[int(item/maxnum) for item in lst]
			y_pred.append(lst)
			#print lst
			#print (i,j)
			yt=y_test_8[i][j].strip("[").strip("]").split(",")
			yt1=[int(item) for item in yt]
			y_true.append(yt1)

print (classification_report(np.array(y_true),np.array(y_pred)))




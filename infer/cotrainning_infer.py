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

with open(os.path.join("result","empty_crf.txt"),"r") as f:
	empty_crf=f.readlines()
with open(os.path.join("result","probability_ann.txt"),"r") as f:
	ann=f.readlines()

with open(os.path.join("result","crf.txt"),"r") as f:
	crf=f.readlines()
#print len(crf)
temp=["None"]*5##
ann_final=["None"]*4539
crf_final=[["None"]*5 for i in range(4539)]
empty=["None"]*4539
for item in empty_crf:
	ls=item.strip("\n").split(" ")
	for it in ls:
		itt=it.split("_")
		if itt[0]=="line":
			line=int(itt[1])
		if itt[0]=="hour":
			hour=int(itt[1])
	crf_final[line][hour]="null"
	#print hour==4
	#4:change from shijiqingkuang len of seq
	if hour==4:
		empty[line]="del"
		#print "ok"
#print empty
for i in range(len(ann)):
	annline=ann[i].strip("\n")
	if not annline=="null":
		if not empty[i]=="del":
			ann_final[i]=annline
#print ann_final
k=0
line_start=0
hour_start=0
m=0
for i in range(len(crf_final)):
	for j in range(len(crf_final[i])):
		if not crf_final[i][j]=="null":
			if not crf[m].strip("\n")=="":
				crf_final[i][j]=crf[m].strip("\n")
			else:
				m+=1
				crf_final[i][j]=crf[m].strip("\n")
			#print crf_final[i][j],i,j
			m+=1
'''
for i in range(len(crf)):
	if not crf_final[line_start][hour_start]=="null":
		print crf[i]
		crf_final[line_start][hour_start]=crf[i].strip("\n")
		hour_start+=1
		if hour_start>=5:
			line_start+=1
			hour_start=0
'''
crf_final_one=[]
for i in range(len(crf_final)):
	crf_final_one.append(crf_final[i][-1])
#print crf_final_one
y_pred=[]
for i in range(len(ann_final)):
	if not ann_final[i]=="None":
		ls1=ann_final[i].strip("[").strip("]").split(" ")
		lst1=[float(item.strip(",")) for item in ls1]
		#print crf_final[i]
		ls2=crf_final_one[i].strip("[").strip("]").split(" ")
		#print i,ls2
		lst2=[float(item.strip(",")) for item in ls2]
		lst=[lst2[k] for k in range(len(lst1))]
		maxnum=max(lst)
		lst=[int(item/maxnum) for item in lst]
		y_pred.append(lst)
	else:
		y_pred.append("null")
		#print lst
		#print (i,j)
print "finish"
#print y_pred
with open("infer_result.txt","a+") as f:
	for i in range(len(y_pred)):
		f.write(str(y_pred[i])+"\n")




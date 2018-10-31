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
from sklearn.externals import joblib

def bio_classification_report(y_true, y_pred):
	"""
	Classification report for a list of BIO-encoded sequences.
	It computes token-level metrics and discards "O" labels.
	
	Note that it requires scikit-learn 0.15+ (or a version from github master)
	to calculate averages properly!
	"""
	lb = LabelBinarizer()
	y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
	y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))
        
	tagset = set(lb.classes_) - {'O'}
	tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
	class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
	
	return classification_report(
		y_true_combined,
		y_pred_combined,
		labels = [class_indices[cls] for cls in tagset],
		target_names = tagset,
	)

def dataset(xtrain,x_train):
	kk=0
	for item in xtrain:
		listitem=item.strip("\n").split(" ")
		feature=[]
		count=0
		temp=[]
		if not len(item.strip("\n"))==0:
			#print item
			if not item.strip("\n")[0]=="n":
				kk+=1
				for it in listitem:
					
					if not it[0]=="[" and (not it[-1]=="]") and (not it[-1]==","):
						feature.append(float(it))
					else:
						#print it
						temp.append(float(it.strip(",").strip("[").strip("]")))
						count+=1
						if count==5:
							for k in temp:
								feature.append(k)
							temp=[]
							count=0
			#print feature
				x_train.append(feature)
	print kk
	return x_train
	
def datasetlabel(xtrain,x_train):
	kk=0
	for item in xtrain:
		listitem=item.strip("\n").split(" ")
		feature=[]
		count=0
		temp=[]
		if (not item.strip("\n")=="null") and(not item.strip("\n")==""):
			kk+=1
			for it in listitem:
				
				if not it[0]=="[" and (not it[-1]=="]") and (not it[-1]==","):
					feature.append(int(it))
				else:
					#print it
					temp.append(int(it.strip(",").strip("[").strip("]")))
					count+=1
					if count==5:
						for k in temp:
							feature.append(k)
						temp=[]
						count=0
			#print feature
			x_train.append(feature)
	print kk
	return x_train
	
grid=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,2218,811,4166,2603,4331,3992]
grid_x=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,0,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,0,2218,811,4166,0,0,2603,4331,3992,0,0,0,0,0]
#grid=[3862,3198,3056,2762,2462,2124,1999,1061,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,2218,811,4166,2603,4331,3992]

grid_dict={}
index=0
for i in grid_x:
	grid_dict[i]=index
	index+=1
with open(os.path.join("spatialmodel","featuresTrain.txt"),"r") as f:
	xtrain=f.readlines()
#print xtrain
with open(os.path.join("spatialmodel","LabelTrain.txt"),"r") as f:
	ytrain=f.readlines()
with open(os.path.join("spatialmodel","featuresTest.txt"),"r") as f:
	xtest=f.readlines()
with open(os.path.join("spatialmodel","LabelTest.txt"),"r") as f:
	ytest=f.readlines()
x_train=[]
x_test=[]
y_train=[]
y_test=[]
x_train=dataset(xtrain,x_train)
x_test=dataset(xtest,x_test)
y_train=datasetlabel(ytrain,y_train)
y_test=datasetlabel(ytest,y_test)
print len(y_test),len(x_test)
#y_test=dataset(ytest,y_test)
#print x_train
print("start")
clf = MLPClassifier( solver='adam',activation='tanh',alpha=0.0012,learning_rate_init=0.0001,max_iter=800,hidden_layer_sizes=(7,),verbose=True,beta_1=0.75,beta_2=0.72,shuffle=True)
clf.fit(x_train, y_train)
joblib.dump(clf, 'clf.pkl')
pre=clf.predict_proba(x_test)
print pre
#print len(pre),len(ytest)
#y_pre_report=np.array([])
for i in range(len(pre)):
	m=np.max(pre[i],axis=0)
	maxnum=np.divide(pre[i],np.ones(5)*m).astype(np.int32)
	#print maxnum
	
	if not i==0:
		y_pre_report=np.row_stack((y_pre_report,maxnum))
		
	else:
		y_pre_report=maxnum
m=0
for i in range(len(ytest)):
	if ytest[i].strip("\n")=="null":
		with open(os.path.join(os.path.join("spatialmodel","result"),"probability_ann.txt"),"a+") as f:
			f.write("null"+"\n")
	else:
		with open(os.path.join(os.path.join("spatialmodel","result"),"probability_ann.txt"),"a+") as f:
			#print m
			ls=[float(item) for item in pre[m]]
			for it in range(len(ls)):
				if "e" in str(ls[it]):
					ls[i]=0
			f.write(str(ls)+"\n")
			m+=1
#print clf.predict(x_test)
#print y_test[0]
target_names=["G","M","US","U","VU-H"]
labels=[0,1,2,3,4]
#print y_test
#labels=[[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]
print (classification_report(np.array(y_test),y_pre_report,target_names=target_names,labels=labels))
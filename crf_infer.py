# -*- coding: UTF-8 -*- 
from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import os
import numpy as np

class crffeature:
	def __init__(self,i):
		self.features=[]
		self.temperature=0
		self.humidity=0
		self.pressure=0
		self.wind_speed=0
		self.speed=0.0
		self.label=""
		self.hour=i+1
	def weafeatures(self,line):
		if line=="None":
			self.features=[]
			self.label=""
		else:
			#print "k"
			elem=line.split(" ")
			for i in range(len(elem)):
				if i>=2:
					ele = elem[i].split("_")
					if ele[0]=="Temperature":
						if not ele[1]=="None":
							self.temperature=float(ele[1])
						else: 
							self.label=None
							break
					if ele[0]=="Humidity":
						if not ele[1]=="None":
							self.humidity=int(ele[1])
						else: 
							self.label=None
							break
					if ele[0]=="Pressure":
						if not ele[1]=="None":
							self.pressure=int(ele[1])
						else: 
							self.label=None
							break
					if ele[0]=="Wind":
						if not ele[1]=="None":
							self.wind_speed=int(ele[1])
						else: 
							self.label=None
							break
					'''
					if ele[0]=="PM10":
						if not ele[1]=="None":
							pm10=int(ele[1])
							#print self.hour
							#print pm10
							if pm10<=50:
								self.label="G" 
							else:
								if pm10<=100:
									self.label="M"
								else:
									if pm10<=150:
										self.label="US"
									else:
										if pm10<=200:
											self.label="U"
										else:
											if pm10<=300:
												self.label="VU"
											else:
												if pm10<=500:
													self.label="H"
						else: 
							self.label=None
							break
					'''
	def setspeed(self,line):
		speedlist=[]
		items=line.strip("\n").split(" ")
		if not len(items)==1:
			for i in range(len(items)):
				itemlist=items[i].split("_")
				if i==0:
					if not itemlist[2]=="ns" and itemlist[2]=="UN" and itemlist[2]=="0" and itemlist[2]=="statuser":
						speedlist.append(float(itemlist[2]))
				else:
					if not itemlist[1]=="ns" and itemlist[1]=="UN" and itemlist[1]=="0" and itemlist[1]=="statuser":
						speedlist.append(float(itemlist[1]))
			if not len(speedlist)==0:
				self.speed=sum(speedlist)/len(speedlist)
		else:
			self.speed=0.0
	def setfeatures(self):
		self.features = [
		'temperature=%d' % self.temperature,
		'humidity=%d' % self.humidity,
		'pressure=%d' % self.pressure,
		'wind_speed=%d' % self.wind_speed,
		"speed=%f" %self.speed,
		]
		#print self.features
	

def bio_classification_report(y_true, y_pred):
	"""
	Classification report for a list of BIO-encoded sequences.
	It computes token-level metrics and discards "O" labels.
	
	Note that it requires scikit-learn 0.15+ (or a version from github master)
	to calculate averages properly!
	"""
	'''
	lb = LabelBinarizer()
	y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
	y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))
	#print y_true
	#print len(y_true_combined),len(y_pred_combined)
	tagset = set(lb.classes_) - {'O'}
	tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
	class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}
	'''
	y_true_combined=[]
	y_pred_combined=[]
	label_dict={"G":[1,0,0,0,0],"M":[0,1,0,0,0],"US":[0,0,1,0,0],"U":[0,0,0,1,0],"VU-H":[0,0,0,0,1]}
	for i in range(len(y_true)):
		for j in range(len(y_true[i])):
			y_true_combined.append(label_dict[y_true[i][j]])
	for i in range(len(y_pred)):
		for j in range(len(y_pred[i])):
			y_pred_combined.append(label_dict[y_pred[i][j]])
				
	target_names=["G","M","US","U","VU-H"]
	#labels=[0,1,2,3,4,5]
	return classification_report(
		np.array(y_true_combined),
		np.array(y_pred_combined),
		#labels = [class_indices[cls] for cls in tagset],
		target_names = target_names
	)
insts=[]
inststest=[]
index_empty=[]
dates=["0226_1030","0226_1230","0226_1330","0226_1530","0226_1630"]
#dates=["0225"]
#dates=["0225","0226","0227","0228","0302","0303","0323","0324","0326","0327","0328","0331","0401","0402","0403","0404","0405","0406","0407","0408","0409","0410","0411","0412","0413"]

grid=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,0,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,0,2218,811,4166,0,0,2603,4331,3992,0,0,0,0,0]
#print len(grid)
hours=0
speedlist=[]
alline=[]
for date in dates:
	print date
	filename=os.path.join(os.path.join("crawl","infer"),"aqi_"+date+".txt")
	#print filename
	#print filelist
	
	
	filecrawlname=os.path.join(os.path.join(os.path.join("crawl","infer"),date),"speed.txt")
	#print filecrawlname
	with open(filecrawlname,"r") as f:
		#listname="allcrawlline"+str(i)
		listname=f.readlines()
		speedlist.append(listname)
		hours+=1

	#print len(speedlist)
	with open(filename,"r")as f:
		alline+=f.readlines()
		
print hours
grid_true=[item-1 for item in grid]
print grid_true
circle=len(listname)
for k in range(len(listname)):
	
	for i in range(hours):
		
		ins=crffeature(i)
		#print alline[i*circle+k]
		ins.weafeatures(alline[i*circle+k])
		#ins.setspeed()
		if not ins.label==None:
			
			#print len(speedlist[i]),grid[k]
			ins.setspeed(speedlist[i][k])
			ins.setfeatures()
			inststest.append(ins)
			#print ins.hour,k
		else:
			index="hour_"+str(i)+" line_"+str(k)#from 0
			index_empty.append(index)
			#print i
	if not inststest[-1].features==[]:
		ins_empty=crffeature(i)
		ins_empty.weafeatures("None")
		inststest.append(ins_empty)
			
				
	#for ob in insts:
		#print ob.features

x_test=[]
y_test=[]
l1=[]


for item in inststest:
	if not item.features==[]:
		l1.append(item.features)
	else:
		x_test.append(l1)
		l1=[]

for item in inststest:
	if not item.label=="":
		l1.append(item.label)
	else:
		y_test.append(l1)
		l1=[]
#print y_test
tagger = pycrfsuite.Tagger()
tagger.open('temporalmodel.crfsuite')
#y_pred = [tagger.tag(xseq) for xseq in x_test]
label=["G","M","US","U","VU-H"]

#print len(inststest)
pro=[]
#print y_pred
y_pred=[]
ww=[]
www=[]
print len(y_test)
for xseq in x_test:
	temp1=[]
	lb=tagger.tag(xseq)
	y_pred.append(lb)
	ww=[]
	for j in range(len(xseq)):
		temp=[]
		for k in label:
			#print tagger.marginal(k,j)
			temp.append(tagger.marginal(k,j))
		temp1.append(temp)
		#print temp1
		ww.append(temp.index(max(temp)))
		#print ww[-1]
	#print temp1
	#print "\n"
	pro.append(temp1)
	www.append(ww)

#
#print pro
#print y_pred
#print y_test
#print www
#print index_empty
with open(os.path.join(os.path.join("infer","result"),"empty_crf.txt"),"a+") as f:
	for item in index_empty:
		f.write(item+"\n")
with open(os.path.join(os.path.join("infer","result"),"crf.txt"),"a+") as f:
	for item in pro:
		for i in item:
			f.write(str(i)+"\n")
		f.write("\n")
#print y_test
print len(y_test),len(y_pred)
print(bio_classification_report(y_test, y_pred))
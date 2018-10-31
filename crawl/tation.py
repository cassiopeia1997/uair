# #coding:utf-8  
import urllib  
import urllib2 
import json
import jsonpath
from math import*
import sys
import time


class analysishtml:
	def __init__(self):
		self.aqi={}
	def getway(self,url):
		req = urllib2.Request(url) 
		response = urllib2.urlopen(req)
		html=response.read()
		unicodestr=json.loads(html)
		self.aqi=unicodestr
		#print(self.aqi)


		#print(self.length,self.count)


with open("ss.txt","r") as f:
	for line in f.readlines():
		boundary=line.strip("\n").split(" ")
		time_1=sys.argv[1]
		time_2=sys.argv[2]
		i=0
		#print(time_1,time_2)
		url="http://www.uairquality.com/U_Air/SearchStation?Latitude="+boundary[0]+"&Longitude="+boundary[1]+"&Standard=0&time="+time_1+"&Culture=zh-CN&_="+time_2
		#print i
		a1=analysishtml()
		a1.getway(url)
		with open("weather.txt","a+") as f1:
			for j in a1.aqi:
				if not j=="Name":
					f1.write(j+"_"+str(a1.aqi[j]))
					i+=1
					#print(j)
				else:
					#print a1.aqi[j]
					pass
				if not i==13:
					f1.write(" ")
			f1.write("\n")

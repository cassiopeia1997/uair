# #coding:utf-8  
import urllib  
import urllib2 
import json
import jsonpath
from math import*
import sys
class analysishtml:
	def __init__(self):
		self.aqi=[]
		#self.time=None
	def getway(self,url):
		req = urllib2.Request(url) 
		response = urllib2.urlopen(req)
		html=response.read()
		unicodestr=json.loads(html)
		self.aqi=unicodestr["Stations"]
		time=unicodestr["UpdateTime"]
		print(time)


		#print(self.length,self.count)



time_1=sys.argv[1]
time_2=sys.argv[2]
#print(time_1,time_2)
url="http://www.uairquality.com/U_Air/ChangeCity?CityId=001&Standard=0&time="+time_1+"&_="+time_2
#print i
a1=analysishtml()
a1.getway(url)
i=0
with open("crawl_station.txt","a+") as f1:
	for item in a1.aqi:
		for j in item:
			f1.write(j+"_"+str(item[j]))
			i+=1
			if not i==9:
				f1.write(" ")
		f1.write("\n")

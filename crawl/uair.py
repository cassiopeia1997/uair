# #coding:utf-8  
import urllib  
import urllib2 
import json
import jsonpath
from math import*
import sys
class analysishtml:
	def __init__(self):
		self.aqi={}
	def getway(self,url):
		#req = urllib2.Request(url) 
		#response = urllib2.urlopen(req)
		#html=response.read()
		html=self.getUrl_multiTry(url)
		unicodestr=json.loads(html)
		self.aqi=unicodestr
		#print(self.aqi)


		#print(self.length,self.count)
	def getUrl_multiTry(self,url):  
		user_agent ='"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'  
		headers = { 'User-Agent' : user_agent }  
		maxTryNum=10  
		for tries in range(maxTryNum):  
			try:  
				req = urllib2.Request(url, headers = headers)   
				html=urllib2.urlopen(req).read()  
				break  
			except:  
				if tries <(maxTryNum-1):  
					continue  
				else:  
					logging.error("Has tried %d times to access url %s, all failed!",maxTryNum,url)  
					break  
		return html  

with open("grid_p1.json","r") as f:
	for line in f.readlines():
		boundary=line.strip("\n").split(" ")
		time_1=sys.argv[1]
		time_2=sys.argv[2]
		i=0
		#print(time_1,time_2)
		url="http://www.uairquality.com/U_Air/SearchGeoPoint?Latitude="+str((float(boundary[0])+float(boundary[1]))/2)+"&Longitude="+str((float(boundary[2])+float(boundary[3]))/2)+"&Standard=0&time="+time_1+"&Culture=zh-CN&_="+time_2
		#print url
		a1=analysishtml()
		a1.getway(url)
		with open("aqi.txt","a+") as f1:
			for j in a1.aqi:
				f1.write(j+"_"+str(a1.aqi[j]))
				i+=1
				if not i==13:
					f1.write(" ")
			f1.write("\n")

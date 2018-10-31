# #coding:utf-8  
import urllib  
import urllib2 
import json
import jsonpath
class analysishtml:
	def __init__(self,url):
		self.url=url
	def getpoi(self):
		req = urllib2.Request(self.url) 
		response = urllib2.urlopen(req)
		html=response.read()
		unicodestr=json.loads(html)
		return len(unicodestr["pois"])

types="010000|030000|150000|170300|060000|050000|080000|110000|140000|170100|170200|100000|120000"
poi_sum_list=[]
with open("poi.txt","r") as f1:
	for line in f1.readlines():
		poi_sum=0
		poi=line.strip("\n").split(" ")
		#print(poi)
		for item in poi:
			#print(item)
			poi_sum+=int(item)
			poi_sum_list.append(poi_sum)
		#print(poi_sum)
	f1.close()

with open("grid_p1.json","r") as f:
	for line in f.readlines():
		boundary=line.strip("\n").split(" ")
		poi_vacant_count=0
		diff_log=(float(boundary[2])-float(boundary[3]))/10
		diff_lat=(float(boundary[0])-float(boundary[1]))/10
		#print(diff_log,diff_lat)
		log_origin=float(boundary[3])
		lat_origin=float(boundary[1])
		for i in range(10):
			
			lat=diff_lat+lat_origin
			for j in range(10):
				
				log=diff_log+log_origin
				url="http://restapi.amap.com/v3/place/polygon?polygon="+str(log_origin)+","+str(lat_origin)+";"+str(log)+","+str(lat)+"&types="+types+"&output=json&key=8d41d63726bbf7c6d07c43f78244aed8"
				a1=analysishtml(url)
				log_origin=log
				#print url
				if a1.getpoi()==0:
					poi_vacant_count+=1
			lat_origin=lat
		with open("poi_vacant.txt","a+")as f1:
			f1.write(str(poi_vacant_count))
			f1.write("\n")

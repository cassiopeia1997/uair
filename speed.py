# #coding:utf-8  
import urllib  
import urllib2 
import json
import jsonpath
from math import*
class analysishtml:
	def __init__(self):
		self.dis_list=[]
	def getway(self,url,level,boundary):
		req = urllib2.Request(url) 
		response = urllib2.urlopen(req)
		html=response.read()
		unicodestr=json.loads(html)
		if "trafficinfo" in unicodestr:
			road_list=unicodestr["trafficinfo"]["roads"]
			self.dis_list=[]
			#print(url,road_list)
			for item in road_list:
				dis=0
				if "polyline" in item:
					points=item["polyline"].split(";")
					for i in range(len(points)-1):
						p1=points[i].split(",")
						p2=points[i+1].split(",")
						#dis+=self.haversine(float(p1[0]),float(p1[1]),float(p2[0]),float(p2[1]))
						#print (url,dis,float(p1[0]),float(p1[1]),float(p2[0]),float(p2[1]))
						#print i
						if float(p1[0])>float(boundary[2])or float(p2[0])>float(boundary[2]) :
							break
						else:
							if float(p1[0])<float(boundary[3]):
								continue
							else:
								#print(p1[0],p2[0])
								if float(p1[1])<=float(boundary[0]) and float(p1[1])>=float(boundary[1]):
									if float(p2[1])<=float(boundary[0]) and float(p2[1])>=float(boundary[1]):
										if "speed" in item:
											dis=item["speed"]
											#self.dis_list.append(level+"_"+str(dis))
											break
										else:
											dis="ns"
											break
				else:
					dis="statuser"
				self.dis_list.append(level+"_"+str(dis))
										#print (p1,p2)
				
				
				
				
				
				#self.dis_list.append(level+"_"+str(dis))
		else:
			self.dis_list.append("UN")
		


		#print(self.length,self.count)


with open("grid_p1.json","r") as f:
	for line in f.readlines():
		boundary=line.strip("\n").split(" ")
		with open("speed.txt","a+") as f1:
			f1.write("speed_")
			f1.close()
		i=3
		while (i==3 or i==6):
			url="http://restapi.amap.com/v3/traffic/status/rectangle?rectangle="+boundary[3]+","+boundary[1]+";"+boundary[2]+","+boundary[0]+"&level="+str(i)+"&extensions=all&output=json&key=e64599546fed7d8dd6fd8c9e3b3949c3"
			print url
			a1=analysishtml()
			a1.getway(url,str(i),boundary)
			with open("speed.txt","a+") as f1:
				#f1.write("roadinfo_")
				max=len(a1.dis_list)
				for j in range(max):
					if i==6 and j==max-1:
						f1.write(a1.dis_list[j])
					else:
						f1.write(a1.dis_list[j]+" ")
			if i==3:
				i=6
			else:
				i=0
		with open("speed.txt","a+") as f1:
			f1.write("\n")
			f1.close()
		#print(poi_sum)

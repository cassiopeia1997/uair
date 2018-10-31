# #coding:utf-8  
import urllib  
import urllib2 
import json
import jsonpath
class analysishtml:
	def __init__(self):
		self.count=0
		self.length=0
	def getpoi(self,url):
		req = urllib2.Request(url) 
		response = urllib2.urlopen(req)
		html=response.read()
		unicodestr=json.loads(html)
		self.length=len(unicodestr["pois"])
		self.count+=self.length
		#print(self.length,self.count)

types=["010000|030000","150000","170300","060000","050000","080000","110000","140000","170100|170200","100000|120000"]

with open("grid_p1.json","r") as f:
	for line in f.readlines():
		boundary=line.strip("\n").split(" ")
		poi_sum=""
		for i in range(10):
			url="http://restapi.amap.com/v3/place/polygon?polygon="+boundary[3]+","+boundary[1]+";"+boundary[2]+","+boundary[0]+"&types="+types[i]+"&offset=25&output=json&key=8d41d63726bbf7c6d07c43f78244aed8"
			a1=analysishtml()
			a1.getpoi(url)
			check_page=a1.length
			page_num=1
			#print(url)
			while(check_page==25):
				page_num+=1
				url1="http://restapi.amap.com/v3/place/polygon?polygon="+boundary[3]+","+boundary[1]+";"+boundary[2]+","+boundary[0]+"&types="+types[i]+"&page="+str(page_num)+"&offset=25&output=json&key=8d41d63726bbf7c6d07c43f78244aed8"
				a1.getpoi(url1)
				check_page=a1.length
			poi_sum+=str(a1.count)
			if not i==9:
				poi_sum+=" "
			#print(a1.getpoi(types[i]))
		with open("poi.txt","a+") as f1:
			f1.write(poi_sum+'\n')
		#print(poi_sum)

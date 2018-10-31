# #coding:utf-8  
import urllib  
import urllib2 
import json
import jsonpath
class analysishtml:
	def __init__(self):
		self.poi={}
		self.result_count=[0,0,0,0,0,0,0,0,0,0]
	def getpoi(self,url):
		req = urllib2.Request(url) 
		response = urllib2.urlopen(req)
		html=response.read()
		unicodestr=json.loads(html)
		self.poi=unicodestr

	def getlength(self):
		return len(self.poi)
	def getpoicount(self):
		result=self.poi["pois"]
		for item in result:
			cmp=item["typecode"][0:2]
			cmp1=item["typecode"][0:4]
			if cmp=="01" or  cmp=="03":
				self.result_count[0]+=1
			if cmp=="15":
				self.result_count[1]+=1
			if cmp1=="1703":
				self.result_count[2]+=1
			if cmp=="06":
				self.result_count[3]+=1
			if cmp=="05":
				self.result_count[4]+=1
			if cmp=="08":
				self.result_count[5]+=1
			if cmp=="11":
				self.result_count[6]+=1
			if cmp=="14":
				self.result_count[7]+=1
			if cmp1=="1701" or cmp1=="1702":
				self.result_count[8]+=1
			if cmp=="10" or  cmp=="12":
				self.result_count[9]+=1
			

types=["010000|030000","150000","170300","060000","050000","080000","110000","140000","170100|170200","100000|120000"]
type_search="010000|030000|150000|170300|060000|050000|080000|110000|140000|170100|170200|100000|120000"
with open("grid.json","r") as f:
	for line in f.readlines():
		boundary=line.strip("\n").split(" ")
		poi_sum=""
		page_num=1
		url="http://restapi.amap.com/v3/place/polygon?polygon="+boundary[3]+","+boundary[1]+";"+boundary[2]+","+boundary[0]+"&types="+type_search+"&output=json&offset=25&key=cfc1b3c98acdf8f67d2290adde8fd724"
		a1=analysishtml()
		a1.getpoi(url)
		a1.getpoicount()
		check_page=a1.getlength()
		while (check_page==25):
			page_num+=1
			url1="http://restapi.amap.com/v3/place/polygon?polygon="+boundary[3]+","+boundary[1]+";"+boundary[2]+","+boundary[0]+"&types="+type_search+"&page="+str(page_num)+"&output=json&offset=25&key=cfc1b3c98acdf8f67d2290adde8fd724"
			a1.getpoi(url1)
			if not check_page==0:
				a1.getpoicount()
			check_page=a1.getlength()
			
		with open("poi.txt","a+") as f1:
			for i in range(10):
				f1.write(str(a1.result_count[i]))
				if not i==9:
					f1.write(" ")
			f1.write("\n")

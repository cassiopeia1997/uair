# #coding:utf-8  

 
import urllib  
import urllib2 
import json
import jsonpath
  
url = "http://www.uairquality.com/U_Air/GetAllCity?CityId=001&Standard=0&category=0&station=true&Lat_bottom=39.61481594895395&Lat_up=40.16484091687096&Lng_left=115.68412060839846&Lng_right=117.10822339160158&time=1518191563236&_=1518191029877"  
"""
areaCode:110000
roadId:1100000san1li3tun2lu4
startDate:0
timeSize:5
"""
"""
value = {}  
value['areaCode'] = '110000'  
value['roadId'] = '1100000san1li3tun2lu4'  
value['startDate'] = '0' 
value['timeSize'] = '5' 
data = urllib.urlencode(value)  
"""
#req = urllib2.Request(url, data)  
req = urllib2.Request(url) 
response = urllib2.urlopen(req)
html=response.read()
unicodestr=json.loads(html)
latmax_list=jsonpath.jsonpath(unicodestr,"$.AllCity.*.Lat_max")
latmin_list=jsonpath.jsonpath(unicodestr,"$.AllCity.*.Lat_min")
lngmax_list=jsonpath.jsonpath(unicodestr,"$.AllCity.*.Lng_max")
lngmin_list=jsonpath.jsonpath(unicodestr,"$.AllCity.*.Lng_min")
#$..Lat_max,$..Lat_min,$..Lng_max,$..Lng_min
array0=json.dumps(latmax_list,ensure_ascii=False).strip('[').strip(']').split(',')
array1=json.dumps(latmin_list,ensure_ascii=False).strip('[').strip(']').split(',')
array2=json.dumps(lngmax_list,ensure_ascii=False).strip('[').strip(']').split(',')
array3=json.dumps(lngmin_list,ensure_ascii=False).strip('[').strip(']').split(',')
with open("grid.json","w") as f:  
    for i in range(len(latmax_list)):
        f.write(array0[i].encode("utf-8").strip(' ')+' ') 
        f.write(array1[i].encode("utf-8").strip(' ')+' ') 
        f.write(array2[i].encode("utf-8").strip(' ')+' ') 
        f.write(array3[i].encode("utf-8").strip(' ')+'\n') 
        
   
#print response.read().decode('utf-8') 
# #coding:utf-8  
from math import radians, cos, sin, asin, sqrt
import numpy as np
import random
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from scipy import stats

grid=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,2218,811,4166,2603,4331,3992]
grid_x=[3862,3198,3056,2762,2462,1658,2124,1999,2051,1061,0,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,0,2218,811,4166,0,0,2603,4331,3992,0,0,0,0,0]
grid_dict={}
index=0
for i in grid_x:
	grid_dict[i]=index
	index+=1
print grid_dict
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）

	# 将十进制度数转化为弧度
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine公式
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	r = 6371 # 地球平均半径，单位为公里
	return c * r * 1000
def getfr(listroad):
	highway=0
	totalroad=0
	for item in listroad:
		line=item.split("_")
		
		if line[-1]=="UN":
			continue
		else:
			#print line
			if len(line)==3:
				if line[1]=="3":
					if not line[2]=="statuser":
						highway+=float(line[2])
				else:
					if line[1]=="6":
						if not line[2]=="statuser":
							totalroad+=float(line[2])
			else:
				#print line[0],line[1]
				#print line[1]==""
				if len(line)==2:
					if line[0]=="3":
						if not line[1]=="statuser" :
							highway+=float(line[1])
					else:
						if line[0]=="6":
							if not line[1]=="statuser" :
								#print line[1]
								totalroad+=float(line[1])
	result=[highway,totalroad]
	return result
	#print i,highway,totalroad


'''
lo1 = float(input('Longitude1:'))
la1 = float(input('Latitude1:'))
lo2 = float(input('Longitude2:'))
la2 = float(input('Latitude2:'))

print(haversine(lo1, la1, lo2, la2))
'''

with open(os.path.join("crawl","ss.txt"),"r") as f:
	lat_log=f.readlines()
	f.close()
with open ("roadnet.txt","r") as f:
	roadnet=f.readlines()
	f.close()
with open("poi.txt","r") as f:
	poi=f.readlines()
	f.close()
with open("poi_vacant.txt","r") as f:
	poi_vacant=f.readlines()
	f.close()
with open("grid_test.txt","r") as f:
	infer=f.readlines()
with open("grid_choice.txt", "r") as f:
	choice=f.readlines()
with open("spatial_features_test.txt","a+") as f:
	for i in range(len(infer)):
		infergrid=infer[i].strip("\n")
		grids=choice[i].strip("\n").split(" ")
		linegrid2=grid_dict[int(infergrid)]
		lat_long2=lat_log[linegrid2].strip("\n").split(" ")
		fr2=np.array(getfr(roadnet[linegrid2].strip("\n").split(" ")))
		fp2=np.append(np.array(map(int,poi[linegrid2].strip("\n").split(" "))),np.array([int(poi_vacant[linegrid2].strip("\n"))]))
		for item in grids:
			linegrid1=grid_dict[int(item)]
			lat_long1=lat_log[linegrid1].strip("\n").split(" ")
			geo_dis=haversine(float(lat_long1[0]),float(lat_long1[1]),float(lat_long2[0]),float(lat_long2[1]))
			fr1=np.array(getfr(roadnet[linegrid1].strip("\n").split(" ")))
			fp1=np.append(np.array(map(int,poi[linegrid1].strip("\n").split(" "))),np.array([float(poi_vacant[linegrid1].strip("\n"))/100]))
			#print fr1,fr2
			#print fp1,fp2
			#pearsonfr=stats.pearsonr(fr1,fr2)
			pearsonfp=stats.pearsonr(fp1, fp2)
			diffp=abs(fr1[0]-fr2[0])
			#print pearsonfp
			f.write(str(geo_dis)+" "+str(pearsonfp[0])+" "+str(diffp)+"\n")




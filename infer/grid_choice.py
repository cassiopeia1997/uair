import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

grid=[3862,3198,3056,2762,2462,2124,1999,1061,3063,2626,2699,2770,2197,2619,2624,2273,2341,863,1524,2218,811,4166,2603,4331,3992]
'''
with open ("roadnet.txt","r") as f:
	roadnet=f.readlines()
	f.close()
with open("poi.txt","r") as f:
	poi=f.readlines()
	f.close()
with open("poi_vacant.txt","r") as f:
	poi_vacant=f.readlines()
	f.close()
'''
#grid_total3=[]

grid_used=[]
times=1
used_max=2
while(times<=5000):
	used=0
	temp_list=random.sample(grid,3)
	check=1
	record=0
	for item in temp_list:
		if item in grid_used:
			used+=1
		if used<=2:
			grid_used.append(item)
			record+=1
			with open("grid_choice.txt","a+") as f:
				if record<3:
					f.write(str(item)+" ")
				else:
					f.write(str(item)+"\n")
				
		else:
			while(check==1):
				choice=random.sample(grid,1)
				if not choice in grid_used:
					check=0
			grid_used.append(choice[0])
			with open("grid_choice.txt","a+") as f:
				f.write(str(choice[0])+"\n")
	times+=1
	
		
	print times
	#print grid_used

#clf=MLPClassifier(hidden_layer_sizes=(9,),solver='lbfgs',max_iter=500)
#mlp.fit(x_train,y_train)

'''
with open("grid_choice.txt","r") as f:
	for line in f.readlines():
		grid_list=line.strip("\n").split(" ")
		check=1
		#print grid_list
		while (check==1):
			infer_grid=random.sample(grid,1)
			if not infer_grid[0] in grid_list:
				with open("grid_infer.txt","a+") as f1:
					f1.write(str(infer_grid[0])+"\n")
					check=0
'''

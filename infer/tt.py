with open("grid.json","r") as f:
	for line in f.readlines():
		boundary=line.strip("\n").split(" ")
		
		with open("grid.txt","a+") as f1:
			f1.write(str((float(boundary[0])+float(boundary[1]))/2)+" "+str((float(boundary[2])+float(boundary[3]))/2))
			f1.write("\n")

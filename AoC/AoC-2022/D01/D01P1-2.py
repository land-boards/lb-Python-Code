""" 
D01P1-2
"""

fileName="input.txt"
maxCal = 0
accum = 0
calsList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		if inLine != '':
			val = int(inLine)
			accum += val
			print("accum",accum)
		else:
			print("Accum",accum)
			calsList.append(accum)
			if accum > maxCal:
				maxCal = accum
				print("New max",maxCal)
			accum = 0
print("Max",maxCal)
print("calsList",calsList)
print("calsList",sorted(calsList))
sList = sorted(calsList)
print("sList",sList)
print("sList",sList[-3:])
last3 = sList[-3:]
print(last3)
print("sum",last3[0]+last3[1]+last3[2])
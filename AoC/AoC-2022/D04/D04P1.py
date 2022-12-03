""" 
D02P1

"""

fileName = 'input.txt'
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		print(inLine)

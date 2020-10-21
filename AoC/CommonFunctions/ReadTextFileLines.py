def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			#inLine = inLine.split('x')
			inList.append(inLine)
	#print(inList)
	return inList

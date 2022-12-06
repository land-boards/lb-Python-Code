""" 
D06P1

"""

def compareRange(inStr):
	termCt=len(inStr)-1
	for currChar in range(termCt):
		for offChar in range(currChar+1,termCt):
			if inStr[currChar] == inStr[offChar]:
				return True
	# print(inStr)
	return False

fileName = 'input.txt'
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		print(inLine)
gotResult = False
rangeVal = 14
for offset in range(len(inLine)-rangeVal+1):
	if not compareRange(inLine[offset:offset+rangeVal]):
		if not gotResult:
			print(offset+rangeVal)
			gotResult = True
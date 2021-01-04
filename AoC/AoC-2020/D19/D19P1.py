""" 
2020 D19 P1
"""

# DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileOfStringsToListOfLists(inFileName):
	global DEBUG_PRINT		# need to put in each function
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	debugPrint('(readFileOfStringsToListOfLists): inList - ' + str(inList))
	return inList

def formatInputList(inList):
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	# Input = ['0: 4 1 5', '1: 2 3 | 3 2', '3: 4 5 | 5 4', 
	# Output = 
	for line in inList:
		if ':' in line:
			line = line.replace(' ', ',')
			line = line.replace(':', '')
			line = line.replace('"', '')
			sp = line.split(',')
			print('sp',sp)
			if len(sp) == 2:
				solvedDict[int(sp[0])] = sp[1]
			elif len(sp) == 3:
				unsolvedDict[int(sp[0])] = [[int(sp[1]),int(sp[2])]]
			elif len(sp) == 4:
				unsolvedDict[int(sp[0])] = [[int(sp[1]),int(sp[2])]]
			elif len(sp) == 6:
				unsolvedDict[int(sp[0])] = [[int(sp[1]),int(sp[2])],[int(sp[4]),int(sp[5])]]
			else:
				print('wtf-1')
		elif line != '':
			break
	return

# Program start
inList = readFileOfStringsToListOfLists('input1.txt')
print(inList)
solvedDict = {}
unsolvedDict = {}

formatInputList(inList)
DEBUG_PRINT = True
print('solvedDict',solvedDict)
print('unsolvedDict',unsolvedDict)

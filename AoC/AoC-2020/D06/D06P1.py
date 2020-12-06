DEBUG_PRINT = True
#DEBUG_PRINT = False

import itertools

DEBUG_PRINT = True
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings()
debugPrint(inList)
newList = []
newLine = ''
for row in inList:
	if row == '':
		newList.append(newLine)
		newLine = ''
	else:
		newLine += row
if newLine != []:
	newList.append(newLine)
debugPrint(newList)
totalCount = 0
countPerSet = 0
for row in newList:
	listOfChars = []
	for c in row:
		if c not in listOfChars:
			listOfChars.append(c)
	debugPrint('chars in row')
	debugPrint(listOfChars)
	countPerSet = len(listOfChars)
	totalCount += countPerSet
	debugPrint(countPerSet)
	
print('totalCount',totalCount)

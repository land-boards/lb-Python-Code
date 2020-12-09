import itertools
# 23278925 too high

DEBUG_PRINT = True
DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(int(line.rstrip()))
	return inList

preambleLength = 25
inList = readFileToListOfStrings()
DEBUG_PRINT = True
debugPrint(inList)
DEBUG_PRINT = False
listLen = len(inList)
debugPrint('inList length' + str(listLen))
preambleOffset = 0
listOffset = preambleLength
noMatchVal = 0
for checkIndex in range(preambleLength,listLen):
	#print('checking',inList[checkIndex],end = ' ')
	preambleSlice = inList[preambleOffset:preambleOffset+preambleLength]
	#print('preambleSlice',preambleSlice)
	preambleOffset += 1
	preamblePairs = list(itertools.combinations(preambleSlice,2))
	foundMatch = False
	for pair in preamblePairs:
		if inList[checkIndex] == sum(pair):
			#print('match',pair[0],pair[1])
			foundMatch = True
			break
	if (not foundMatch) and (noMatchVal == 0):
		debugPrint('no match'+str(inList[checkIndex]))
		noMatchVal = inList[checkIndex]
print('Looking for noMatchVal',noMatchVal)
DEBUG_PRINT = True
gotMatch = False
for countWidth in range(2,listLen):
	print('countWidth',countWidth)
	for valOffset in range(0,listLen-countWidth):
		sumVal = sum(inList[valOffset:valOffset+countWidth+1])
		print('sum of',inList[valOffset:valOffset+countWidth],'sumVal',sumVal)
		if sumVal == noMatchVal:
			matchSlice = inList[valOffset:valOffset+countWidth]
			print('matchSlice',matchSlice)
			print('slice',inList[valOffset],inList[valOffset+countWidth])
			print('minValue in match',min(matchSlice))
			print('maxValue in match',max(matchSlice))
			sum = min(matchSlice) + max(matchSlice)
			print('sum',sum)
			gotMatch = True
			break
	if gotMatch:
		break
		
		
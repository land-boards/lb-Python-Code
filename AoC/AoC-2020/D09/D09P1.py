import itertools
# 23278925 too high

DEBUG_PRINT = True
#DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(int(line.rstrip()))
	return inList

inList = readFileToListOfStrings()
debugPrint(inList)
listLen = len(inList)
print('inList length',listLen)
preambleLength = 25
preambleOffset = 0
listOffset = preambleLength
noMatchVal = 0
for checkIndex in range(preambleLength,listLen):
	print('checking',inList[checkIndex],end = ' ')
	preambleSlice = inList[preambleOffset:preambleOffset+preambleLength]
	print('preambleSlice',preambleSlice)
	preambleOffset += 1
	preamblePairs = list(itertools.combinations(preambleSlice,2))
	foundMatch = False
	for pair in preamblePairs:
		if inList[checkIndex] == sum(pair):
			print('match',pair[0],pair[1])
			foundMatch = True
			break
	if (not foundMatch) and (noMatchVal == 0):
		print('no match',inList[checkIndex])
		noMatchVal = inList[checkIndex]
print('noMatchVal',noMatchVal)

		
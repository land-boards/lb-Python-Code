# D08P2.py
# 2021 Advent of Code
# Day 8
# Part 2
# 1020919 is too low
# 1045624 not it

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

# 2 Active Wires = 1
# 3 Active Wires = 7
# 4 Active Wires = 4
# 5 Active Wires = 2, 3, 5
# 6 Active Wires = 0, 6, 9
# 7 Active Wires = 8

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			if line != '':
				inList.append(line.rstrip())
	return inList

def sortString(stringIn):
	charsInVal = sorted(stringIn)
	mergedChars = "".join(charsInVal)
	return mergedChars

def isShortInLonger(shorter,longer):
	for element in shorter:
		if element not in longer:
			return False
	return True
	
def mapDigits(digitsMapIn):
	# print("digitsMapIn",digitsMapIn,end=' ')
	sortedValsList = []
	for unsortedVal in digitsMapIn:
		sortedValsList.append(sortString(unsortedVal))
	remainingValsList = []
	remainingValsList = list(sortedValsList)
	valList = {}
	for sortedVal in sortedValsList:
		if len(sortedVal) == 2:
			valList[sortedVal] = 1
			oneVal = sortedVal
			remainingValsList.remove(oneVal)
		elif len(sortedVal) == 3:
			valList[sortedVal] = 7
			sevenVal = sortedVal
			remainingValsList.remove(sevenVal)
		elif len(sortedVal) == 4:
			valList[sortedVal] = 4
			fourVal = sortedVal
			remainingValsList.remove(fourVal)
		elif len(sortedVal) == 7:
			valList[sortedVal] = 8
			eightVal = sortedVal
			remainingValsList.remove(eightVal)
	for sortedVal in sortedValsList:
		if len(sortedVal) == 5:	# 2,3,5 > 2,5
			if isShortInLonger(oneVal,sortedVal):
				valList[sortedVal] = 3
				threeVal = sortedVal
				remainingValsList.remove(threeVal)
	for sortedVal in sortedValsList:
		if len(sortedVal) == 6:	# 0,6,9 > 0,9
			if not isShortInLonger(oneVal,sortedVal):
				valList[sortedVal] = 6
				sixVal = sortedVal
				remainingValsList.remove(sixVal)
	for sortedVal in remainingValsList:	# 0,9 > 9
		if len(sortedVal) == 6:
			if isShortInLonger(threeVal,sortedVal):
				valList[sortedVal] = 9
				nineVal = sortedVal
				remainingValsList.remove(nineVal)
	for sortedVal in remainingValsList:	# 9
		if len(sortedVal) == 6:
			valList[sortedVal] = 0
			zeroVal = sortedVal
			remainingValsList.remove(zeroVal)
	
	print("remainingValsList",remainingValsList)
	
	testVal = remainingValsList[0]
	segE = segInLongNotInShort(testVal,sixVal)	# 6 vs 2,5
	if segE:
		valList[remainingValsList[0]] = 5
		valList[remainingValsList[1]] = 2
	else:
		valList[remainingValsList[0]] = 2
		valList[remainingValsList[1]] = 5
	# print("valList",valList)
	return valList

def segInLongNotInShort(shorter,longer):
	print("shorter",shorter,"longer",longer)
	allIn = True
	for element in shorter:
		if element not in longer:
			allIn = False
	return allIn

inList = readFileToListOfStrings('input.txt')

newList = []
for row in inList:
	row1 = row.replace(' | ','|')
	newRow = row1.split('|')
	newList.append(newRow)

allDisplayVals = []
countVals = 0
listOfVals = []
for row in newList:
	digitsMapIn = row[0].split(' ')
	displayVals = row[1].split(' ')
	digitsMapOut = mapDigits(digitsMapIn)
	segs1000 = sortString(displayVals[0])
	segs100 = sortString(displayVals[1])
	segs10 = sortString(displayVals[2])
	segs1 = sortString(displayVals[3])
	dig1000	= digitsMapOut[segs1000]
	dig100	= digitsMapOut[segs100]
	dig10	= digitsMapOut[segs10]
	dig1	= digitsMapOut[segs1]
	val = (1000*dig1000) + (100*dig100) + (10*dig10) + dig1
	listOfVals.append(val)
print("listOfVals",listOfVals)
print("List of nums length",len(listOfVals))
sumVal = 0
for countVal in listOfVals:
	sumVal += countVal
print("sumVal",sumVal)

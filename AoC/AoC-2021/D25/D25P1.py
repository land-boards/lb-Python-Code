# D25P1.py
# 2021 Advent of Code
# Day 25
# Part 1

def readFileOfStringsToListOfLists(fileName):
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip('\n')
			inList.append(list(inLine))
	return inList

def emptyOutList(inList):
	outArray = []
	for row in inList:
		newRow = []
		for col in row:
			newRow.append('.')
		outArray.append(newRow)
	return outArray

def printHerd(inList):
	for row in inList:
		for col in row:
			print(col,end='')
		print()

def moveHerdEast(inList):
	outList = emptyOutList(inList)
	lastColNumber = len(inList[0]) - 1
	for yOffset in range(len(inList)):
		xOffset = 0
		while xOffset < len(inList[0]):
			if inList[yOffset][xOffset] == '>':
				if xOffset != lastColNumber:
					if inList[yOffset][xOffset+1] == '.':
						outList[yOffset][xOffset] = '.'
						outList[yOffset][xOffset+1] = '>'
						xOffset += 1
					else:
						outList[yOffset][xOffset] = inList[yOffset][xOffset]
				else:
					if inList[yOffset][0] == '.':
						outList[yOffset][xOffset] = '.'
						outList[yOffset][0] = '>'
					else:
						outList[yOffset][xOffset] = inList[yOffset][xOffset]
			else:
				outList[yOffset][xOffset] = inList[yOffset][xOffset]
			xOffset += 1
	return outList

def moveHerdSouth(inList):
	outList = emptyOutList(inList)
	lastRowNum = len(inList) -1
	for xOffset in range(len(inList[0])):
		yOffset = 0
		while yOffset < len(inList):
			if inList[yOffset][xOffset] == 'v':
				if yOffset != lastRowNum:
					if inList[yOffset+1][xOffset] == '.':
						outList[yOffset][xOffset] = '.'
						outList[yOffset+1][xOffset] = 'v'
						yOffset += 1
					else:
						outList[yOffset][xOffset] = inList[yOffset][xOffset]
				else:
					if inList[0][xOffset] == '.':
						outList[yOffset][xOffset] = '.'
						outList[0][xOffset] = 'v'
					else:
						outList[yOffset][xOffset] = inList[yOffset][xOffset]
			else:
				outList[yOffset][xOffset] = inList[yOffset][xOffset]
			yOffset += 1
	return outList

def transformList(inList):
	saveList = list(inList)
	count = 0
	# printHerd(inList)
	while True:
		inList = moveHerdEast(inList)
		inList = moveHerdSouth(inList)
		if saveList != inList:
			count += 1
			# print("\nAfter",count,"step")
			saveList = list(inList)
			# printHerd(inList)
		else:
			break
		break
	return inList

inList =  readFileOfStringsToListOfLists('input.txt')

newList = inList
stillRunning = True
loopCount = 0
while stillRunning:
	tranList = transformList(newList)
	loopCount += 1
	if tranList == newList:
		stillRunning = False
	else:
		newList = []
		newList = tranList
	# print(loopCount)
printHerd(inList)
print("loopCount",loopCount)

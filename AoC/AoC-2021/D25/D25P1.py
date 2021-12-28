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
	for yOffset in range(len(inList)):
		for xOffset in range(len(inList[0])-1):
			if inList[yOffset][xOffset] == '>':
				if inList[yOffset][xOffset+1] == '.':
					outList[yOffset][xOffset] = '.'
					outList[yOffset][xOffset+1] = '>'
				else:
					outList[yOffset][xOffset] = inList[yOffset][xOffset]
			elif outList[yOffset][xOffset] != '>':
				outList[yOffset][xOffset] = inList[yOffset][xOffset]
		if inList[yOffset][len(inList[0])-1] == '>':
			if inList[yOffset][0] =='.':
				outList[yOffset][0] = inList[yOffset][len(inList[yOffset])-1]
				outList[yOffset][len(inList[yOffset])-1] = '.'
			else:
				outList[yOffset][len(inList[yOffset])-1] = inList[yOffset][len(inList[yOffset])-1]
		else:
			outList[yOffset][len(inList[yOffset])-1] = inList[yOffset][len(inList[yOffset])-1]
	return outList

def moveHerdSouth(inList):
	debugSouth = False
	outList = emptyOutList(inList)
	for xOffset in range(len(inList[0])):
		if debugSouth:
			print("\ncolCount",xOffset)
		for yOffset in range(len(inList)-1):
			if debugSouth:
				print("yOffset",yOffset)
				print("Val at x y",xOffset,yOffset,"is",inList[yOffset][xOffset])
			if inList[yOffset][xOffset] == 'v':
				if debugSouth:
					print("Found a v at x y",xOffset,yOffset)
				if inList[yOffset+1][xOffset] == '.':
					outList[yOffset][xOffset] = '.'
					outList[yOffset+1][xOffset] = 'v'
					if debugSouth:
						print("Moved v from",xOffset,yOffset,"to",xOffset,yOffset+1,"val",outList[yOffset+1][xOffset])
				else:
					outList[yOffset][xOffset] = inList[yOffset][xOffset]
			elif outList[yOffset][xOffset] != 'v':
				outList[yOffset][xOffset] = inList[yOffset][xOffset]
		lastRowNum = len(inList)-1
		if debugSouth:
			print("Finished most rows, last row number",lastRowNum,"column",xOffset)
			printHerd(inList)
			print("inList",inList)
		if inList[lastRowNum][xOffset] == 'v':
			if inList[0][xOffset] == '.':
				outList[lastRowNum][xOffset] = '.'
				outList[0][xOffset] = 'v'
			else:
				outList[lastRowNum][xOffset]= inList[lastRowNum][xOffset]
		else:
			outList[lastRowNum][xOffset] = inList[lastRowNum][xOffset]
	return outList

def transformList(inList):
	saveList = list(inList)
	count = 0
	printHerd(inList)
	while True:
		inList = moveHerdEast(inList)
		print("\nAfter East")
		printHerd(inList)
		inList = moveHerdSouth(inList)
		print("\nAfter south")
		printHerd(inList)
		if saveList != inList:
			count += 1
			print("\nAfter",count,"step")
			saveList = list(inList)
			printHerd(inList)
		else:
			break
		break
	return inList

inList =  readFileOfStringsToListOfLists('input2.txt')
# print("Initial inList")
# printHerd(inList)

inList = transformList(inList)
# print("After 1 move")
# printHerd(inList)


quit()



newList = inList
stillRunning = True
loopCount = 0
while stillRunning:
	tranList = transformList(newList)
	if tranList == newList:
		stillRunning = False
	else:
		loopCount += 1
		newList = []
		newList = tranList
	print(loopCount)

print(loopCount)

# D09P1.py
# 2021 Advent of Code
# Day 9
# Part 1

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	inListOut = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	for line in inList:
		lineChars = []
		for charInRow in line:
			lineChars.append(int(charInRow))
		inListOut.append(lineChars)
	return inListOut

def padArray(inList,padVal):
	# Pad out the Array with padVal
	outArray = []
	xSize = len(inList[0])

	newRow = []
	for offset in range(xSize + 2):
		newRow.append(padVal)
	outArray.append(newRow)

	for row in inList:
		newRow = []
		newRow.append(padVal)
		for charInRow in row:
			newRow.append(charInRow)
		newRow.append(padVal)
		outArray.append(newRow)

	newRow = []
	for offset in range(xSize + 2):
		newRow.append(padVal)
	outArray.append(newRow)
	return outArray

def findLowPoints(paddedArray):
	lowPointList = []
	xSize = len(paddedArray[0])
	ySize = len(paddedArray)
	print("xSize",xSize)
	print("ySize",ySize)
	for y in range(1,ySize):
		for x in range(1,xSize):
			if (paddedArray[y][x] < paddedArray[y-1][x-1]) and \
			(paddedArray[y][x] < paddedArray[y-1][x]) and \
			(paddedArray[y][x] < paddedArray[y-1][x+1]) and \
			(paddedArray[y][x] < paddedArray[y][x-1]) and \
			(paddedArray[y][x] < paddedArray[y][x+1]) and \
			(paddedArray[y][x] < paddedArray[y+1][x-1]) and \
			(paddedArray[y][x] < paddedArray[y+1][x]) and \
			(paddedArray[y][x] < paddedArray[y+1][x+1]):
				print("paddedArray[y][x]",paddedArray[y][x])
				lowPointList.append(paddedArray[y][x])
	return lowPointList

inList = readFileToListOfStrings('input.txt')
for row in inList:
	print(row)
paddedArray = padArray(inList,9)
for row in paddedArray:
	print(row)
lowPointsList = findLowPoints(paddedArray)
sum = 0
for row in lowPointsList:
	print(row)
	sum += row + 1
print("sum",sum)
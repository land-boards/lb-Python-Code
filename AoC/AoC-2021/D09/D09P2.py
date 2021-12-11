# D09P2.py
# 2021 Advent of Code
# Day 9
# Part 2

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
				# print("paddedArray[y][x]",paddedArray[y][x])
				lowPoint = []
				lowPoint.append(x)
				lowPoint.append(y)
				lowPointList.append(lowPoint)
	return lowPointList

def findAreaAroundPoint(inList,x,y):
	# print("inList",inList)
	print("Find area around",x,y)
	lowPointsList = []
	lowPointsList.append([x,y])
	# print("lowPointsList",lowPointsList)
	foundNewPoint = True
	while foundNewPoint:
		foundNewPoint = False
		for location in lowPointsList:
			locX = location[0]
			locY = location[1]
			# print("Check from",locX,locY)
			# Check to the left
			checkLoc = [locX-1,locY]
			# print("Checking",checkLoc)
			val = inList[checkLoc[1]][checkLoc[0]]
			if val != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
			checkLoc = [locX+1,locY]
			if inList[checkLoc[1]][checkLoc[0]] != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
			# Check to the right
			checkLoc = [locX+1,locY]
			# print("Checking",checkLoc)
			val = inList[checkLoc[1]][checkLoc[0]]
			if val != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
			checkLoc = [locX+1,locY]
			if inList[checkLoc[1]][checkLoc[0]] != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
			# Check up
			checkLoc = [locX,locY+1]
			# print("Checking",checkLoc)
			val = inList[checkLoc[1]][checkLoc[0]]
			if val != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
			checkLoc = [locX+1,locY]
			if inList[checkLoc[1]][checkLoc[0]] != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
			# Check down
			checkLoc = [locX,locY-1]
			# print("Checking",checkLoc)
			val = inList[checkLoc[1]][checkLoc[0]]
			if val != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
			checkLoc = [locX+1,locY]
			if inList[checkLoc[1]][checkLoc[0]] != 9:
				if checkLoc not in lowPointsList:
					lowPointsList.append(checkLoc)
					foundNewPoint = True
	print("len",len(lowPointsList))
	print("lowPointsList",lowPointsList)
	return len(lowPointsList)

def calcArea(pointsList,inList):
	area = 0
	for point in pointsList:
		x = point[0]
		y = point[1]
		area += inList[y][x]
	print("area",area)

inList = readFileToListOfStrings('input.txt')
# for row in inList:
	# print(row)
paddedArray = padArray(inList,9)
# for row in paddedArray:
	# print(row)
lowPointsList = findLowPoints(paddedArray)
areasList = []
for row in lowPointsList:
	print(row)
	areasList.append(findAreaAroundPoint(paddedArray,row[0],row[1]))
areasList.sort()
print(areasList)
totalArea = areasList[-1] * areasList[-2] * areasList[-3]
print("totalArea",totalArea)

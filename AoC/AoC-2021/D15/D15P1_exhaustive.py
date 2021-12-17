# D15P1.py
# 2021 Advent of Code
# Day 15
# Part 1

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def makeAllPaths(xSize,ySize,initPath):
	# print("makeAllPaths: xSize",xSize)
	# print("makeAllPaths: ySize",ySize)
	currentPaths = initPath
	# print("makeAllPaths: currentPaths (before)",currentPaths)
	keepRunningLoop = True
	lastPath = []
	while keepRunningLoop:
		# print("makeAllPaths: Looping main")
		newPaths = []
		keepRunningLoop1 = True
		keepRunningLoop2 = True
		for path in currentPaths:
			# print("makeAllPaths: Looping inner")
			# print("makeAllPaths: Examining path",path)
			lastPoint = path[-1]
			# print("makeAllPaths: lastPoint",lastPoint)
			xVal = lastPoint[0]
			yVal = lastPoint[1]
			# print("makeAllPaths: point x",xVal)
			# print("makeAllPaths: point y",yVal)
			nextPtX = xVal+1
			# print("makeAllPaths: nextPtX",nextPtX)
			newPathRow1 = []
			newPathRow1 = list(path)
			if (nextPtX < xSize) and (yVal < ySize):
				newPathRow1.append([nextPtX,yVal])
				newPaths.append(newPathRow1)
				keepRunningLoop1 = True
			else:
				keepRunningLoop1 = False
			nextPtY = yVal+1
			# print("makeAllPaths: nextPtY",nextPtY)
			newPathRow2 = []
			newPathRow2 = list(path)
			if (xVal < xSize) and (nextPtY < ySize):
				newPathRow2.append([xVal,nextPtY])
				newPaths.append(newPathRow2)
				keepRunningLoop2 = True
			else:
				keepRunningLoop2 = False
			currentPaths = newPaths
			# print("makeAllPaths: currentPaths (after)")
			for myPath in newPaths:
				# print(myPath)
				continue
			if (not keepRunningLoop1) and (not keepRunningLoop2):
				# print("makeAllPaths: Stopped")
				keepRunningLoop = False
		if newPaths != []:
			lastPath = newPaths
	# print("lastPath")
	# for row in lastPath:
		# print(row)
	return lastPath

inList = readFileToListOfStrings('input.txt')
# print(inList)
newList = []
for col in inList:
	newRow = []
	for element in col:
		newRow.append(int(element))
	newList.append(newRow)
# print("newList",newList)	
xSize = len(inList[0])
ySize = len(inList)
print("main: xSize",xSize)
print("main: ySize",ySize)

pointValsList = {}
for yLoc in range(ySize):
	for xLoc in range(xSize):
		xyPair = xLoc,yLoc
		# print("xyPair",xyPair)
		val = newList[yLoc][xLoc]
		# print("val",val)
		pointValsList[xyPair] = val
print("pointValsList",pointValsList)

# xSize = 4
# ySize = 4
minVal = 99999
pathsList = makeAllPaths(xSize,ySize,[[[0,0]]])
for path in pathsList:
	total = 0
	for point in path:
		# print("point",point)
		total += pointValsList[(point[0],point[1])]
	if minVal > total:
		minVal = total
		print("min path",path)
print("minVal",minVal-newList[0][0])
		
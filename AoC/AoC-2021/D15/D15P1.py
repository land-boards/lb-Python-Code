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

def shortestPathToPoints(newList,pointValsList):
	shortestPathVals = {}
	newList[0][0] = 0
	# Fill in edges
	print("shortestPathToPoints: newList first line",newList[0])
	shortestPathVals[(0,0)] = 0
	print("X's")
	for xVal in range(1,len(newList[0])):
		valAtPoint = newList[0][xVal] 
		valAtPoint += shortestPathVals[(xVal-1,0)]
		print("valAtPoint",valAtPoint)
		shortestPathVals[(xVal,0)] = valAtPoint
	print("Y's")
	for yVal in range(1,len(newList)):
		valAtPoint = newList[yVal][0] 
		valAtPoint += shortestPathVals[(0,yVal-1)]
		print("valAtPoint",valAtPoint)
		shortestPathVals[(0,yVal)] = valAtPoint
	print("shortestPathToPoints: shortestPathVals at start",shortestPathVals)
	for xyVal in range(1,len(newList)):
		print("xyVal =",xyVal)
		for xVal in range(1,xyVal):
			val = newList[xyVal][xVal]
			if shortestPathVals[(xVal-1,xyVal)] < shortestPathVals[(xVal,xyVal-1)]:
				shortestPathVals[(xVal,xyVal)] = shortestPathVals[(xVal-1,xyVal)] + val
			else:
				shortestPathVals[(xVal,xyVal)] = shortestPathVals[(xVal,xyVal-1)] + val
		print("shortestPathToPoints: shortestPathVals at mid 1",shortestPathVals)
		for yVal in range(1,xyVal):
			val = newList[yVal][xyVal]
			if shortestPathVals[(xyVal-1,yVal)] < shortestPathVals[(xyVal,yVal-1)]:
				shortestPathVals[(xyVal,yVal)] = shortestPathVals[(xyVal-1,yVal)] + val
			else:
				shortestPathVals[(xyVal,yVal)] = shortestPathVals[(xyVal,yVal-1)] + val
		print("shortestPathToPoints: shortestPathVals at mid 2",shortestPathVals)
		val = newList[xyVal][xyVal]
		if shortestPathVals[(xyVal,xyVal-1)] < shortestPathVals[(xyVal-1,xyVal)]:
			shortestPathVals[(xyVal,xyVal)] = val + shortestPathVals[(xyVal,xyVal-1)]
		else:
			shortestPathVals[(xyVal,xyVal)] = val + shortestPathVals[(xyVal-1,xyVal)]
			print("shortestPathToPoints: shortestPathVals at point",shortestPathVals)
	print("shortestPathToPoints: shortestPathVals at end",shortestPathVals)
	# print("len(newList)-1",len(newList)-1)
	# print("len(newList[0])-1)",len(newList[0])-1)
	keyVal = (len(newList)-1,len(newList[0])-1)
	retVal = shortestPathVals[keyVal]
	print("retVal",retVal)
#	quit()
	return retVal

inList = readFileToListOfStrings('input.txt')
newList = []
for col in inList:
	newRow = []
	for element in col:
		newRow.append(int(element))
	newList.append(newRow)
print("newList")
for row in newList:
	print(row)
xSize = len(inList[0])
ySize = len(inList)
# print("main: xSize",xSize)
# print("main: ySize",ySize)

pointValsList = {}
for yLoc in range(ySize):
	for xLoc in range(xSize):
		xyPair = xLoc,yLoc
		# print("xyPair",xyPair)
		val = newList[yLoc][xLoc]
		# print("val",val)
		pointValsList[xyPair] = val
# print("pointValsList",pointValsList)

shortestVal = shortestPathToPoints(newList,pointValsList)
print("shortestVal",shortestVal)

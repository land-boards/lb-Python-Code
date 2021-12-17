# D15P2.py
# 2021 Advent of Code
# Day 15
# Part 2
# 315 is too low
# 2822 is too high

import time

# At start
startTime = time.time()

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
	# print("shortestPathToPoints: newList first line",newList[0])
	shortestPathVals[(0,0)] = 0
	# print("X's")
	for xVal in range(1,len(newList[0])):
		valAtPoint = newList[0][xVal] 
		valAtPoint += shortestPathVals[(xVal-1,0)]
		# print("valAtPoint",valAtPoint)
		shortestPathVals[(xVal,0)] = valAtPoint
	# print("Y's")
	for yVal in range(1,len(newList)):
		valAtPoint = newList[yVal][0] 
		valAtPoint += shortestPathVals[(0,yVal-1)]
		# print("valAtPoint",valAtPoint)
		shortestPathVals[(0,yVal)] = valAtPoint
	# print("shortestPathToPoints: shortestPathVals at start",shortestPathVals)
	for xyVal in range(1,len(newList)):
		# print("xyVal =",xyVal)
		for xVal in range(1,xyVal):
			val = newList[xyVal][xVal]
			if shortestPathVals[(xVal-1,xyVal)] < shortestPathVals[(xVal,xyVal-1)]:
				shortestPathVals[(xVal,xyVal)] = shortestPathVals[(xVal-1,xyVal)] + val
			else:
				shortestPathVals[(xVal,xyVal)] = shortestPathVals[(xVal,xyVal-1)] + val
		# print("shortestPathToPoints: shortestPathVals at mid 1",shortestPathVals)
		for yVal in range(1,xyVal):
			val = newList[yVal][xyVal]
			if shortestPathVals[(xyVal-1,yVal)] < shortestPathVals[(xyVal,yVal-1)]:
				shortestPathVals[(xyVal,yVal)] = shortestPathVals[(xyVal-1,yVal)] + val
			else:
				shortestPathVals[(xyVal,yVal)] = shortestPathVals[(xyVal,yVal-1)] + val
		# print("shortestPathToPoints: shortestPathVals at mid 2",shortestPathVals)
		val = newList[xyVal][xyVal]
		if shortestPathVals[(xyVal,xyVal-1)] < shortestPathVals[(xyVal-1,xyVal)]:
			shortestPathVals[(xyVal,xyVal)] = val + shortestPathVals[(xyVal,xyVal-1)]
		else:
			shortestPathVals[(xyVal,xyVal)] = val + shortestPathVals[(xyVal-1,xyVal)]
			# print("shortestPathToPoints: shortestPathVals at point",shortestPathVals)
	# print("shortestPathToPoints: shortestPathVals at end",shortestPathVals)
	# print("len(newList)-1",len(newList)-1)
	# print("len(newList[0])-1)",len(newList[0])-1)
	keyVal = (len(newList)-1,len(newList[0])-1)
	retVal = shortestPathVals[keyVal]
	# print("retVal",retVal)
#	quit()
	return retVal

inList = readFileToListOfStrings('input1.txt')
newList1 = []
for col in inList:
	newRow = []
	for element in col:
		newRow.append(int(element))
	newList1.append(newRow)
print("First loop len(newList1[0])",len(newList1[0]))
print("First loop len(newList1)",len(newList1))
# print("newList")
# for row in newList:
	# print(row)

newList2 = []
for row in newList1:
	# print("row",row)
	wideRow = []
	for colCount in range(5):
		newRow = []
		for col in row:
			originalVal = col
			originalVal += colCount
			if originalVal > 9:
				originalVal %= 9
			newRow.append(originalVal)
		wideRow += newRow
	# print("wideRow",wideRow)
	newList2.append(wideRow)
print("\n2nd loop len(newList2[0])",len(newList2[0]))
print("2nd loop len(newList2)",len(newList2))
# for col in newList2:
	# for row in col:
		# print(row,end='')
	# print()

newList = []
for rowCountVal in range(5):
	for row in newList2:
		newRow = []
		for col in row:
			originalVal = col
			originalVal += rowCountVal
			if originalVal > 9:
				originalVal %= 9
			newRow.append(originalVal)
		newList.append(newRow)

print("\n3rd nlen(newList[0])",len(newList[0]))
print("3rd len(newList)",len(newList))
for col in newList:
	for row in col:
		print(row,end='')
	print()
# xc=0
# yc=0
# for col in newList:
	# for row in col:
		# print(row,end='')
		# if xc%10 == 9:
			# print(" ",end='')
		# xc += 1
	# print()
	# if yc%10 == 9:
		# print(" ")
	# yc += 1

# print("newList",newList)

xSize = len(newList[0])
ySize = len(newList)
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
endTime = time.time()
print('time',endTime-startTime)

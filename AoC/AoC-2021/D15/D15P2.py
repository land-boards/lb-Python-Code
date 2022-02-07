# D15P2.py
# 2021 Advent of Code
# Day 15
# Part 2
# 315 is too low
# 2822 is too high

import time
from collections import deque

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

def make5xList(inList):
	newList1 = []
	for col in inList:
		newRow = []
		for element in col:
			newRow.append(int(element))
		newList1.append(newRow)

	newList2 = []
	for row in newList1:
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
		newList2.append(wideRow)
		
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
	return newList
	
def printArray(inList):
	for col in newList:
		for row in col:
			print(row,end='')
		print()

def makePointsValList(newList):
	pointValsList = {}
	for yLoc in range(ySize):
		for xLoc in range(xSize):
			xyPair = xLoc,yLoc
			val = newList[yLoc][xLoc]
			pointValsList[xyPair] = val
	return pointValsList

inList = readFileToListOfStrings('input1.txt')
newList = make5xList(inList)
printArray(newList)

xSize = len(newList[0])
ySize = len(newList)

pointValsList = makePointsValList(newList)

shortestVal = 999999
tovisit = deque([[0,0,0]])
while len(tovisit):
	current = tovisit.popleft()
	xLoc = current[0]
	yLoc = current[1]
	count = current[2]
	# print(current)
	if xLoc < xSize-1:
		x1 = xLoc + 1
		y1 = yLoc
		c1 = pointValsList[x1,y1] + count
		tovisit.append([x1,y1,c1])
	if yLoc < ySize-1:
		x2 = xLoc
		y2 = yLoc + 1
		c2 = pointValsList[x1,y1] + count
		tovisit.append([x2,y2,c2])
	if (xLoc == xSize-1) and (yLoc == ySize-1):
		if count < shortestVal:
			shortestVal = count
	# print(tovisit)
	# if len(tovisit) > 6:
		# quit()

print("shortestVal",shortestVal)
endTime = time.time()
print('time',endTime-startTime)

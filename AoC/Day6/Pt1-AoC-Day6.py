# Pt1-AoCDay5.py
# 2018 Advent of Code
# Day 6
# Part 1
# https://adventofcode.com/2018/day/6

import time
import re

"""
--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

"""

def readTextFileTo2DList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	list is converted into a 2D array
	:returns: the list sorted list
	"""
	with open(fileName, 'r') as filehandle: 
		lineData = []
		for line in filehandle:
			lineData.append(line)
	return lineData

def turnTextListInto2DList(list):
	array2D = []
	for line in list:
		lineDat = []
		line = line.strip()
		lineDatA = line.split(',')
		lineDat.append(int(lineDatA[0]))
		lineDat.append(int(lineDatA[1]))
		array2D.append(lineDat)
	return array2D

def getMaxVals(list2D):
	maxX = 0
	maxY = 0
	for row in list2D:
		if row[0] > maxX:
			maxX = row[0]
		if row[1] > maxY:
			maxY = row[1]
	return [maxX,maxY]
	
def getMinVals(list2D):
	minX = 9999
	minY = 9999
	for row in list2D:
		if row[0] < minX:
			minX = row[0]
		if row[1] < minY:
			minY = row[1]
	return [minX,minY]

def make2dList(cols,rows):
	"""make2dList - Make a 2D list
	"""
	a=[]
	for row in xrange(rows): a += [[0]*(cols+1)]
	return a

def get(x,y):
	return(myListArray[x][y])

def dumpArray():
	for row in myListArray:
		for cell in row:
			if cell == -1:
				print '_',
			else:
				print cell,
		print

def countCellsInArray(cellNum):
	retCount = 0
	for row in myListArray:
		for cell in row:
			if cell == cellNum:
				retCount += 1
	return retCount
				
def isArrayFull(maxVals):
	for y in range(maxVals[1]+1):
		for x in range(maxVals[0]+2):
			if myListArray[y][x] == -1:
				return False
	return True
	
def clearArray(maxVals):
	"""clearArray - Fill array with -1 values
	"""
	for y in range(maxVals[1]+1):
		for x in range(maxVals[0]+2):
			myListArray[y][x] = -1

def getloc(id):
	""" return the x,y of the id - the first point
	"""
	#print 'id',id,
	return list2D[id]

def manhattanDistance(x1,y1,x2,y2):
	distance = abs(x1-x2) + abs(y1-y2)
	return distance
	
def isEqualDistance(x,y,id1,id2):
	"""isEqualDistance - if x,y location is equidistant to id1 and id2
	:returns: True if the point is equidistant from the two cells
	"""
	isEqDist = False
	if id1 == 9999 or id2 == 9999:
		return True
	id1LocXY = getloc(id1)
	id2LocXY = getloc(id2)
	if isEqDist:
		print '\nisEqualDistance',id1LocXY,id2LocXY,'to',x,y,
	distance1 = manhattanDistance(id1LocXY[0],id1LocXY[1],x,y)
	distance2 = manhattanDistance(id2LocXY[0],id2LocXY[1],x,y)
	if distance1 == distance2:
		return True
	return False

def put(x,y,val):
	"""put val at x,y
	Don't put if outside the array
	Don't put if there's already a point there
	:returns: putWasOK if able to put the value at the point, 
	outside if unable to put the point due to infinite area constraint
	alreadyFull
	"""
	debugFunct = False
	if debugFunct:
		print 'put at x,y',x,y,'value',val,
	retVal = ''
	if x < 0 or x > maxVals[0]+1:
		retVal = 'outside'
	elif y < 0 or y> maxVals[1]:
		retVal = 'outside'
	elif myListArray[y][x] == -1:
		myListArray[y][x] = val
		retVal = 'putWasOK'
	elif myListArray[y][x] == val:
		retVal = 'already at value'
	else:
		currentVal = myListArray[y][x]
		if isEqualDistance(x,y,currentVal,val):
			myListArray[y][x] = 9999
		retVal = 'collision'
	if debugFunct:
		print retVal
	return retVal

def putRect(cellPoint,size,cell):
	debugFunct = False
	if debugFunct:
		print 'putRect x',cellPoint[0],'y',cellPoint[1],'size',size,'cell',cell
	collisionVal = False
	atLeastOneOK = False
	atLeastOneOutside = False
	# result vector = [collisionVal,atLeastOneOK,atLeastOneOutside]		# [Collision,At_Least_One_OK,At_Least_One_Outside]
	for y in range(size*2+1):
		for x in range(size*2+1):
			putStatus = put(cellPoint[0]+x-size,cellPoint[1]+y-size,cell)
			if putStatus == 'collision':
				collisionVal = True
			elif putStatus == 'putWasOK':
				atLeastOneOK = True	
			elif putStatus == 'outside':
				atLeastOneOutside = True
			elif putStatus == 'already at value':
				continue
	return [collisionVal,atLeastOneOK,atLeastOneOutside]

def fillEqualDistantCells():
	listToWorkOff = []
	listToWorkOff.extend(range(0, len(list2D)))
	while len(listToWorkOff) > 1:
		print 'listToWorkOff',listToWorkOff
		cellOff1 = listToWorkOff[0]
		cellOff2 = listToWorkOff[1]
		manhattanMinDistance = 9999
		closestCell = 9999
		while cellOff2 < len(listToWorkOff):
			print 'comparing cells',cellOff1,cellOff2
			gotManhattanDistance = manhattanDistance(list2D[cellOff1][0],list2D[cellOff1][1],list2D[cellOff2][0],list2D[cellOff2][1])
			print 'dist =',gotManhattanDistance
			if  gotManhattanDistance < manhattanMinDistance:
				manhattanMinDistance = gotManhattanDistance
				closestCell = cellOff2
			cellOff2 += 1
		print 'closest cells',cellOff1,closestCell
		listToWorkOff.remove(cellOff1)
		listToWorkOff.remove(closestCell)
		cellOff1 += 1
		# for y in range(maxVals[1]+1):
			# for x in range(maxVals[0]+2):
						# if isEqualDistance(x,y,cellOff1,cellOff2):
							# put(x,y,9999)
							# print 'cells are equidistant',x,y,list2D[cellOff1],list2D[cellOff2]
						# cellOff2 += 1
					# cellOff1 += 1

list2D = turnTextListInto2DList(readTextFileTo2DList('input2.txt'))
print 'list2D',list2D
minVals = getMinVals(list2D)
#print 'minVals',minVals
maxVals = getMaxVals(list2D)
inListLen = len(list2D)
#print 'maxVals',maxVals
myListArray = make2dList(maxVals[0]+1,maxVals[1]+1)
clearArray(maxVals)
# print 'Initial Array'
# dumpArray()

item = 0
for vals in list2D:
	put(vals[0],vals[1],item)
	item += 1
#print 'Array with first Points'
#dumpArray()
#print

bloomSize = 1
keepProcessingArray = True
couldntPutRect = []
while keepProcessingArray:
	keepProcessingArray = False
	cellVal = 0
	for point in list2D:
		putRectStatus = putRect(point,bloomSize,cellVal)
		# status vector = [collisionVal,atLeastOneOK,atLeastOneOutside]
		#print 'putRectStatus [x,y]',point,'Size =',bloomSize,'cellVal =',cellVal,'cellVal =',putRectStatus
		if putRectStatus[1] == True:
			#print 'Was able to change cell',cellVal
			keepProcessingArray = True
		if putRectStatus[2] == True:
			if cellVal not in couldntPutRect:
				#print 'pushing cellVal',cellVal
				couldntPutRect.append(cellVal)
#		elif putRectStatus[0] == True:
#			print 'Any collisions cellVal =',cellVal
		cellVal += 1
#	if couldntPutRect:
#		print 'Couldnt place cells',couldntPutRect
	if isArrayFull(maxVals):
		#print 'array is full'
		keepProcessingArray = False
	#print 'Array after',bloomSize,'push'
	#dumpArray()
	bloomSize += 1
	#print 

print 'Array after bloom is full'
dumpArray()

couldntPutRect.sort()
#print 'infinite sized arrays',couldntPutRect
finiteArrays = []
for i in range(len(list2D)):
	if i not in couldntPutRect:
		finiteArrays.append(i)

fillEqualDistantCells()	

print 'Array after filling equidistant cells'
dumpArray()

print 'finiteArrays',finiteArrays
cellCounts = []
for cellNumber in finiteArrays:
	cellRow = []
	cellRow.append(cellNumber)
	cellRow.append(countCellsInArray(cellNumber))
	cellCounts.append(cellRow)
print 'cellCounts',cellCounts

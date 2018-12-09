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

xrange

"""

def getMaxVals(list2D):
	maxX = 0
	maxY = 0
	for row in list2D:
		if row[0] > maxX:
			maxX = row[0]
		if row[1] > maxY:
			maxY = row[1]
	return [maxX,maxY]
	
def clearArray(maxVals):
	"""clearArray - Fill array with -1 values
	"""
	for y in range(maxVal):
		for x in range(maxVal):
			myListArray[y][x] = 0

def get(x,y):
	return(myListArray[x][y])

def dumpArray():
	for row in myListArray:
		for cell in row:
			if cell == -1:
				print 'X',
			elif cell == 9999:
				print '.',
			else:
				print cell,
		print

def getloc(id):
	""" return the x,y of the id - the first point
	"""
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
	myListArray[y][x] = val
		
def findDistanceToClosestPointsIn2DList(x,y):
	shortestManhattanDistance = maxVal + 1
	for point in list2D:
		manhattanDist = manhattanDistance(x,y,point[0],point[1])
		if manhattanDist < shortestManhattanDistance:
			shortestManhattanDistance = manhattanDist
	return shortestManhattanDistance
		
def countPointsAtParticularDistance(x,y,distance):
	pointCount = 0
	for point in list2D:
		manhattanDist = manhattanDistance(x,y,point[0],point[1])
		if manhattanDist == distance:
			pointCount += 1
	return pointCount

def findEdgeVals():
	edgeValList = []
	for x in range(maxVal):
		y = 0
		getVal = get(x,y)
		if getVal not in edgeValList:
			edgeValList.append(getVal)
		y = maxVal-1
		getVal = get(x,y)
		if getVal not in edgeValList:
			edgeValList.append(getVal)
	for y in range(maxVal):
		x = 0
		getVal = get(x,y)
		if getVal not in edgeValList:
			edgeValList.append(getVal)
		x = maxVal-1
		getVal = get(x,y)
		if getVal not in edgeValList:
			edgeValList.append(getVal)
	return edgeValList
		

def findOnePointAtParticularDistance(x,y,distance):
	pointOffset = 0
	for point in list2D:
		manhattanDist = manhattanDistance(x,y,point[0],point[1])
		if manhattanDist == distance:
			return pointOffset 
		pointOffset += 1
	print 'wft'

def make2dList(cols,rows):
	"""make2dList - Make a 2D list
	"""
	a=[]
	for row in xrange(rows): a += [[0]*(cols)]
	return a

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

#############################################################################
## Code follows
#############################################################################

list2D = turnTextListInto2DList(readTextFileTo2DList('input.txt'))
maxVals = getMaxVals(list2D)
maxVal = max(maxVals[0],maxVals[1]) + 1
inListLen = len(list2D)
print 'inListLen',inListLen
maxDistance = 10000
print 'approx array size',maxDistance/inListLen
print 'make the array 2x the size for safety sake'
maxVal = 2*maxDistance/inListLen
print 'making the array square',maxVal,'by',maxVal
myListArray = make2dList(maxVal,maxVal)
clearArray(maxVals)

for x in range(maxVal):
	for y in range(maxVal):
		distanceSum = 0
		for point in list2D:
			distanceSum += manhattanDistance(x,y,point[0],point[1])
			#print 'distance from x,y to x,y =',x,y,point[0],point[1],'is',distanceSum
		if distanceSum < maxDistance:
			put(x,y,1)
dumpArray()
accumSum = 0
for x in range(maxVal):
	for y in range(maxVal):
		accumSum += get(x,y)
		
print 'accumSum',accumSum

# Pt2-AoCDay3.py
# 2019 Advent of Code
# Day 3
# Part 2
# https://adventofcode.com/2019/day/3

"""
--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:

_01234567890
........... 8
.+-----+...	7
.|.....|...	6
.|..+--X-+.	5
.|..|..|.|.	4
.|.-X--+.|.	3
.|..|....|.	2
.|.......|.	1
.o-------+.	0
...........

In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?

"""
from __future__ import print_function

def makeLinesList(listOfCircuits):
	#print("Number of circuits :",len(listOfCircuits))
	#print("List of circuits :",listOfCircuits)
	lines = []
	for circuit in listOfCircuits:
		startX = 0
		startY = 0
		endX = 0
		endY = 0
		circuitLines = []
		for point in circuit:
			lineSeg = []
			delta = int(point[1:])
			if point[0] == 'R':
				endX=startX+delta
				endY=startY
				lineSeg.append(startX)
				lineSeg.append(startY)
				lineSeg.append(endX)
				lineSeg.append(endY)
			elif point[0] == 'L':
				endX=startX-delta
				endY=startY
				lineSeg.append(endX)
				lineSeg.append(endY)
				lineSeg.append(startX)
				lineSeg.append(startY)
			elif point[0] == 'U':
				endY=startY+delta
				endX=startX
				lineSeg.append(startX)
				lineSeg.append(startY)
				lineSeg.append(endX)
				lineSeg.append(endY)
			elif point[0] == 'D':
				endY=startY-delta
				endX=startX
				lineSeg.append(endX)
				lineSeg.append(endY)
				lineSeg.append(startX)
				lineSeg.append(startY)
			else:
				print("Bad direction")
				exit()
			circuitLines.append(lineSeg)
			startX = endX
			startY = endY
		lines.append(circuitLines)
	#print("lines",lines)
	return(lines)

def makechainedLinesList(listOfCircuits):
	#print("Number of circuits :",len(listOfCircuits))
	#print("List of circuits :",listOfCircuits)
	lines = []
	for circuit in listOfCircuits:
		startX = 0
		startY = 0
		endX = 0
		endY = 0
		circuitLines = []
		for point in circuit:
			lineSeg = []
			delta = int(point[1:])
			if point[0] == 'R':
				endX=startX+delta
				endY=startY
			elif point[0] == 'L':
				endX=startX-delta
				endY=startY
			elif point[0] == 'U':
				endY=startY+delta
				endX=startX
			elif point[0] == 'D':
				endY=startY-delta
				endX=startX
			else:
				print("Bad direction")
				exit()
			lineSeg.append(startX)
			lineSeg.append(startY)
			lineSeg.append(endX)
			lineSeg.append(endY)
			circuitLines.append(lineSeg)
			startX = endX
			startY = endY
		lines.append(circuitLines)
	#print("lines",lines)
	return(lines)

def orderPoints(points):
	if points[1] < points[3]:
		return(points)
	if points[0] < points[2]:
		return(points)
	if points[0] > points[2]:
		return([points[2],points[3],points[0],points[1]])
	if points[1] > points[3]:
		return([points[2],points[3],points[0],points[1]])
	else:
		print("Error points were not resortable")

def checkIntersect(wire1,wire2):
	""" Check to see if two wires intersect
	"""
	newWire1 = orderPoints(wire1)
	newWire2 = orderPoints(wire2)
	#print("Checking wire pair",newWire1,newWire2)
	xs1 = newWire1[0]
	ys1 = newWire1[1]
	xe1 = newWire1[2]
	ye1 = newWire1[3]
	xs2 = newWire2[0]
	ys2 = newWire2[1]
	xe2 = newWire2[2]
	ye2 = newWire2[3]
	if ((xs1 <= xs2) and (xe1 >= xe2) and (ys1 >= ys2) and (ye1 <= ye2) or 
		(xs2 <= xs1) and (xe2 >= xe1) and (ys2 >= ys1) and (ye2 <= ye1)):
		if xs1==xe1:
			xIntersect = xs1
		if xs2==xe2:
			xIntersect = xs2
		if ys1==ye1:
			yIntersect = ys1
		if ys2==ye2:
			yIntersect = ys2
		#print("Wires intersect at : ", xIntersect, yIntersect)
		return([xIntersect,yIntersect])
	return([0,0])
	
def findIntersections(nets):
	""" Create a list of intersections
	Ignore node at 0,0
	"""
	net1 = nets[0]
	net2 = nets[1]
	#print("Net1:",net1)
	#print("Net2:",net2)
	intersectList = []
	for wire1 in net1:
		for wire2 in net2:
			intersectPair = checkIntersect(wire1,wire2)
			if (intersectPair != [0,0]):
				intersectList.append(intersectPair)
				#print("Intersecting lines : ",wire1,wire2,intersectPair)
	#print("intersections are at : ",intersectList)
	return intersectList

def isBetween(coord1,coord2,pointToCheck):
	""" Return True if the point is between two ends (in a single axis)
	"""
	if (pointToCheck >= coord1) and (pointToCheck <= coord2):
		return True
	elif (pointToCheck <= coord1) and (pointToCheck >= coord2):
		return True
	else:
		return False

def manhattanDistanceBetweenPins(pinsPair):
	return(abs(pinsPair[0]-pinsPair[2])+abs(pinsPair[1]-pinsPair[3]))

def findIntersectionOnLine(lineEndPoints, currentIntersection):
	"""
	Returns intersection if the line has an intersection
	Otherwise returns [0,0]
	"""
#	print("findIntersectionOnLine: currentIntersection",currentIntersection)
#	print("Checking line :",lineEndPoints," for intersection at :",currentIntersection)
	if ((lineEndPoints[0] != currentIntersection[0]) and (lineEndPoints[1] != currentIntersection[1])):
#		print("findIntersectionOnLine: Not on line")
		return [0,0]
	if ((lineEndPoints[2] != currentIntersection[0]) and (lineEndPoints[3] != currentIntersection[1])):
#		print("findIntersectionOnLine: Not on line")
		return [0,0]
	if (lineEndPoints[0] == lineEndPoints[2]):
		if (isBetween(lineEndPoints[1],lineEndPoints[3],currentIntersection[1])):
			#print("*** findIntersectionOnLine: Is on X line")
			return currentIntersection
	if (lineEndPoints[1] == lineEndPoints[3]):
		if (isBetween(lineEndPoints[0],lineEndPoints[2],currentIntersection[0])):
			#print("*** findIntersectionOnLine: Is on Y line")
			return currentIntersection
#		print("findIntersectionOnLine: Not on line")
		return [0,0]

def distToIntersects(linesList,intersList):
	"""
	"""
	distancesList1 = []
	for intersPoint in intersList:
		nodeAccumDist1 = 0
		distanceToNode = 0;
		for lineEndPoints in linesList[0]:
			checkIfPointOnLine = findIntersectionOnLine(lineEndPoints, intersPoint)
			if checkIfPointOnLine!=[0,0]:
				distanceToNode = nodeAccumDist1 + manhattanDistanceBetweenPins([lineEndPoints[0],lineEndPoints[1],checkIfPointOnLine[0],checkIfPointOnLine[1]])
				distancesList1.append(distanceToNode)
			nodeAccumDist1 = nodeAccumDist1 + manhattanDistanceBetweenPins(lineEndPoints)
	distancesList2 = []
	for intersPoint in intersList:
		nodeAccumDist2 = 0
		distanceToNode = 0;
		for lineEndPoints in linesList[1]:
			checkIfPointOnLine = findIntersectionOnLine(lineEndPoints, intersPoint)
			if checkIfPointOnLine!=[0,0]:
				distanceToNode = nodeAccumDist2 + manhattanDistanceBetweenPins([lineEndPoints[0],lineEndPoints[1],checkIfPointOnLine[0],checkIfPointOnLine[1]])
				distancesList2.append(distanceToNode)
			nodeAccumDist2 = nodeAccumDist2 + manhattanDistanceBetweenPins(lineEndPoints)
	listOffset = 0
	distMin=999999
	while(listOffset < len(distancesList1)):
		if (distancesList1[listOffset] + distancesList2[listOffset]) < distMin:
			distMin = distancesList1[listOffset] + distancesList2[listOffset]
		listOffset = listOffset + 1
	print("distMin : ",distMin)

#########################################################################
				
circuits = []
inFileName="AOC2019D03input.txt"
with open(inFileName, 'r') as filehandle:
	circuits = [line.split(',') for line in filehandle.readlines()]

# Make list of lines that are of regular direction
sortedLinesList = makeLinesList(circuits)
#print("Sorted lines list",sortedLinesList)
intersList = findIntersections(sortedLinesList)
# Make list of lines that have ends touching
#print("Intersection list",intersList)
chainedLinesList = makechainedLinesList(circuits)
#print("Chained lines list",chainedLinesList)
distToIntersects(chainedLinesList,intersList)

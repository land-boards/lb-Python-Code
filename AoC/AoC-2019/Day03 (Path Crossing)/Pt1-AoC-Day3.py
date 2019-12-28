# Pt2-AoCDay3.py
# 2019 Advent of Code
# Day 3
# Part 1
"""
--- Day 3: Crossed Wires ---
The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
What is the Manhattan distance from the central port to the closest intersection?

1223 was too low?
1231 is too high?
1225 is the right answer.
"""
from __future__ import print_function

def makeLinesList(listOfCircuits):
	lines = []
	for circuit in listOfCircuits:
		startX = 0
		startY = 0
		endX = 0
		endY = 0
		circuitLines = []
		for point in circuit:
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
			lineSeg = []
			lineSeg.append(startX)
			lineSeg.append(startY)
			lineSeg.append(endX)
			lineSeg.append(endY)
			circuitLines.append(lineSeg)
			startX = endX
			startY = endY
		lines.append(circuitLines)
	return(lines)

def orderPoints(points):
	if points[1] < points[3]:
		return(points)
	elif points[0] < points[2]:
		return(points)
	elif points[0] > points[2]:
		return([points[2],points[3],points[0],points[1]])
	elif points[1] > points[3]:
		return([points[2],points[3],points[0],points[1]])
	else:
		assert False,"Error points were not resortable"

def checkIntersect(wire1,wire2):
	newWire1 = orderPoints(wire1)
	newWire2 = orderPoints(wire2)
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
		return([xIntersect,yIntersect])
	return([0,0])
	
def findIntersections(nets):
	net1 = nets[0]
	net2 = nets[1]
	intersectList = []
	for wire1 in net1:
		for wire2 in net2:
			intersectPair = checkIntersect(wire1,wire2)
			if (intersectPair != [0,0]):
				intersectList.append(intersectPair)
	return intersectList

def findManhattanDistances(intersections):
	manDists = []
	for intersect in intersections:
		manDists.append(abs(intersect[0])+abs(intersect[1]))
	return sorted(manDists)

# open file and read the content into an accumulated sum
circuits = []
inFileName="input.txt"
with open(inFileName, 'r') as filehandle:
	circuits = [line.split(',') for line in filehandle.readlines() if True]
linesList = makeLinesList(circuits)
intersList = findIntersections(linesList)
manDistList = findManhattanDistances(intersList)
lowestDistance = 999999
for distance in manDistList:
	if distance > 0:
		if distance < lowestDistance:
			lowestDistance = distance
print("Lowest distance", lowestDistance)

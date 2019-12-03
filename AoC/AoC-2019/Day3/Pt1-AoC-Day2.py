# Pt1-AoCDay3.py
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
"""
from __future__ import print_function

def makeLinesList(listOfCircuits):
	#print("Number of circuits :",len(listOfCircuits))
	print("List of circuits :",listOfCircuits)
	lines = []
	for circuit in listOfCircuits:
		startX = 1
		startY = 1
		endX = 1
		endY = 1
		circuitLines = []
		for point in circuit:
			#print("\npoint:",point)
			delta = int(point[1:])
			#print(delta)
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
	print("lines",lines)
	return(lines)

def checkIntersect(wire1,wire2):
	print("wires",wire1,wire2)

def findIntersections(nets):
	net1 = nets[0]
	net2 = nets[1]
	print("Net1:",net1)
	print("Net2:",net2)
	for wire1 in net1:
		for wire2 in net2:
			checkIntersect(wire1,wire2)

# open file and read the content into an accumulated sum
circuits = []
with open('input2.txt', 'r') as filehandle:
	lines = filehandle.readlines()
	#print(lines)
	for line in lines:
		#print(line)
		theLine = line.split(',')
		circuits.append(theLine)
	#print(circuits)
linesList = makeLinesList(circuits)
print(linesList)
findIntersections(linesList)

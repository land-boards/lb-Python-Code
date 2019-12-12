# Pt1-AoCDay12.py
# 2019 Advent of Code
# Day 12
# Part 1
# https://adventofcode.com/2019/day/12

"""
--- Part Two ---

All this drifting around in space makes you wonder about the nature of the universe. Does history really repeat itself? You're curious whether the moons will ever return to a previous state.

Determine the number of steps that must occur before all of the moons' positions and velocities exactly match a previous point in time.

For example, the first example above takes 2772 steps before they exactly match a previous point in time; it eventually returns to the initial state:

After 0 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

After 2770 steps:
pos=<x=  2, y= -1, z=  1>, vel=<x= -3, y=  2, z=  2>
pos=<x=  3, y= -7, z= -4>, vel=<x=  2, y= -5, z= -6>
pos=<x=  1, y= -7, z=  5>, vel=<x=  0, y= -3, z=  6>
pos=<x=  2, y=  2, z=  0>, vel=<x=  1, y=  6, z= -2>

After 2771 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x= -3, y=  1, z=  1>
pos=<x=  2, y=-10, z= -7>, vel=<x= -1, y= -3, z= -3>
pos=<x=  4, y= -8, z=  8>, vel=<x=  3, y= -1, z=  3>
pos=<x=  3, y=  5, z= -1>, vel=<x=  1, y=  3, z= -1>

After 2772 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

Of course, the universe might last for a very long time before repeating. Here's a copy of the second example from above:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>

This set of initial positions takes 4686774924 steps before it repeats a previous state! Clearly, you might need to find a more efficient way to simulate the universe.

How many steps does it take to reach the first state that exactly matches a previous state?

4225920359840280	too high

528250271633772 right on 


"""

from __future__ import print_function
import numpy

example1Data = [[-1,0,2],[2,-10,-7],[4,-8,8],[3,5,-1]]
example2Data = [[-8,-10,0],[5,5,10],[2,-7,3],[9,-8,-3]]
problemData  = [[-19,-4,2],[-9,8,-16],[-4,5,-11],[1,9,-13]]
moonVelocities = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

def printPositionAndVelocity(position,velocity):
	print("After",step,"steps:")
	print("pos=<x=%3d"%position[0][0],", y=%3d"%position[0][1]," z=%3d"%position[0][2],">, vel=<x=%3d"%moonVelocities[0][0],">, y=<%3d"%moonVelocities[0][1],">, z=<%3d"%moonVelocities[0][2],">")
	print("pos=<x=%3d"%position[1][0],", y=%3d"%position[1][1]," z=%3d"%position[1][2],">, vel=<x=%3d"%moonVelocities[1][0],">, y=<%3d"%moonVelocities[1][1],">, z=<%3d"%moonVelocities[1][2],">")
	print("pos=<x=%3d"%position[2][0],", y=%3d"%position[2][1]," z=%3d"%position[2][2],">, vel=<x=%3d"%moonVelocities[2][0],">, y=<%3d"%moonVelocities[2][1],">, z=<%3d"%moonVelocities[2][2],">")
	print("pos=<x=%3d"%position[3][0],", y=%3d"%position[3][1]," z=%3d"%position[3][2],">, vel=<x=%3d"%moonVelocities[3][0],">, y=<%3d"%moonVelocities[3][1],">, z=<%3d"%moonVelocities[3][2],">")
	
def calVelocityDelta(refPos,other1,other2,other3):
	# returns a relative velocity adjustment based on the other moon
	#print("calVelocityDelta: ",refPos,other1,other2,other3,end='')
	if other1 > refPos:
		delta1 = 1
	elif other1 < refPos:
		delta1 = -1
	else:
		delta1 = 0
	if other2 > refPos:
		delta2 = 1
	elif other2 < refPos:
		delta2 = -1
	else:
		delta2 = 0
	if other3 > refPos:
		delta3 = 1
	elif other3 < refPos:
		delta3 = -1
	else:
		delta3 = 0
	totalDelta = delta1 + delta2 + delta3
	#print(", totalDelta",totalDelta)
	return(totalDelta)

moonPositions = example1Data

step = 0
lastStep = 2000

axisList = []

checkIndex = 0

checkVal = [moonPositions[0][checkIndex],moonPositions[1][checkIndex],moonPositions[2][checkIndex],moonPositions[3][checkIndex]]

#checkVal = [-88,-195,340,-88]

p0 = checkVal[0]
v0 = 0
p1 = checkVal[1]
v1 = 0
p2 = checkVal[2]
v2 = 0
p3 = checkVal[3]
v3 = 0

print("Looking for :",checkVal)

step = 0
repeated = False
print("Repeated at step ",end='')
while step < 3000000:
	step += 1
	#print("\nstep",step)
	g0 = calVelocityDelta(p0,p1,p2,p3)
	g1 = calVelocityDelta(p1,p0,p2,p3)
	g2 = calVelocityDelta(p2,p1,p0,p3)
	g3 = calVelocityDelta(p3,p1,p2,p0)
	#print("x velocity deltas",g0,g1,g2,g3)
	p0 += g0 + v0
	p1 += g1 + v1
	p2 += g2 + v2
	p3 += g3 + v3
	v0 += g0
	v1 += g1
	v2 += g2
	v3 += g3
	# print("x position after",p0,p1,p2,p3)
	# print("x velocity after",v0,v1,v2,v3)
	if [p0,p1,p2,p3] == [checkVal[0],checkVal[1],checkVal[2],checkVal[3]]:
		print(step)
		repeated = True
		break
if repeated:
	print(step)
else:
	print("Never before count",step)
print([p0,p1,p2,p3])

exit()
	
while step < lastStep:
	step += 1
	print("Step ",step)
	gravityDelta00 = calVelocityDelta(moonPositions[0][0],moonPositions[1][0],moonPositions[2][0],moonPositions[3][0])
	gravityDelta01 = calVelocityDelta(moonPositions[0][1],moonPositions[1][1],moonPositions[2][1],moonPositions[3][1])
	gravityDelta02 = calVelocityDelta(moonPositions[0][2],moonPositions[1][2],moonPositions[2][2],moonPositions[3][2])
	
	gravityDelta10 = calVelocityDelta(moonPositions[1][0],moonPositions[0][0],moonPositions[2][0],moonPositions[3][0])
	gravityDelta11 = calVelocityDelta(moonPositions[1][1],moonPositions[0][1],moonPositions[2][1],moonPositions[3][1])
	gravityDelta12 = calVelocityDelta(moonPositions[1][2],moonPositions[0][2],moonPositions[2][2],moonPositions[3][2])
	
	gravityDelta20 = calVelocityDelta(moonPositions[2][0],moonPositions[0][0],moonPositions[1][0],moonPositions[3][0])
	gravityDelta21 = calVelocityDelta(moonPositions[2][1],moonPositions[0][1],moonPositions[1][1],moonPositions[3][1])
	gravityDelta22 = calVelocityDelta(moonPositions[2][2],moonPositions[0][2],moonPositions[1][2],moonPositions[3][2])

	gravityDelta30 = calVelocityDelta(moonPositions[3][0],moonPositions[0][0],moonPositions[1][0],moonPositions[2][0])
	gravityDelta31 = calVelocityDelta(moonPositions[3][1],moonPositions[0][1],moonPositions[1][1],moonPositions[2][1])
	gravityDelta32 = calVelocityDelta(moonPositions[3][2],moonPositions[0][2],moonPositions[1][2],moonPositions[2][2])

	moonPositions[0][0] += gravityDelta00 + moonVelocities[0][0]
	moonPositions[0][1] += gravityDelta01 + moonVelocities[0][1]
	moonPositions[0][2] += gravityDelta02 + moonVelocities[0][2]

	moonPositions[1][0] += gravityDelta10 + moonVelocities[1][0]
	moonPositions[1][1] += gravityDelta11 + moonVelocities[1][1]
	moonPositions[1][2] += gravityDelta12 + moonVelocities[1][2]

	moonPositions[2][0] += gravityDelta20 + moonVelocities[2][0]
	moonPositions[2][1] += gravityDelta21 + moonVelocities[2][1]
	moonPositions[2][2] += gravityDelta22 + moonVelocities[2][2]

	moonPositions[3][0] += gravityDelta30 + moonVelocities[3][0]
	moonPositions[3][1] += gravityDelta31 + moonVelocities[3][1]
	moonPositions[3][2] += gravityDelta32 + moonVelocities[3][2]
	
	moonVelocities[0][0] += gravityDelta00
	moonVelocities[0][1] += gravityDelta01
	moonVelocities[0][2] += gravityDelta02

	moonVelocities[1][0] += gravityDelta10
	moonVelocities[1][1] += gravityDelta11
	moonVelocities[1][2] += gravityDelta12
	
	moonVelocities[2][0] += gravityDelta20
	moonVelocities[2][1] += gravityDelta21
	moonVelocities[2][2] += gravityDelta22
	
	moonVelocities[3][0] += gravityDelta30
	moonVelocities[3][1] += gravityDelta31
	moonVelocities[3][2] += gravityDelta32
	
	print("Moon positions",moonPositions)
	print("Moon Velocities",moonVelocities)
	
	pe0 = abs(moonPositions[0][0]) + abs(moonPositions[0][1]) + abs(moonPositions[0][2])
	pe1 = abs(moonPositions[1][0]) + abs(moonPositions[1][1]) + abs(moonPositions[1][2])
	pe2 = abs(moonPositions[2][0]) + abs(moonPositions[2][1]) + abs(moonPositions[2][2])
	pe3 = abs(moonPositions[3][0]) + abs(moonPositions[3][1]) + abs(moonPositions[3][2])
	
	ke0 = abs(moonVelocities[0][0]) + abs(moonVelocities[0][1]) + abs(moonVelocities[0][2])
	ke1 = abs(moonVelocities[1][0]) + abs(moonVelocities[1][1]) + abs(moonVelocities[1][2])
	ke2 = abs(moonVelocities[2][0]) + abs(moonVelocities[2][1]) + abs(moonVelocities[2][2])
	ke3 = abs(moonVelocities[3][0]) + abs(moonVelocities[3][1]) + abs(moonVelocities[3][2])
	
	te0 = pe0 * ke0
	te1 = pe1 * ke1
	te2 = pe2 * ke2
	te3 = pe3 * ke3
	
	teSum = te0 + te1 + te2 + te3
	print("Total Kinetic Energy", teSum)
	
	
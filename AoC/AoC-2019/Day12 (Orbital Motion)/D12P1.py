# Pt1-AoCDay12.py
# 2019 Advent of Code
# Day 12
# Part 1
# https://adventofcode.com/2019/day/12

"""
--- Day 12: The N-Body Problem ---
The space near Jupiter is not a very safe place; you need to be careful of a big distracting red spot, extreme radiation, and a whole lot of moons swirling around. You decide to start by tracking the four largest moons: Io, Europa, Ganymede, and Callisto.

After a brief scan, you calculate the position of each moon (your puzzle input). You just need to simulate their motion so you can avoid them.

Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional velocity. The position of each moon is given in your scan; the x, y, and z velocity of each moon starts at 0.

Simulate the motion of the moons in time steps. Within each time step, first update the velocity of every moon by applying gravity. Then, once all moons' velocities have been updated, update the position of every moon by applying velocity. Time progresses by one step once all of the positions are updated.

To apply gravity, consider every pair of moons. On each axis (x, y, and z), the velocity of each moon changes by exactly +1 or -1 to pull the moons together. For example, if Ganymede has an x position of 3, and Callisto has a x position of 5, then Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x velocity changes by -1 (because 3 < 5). However, if the positions on a given axis are the same, the velocity on that axis does not change for that pair of moons.

Once all gravity has been applied, apply velocity: simply add the velocity of each moon to its own position. For example, if Europa has a position of x=1, y=2, z=3 and a velocity of x=-2, y=0,z=3, then its new position would be x=-1, y=2, z=6. This process does not modify the velocity of any moon.

For example, suppose your scan reveals the following positions:

<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
Simulating the motion of these moons would produce the following:

After 0 steps:
pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>

After 1 step:
pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>

After 2 steps:
pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>

After 3 steps:
pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>
pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>
pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>
pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>

After 4 steps:
pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>
pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>
pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>
pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>

After 5 steps:
pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>
pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>
pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>
pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>

After 6 steps:
pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>
pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>
pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>
pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>

After 7 steps:
pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>
pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>
pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>
pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>

After 8 steps:
pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>
pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>
pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>

After 9 steps:
pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>
pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>

After 10 steps:
pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
Then, it might help to calculate the total energy in the system. The total energy for a single moon is its potential energy multiplied by its kinetic energy. A moon's potential energy is the sum of the absolute values of its x, y, and z position coordinates. A moon's kinetic energy is the sum of the absolute values of its velocity coordinates. Below, each line shows the calculations for a moon's potential energy (pot), kinetic energy (kin), and total energy:

Energy after 10 steps:
pot: 2 + 1 + 3 =  6;   kin: 3 + 2 + 1 = 6;   total:  6 * 6 = 36
pot: 1 + 8 + 0 =  9;   kin: 1 + 1 + 3 = 5;   total:  9 * 5 = 45
pot: 3 + 6 + 1 = 10;   kin: 3 + 2 + 3 = 8;   total: 10 * 8 = 80
pot: 2 + 0 + 4 =  6;   kin: 1 + 1 + 1 = 3;   total:  6 * 3 = 18
Sum of total energy: 36 + 45 + 80 + 18 = 179
In the above example, adding together the total energy for all moons after 10 steps produces the total energy in the system, 179.

Here's a second example:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
Every ten steps of simulation for 100 steps produces:

After 0 steps:
pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>

After 10 steps:
pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>

After 20 steps:
pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>
pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>
pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>
pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>

After 30 steps:
pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>
pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>
pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>
pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>

After 40 steps:
pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>
pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>
pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>
pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>

After 50 steps:
pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>

After 60 steps:
pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>
pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>
pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>
pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>

After 70 steps:
pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>
pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>
pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>
pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>

After 80 steps:
pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>
pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>
pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>
pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>

After 90 steps:
pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>
pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>
pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>
pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>

After 100 steps:
pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>

Energy after 100 steps:
pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
Sum of total energy: 290 + 608 + 574 + 468 = 1940
What is the total energy in the system after simulating the moons given in your scan for 1000 steps?
<x=-19, y=-4, z=2>
<x=-9, y=8, z=-16>
<x=-4, y=5, z=-11>
<x=1, y=9, z=-13>
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

moonPositions = problemData

step = 0
lastStep = 1000

# p0 = -1
# v0 = 0
# p1 = 2
# v1 = 0
# p2 = 4
# v2 = 0
# p3 = 3
# v3 = 0

# while step < lastStep:
	# step += 1
	# print("\nstep",step)
	# g0 = calVelocityDelta(p0,p1,p2,p3)
	# g1 = calVelocityDelta(p1,p0,p2,p3)
	# g2 = calVelocityDelta(p2,p1,p0,p3)
	# g3 = calVelocityDelta(p3,p1,p2,p0)
	# #print("x velocity deltas",g0,g1,g2,g3)
	# p0 += g0 + v0
	# p1 += g1 + v1
	# p2 += g2 + v2
	# p3 += g3 + v3
	# v0 += g0
	# v1 += g1
	# v2 += g2
	# v3 += g3
	# print("x position after",p0,p1,p2,p3)
	# print("x velocity after",v0,v1,v2,v3)
	

# exit()
	
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
	
	
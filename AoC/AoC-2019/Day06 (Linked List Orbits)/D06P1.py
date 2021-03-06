# Pt1-AoCDay6.py
# 2019 Advent of Code
# Day 6
# Part 1
# https://adventofcode.com/2019/day/6

"""
--- Day 6: Universal Orbit Map ---
You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /
In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".

Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
COM orbits nothing.
The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?

Your puzzle answer was 387356.
"""
from __future__ import print_function

import time

def findParent(node,nodeList):
	for nodePair in nodeList:
		if nodePair[1] == node:
			#print("Parent of",node,"is",nodePair[0])
			return nodePair[0]

def countStepsToCom(node,nodeList):
	#print("countStepsToCom: Current node :",node)
	parent = ''
	pathsCount = 0
	while(parent != 'COM'):
		parent = findParent(node,nodeList)
		node = parent
		pathsCount = pathsCount + 1
	#print("took",pathsCount,"steps")
	return(pathsCount)

def processList(newNodeNames,nodesList):
	totalSteps = 0
	for node in newNodeNames:
		#print("Tracing back from node :",node)
		totalSteps = totalSteps + countStepsToCom(node,nodesList)
	print("Total number of steps:",totalSteps)

inputVal = 1
# open file and read the content into a list
inList = [line.rstrip('\n') for line in open('AOC2019D06input.txt')]

print('Reading in file',time.strftime('%X %x %Z'))
#nodesList = []
nodesList = [pair.split(')') for pair in inList]
nodeNames = []
for nodePairs in nodesList:
	if nodePairs[0] not in nodeNames:
		nodeNames.append(nodePairs[0])
	if nodePairs[1] not in nodeNames:
		nodeNames.append(nodePairs[1])
print("Node Count",len(nodeNames))
# Make a list without 'COM'
newNodeNames = [node for node in nodeNames if node != 'COM']
processList(newNodeNames,nodesList)
print('Completed processing',time.strftime('%X %x %Z'))

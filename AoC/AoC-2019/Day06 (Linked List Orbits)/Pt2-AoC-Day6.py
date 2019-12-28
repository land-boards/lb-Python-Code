# Pt2-AoCDay6.py
# 2019 Advent of Code
# Day 6
# Part 2
# https://adventofcode.com/2019/day/6

"""
--- Part Two ---
Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you move from any object to an object orbiting or orbited by that object.

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
K)YOU
I)SAN
Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4 orbital transfers are required:

K to J
J to E
E to D
D to I
Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU
What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)
533 was too high.

"""
from __future__ import print_function

def findParent(node,nodeList):
	for nodePair in nodeList:
		if nodePair[1] == node:
			return nodePair[0]

def countStepsToPoint(goalNode,node,nodeList):
	parent = ''
	pathsCount = 0
	while(parent != goalNode):
		parent = findParent(node,nodeList)
		node = parent
		pathsCount = pathsCount + 1
	return(pathsCount)

def pathToCom(node,nodeList):
	parent = ''
	thePath = []
	while(parent != 'COM'):
		parent = findParent(node,nodeList)
		thePath.append(parent)
		node = parent
	return(thePath)

def processList(newNodeNames,nodesList):
	myPathToCom = pathToCom('YOU',nodesList)
	santaPathToCom = pathToCom('SAN',nodesList)
	for node in myPathToCom:
		if node in santaPathToCom:
			goalNode = node
			break
	myDistanceToCommon = countStepsToPoint(goalNode,'YOU',nodesList)
	santaDistanceToCommon = countStepsToPoint(goalNode,'SAN',nodesList)
	print("Total steps",myDistanceToCommon+santaDistanceToCommon-2)

inputVal = 1
# open file and read the content into a list
inList = [line.rstrip('\n') for line in open('AOC2019D06input.txt')]
nodesList = [pair.split(')') for pair in inList]
nodeNames = []
for nodePairs in nodesList:
	if nodePairs[0] not in nodeNames:
		nodeNames.append(nodePairs[0])
	if nodePairs[1] not in nodeNames:
		nodeNames.append(nodePairs[1])
# Make a list without 'COM'
newNodeNames = [node for node in nodeNames if node != 'COM']
processList(newNodeNames,nodesList)

# Pt1-AoCDay6.py
# 2019 Advent of Code
# Day 6
# Part 1

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
			#print("Parent of",node,"is",nodePair[0])
			return nodePair[0]

def countStepsToPoint(goalNode,node,nodeList):
	print("countStepsToCom: Current node :",node)
	parent = ''
	pathsCount = 0
	while(parent != goalNode):
		parent = findParent(node,nodeList)
		node = parent
		pathsCount = pathsCount + 1
	print("took",pathsCount,"steps")
	return(pathsCount)

def pathToCom(node,nodeList):
	#print("pathToCom: Current node :",node)
	parent = ''
	thePath = []
	while(parent != 'COM'):
		parent = findParent(node,nodeList)
		thePath.append(parent)
		node = parent
	return(thePath)

def processList(newNodeNames,nodesList):
	myPathToCom = pathToCom('YOU',nodesList)
	print("My path to com",myPathToCom)
	santaPathToCom = pathToCom('SAN',nodesList)
	print("Santa's path to com",santaPathToCom)
	for node in myPathToCom:
		if node in santaPathToCom:
			goalNode = node
			print("First common point",node)
			break
	myDistanceToCommon = countStepsToPoint(goalNode,'YOU',nodesList)
	santaDistanceToCommon = countStepsToPoint(goalNode,'SAN',nodesList)
	print("Total steps",myDistanceToCommon+santaDistanceToCommon-2)

inputVal = 1
# open file and read the content into a list
inList = [line.rstrip('\n') for line in open('input.txt')]

nodesList = []
for pair in inList:
	nodePair = pair.split(')')
	nodesList.append(nodePair)
#print(nodesList)
nodeNames = []
for nodePairs in nodesList:
	if nodePairs[0] not in nodeNames:
		nodeNames.append(nodePairs[0])
	if nodePairs[1] not in nodeNames:
		nodeNames.append(nodePairs[1])
print("Node Count",len(nodeNames))
# Make a list without 'COM'
newNodeNames = []
for node in nodeNames:
	if node != 'COM':
		newNodeNames.append(node)
# for node in newNodeNames:
	# print(node,end=' ')
# print()
processList(newNodeNames,nodesList)


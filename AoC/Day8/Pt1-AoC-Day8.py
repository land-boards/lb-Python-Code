# Pt1-AoCDay8.py
# 2018 Advent of Code
# Day 8
# Part 1
# https://adventofcode.com/2018/day/8

import time
import re

"""

--- Day 8: Memory Maneuver ---
The sleigh is much easier to pull than you'd expect for something its weight. Unfortunately, neither you nor the Elves know which way the North Pole is from here.

You check your wrist device for anything that might help. It seems to have some kind of navigation system! Activating the navigation system produces more bad news: "Failed to start navigation system. Could not read software license file."

The navigation system's license file consists of a list of numbers (your puzzle input). The numbers define a data structure which, when processed, produces some kind of tree that can be used to calculate the license number.

The tree is made up of nodes; a single, outermost node forms the tree's root, and it contains all other nodes in the tree (or contains nodes that contain nodes, and so on).

Specifically, a node consists of:

A header, which is always exactly two numbers:
The quantity of child nodes.
The quantity of metadata entries.
Zero or more child nodes (as specified in the header).
One or more metadata entries (as specified in the header).
Each child node is itself a node that has its own header, child nodes, and metadata. For example:

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A----------------------------------
    B----------- C-----------
                     D-----
In this example, each node of the tree is also marked with an underline starting with a letter for easier identification. In it, there are four nodes:

A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
C, which has 1 child node (D) and 1 metadata entry (2).
D, which has 0 child nodes and 1 metadata entry (99).
The first check done on the license file is to simply add up all of the metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.

What is the sum of all metadata entries?

Note: It's really more like this

2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
A--                           -----
    B----------- C--       --
                     D-----

2044 nodes

Traceback (most recent call last):
 line 98, in pushNodeAtPoint
    currentMetaCount = myList[listOffset + 1]
IndexError: list index out of range

"""


def readTextFileToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
	:returns: the list sorted list
	"""
	textFile = ''
	with open(fileName, 'r') as filehandle:  
		for char in filehandle:
			textFile += char
	return textFile
	
def stringOfNumbersToList(str):
	"""stringOfNumbersToList - Take the input file which is a really long list and turn it into a python list
	"""
	theList = []
	num = 0
	for letter in str:
		if letter >= '0' and letter <= '9':
			num = num*10 + ord(letter)-ord('0')
		else:
			theList.append(num)
			num = 0
	return theList

#####################################################################################
## Functions which operate on the input file and node lists

def pushNodeAtPoint(listOffset,parentID):
	"""pushNodeAtPoint
	:returns: True if the node being pushed has no children
	False if there are additional children
	"""
	global nodeList
	global myList
	endNode = False
	currentChildCountOffset = listOffset
	if listOffset == len(myList):
		return True
	currentChildCount = myList[listOffset]
	if currentChildCount == 0:
		currentMetaCountOffset = listOffset+2
		endNode = True
	else:
		currentMetaCountOffset = -1
	currentMetaCount = myList[listOffset + 1]
	newNode = [currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentID]
	nodeList.append(newNode)
	print '+',
	return endNode
	
def isNodeStored(listOffset):
	"""isNodeStored - Check to see if a node is already stored in the node list
	Ignores the metaOffset field
	"""
	global nodeList
	global myList
	for nodeVal in nodeList:
		if nodeVal[0] == listOffset and nodeVal[1] == myList[listOffset] and nodeVal[3] == myList[listOffset + 1]:
			return True
	return False

#####################################################################################
## Functions which operate on the node list

def getNode(nodeNum):
	"""Pull the node from the node list by node number
	"""
	global nodeList
	return nodeList[nodeNum]

def isNodeComplete(nodeNum):
	"""
	nodeList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentID]
	"""
	global nodeList
	if nodeList[nodeNum][2] != -1:
		return True
	return False

def getNodeCount():
	"""getNodeCount - Get the count of the number of nodes 
	Used to terminate loops
	"""
	global nodeList
	return len(nodeList)
	
def getChildCount(nodeNum):
	"""getChildCount - get the count of the children of a particular node
	Used as a helper function to remember the name 
	"""
	global nodeList
	return nodeList[nodeNum][1]

def getNumberOfChildrenForAnyParent(parentNodeNum):
	"""getNumberOfChildrenForAnyParent - get the number of children populated in the nodeList for any parent
	"""
	global nodeList
	childCount = 0
	for i in xrange(1,len(nodeList)):		# skip top of tree
		if nodeList[i][4] == parentNodeNum:
			childCount += 1
	return childCount

def getLastChildWithParentNumber(parentNodeNum):
	"""getLastChildWithParentNumber - scan the node list to find the last child that has a particular parent number
	"""
	global nodeList
	for i in xrange(len(nodeList)-1, 0, -1):
		if nodeList[i][4] == parentNodeNum:
			return i
	return 0

def allChildrenAreComplete(parentNodeNum):
	"""allChildrenAreComplete - checkes all of the children below a parent node to see if the metadata count is update
	:returns" True if all of the children below that parent are completed
	"""
	global nodeList
	for i in xrange(1,len(nodeList)):
		if nodeList[i][4] == parentNodeNum:
			if nodeList[i][2] == -1:
				return False
	return True
	
def isTreeDone():
	"""isTreeDone - scans the entire tree to see if all of the nodes have their metadata count updated
	Filling the metadata count is the last step to being complete
	nodeList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentID
	"""
	global nodeList
	for record in nodeList:
		if record[2] == -1:
			return False
	return True
	
def checkChildrenTree():
	"""checkChildrenTree - scans the entire tree to see if any nodes can have their metadata count updated
	nodeList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentID]
	"""
	global nodeList
	recNum = 0
	for record in nodeList:
		if record[2] == -1:
			if getNumberOfChildrenForAnyParent(recNum) == record[1]:	# record needs filled in better
				if allChildrenAreComplete(recNum):
					recNumLastChild = getLastChildWithParentNumber(recNum)
					metaOffset = nodeList[recNumLastChild][2]+nodeList[recNumLastChild][3]
					nodeList[recNum][2] = metaOffset
					print '.',
					return True
		recNum += 1
	return False

def dumpNodes():
	"""dumpNodes - print out a dump of the nodes
	Format is: chOff,chCt,metaOff,metaCt,parentID
	chOff is the offset of the node itself
	chCt is the count of the children from this node
	metaOff is the offset to the start of the metadata
	metaCt is the count of metadata elements
	parentID is the ID of the parent to this node
	"""
	global nodeList
	print 'dumpNodes: length of nodes',len(nodeList)
	for node in nodeList:
		print '[chOff,chCt,metaOff,metaCt,parentID] =',
		print node

########################################################################
## This is the workhorse of this assignment

def scanTree():
	"""scanTree - This is the core of the code.
	I put this into a function to make it easier to return out in the middle
	This is a nested mess
	It works with the data set but seems way to slow to be practical for real use
	Solution is pure brute force
	calling function primes pushNodeAtPoint() for the first node
	"""
	global nodeList
	continueLooping = True
	checkNodeNumber = 0
	while continueLooping:
		continueLooping = False
		nodeOffset = 0
		if getChildCount(checkNodeNumber) > 0:
			nodeVect = getNode(checkNodeNumber)
			nodeOffset = nodeVect[0] + 2
			if not isNodeStored(nodeOffset):
				continueLooping = True
				if pushNodeAtPoint(nodeOffset,checkNodeNumber): # last point was an endpoint
					while checkChildrenTree():
						continue
					if isTreeDone() == True:
						return
					lastNode = getNode(checkNodeNumber+1)
					pushNodeAtPoint(lastNode[2]+lastNode[3],checkNodeNumber)
					while checkChildrenTree():
						continue
					if isTreeDone() == True:
						return
		checkNodeNumber += 1
		if checkNodeNumber == len(nodeList):
			checkNodeNumber = 0		
		else:
			continueLooping = True

########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

textList = readTextFileToList('input.txt')

myList = stringOfNumbersToList(textList)

nodeList = []
listOffset = 0
listLength = len(myList)

pushNodeAtPoint(listOffset,0)	# prime with the first node

print 'Scanning Tree',time.strftime('%X %x %Z')

scanTree()

print 'Done scanning tree',time.strftime('%X %x %Z')

print
dumpNodes()

print 'Accumulate sums',time.strftime('%X %x %Z')

accumMetaRecLens = 0
for node in nodeList:
	startSpan = node[2]
	endSpan = node[2] + node[3]
	while(startSpan < endSpan):
		accumMetaRecLens += myList[startSpan]
		startSpan += 1
print '\nSum =',accumMetaRecLens

	
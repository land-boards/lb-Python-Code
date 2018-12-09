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
 line 98, in pushNodeAtPointToUnsolvedList
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
## Functions which operate on the node list

def getNumberOfChildrenForAnyParentBothLists(parentNodeNum):
	"""getNumberOfChildrenForAnyParentBothLists - get the number of children populated in the unsolvedNodesList for any parent
	"""
	global unsolvedNodesList
	global solvedNodesList
	childCount = 0
	for i in xrange(1,len(unsolvedNodesList)):		# skip top of tree
		if unsolvedNodesList[i][4] == parentNodeNum:
			childCount += 1
	for i in xrange(0,len(solvedNodesList)):		# skip top of tree
		if solvedNodesList[i][4] == parentNodeNum:
			childCount += 1
	return childCount

def getLastChildWithParentNumber(parentNodeNum):
	"""getLastChildWithParentNumber - scan the node list to find the last child that has a particular parent number
	"""
	global unsolvedNodesList
	for i in xrange(len(unsolvedNodesList)-1, 0, -1):
		if unsolvedNodesList[i][4] == parentNodeNum:
			return i
	return 0

def allChildrenAreComplete(parentNodeNum):
	"""allChildrenAreComplete - checkes all of the children below a parent node to see if the metadata count is update
	:returns" True if all of the children below that parent are completed
	"""
	global unsolvedNodesList
	for i in xrange(1,len(unsolvedNodesList)):
		if unsolvedNodesList[i][4] == parentNodeNum:
			if unsolvedNodesList[i][2] == -1:
				return False
	return True
	
def moveChildFromUnsolvedToSolvedNodesList(recNum):
	"""
	"""
	global unsolvedNodesList
	global solvedNodesList
	#print 'moveChildFromUnsolvedToSolvedNodesList: recNum',recNum,'contents',unsolvedNodesList[recNum]
	recordToMove = unsolvedNodesList[recNum]
	#print 'moving record',recordToMove
	unsolvedNodesList.remove(recordToMove)
	solvedNodesList.append(recordToMove)
	#print 'unsolvedNodesList',unsolvedNodesList
	#print 'solvedNodesList',solvedNodesList

def checkChildrenTree():
	"""checkChildrenTree - scans the entire tree to see if any nodes can have their metadata count updated
	unsolvedNodesList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber]
	"""
	global unsolvedNodesList
	recNum = 0
	for record in unsolvedNodesList:
		if record[2] == -1:
			if getNumberOfChildrenForAnyParentBothLists(recNum) == record[1]:
				if allChildrenAreComplete(recNum):
					recNumLastChild = getLastChildWithParentNumber(recNum)
					metaOffset = unsolvedNodesList[recNumLastChild][2]+unsolvedNodesList[recNumLastChild][3]
					unsolvedNodesList[recNum][2] = metaOffset
					print '.',
					moveChildFromUnsolvedToSolvedNodesList(recNum)
					return True
		recNum += 1
	return False

def getSisterOffset(unsolvedNodesIndex):
	"""If a node has a sister and the sister is not on the node list, then add it to the node list
	unsolvedNodesList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber]
	:returns: -1 if failed
	otherwise offset to the start of the next record
	"""
	global unsolvedNodesList
	global myList
	nodeElement = unsolvedNodesList[unsolvedNodesIndex]
	#print 'checkNodeForSister: nodeElement',nodeElement,
	if nodeElement[2] == -1:	# Node itself is not resolved
		#print 'node is not yet resolved'
		return -1
	nextNodeOffset = nodeElement[0] + nodeElement[2] + 1
	#print 'nextNodeOffset',nextNodeOffset,
	if nextNodeOffset >= len(myList):	# can't push past the end of the list
		#print 'cant go past end of the node'
		return -1
	#print 'sister found'
	return nextNodeOffset

def getParentNodeNumberOfSisterAtLocation(nextOffset):
	global unsolvedNodesList
	global solvedNodesList
	global myList
	print 'getParentNodeNum...:nextOffset',nextOffset
	for nodeVal in unsolvedNodesList:
		if nodeVal[0] == nextOffset:
			return nodeVal[4]
	for nodeVal in solvedNodesList:
		if nodeVal[0] == nextOffset:
			return nodeVal[4]
	print 'getParentNodeNum...: didnt find parent'
	exit()

def getChildCount(nodeNum):
	"""getChildCount - get the count of the children of a particular node
	Used as a helper function to remember the name 
	"""
	global unsolvedNodesList
	#print 'getChildCount: with nodeNum',nodeNum,'from list',unsolvedNodesList[nodeNum][1]
	return unsolvedNodesList[nodeNum][1]

def checkNodeForSister(exampleOffset):
	"""If a node has a sister and the sister is not on the node list, then add it to the node list
	unsolvedNodesList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber]
	:returns: -1 if failed
	otherwise offset to the start of the next record
	"""
	global unsolvedNodesList
	global myList
	if len(unsolvedNodesList) <= exampleOffset:
		print 'checkNodeForSister: offset too big',
		print 'exampleOffset',exampleOffset
		print 'len(unsolvedNodesList)',len(unsolvedNodesList)
		exit()
	nodeElement = unsolvedNodesList[exampleOffset]
	#print 'checkNodeForSister: nodeElement',nodeElement,
	if nodeElement[2] == -1:	# Node itself is not resolved
		#print 'node is not yet resolved'
		return False
	nextNodeOffset = nodeElement[0] + nodeElement[2] + 1
	#print 'nextNodeOffset',nextNodeOffset,
	if nextNodeOffset >= len(myList):	# can't push past the end of the list
		#print 'cant go past end of the node'
		return False
	#print 'sister found'
	return True

#####################################################################################
## Functions which operate on the input file and node lists

def isNodeStoredInUnsolvedNodesList(listOffset):
	"""isNodeStoredInUnsolvedNodesList - Check to see if a node is already stored in the node list
	Ignores the metaOffset field
	"""
	global unsolvedNodesList
	global myList
	for nodeVal in unsolvedNodesList:
		if nodeVal[0] == listOffset and nodeVal[1] == myList[listOffset] and nodeVal[3] == myList[listOffset + 1]:
			return True
	return False

def pushNodeAtPointToUnsolvedList(listOffset,parentNodeNumber):
	"""pushNodeAtPointToUnsolvedList
	:returns: True if the node being pushed has no children
	False if there are additional children
	"""
	global unsolvedNodesList
	global myList
	global nodeNumber
	print 'push...: pushing child @',listOffset#,'nodeNumber',nodeNumber
	endNode = False
	currentChildCountOffset = listOffset
	if listOffset >= len(myList)-2:
		return False
	currentChildCount = myList[listOffset]
	if currentChildCount == 0:
		currentMetaCountOffset = listOffset+2
		endNode = True
	else:
		currentMetaCountOffset = -1
	currentMetaCount = myList[listOffset + 1]
	newNode = [currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	unsolvedNodesList.append(newNode)
	nodeNumber = nodeNumber + 1
	#print 'nodeNumber',nodeNumber
	#print '+',
	#print 'unsolvedNodesList',unsolvedNodesList
	return endNode
	
def countSolvedNodesWithParentID(parentID):
	global solvedNodesList
	matchCount = 0
	for record in solvedNodesList:
		if record[4] == parentID:
			matchCount += 1
	#print 'countSolvedNodesWithParentID: lookiung for parentID',parentID,'matchCount =',matchCount
	return matchCount

def checkNodeForComplete(nodeToCheck):
	global unsolvedNodesList
	#print 'checkNodeForComplete: @',nodeToCheck,'val',
	if unsolvedNodesList[nodeToCheck][2] != -1:
		#print 'true'
		return True
	else:
		#print 'false'
		return False
	
def isChildInEitherList(listOffset):
	"""isNodeStoredInUnsolvedNodesList - Check to see if a node is already stored in either node list
	Ignores the metaOffset field
	"""
	global unsolvedNodesList
	global solvedNodesList
	global myList
	#print 'isChildInEitherList: listOffset',listOffset,
	for nodeVal in unsolvedNodesList:
		if nodeVal[0] == listOffset:
			#print 'in unsolved list'
			return True
	for nodeVal in solvedNodesList:
		if nodeVal[0] == listOffset:
			#print 'in solved list'
			return True
	#print 'in neither list'
	return False

def dumpNodes():
	"""dumpNodes - print out a dump of the nodes
	Format is: chOff,chCt,metaOff,metaCt,parentNodeNumber
	chOff is the offset of the node itself
	chCt is the count of the children from this node
	metaOff is the offset to the start of the metadata
	metaCt is the count of metadata elements
	parentNodeNumber is the ID of the parent to this node
	"""
	global solvedNodesList
	print 'dumpNodes: length of nodes',len(solvedNodesList)
	print 'solved list'
	for node in solvedNodesList:
		print '[chOff,chCt,metaOff,metaCt,parentNodeNumber] =',
		print node
	print 'unsolved list'
	for node in unsolvedNodesList:
		print '[chOff,chCt,metaOff,metaCt,parentNodeNumber] =',
		print node

def findLastChildEndOffset(listItemNum):
	"""
	Format is: chOff,chCt,metaOff,metaCt,parentNodeNumber
	
	0 0 0 0  0  0  0 0 0 0 0  1 1 1 1 1
	0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
	
	2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
	A----------------------------------
        B----------- C-----------
                         D-----
	"""
	print '\nfindLastChildEndOffset: listItemNum',listItemNum
	print 'findLastChildEndOffset: looking for children in solved list with me as parent in list'
	print unsolvedNodesList[listItemNum]
	print 'findLastChildEndOffset:\nsolvedNodesList'
	for myItem in unsolvedNodesList:
		print myItem
	myID = unsolvedNodesList[listItemNum][5]
	print 'myID',myID
	maxVal = 0
	matchingItem = []
	for item in solvedNodesList:
		if item[4] == myID and item[0] != 0:
			if item[0] > maxVal:
				maxVal = item[0]
				matchingItem = item
	print 'maxVal',maxVal
	print 'matchingItem[]',matchingItem
	newOff = matchingItem[2] + matchingItem[3]
	print 'newOff',newOff,'\n'
	return newOff

########################################################################
## This is the workhorse of this assignment

def scanTree():
	"""scanTree - This is the core of the code.
	I put this into a function to make it easier to return out in the middle
	This is a nested mess
	It works with the data set but seems way to slow to be practical for real use
	Solution is pure brute force
	calling function primes pushNodeAtPointToUnsolvedList() for the first node
	"""
	global unsolvedNodesList
	global solvedNodesList
	while len(unsolvedNodesList) > 0:
		didSomethingInEntireList = False
		for unsolvedNodesIndex in xrange(len(unsolvedNodesList)):
			didSomethingInThisPass = True
			#print 'scanTree: u-s-Index',unsolvedNodesIndex
			if checkNodeForSister(unsolvedNodesIndex) and (isChildInEitherList(getSisterOffset(unsolvedNodesIndex)) == False):
				nextOffset = getSisterOffset(unsolvedNodesIndex)
				print 'scanTree: pushing sister node at',nextOffset,'to unsolved list',
				parentNodeNumber = unsolvedNodesList[unsolvedNodesIndex][4]
				print 'sisters parent ID is',parentNodeNumber
				pushNodeAtPointToUnsolvedList(nextOffset,parentNodeNumber)
				while checkChildrenTree():
					continue
			elif getChildCount(unsolvedNodesIndex) == 0:
				#print 'scanTree: node has no children so move it to the solved list'
				moveChildFromUnsolvedToSolvedNodesList(unsolvedNodesIndex)
			elif getChildCount(unsolvedNodesIndex) == countSolvedNodesWithParentID(unsolvedNodesList[unsolvedNodesIndex][5]):
				#print 'scanTree: moving node from unsolved to solved list',unsolvedNodesList[unsolvedNodesIndex]
				unsolvedNodesList[unsolvedNodesIndex][2] = findLastChildEndOffset(unsolvedNodesIndex)
				#print 'end',unsolvedNodesList[unsolvedNodesIndex][2]
				moveChildFromUnsolvedToSolvedNodesList(unsolvedNodesIndex)					
			elif checkNodeForComplete(unsolvedNodesIndex) == True:
				#print 'scanTree: moving another solved one over to solved list',
				moveChildFromUnsolvedToSolvedNodesList(unsolvedNodesIndex)					
			elif not isChildInEitherList(unsolvedNodesList[unsolvedNodesIndex][0] + 2):
				print 'scanTree: pushing new child to unsolved list',
				countTimesThrough = 0
				parentNodeNumber = unsolvedNodesList[unsolvedNodesIndex][5]
				print 'parent is',parentNodeNumber,'from',unsolvedNodesList[unsolvedNodesIndex]
				pushNodeAtPointToUnsolvedList(unsolvedNodesList[unsolvedNodesIndex][0] + 2,parentNodeNumber) # last point was an endpoint
				while checkChildrenTree():
					continue
			else:
				#print 'did nothing in this pass'
				didSomethingInThisPass = False
			if didSomethingInThisPass:
				#print 'did someting in this pass'
				didSomethingInEntireList = True
				break
		if not didSomethingInEntireList:
			print 'finished the list except for',unsolvedNodesList
			print 'solved',solvedNodesList,'\n\n'
			unsolvedNodesList[0][2] = findLastChildEndOffset(0)
			print 'end',unsolvedNodesList[0][2]
			moveChildFromUnsolvedToSolvedNodesList(0)					
			return
	print 'wtf'
	return
		

########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

textList = readTextFileToList('input2.txt')

myList = stringOfNumbersToList(textList)

nodeNumber = 0

unsolvedNodesList = []
pushNodeAtPointToUnsolvedList(0,0)	# prime with the first node

solvedNodesList = []

print 'Scanning Tree',time.strftime('%X %x %Z')

scanTree()
solvedNodesList = sorted(solvedNodesList, key = lambda errs: errs[5])

print 'Done scanning tree',time.strftime('%X %x %Z')

print
dumpNodes()

print 'Accumulate sums',time.strftime('%X %x %Z')

accumMetaRecLens = 0
for node in solvedNodesList:
	startSpan = node[2]
	endSpan = node[2] + node[3]
	while(startSpan < endSpan):
		accumMetaRecLens += myList[startSpan]
		startSpan += 1
print '\nSum =',accumMetaRecLens

	
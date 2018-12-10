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

#####################################################################################
## Functions which read and form the input file

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

def moveChildFromUnsolvedToSolvedNodesList(recNum):
	"""moveChildFromUnsolvedToSolvedNodesList - Take the node out of the unsolved list and move it to the solved list
	"""
	global unsolvedNodesList
	global solvedNodesList
	recordToMove = unsolvedNodesList[recNum]
	unsolvedNodesList.remove(recordToMove)
	solvedNodesList.append(recordToMove)
	print '.',

def getChildCount(nodeNum):
	"""getChildCount - get the count of the children of a particular node
	Used as a helper function to remember the name 
	"""
	global unsolvedNodesList
	#print 'getChildCount: with nodeNum',nodeNum,'from list',unsolvedNodesList[nodeNum][currentChCt]
	return unsolvedNodesList[nodeNum][currentChCt]

#####################################################################################
## Functions which operate on the input file and node lists

def pushNodeAtPointToUnsolvedList(listOffset,parentNodeNumber):
	"""pushNodeAtPointToUnsolvedList
	:returns: True if the node being pushed has no children
	False if there are additional children
	
	intFileListOff = 0
	currentChCt = 1
	currentMtOff = 2
	currentMtCt = 3
	parentNum = 4
	nodeNum = 5

	"""
	debug_pushNodeAtPointToUnsolvedList = False
	global unsolvedNodesList
	global myList
	global nodeNumber
	if debug_pushNodeAtPointToUnsolvedList:
		print 'push...: pushing child @',listOffset,
		print 'nodeNumber',nodeNumber,
	if listOffset >= len(myList)-2:
		print 'pushNodeAtPointToUnsolvedList: tried to get a node past the end'
		exit()
		return False
	if debug_pushNodeAtPointToUnsolvedList:
		print 'child ct = ',myList[listOffset],
	currentChildCount = myList[listOffset]
	if currentChildCount == 0:
		currentMetaCountOffset = listOffset+2
	else:
		currentMetaCountOffset = -1
	currentMetaCount = myList[listOffset + 1]
	newNode = [0,0,0,0,0,0]
	newNode[intFileListOff] = listOffset
	newNode[currentChCt] = currentChildCount
	newNode[currentMtOff] = currentMetaCountOffset
	newNode[currentMtCt] = currentMetaCount
	newNode[parentNum] = parentNodeNumber
	newNode[nodeNum] = nodeNumber
	unsolvedNodesList.append(newNode)
	nodeNumber = nodeNumber + 1
	if debug_pushNodeAtPointToUnsolvedList:
		print 'nodeNumber',nodeNumber,
		print '+'
		#print 'unsolvedNodesList',unsolvedNodesList
	return
	
def countSolvedNodesWithParentID(parentID):
	"""
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	"""
	debug_countSolvedNodesWithParentID = True
	global solvedNodesList
	matchCount = 0
	for record in solvedNodesList:
		if record[parentNum] == parentID:
			matchCount += 1
	if debug_countSolvedNodesWithParentID:
		print 'countSolvedNodesWithParentID: nodes with parentID',parentID,'Count =',matchCount
	return matchCount

def countUnsolvedNodesWithParentID(parentID):
	"""
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	"""
	debug_countUnsolvedNodesWithParentID = True
	global unsolvedNodesList
	matchCount = 0
	for record in unsolvedNodesList:
		if record[parentNum] == parentID:
			matchCount += 1
	if debug_countUnsolvedNodesWithParentID:
		print 'countUnsolvedNodesWithParentID: looking for parentID',parentID,'matchCount =',matchCount
	return matchCount

def checkNodeForComplete(nodeToCheck):
	"""
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	"""
	global unsolvedNodesList
	#print 'checkNodeForComplete: @',nodeToCheck,'val',
	if unsolvedNodesList[nodeToCheck][currentMtOff] != -1:
		#print 'true'
		return True
	else:
		#print 'false'
		return False
	
def isChildInEitherList(listOffset):
	"""isChildInEitherList - Check to see if a node is already stored in either node list
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	Ignores the metaOffset field
	"""
	global unsolvedNodesList
	global solvedNodesList
	global myList
	#print 'isChildInEitherList: listOffset',listOffset,
	for nodeVal in unsolvedNodesList:
		if nodeVal[intFileListOff] == listOffset:
			#print 'in unsolved list'
			return True
	for nodeVal in solvedNodesList:
		if nodeVal[intFileListOff] == listOffset:
			#print 'in solved list'
			return True
	#print 'in neither list'
	return False

def dumpNodes():
	"""dumpNodes - print out a dump of the nodes
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	chOff is the offset of the node itself
	chCt is the count of the children from this node
	metaOff is the offset to the start of the metadata
	metaCt is the count of metadata elements
	parentNodeNumber is the ID of the parent to this node
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
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
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	
	0 0 0 0  0  0  0 0 0 0 0  1 1 1 1 1
	0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
	
	2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
	A----------------------------------
        B----------- C-----------
                         D-----
	"""
	#print '\nfindLastChildEndOffset: listItemNum',listItemNum
	#print 'findLastChildEndOffset: looking for children in solved list with me as parent in list'
	#print unsolvedNodesList[listItemNum]
	#print 'findLastChildEndOffset:\n unsolvedNodesList'
	# for myItem in unsolvedNodesList:
		# print myItem
	myID = unsolvedNodesList[listItemNum][nodeNum]
	#print 'myID',myID
	maxVal = 0
	matchingItem = []
	for item in solvedNodesList:
		#print 'checking item',item,'for',myID
		if item[parentNum] == myID:
			#print 'a hit'
			if item[intFileListOff] > maxVal:
				maxVal = item[intFileListOff]
				matchingItem = item
	#print 'maxVal',maxVal
	#print 'matchingItem[]',matchingItem
	newOff = matchingItem[currentMtOff] + matchingItem[currentMtCt]
	#print 'newOff',newOff,'\n'
	return newOff

def getSisterOffset(unsolvedNodesIndex):
	"""If a node has a sister and the sister is not on the node list, then add it to the node list
	unsolvedNodesList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber]
	:returns: -1 if failed
	otherwise offset to the start of the next record
	"""
	debug_getSisterOffset = True
	global unsolvedNodesList
	global myList
	if debug_getSisterOffset:
		print 'getSisterOffset: nodeElement',unsolvedNodesList[unsolvedNodesIndex][nodeNum],
	# if nodeElement[currentMtOff] == -1:	# Node itself is not resolved
		# #print 'node is not yet resolved'
		# return -1
	if debug_getSisterOffset:
		print 'solved dau',countSolvedNodesWithParentID(unsolvedNodesIndex),
		print 'unsolved dau',countUnsolvedNodesWithParentID(unsolvedNodesIndex),
		print 'total children',unsolvedNodesList[unsolvedNodesIndex][currentChCt]
	nextNodeOffset = unsolvedNodesList[unsolvedNodesIndex][intFileListOff] + unsolvedNodesList[unsolvedNodesIndex][currentMtOff] + 1
	if debug_getSisterOffset:
		print 'nextNodeOffset',nextNodeOffset,
	if nextNodeOffset >= len(myList):	# can't push past the end of the list
		if debug_getSisterOffset:
			print 'cant go past end of the node'
		return -1
	if debug_getSisterOffset:
		print 'sister found'
	return nextNodeOffset

def checkNodeForSister(exampleOffset):
	"""If a node has a sister and the sister is not on the node list, then add it to the node list
	unsolvedNodesList format is -[currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber]
	:returns: False if failed
	otherwise True
	"""
	debug_checkNodeForSister = False
	global unsolvedNodesList
	global myList
	if debug_checkNodeForSister:
		print 'checkNodeForSister: node',unsolvedNodesList[exampleOffset][nodeNum],
	if len(unsolvedNodesList) <= exampleOffset:
		if debug_checkNodeForSister:
			print 'checkNodeForSister: offset too big',
			print 'exampleOffset',exampleOffset
			print 'len(unsolvedNodesList)',len(unsolvedNodesList)
		exit()
	if debug_checkNodeForSister:
		print 'solved dau',countSolvedNodesWithParentID(exampleOffset),
		print 'unsolved dau',countUnsolvedNodesWithParentID(exampleOffset),
		print 'total children',unsolvedNodesList[exampleOffset][currentChCt]
	if (countSolvedNodesWithParentID(exampleOffset) + countUnsolvedNodesWithParentID(exampleOffset)) < unsolvedNodesList[exampleOffset][currentChCt]:
		return True
	if unsolvedNodesList[exampleOffset][currentMtOff] == -1:	# Node itself is not resolved
		if debug_checkNodeForSister:
			print 'node is not yet resolved'
		return False
	nextNodeOffset = unsolvedNodesList[exampleOffset][intFileListOff] + unsolvedNodesList[exampleOffset][currentMtOff] + 1
	if debug_checkNodeForSister:
		print 'nextNodeOffset',nextNodeOffset,
	if nextNodeOffset >= len(myList):	# can't push past the end of the list
		if debug_checkNodeForSister:
			print 'cant go past end of the node'
		return False
	if debug_checkNodeForSister:
		print 'sister found'
	return True

########################################################################
## This is the workhorse of this assignment

def scanTree():
	"""scanTree - This is the core of the code.
	[listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,parentNodeNumber,nodeNumber]
	I put this into a function to make it easier to return out in the middle
	This is a nested mess
	It works with the data set but seems way to slow to be practical for real use
	Solution is pure brute force
	calling function primes pushNodeAtPointToUnsolvedList() for the first node
	"""
	debugScanTree = False
	global unsolvedNodesList
	global solvedNodesList
	while len(unsolvedNodesList) > 0:
		didSomethingInEntireList = False
		for unsolvedNodesIndex in xrange(len(unsolvedNodesList)):
			didSomethingInThisPass = True
			if checkNodeForSister(unsolvedNodesIndex) and (isChildInEitherList(getSisterOffset(unsolvedNodesIndex)) == False):
				nextOffset = getSisterOffset(unsolvedNodesIndex)
				#print 'scanTree: pushing sister node at',nextOffset,'to unsolved list',
				parentNodeNumber = unsolvedNodesList[unsolvedNodesIndex][parentNum]
				#print 'sisters parent ID is',parentNodeNumber
				pushNodeAtPointToUnsolvedList(nextOffset,parentNodeNumber)
			#print 'scanTree: u-s-Index',unsolvedNodesIndex
			elif checkNodeForSister(unsolvedNodesIndex) and (isChildInEitherList(getSisterOffset(unsolvedNodesIndex)) == False):
				nextOffset = getSisterOffset(unsolvedNodesIndex)
				#print 'scanTree: pushing sister node at',nextOffset,'to unsolved list',
				parentNodeNumber = unsolvedNodesList[unsolvedNodesIndex][parentNum]
				#print 'sisters parent ID is',parentNodeNumber
				pushNodeAtPointToUnsolvedList(nextOffset,parentNodeNumber)
			elif getChildCount(unsolvedNodesIndex) == 0:
				#print 'scanTree: node has no children so move it to the solved list'
				moveChildFromUnsolvedToSolvedNodesList(unsolvedNodesIndex)
			elif getChildCount(unsolvedNodesIndex) == countSolvedNodesWithParentID(unsolvedNodesList[unsolvedNodesIndex][nodeNum]):
				#print 'scanTree: moving node from unsolved to solved list',unsolvedNodesList[unsolvedNodesIndex]
				#print 'scanTree: getChildCount(unsolvedNodesIndex)',getChildCount(unsolvedNodesIndex)
				#print 'scanTree: countSolvedNodesWithParentID(unsolvedNodesList[unsolvedNodesIndex][nodeNum])',countSolvedNodesWithParentID(unsolvedNodesList[unsolvedNodesIndex][nodeNum])
				unsolvedNodesList[unsolvedNodesIndex][currentMtOff] = findLastChildEndOffset(unsolvedNodesIndex)
				#print 'end',unsolvedNodesList[unsolvedNodesIndex][currentMtOff]
				moveChildFromUnsolvedToSolvedNodesList(unsolvedNodesIndex)					
			elif checkNodeForComplete(unsolvedNodesIndex) == True:
				#print 'scanTree: moving another solved one over to solved list',
				moveChildFromUnsolvedToSolvedNodesList(unsolvedNodesIndex)					
			elif not isChildInEitherList(unsolvedNodesList[unsolvedNodesIndex][intFileListOff] + 2):
				#print 'scanTree: pushing new child to unsolved list',
				countTimesThrough = 0
				parentNodeNumber = unsolvedNodesList[unsolvedNodesIndex][nodeNum]
				#print 'parent is',parentNodeNumber,'from',unsolvedNodesList[unsolvedNodesIndex]
				pushNodeAtPointToUnsolvedList(unsolvedNodesList[unsolvedNodesIndex][intFileListOff] + 2,parentNodeNumber) # last point was an endpoint
			else:
				#print 'did nothing in this pass'
				didSomethingInThisPass = False
			if didSomethingInThisPass:
				#print 'did someting in this pass'
				didSomethingInEntireList = True
				break
		if not didSomethingInEntireList:
			print 'x'
			print 'unsolved list'
			for item in unsolvedNodesList:
				print item
			print 'solved list'
			for item in solvedNodesList:
				print item
			exit()
	return
		

########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

#listOffset,currentChildCount,currentMetaCountOffset,currentMetaCount,nodeNumber,parentNodeNumber

intFileListOff = 0
currentChCt = 1
currentMtOff = 2
currentMtCt = 3
parentNum = 4
nodeNum = 5

textList = readTextFileToList('input.txt')

myList = stringOfNumbersToList(textList)
print 'length of input file',len(myList)

nodeNumber = 0

unsolvedNodesList = []
pushNodeAtPointToUnsolvedList(0,0)	# prime with the first node

solvedNodesList = []

print 'Scanning Tree',time.strftime('%X %x %Z')

scanTree()
solvedNodesList = sorted(solvedNodesList, key = lambda errs: errs[nodeNum])

print 'Done scanning tree',time.strftime('%X %x %Z')

print
dumpNodes()

print 'Accumulate sums',time.strftime('%X %x %Z')

accumMetaRecLens = 0
for node in solvedNodesList:
	startSpan = node[currentMtOff]
	endSpan = node[currentMtOff] + node[currentMtCt]
	while(startSpan < endSpan):
		accumMetaRecLens += myList[startSpan]
		startSpan += 1
print '\nSum =',accumMetaRecLens

	
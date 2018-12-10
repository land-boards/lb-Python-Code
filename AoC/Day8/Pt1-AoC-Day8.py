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

inputList = []
inFileListOff = 0

class filer():
	
	
	def loadListFromFile(self,filename):
		global inputList
		debug_loadListFromFile = False
		inFileString = self.readTextFileToList(filename)
		self.stringOfNumbersToList(inFileString)
		inFileListOff = 0
		if debug_loadListFromFile:
			print 'loadListFromFile: Input File Length =',len(inputList)

	def getNextNodeFromList(self):
		global inputList
		global inFileListOff
		debug_getNextNodeFromList = False
		if debug_getNextNodeFromList:
			print 'getNextNodeFromList: getting next node'
		nextNode = [inputList[inFileListOff],inputList[inFileListOff+1]]
		inFileListOff += 2
		if debug_getNextNodeFromList:
			print 'getNextNodeFromList: nextNode = ',nextNode
		return nextNode
	
	def getFileOffset(self):
		return inFileListOff

	def readTextFileToList(self,fileName):
		"""readTextFileAndSrtToList - open file and read the content to a list
		File is sorted to produce a date/time ordered file
		:returns: the list sorted list
		"""
		global inputList
		textFile = ''
		with open(fileName, 'r') as filehandle:  
			for char in filehandle:
				textFile += char
		return textFile
		
	def stringOfNumbersToList(self,str):
		"""stringOfNumbersToList - Take the input file which is a really long list and turn it into a python list
		"""
		num = 0
		for letter in str:
			if letter >= '0' and letter <= '9':
				num = num*10 + ord(letter)-ord('0')
			else:
				inputList.append(num)
				num = 0

#####################################################################################
## Functions which operate on the node list

nodeList = []
currentNodeNumber = 0
UPNODENUM = 0
DNNODENUM = 1
LFNODENUM = 2
RTNODENUM = 3
NUMOFKIDS = 4
METAOFFST = 5
METALENGTH = 6
FILEOFFST = 7

class NodeFunctions():
	
	
	def createChildNodes(self):
		"""createChildnewNodes - Add the child newNodes to the newNodes list
		"""
		global nodeList
		global currentNodeNumber
		global inputList
		global inFileListOff
		debug_createChildNodes = True
		currNodeNum = self.getCurrentNodeNumber()
		if debug_createChildNodes:
			print 'createChildNodes: currNodeNum',currNodeNum
		currentNodeVec = nodeList[currNodeNum]
		if debug_createChildNodes:
			print 'createChildNodes: currentNodeVec',currentNodeVec
		numberOfKids = currentNodeVec[NUMOFKIDS]
		if debug_createChildNodes:
			print 'createChildNodes: numberOfKids',numberOfKids
		if not (numberOfKids > 0):
			print 'ERROR - createChildnewNodes called with bad child count'
			self.dumpAllNodeVals()
			exit()
		i = 1
		rootNodeFileOffset = currentNodeVec[FILEOFFST]
		while i < (numberOfKids+1):
			newNode = [0,0,0,0,0,0,0,0]
			# if debug_createChildNodes:
				# print 'newNode',newNode
			newNode[UPNODENUM] = currNodeNum
			newNode[DNNODENUM] = -2
			nodeList[currNodeNum][DNNODENUM] = currNodeNum + 1
			newNode[METAOFFST] = -2
			newNode[METALENGTH] = -1
			newNode[RTNODENUM] = currNodeNum + i
			newNode[LFNODENUM] = i - 1
			newNode[FILEOFFST] = rootNodeFileOffset + (2*i)
			newNode[NUMOFKIDS] = -1
			if i == 1:
				if debug_createChildNodes:
					print 'createChildNodes: pushed first child'
				newNode[NUMOFKIDS] = inputList[inFileListOff]  # children count are known
				newNode[LFNODENUM] = -1
			elif i == numberOfKids:
				if debug_createChildNodes:
					print 'createChildNodes: pushed last child'
				newNode[RTNODENUM] = -1
			else:
				if debug_createChildNodes:
					print 'createChildNodes: pushed middle child'
				newNode[LFNODENUM] = i - 1
				newNode[RTNODENUM] = -1
			if debug_createChildNodes:
				print 'newNode',newNode
			self.pushNode(newNode)
			i += 1
		return

	def pushNode(self,node):
		"""pushNode - 
		"""
		global nodeList
		nodeList.append(node)		
		
	def addFirstNode(self,firstNode,inFileOffset):
		"""addFirstNode - add the first node
		Initialize the pointers for the first node
		Special values for pointers are
		-1 dead end (will not be updated later)
		-2 uninitialized but will be later set to something
		
		:param nodeList: the pair [numberKids,lengthOfMetaData] from the input file
		:returns: True when done
		"""
		global nodeList
		global currentNodeNumber
		debug_getNextNodeFromList = False
		currentNodeNumber = 0
		node = [0,0,0,0,0,0,0,0]
		node[UPNODENUM] = -1
		node[DNNODENUM] = -2
		node[LFNODENUM] = -1
		node[RTNODENUM] = -1
		node[NUMOFKIDS] = firstNode[0]
		node[METAOFFST] = -2
		node[METALENGTH] = firstNode[1]
		node[FILEOFFST] = inFileOffset - 2
		self.pushNode(node)
		if debug_getNextNodeFromList:
			print 'Added first node',node
		return
		
	def processNode(self,nodeNumber):
		"""processNode(nodeNumber) - Process the node

		:param nodeNumber: The number of the current node
		:returns: True
		"""
		debug_processNode = True
		# if debug_processNode:
			# self.dumpNodeVals(nodeNumber)
		nodeVec = nodeList[nodeNumber]
		if nodeVec[DNNODENUM] == -2:			# uninitialized down pointer
			if nodeVec[NUMOFKIDS] == 0:			# node has no children
				nodeVec[DNNODENUM] = -1		# node is an endpoint down
			else:	# initialize kids
				self.createChildNodes()
		else:
			return False	# fill in as I go along
		return True
		
	def dumpAllNodeVals(self):
		i = 0
		print 'Dump of entire node table'
		print 'node,[UP,DN,LEFT,RIGHT,KIDS,METAOFF,METALEN,FILEOFF]'
		while i < len(nodeList):
			print i,nodeList[i]
#			self.dumpNodeVals(i)
			i += 1
	
	def dumpNodeVals(self,nodeNumber):
		"""dumpNodeVals
		
		:param: nodeNumber the offset to the node in array
		"""
		debug_dumpNodeVals = True
		print 'Dump of node Number',nodeNumber
		if nodeNumber > len(nodeList) - 1:
			print 'dumpNodeVals: ERROR - Offset is not in list, exiting...'
			exit()
		nodeVec = nodeList[nodeNumber]
		if nodeVec[UPNODENUM] == -1:
			print ' This is node 0'
		else:
			print ' Up node number',nodeVec[UPNODENUM]
		if nodeVec[DNNODENUM] == -1:
			print ' End point down'
		elif nodeVec[DNNODENUM] == -2:
			print ' Unsolved down'
		else:
			print ' First child node number',nodeVec[DNNODENUM]
		if nodeVec[LFNODENUM] == -1:
			print ' Nothing to the left'
		elif nodeVec[LFNODENUM] == -2:
			print ' Left uninitialized'
		else:
			print ' Left node',nodeVec[LFNODENUM]
		if nodeVec[RTNODENUM] == -1:
			print ' No sister to the right'
		elif nodeVec[RTNODENUM] == -2:
			print 'ERROR - uninitialized sister node - should never happen'
			exit()
		else:
			print ' Sister node to the right',nodeVec[RTNODENUM]
		if nodeVec[NUMOFKIDS] == 0:
			print ' Node has no children'
		else:
			print ' Node has',nodeVec[NUMOFKIDS],'children'
		if nodeVec[METAOFFST] == -2:
			print ' Metadata offset is not yet known'
		else:
			print ' Metadata offset',nodeVec[METAOFFST]
		print ' Metadata offset',nodeVec[FILEOFFST]

	def getCurrentNodeNumber(self):
		global currentNodeNumber
		return currentNodeNumber
	
########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

inFileName = 'input2.txt'

InputListHandler = filer()
InputListHandler.loadListFromFile(inFileName)

NodeHandler = NodeFunctions()
firstNode = InputListHandler.getNextNodeFromList()
#print 'firstNode is',firstNode

inFileOff = InputListHandler.getFileOffset()	# should return 0
NodeHandler.addFirstNode(firstNode,inFileOff)
#print 'node',NodeHandler.getCurrentNodeNumber()

while True:
	inFileOff = InputListHandler.getFileOffset()
	currentNodeNumber = NodeHandler.getCurrentNodeNumber()
	if not NodeHandler.processNode(currentNodeNumber):
		break

print 'done', NodeHandler.dumpAllNodeVals()

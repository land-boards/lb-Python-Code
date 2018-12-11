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

0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5

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
		
	def getLenInFile(self):
		global inputList
		return len(inputList)
		
	def stringOfNumbersToList(self,str):
		"""stringOfNumbersToList - Take the input file which is a really long list and turn it into a python list
		"""
		global inputList
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
NODECOMPL = 8
CURRCHWIP = 9
CURRCHNUM = 10

DONE = -1
UNINIT = -2

class NodeFunctions():

	def dumpAllNodeVals(self):
		i = 0
		print '*** Node table ***'
		print 'dumpAllNodeVals: nodes in table',len(nodeList)
		print 'node,[UP,DN,LT,RT,KIDS,METAOFF,METALEN,FILEOFF,NODECOMP,CURRCHIP,CURRCHNUM]'
		for i in xrange(len(nodeList)):
			print i,nodeList[i]
#			self.dumpNodeVals(i)
#		print 'dumpAllNodeVals: done dumping'
		return
		
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
		if nodeVec[UPNODENUM] == DONE:
			print ' This is node 0'
		else:
			print ' Up node number',nodeVec[UPNODENUM]
		if nodeVec[DNNODENUM] == DONE:
			print ' End point down'
		elif nodeVec[DNNODENUM] == UNINIT:
			print ' Unsolved down'
		else:
			print ' First child node number',nodeVec[DNNODENUM]
		if nodeVec[LFNODENUM] == DONE:
			print ' Nothing to the left'
		elif nodeVec[LFNODENUM] == UNINIT:
			print ' Left uninitialized'
		else:
			print ' Left node',nodeVec[LFNODENUM]
		if nodeVec[RTNODENUM] == DONE:
			print ' No sister to the right'
		elif nodeVec[RTNODENUM] == UNINIT:
			print 'ERROR - uninitialized sister node - should never happen'
			exit()
		else:
			print ' Sister node to the right',nodeVec[RTNODENUM]
		if nodeVec[NUMOFKIDS] == 0:
			print ' Node has no children'
		else:
			print ' Node has',nodeVec[NUMOFKIDS],'children'
		if nodeVec[METAOFFST] == UNINIT:
			print ' Metadata offset is not yet known'
		else:
			print ' Metadata offset',nodeVec[METAOFFST]
		if nodeVec[NODECOMPL] == True:
			print ' Node is complete'
		else:
			print ' Node is not complete'
		if nodeVec[CURRCHWIP] == True:
			print ' Current child  is WIP'
		else:
			print ' Current child is complete'
		if nodeVec[CURRCHILD] == DONE:
			print ' Current child done',nodeVec[CURRCHILD]
		else:
			print ' Current child pointer',nodeVec[CURRCHILD]
		print 'Current Child being processed number',nodeVec[CURRCHNUM]
		
	def getCurrentNodeNumber(self):
		global currentNodeNumber
		return currentNodeNumber
	
	def pushNode(self,node):
		"""pushNode - 
		"""
		global nodeList
		nodeList.append(node)		
		
	def incrementCurrentNodeNumber(self):
		global currentNodeNumber
		currentNodeNumber += 1
		
	def createChildNodes(self):
		"""createChildnewNodes - Add the child newNodes to the newNodes list
		"""
		global nodeList
		global currentNodeNumber
		global inputList
		global inFileListOff
		debug_createChildNodes = False
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
			newNode = [0,0,0,0,0,0,0,0,0,0,0]
			# if debug_createChildNodes:
				# print 'newNode',newNode
			newNode[UPNODENUM] = currNodeNum
			newNode[DNNODENUM] = UNINIT
			nodeList[currNodeNum][DNNODENUM] = currNodeNum + 1
			newNode[METAOFFST] = UNINIT
			newNode[METALENGTH] = inputList[rootNodeFileOffset + (2*i) + 1]
			newNode[RTNODENUM] = currNodeNum + i + 1
			newNode[LFNODENUM] = i - 1
			newNode[FILEOFFST] = rootNodeFileOffset + (2*i)
			newNode[NUMOFKIDS] = DONE
			newNode[NODECOMPL] = False
			newNode[CURRCHWIP] = True
			newNode[CURRCHNUM] = DONE
			if i == 1:
				if debug_createChildNodes:
					print 'createChildNodes: pushed first child'
					print 'createChildNodes: newNode[RTNODENUM]',newNode[RTNODENUM]
				nodeList[currNodeNum][CURRCHNUM] = currNodeNum + 1	# point upper list to first child
				newNode[NUMOFKIDS] = inputList[inFileListOff]  # children count are known
				newNode[LFNODENUM] = DONE
			elif i == numberOfKids:
				if debug_createChildNodes:
					print 'createChildNodes: pushed last child'
				newNode[RTNODENUM] = DONE
			else:
				if debug_createChildNodes:
					print 'createChildNodes: pushed middle child'
				newNode[LFNODENUM] = i - 1
				newNode[RTNODENUM] = DONE
			if debug_createChildNodes:
				print 'createChildNodes: newNode',newNode
			self.pushNode(newNode)
			i += 1
		return

	def addFirstNode(self,firstNode,inFileOffset):
		"""addFirstNode - add the first node
		Initialize the pointers for the first node
		Special values for pointers are
		DONE dead end (will not be updated later)
		UNINIT uninitialized but will be later set to something
		
		:param nodeList: the pair [numberKids,lengthOfMetaData] from the input file
		:returns: True when done
		"""
		global nodeList
		global currentNodeNumber
		debug_getNextNodeFromList = False
		currentNodeNumber = 0
		node = [0,0,0,0,0,0,0,0,0,0,0]
		node[UPNODENUM] = DONE
		node[DNNODENUM] = UNINIT
		node[LFNODENUM] = DONE
		node[RTNODENUM] = DONE
		node[NUMOFKIDS] = firstNode[0]
		node[METAOFFST] = InputListHandler.getLenInFile() - firstNode[1]
		node[METALENGTH] = firstNode[1]
		node[FILEOFFST] = inFileOffset - 2
		node[NODECOMPL] = False
		node[CURRCHWIP] = True
		node[CURRCHNUM] = UNINIT
		self.pushNode(node)
		if debug_getNextNodeFromList:
			print 'Added first node',node
		return
	
	def endNode(self):
		"""endNode - this is the very special case where the current point is the bottom of a branch
		Need to do a bunch of things.
		set the node complete flag to true
		Set the current channel WIP flag to false since there's nothing to do below this point

		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----
		"""
		global currentNodeNumber
		global nodeList
		nodeNumber = currentNodeNumber
		debug_endNode = True
		nodeVec = nodeList[nodeNumber]
		nodeVec[DNNODENUM] = DONE			# node is an endpoint down
		nodeList[currentNodeNumber][NODECOMPL] = True	# mark node complete
		nodeList[currentNodeNumber][CURRCHWIP] = False
		nodeList[currentNodeNumber][METAOFFST] = nodeVec[FILEOFFST] + 1
		parentNode = nodeVec[UPNODENUM]
		currentNodeNumber = parentNode	# move up to parent node
		# move parent's pointer to child
		if debug_endNode:
			print 'endNode: no kids, do stuff'
			print '[UP,DN,LT,RT,KIDS,METAOFF,METALEN,FILEOFF,NODECOMP,CURRCHIP,CURRCHNUM]'
			print 'endNode: nodeList[nodeNumber][NODECOMPL]',nodeList[nodeNumber][NODECOMPL]
			print 'endNode: current node number',nodeNumber
			print 'endNode: next node number',currentNodeNumber
		return
		
	def processKids(self):
		global currentNodeNumber
		global nodeList
		nodeNumber = currentNodeNumber
		debug_processKids = True
		nodeVec = nodeList[nodeNumber]
		if debug_processKids:
			print 'processKids: current node number',nodeNumber
			print '[UP,DN,LT,RT,KIDS,METAOFF,METALEN,FILEOFF,NODECOMP,CURRCHIP,CURRCHNUM]'
			print 'processKids: current Node vector',nodeVec
		if nodeVec[DNNODENUM] == UNINIT:			# uninitialized down pointer
			if nodeVec[NUMOFKIDS] == 0:			# node has no children
				self.endNode()
			elif nodeVec[NUMOFKIDS] > 0:		# initialize kids
				self.createChildNodes()
				if debug_processKids:
					print 'processKids: created kids'
				self.incrementCurrentNodeNumber()	# step down to the first kid
				return True
			elif nodeVec[NUMOFKIDS] == DONE:
				if debug_processKids:
					print 'processKids: * * * * not sure if the node has kids or not'
				return False
			else:
				if debug_processKids:
					print 'processKids: need to do stuff with number of kids'
				exit()
			return True
		else:
			print 'processKids: exiting at node number',currentNodeNumber
			return False	# fill in as I go along
		
	def checkKidsDone(self):
		"""checkKidsDone: check to see if the current kid is done
		"""
		global currentNodeNumber
		global nodeList
		debug_checkKidsDone = True
		daughterDoneNodeNum = nodeList[currentNodeNumber][CURRCHNUM]
		if debug_checkKidsDone:
			print 'checkKidsDone: current node number',currentNodeNumber
			print 'checkKidsDone: daughter node current node list number',daughterDoneNodeNum
			print 'checkKidsDone: daughter done? ',nodeList[daughterDoneNodeNum][NODECOMPL]
		if nodeList[currentNodeNumber][NODECOMPL] == False and nodeList[daughterDoneNodeNum][RTNODENUM] != DONE:
			nodeList[currentNodeNumber][CURRCHNUM] = nodeList[daughterDoneNodeNum][RTNODENUM]
			currentNodeNumber = nodeList[daughterDoneNodeNum][RTNODENUM]
			if debug_checkKidsDone:
				print 'checkKidsDone: Need to advance node to next node to right of dau'
				print 'checkKidsDone: node to right is',nodeList[currentNodeNumber][CURRCHNUM]
			return True
		elif nodeList[daughterDoneNodeNum][RTNODENUM] == DONE:
			print 'checkKidsDone:  NEEEEEEEEEEEDDDDDDD DDDONNEEE'
			return False
		return False
	
	def processNode(self):
		"""processNode(nodeNumber) - Process the node

		:param nodeNumber: The number of the current node
		:returns: True
		"""
		global currentNodeNumber
		nodeNumber = currentNodeNumber
		debug_processNode = True
		nodeVec = nodeList[nodeNumber]
		atLeastOneNodeDidSomething = False
		if debug_processNode:
			print 'processNode: nodeNumber',nodeNumber,'vector',nodeVec
		if self.processKids() == True:
			print 'processNode: back from processKids'
			atLeastOneNodeDidSomething = True
		if self.checkKidsDone() == True:
			print 'processNode: completed checkKidsDone'
			atLeastOneNodeDidSomething = True
		if not atLeastOneNodeDidSomething:
			print 'processNode: Exiting because nothing happened'
		return atLeastOneNodeDidSomething
		
	
########################################################################
## Code

def coreCode():
	while True:
		if not NodeHandler.processNode():
			print 'coreCode: ended on node',NodeHandler.getCurrentNodeNumber()
			return

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

coreCode()

print 'main: processing is done'
print NodeHandler.dumpAllNodeVals()
print 'wtf'

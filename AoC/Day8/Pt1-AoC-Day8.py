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

class filer():
		
	def loadListFromFile(self,filename):
		global inputList
		debug_loadListFromFile = False
		inFileString = self.readTextFileToList(filename)
		self.stringOfNumbersToList(inFileString)
		if debug_loadListFromFile:
			print 'loadListFromFile: Input File Length =',len(inputList)

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
			abbyTerminate('dumpNodeVals: Offset is not in list, exiting...')
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
			abbyTerminate('ERROR - dumpNodeVals: uninitialized sister node - should never happen')
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
		
	def createChildNode(self):
		"""createChildnewNodes - Add the child newNodes to the newNodes list

		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----
		"""
		global nodeList
		global currentNodeNumber
		global inputList
		debug_createChildNode = True
		if debug_createChildNode:
			print '.',
		currNodeNum = self.getCurrentNodeNumber()
		if debug_createChildNode:
			print 'createChildNode: currNodeNum',currNodeNum
		currentNodeVec = nodeList[currNodeNum]
		if debug_createChildNode:
			print 'createChildNode: currentNodeVec',currentNodeVec
		numberOfKids = currentNodeVec[NUMOFKIDS]
		if debug_createChildNode:
			print 'createChildNode: numberOfKids',numberOfKids
		if not (numberOfKids > 0):
			abbyTerminate('createChildnewNodes: called with bad child count')
		# do adjustments to the parent
		nodeList[currNodeNum][DNNODENUM] = currNodeNum + 1
		nodeList[currNodeNum][CURRCHNUM] = currNodeNum + 1
		# make the child
		node = [0,0,0,0,0,0,0,0,0,0,0]
		node[UPNODENUM] = currNodeNum
		node[DNNODENUM] = UNINIT
		node[METAOFFST] = UNINIT
		node[METALENGTH] = inputList[nodeList[currNodeNum][FILEOFFST]+3]
		node[RTNODENUM] = UNINIT
		node[LFNODENUM] = -1
		node[FILEOFFST] = nodeList[currNodeNum][FILEOFFST] + 2
		node[NUMOFKIDS] = inputList[nodeList[currNodeNum][FILEOFFST]+2]
		node[NODECOMPL] = False
		node[CURRCHWIP] = False
		node[CURRCHNUM] = DONE
		self.pushNode(node)
		if debug_createChildNode:
			print 'createChildNode: created a single child at node number',currNodeNum+1
			self.dumpAllNodeVals()
		return

	def addFirstNode(self):
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
		debug_addFirstNode = False
		currentNodeNumber = 0
		node = [0,0,0,0,0,0,0,0,0,0,0]
		node[UPNODENUM] = DONE
		node[DNNODENUM] = UNINIT
		node[LFNODENUM] = DONE
		node[RTNODENUM] = DONE
		node[NUMOFKIDS] = inputList[0]
		node[METAOFFST] = InputListHandler.getLenInFile() - inputList[1]
		node[METALENGTH] = inputList[1]
		node[FILEOFFST] = 0
		node[NODECOMPL] = False
		node[CURRCHWIP] = False
		node[CURRCHNUM] = UNINIT
		self.pushNode(node)
		if debug_addFirstNode:
			print 'Added first node',node
			self.dumpAllNodeVals()
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
		debug_endNode = False
		nodeVec = nodeList[nodeNumber]
		nodeVec[DNNODENUM] = DONE			# node is an endpoint down
		nodeList[currentNodeNumber][NODECOMPL] = True	# mark node complete
		nodeList[currentNodeNumber][CURRCHWIP] = False
		leftSisterNodeNum = nodeList[currentNodeNumber][LFNODENUM]
		if debug_endNode:
			print 'left sister node number is',leftSisterNodeNum
		nodeList[currentNodeNumber][METAOFFST] = nodeList[currentNodeNumber][FILEOFFST] + 2
		parentNode = nodeVec[UPNODENUM]
		currentNodeNumber = parentNode	# move up to parent node
		# move parent's pointer to child
		if debug_endNode:
			print 'endNode: no kids, nodeVec',nodeVec
			print '[UP,DN,LT,RT,KIDS,METAOFF,METALEN,FILEOFF,NODECOMP,CURRCHIP,CURRCHNUM]'
			print 'endNode: nodeList[nodeNumber][NODECOMPL]',nodeList[nodeNumber][NODECOMPL]
			print 'endNode: current node number',nodeNumber
			print 'endNode: next node number',currentNodeNumber
		return
		
	def processKids(self):
		"""
		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----
							 
		"""
		global currentNodeNumber
		global nodeList
		global inputList
		nodeNumber = currentNodeNumber
		debug_processKids = True
		nodeVec = nodeList[nodeNumber]
		if debug_processKids:
			print 'processKids: current node number',nodeNumber
			print '[UP,DN,LT,RT,KIDS,METAOFF,METALEN,FILEOFF,NODECOMP,CURRCHIP,CURRCHNUM]'
			print 'processKids: current Node vector',nodeVec
		if nodeNumber < 0:
			abbyTerminate('ERROR processKids: Node number')
		if nodeVec[DNNODENUM] == UNINIT:			# uninitialized down pointer
			if nodeVec[NUMOFKIDS] == 0:			# node has no children
				self.endNode()
			elif nodeVec[NUMOFKIDS] > 0:		# initialize kids
				self.createChildNode()
				if debug_processKids:
					print 'processKids: created kids'
				self.incrementCurrentNodeNumber()	# step down to the first kid
				return True
			elif nodeVec[NUMOFKIDS] == DONE:
				if debug_processKids:
					print 'processKids: * * * * not sure if the node has kids or not'
				return False
			elif nodeVec[FILEOFFST] >= 0 and nodeVec[NUMOFKIDS] == UNINIT:
				print 'processKids: fixing up length and kid counts, etc'
				nodeList[nodeNumber][METALENGTH] = inputList[nodeVec[FILEOFFST] + 1]
				nodeList[nodeNumber][NUMOFKIDS] = inputList[nodeVec[FILEOFFST]]
				if nodeList[nodeNumber][NUMOFKIDS] == 0:
					nodeList[nodeNumber][DNNODENUM] = DONE
					nodeList[nodeNumber][METAOFFST] = nodeVec[FILEOFFST] + 2
				return True
			else:
				abbyTerminate('processKids: need to do stuff with number of kids')
				return True
		elif nodeVec[CURRCHNUM] != DONE:
			if debug_processKids:
				print 'processKids: CURRCHNUM case node number',currentNodeNumber
			if (nodeList[nodeVec[CURRCHNUM]][NODECOMPL] == True) and (nodeList[nodeVec[CURRCHNUM]][RTNODENUM] == -1):
				nodeList[nodeNumber][NODECOMPL] = True
				if currentNodeNumber > 0:
					currentNodeNumber = nodeList[nodeNumber][UPNODENUM]
					if debug_processKids:
						print 'processKids: node number',currentNodeNumber
				else:
					return False
			return True	# fill in as I go along
			self.dumpAllNodeVals()
		else:
			abbyTerminate('ERROR processKids: exiting at node number',currentNodeNumber)
			return False	# fill in as I go along
		
	def checkKidsDone(self):
		"""checkKidsDone: check to see if the current kid is done

		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----		
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
#			self.dumpAllNodeVals()
			if debug_checkKidsDone:
				print 'checkKidsDone: Need to advance node to next node to right of dau'
				print 'checkKidsDone: node to right is',nodeList[currentNodeNumber][CURRCHNUM]
			return True
		elif nodeList[daughterDoneNodeNum][RTNODENUM] == DONE:
			abbyTerminate('ERROR checkKidsDone: TBD')
			return True
		return False
	
	def checkAnotherCase(self):
		"""checkAnotherCase
		There is a solved node to the left but my node hasn't been resolved
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
		debug_checkAnotherCase = False
		leftSisterNodeNum = nodeList[currentNodeNumber][LFNODENUM]
		if debug_checkAnotherCase:
			print 'checkAnotherCase: leftSisterNodeNum',leftSisterNodeNum
		if nodeList[currentNodeNumber][LFNODENUM] != -1:
			if debug_checkAnotherCase:
				print 'checkAnotherCase: '
				self.dumpAllNodeVals()
			nodeList[currentNodeNumber][FILEOFFST] = nodeList[leftSisterNodeNum][METAOFFST] + nodeList[leftSisterNodeNum][METALENGTH]
			nodeList[currentNodeNumber][METALENGTH] = inputList[nodeList[leftSisterNodeNum][METAOFFST] + nodeList[leftSisterNodeNum][METALENGTH] + 1]
			nodeList[currentNodeNumber][NUMOFKIDS] = inputList[nodeList[leftSisterNodeNum][METAOFFST] + nodeList[leftSisterNodeNum][METALENGTH]]
			return True
		else:
			return False
	
	def processNode(self):
		"""processNode(nodeNumber) - Process the node

		:param nodeNumber: The number of the current node
		:returns: True
		"""
		global currentNodeNumber
		global nodeList
		nodeNumber = currentNodeNumber
		debug_processNode = True
		nodeVec = nodeList[nodeNumber]
		atLeastOneNodeDidSomething = False
		if debug_processNode:
			print 'processNode: nodeNumber',nodeNumber,'vector',nodeVec
		if self.processKids() == True:
			if debug_processNode:
				print 'processNode: back from processKids'
			atLeastOneNodeDidSomething = True
		if self.checkKidsDone() == True:
			if debug_processNode:
				print 'processNode: completed checkKidsDone'
			atLeastOneNodeDidSomething = True
		if self.checkAnotherCase() == True:
			if debug_processNode:
				print 'processNode: completed checkAnotherCase'
			atLeastOneNodeDidSomething = True		
		if not atLeastOneNodeDidSomething:
			if debug_processNode:
				print 'processNode: Exiting because nothing happened'
		return atLeastOneNodeDidSomething
		
	
########################################################################
## Code

def abbyTerminate(string):
	print 'ERROR Terminating due to',string
	NodeHandler.dumpAllNodeVals()
	exit()

def coreCode():
	count = 0
	while True:
		# count += 1
		# if count == 10:			
			# NodeHandler.dumpAllNodeVals()
			# exit()
		if not NodeHandler.processNode():
			print 'coreCode: ended on node',NodeHandler.getCurrentNodeNumber()
			return

print 'Reading in file',time.strftime('%X %x %Z')

inFileName = 'input.txt'

InputListHandler = filer()
InputListHandler.loadListFromFile(inFileName)

NodeHandler = NodeFunctions()
NodeHandler.addFirstNode()

coreCode()

print 'main: processing is done'
print NodeHandler.dumpAllNodeVals()
print 'wtf'

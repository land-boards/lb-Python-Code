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
SISTERCNT = 11
defaultNode = [0,0,0,0,0,0,0,0,0,0,0,0]
defaultNodeDescr = '[UP,DN,LT,RT,KDS,METOF,METCT,FILOF,NDCMPL,CURCHIP,CURCHNM,SISCT]'

DONE = -1
UNINIT = -2

class NodeFunctions():

	def dumpAllNodeVals(self):
	
		i = 0
		print '*** Node table ***'
		print 'dumpAllNodeVals: nodes in table - length is',len(nodeList)
		print 'node,',defaultNodeDescr
		for i in xrange(len(nodeList)):
			print i,nodeList[i]
		return
	
	def dumpBitVal(self,myStr,theFieldVal):
		global currentNodeNumber
		print '', myStr,
		if nodeList[currentNodeNumber][theFieldVal] == UNINIT:
			print 'is uninitialized'
		elif nodeList[currentNodeNumber][theFieldVal] == DONE:
			print 'is done'
		else:
			print 'value =', nodeList[currentNodeNumber][theFieldVal]
		
	def dumpNodeVals(self,nodeNumber):
		"""dumpNodeVals
		
		:param: nodeNumber the offset to the node in array
		"""
		debug_dumpNodeVals = True
		print 'dumpNodeVals:'
		print 'Node Number',nodeNumber
		print nodeList[nodeNumber]
		if nodeNumber > len(nodeList) - 1:
			abbyTerminate('dumpNodeVals: Offset is not in list, exiting...')
		nodeVec = nodeList[nodeNumber]
		self.dumpBitVal('Up node number',UPNODENUM)
		self.dumpBitVal('Down node number',DNNODENUM)
		self.dumpBitVal('Left node number',LFNODENUM)
		self.dumpBitVal('Sister to right',RTNODENUM)
		self.dumpBitVal('Number of kids',NUMOFKIDS)
		self.dumpBitVal('Metadata offset',METAOFFST)
		self.dumpBitVal('Node done status',NODECOMPL)
		self.dumpBitVal('Current Child WIP status',CURRCHWIP)
		self.dumpBitVal('Current child number being processed',CURRCHNUM)
		self.dumpBitVal('Current Sister count',SISTERCNT)
		
	def getCurrentNodeNumber(self):
		global currentNodeNumber
		return currentNodeNumber
	
	def pushNode(self,node):
		"""pushNode - 
		"""
		global nodeList
		debug_pushNode = False
		if debug_pushNode:
			print 'pushNode: node is',node,'previous offset',len(nodeList)-1
		nodeList.append(node)
		if debug_pushNode:
			self.dumpAllNodeVals()
		
	def changeNodeNumber(self,newNodeNumber):
		global currentNodeNumber
		debug_changeNodeNumber = False
		if debug_changeNodeNumber:
			print 'changeNodeNumber: old node number',currentNodeNumber,'new node number',newNodeNumber
		currentNodeNumber = newNodeNumber
		
	def createSister(self):
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
		debug_createSister = True
		if debug_createSister:
			print 'createSister: reached function'
			print 'createSister: node number',currentNodeNumber
		parentNode = nodeList[currentNodeNumber][UPNODENUM]
		currentDaughterNodeNum = nodeList[currentNodeNumber][CURRCHNUM]
		sisterFileOffset = nodeList[currentDaughterNodeNum][FILEOFFST]
		sisterMetaOffset = nodeList[currentDaughterNodeNum][METAOFFST]
		sisterMetaLength = nodeList[currentDaughterNodeNum][METALENGTH]
		myStartOffset = sisterMetaOffset + sisterMetaLength
		if debug_createSister:
			print 'createSister: currentDaughterNodeNum',currentDaughterNodeNum
			print 'createSister: sisters file offset',sisterFileOffset
			print 'createSister: sisterMetaOffset',sisterMetaOffset
			print 'createSister: sisterMetaLength',sisterMetaLength
			print 'createSister: myStartOffset',myStartOffset
		node = [0,0,0,0,0,0,0,0,0,0,0,0]	# manual  copy of default node
		node[UPNODENUM] = currentNodeNumber
		node[DNNODENUM] = UNINIT
		node[METAOFFST] = UNINIT
		node[METALENGTH] = inputList[myStartOffset+1]
		node[RTNODENUM] = UNINIT
		node[LFNODENUM] = currentDaughterNodeNum
		node[FILEOFFST] = myStartOffset
		node[NUMOFKIDS] = inputList[myStartOffset]
		node[NODECOMPL] = False
		node[CURRCHWIP] = False
		node[CURRCHNUM] = UNINIT
		nodeList[currentNodeNumber][SISTERCNT] = nodeList[currentNodeNumber][SISTERCNT] + 1
		nodeList[currentDaughterNodeNum][RTNODENUM] = len(nodeList)
		self.pushNode(node)
		self.dumpAllNodeVals()
#		exit()

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
		debug_createChildNode = False
		if debug_createChildNode:
			print '.',
			print 'createChildNode: reached function'
			self.dumpNodeVals(currentNodeNumber)
		currNodeNum = self.getCurrentNodeNumber()
		newNodeNum = currNodeNum + 1
		currentNodeVec = nodeList[currNodeNum]
		if debug_createChildNode:
			print 'createChildNode: currentNodeVec',currentNodeVec
		# make the child
		node = [0,0,0,0,0,0,0,0,0,0,0,0]	# manual  copy of default node
		node[UPNODENUM] = currNodeNum
		node[DNNODENUM] = UNINIT
		node[METAOFFST] = UNINIT
		node[METALENGTH] = inputList[nodeList[currNodeNum][FILEOFFST]+3]
		if inputList[nodeList[currNodeNum][FILEOFFST]+2] == 0:
			node[RTNODENUM] = DONE
		else:
			node[RTNODENUM] = UNINIT
		node[LFNODENUM] = -1
		node[FILEOFFST] = nodeList[currNodeNum][FILEOFFST] + 2
		node[NUMOFKIDS] = inputList[nodeList[currNodeNum][FILEOFFST]+2]
		node[NODECOMPL] = False
		node[CURRCHWIP] = False
		node[CURRCHNUM] = DONE
		node[SISTERCNT] = 1
		self.pushNode(node)
		# do adjustments to the parent
		nodeList[currNodeNum][DNNODENUM] = newNodeNum
		nodeList[currNodeNum][CURRCHNUM] = newNodeNum
		nodeList[currNodeNum][CURRCHWIP] = True
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
		self.changeNodeNumber(0);
		node = [0,0,0,0,0,0,0,0,0,0,0,0]
		node[UPNODENUM] = DONE
		node[DNNODENUM] = UNINIT
		node[LFNODENUM] = DONE
		node[RTNODENUM] = DONE
		node[NUMOFKIDS] = inputList[0]
		node[METAOFFST] = InputListHandler.getLenInFile() - inputList[1]
		node[METALENGTH] = inputList[1]
		node[FILEOFFST] = 0
		node[NODECOMPL] = False
		node[CURRCHWIP] = True
		node[CURRCHNUM] = UNINIT
		node[SISTERCNT] = 1
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
		parentNode = nodeVec[UPNODENUM]
		if debug_endNode:
			print 'endNode: reached function'
			print 'endNode: end node number is',currentNodeNumber,'before'
			self.dumpNodeVals(currentNodeNumber)
			print 'endNode: parent node number is',parentNode
			print 'endNode: contents of parent before change'
			self.dumpNodeVals(parentNode)
		nodeVec[DNNODENUM] = DONE			# node is an endpoint down
		nodeList[currentNodeNumber][NODECOMPL] = True	# mark node complete
		nodeList[currentNodeNumber][CURRCHWIP] = False
		nodeList[currentNodeNumber][METAOFFST] = nodeList[currentNodeNumber][FILEOFFST] + 2
		nodeList[parentNode][NODECOMPL] = True
		nodeList[parentNode][CURRCHWIP] = False
		nodeList[parentNode][SISTERCNT] = 1
		self.changeNodeNumber(parentNode)	# move up to parent node
		# move parent's pointer to child
		if debug_endNode:
			print 'endNode: node after change',currentNodeNumber
			self.dumpNodeVals(currentNodeNumber)
			print defaultNodeDescr
			print 'endNode: nodeList[nodeNumber][NODECOMPL]',nodeList[nodeNumber][NODECOMPL]
			print 'endNode: current node number',nodeNumber
			print 'endNode: next node number',currentNodeNumber
			self.dumpAllNodeVals()
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
		debug_processKids = False
		nodeVec = nodeList[nodeNumber]
		if debug_processKids:
			print 'processKids: nodes',nodeList
			print 'processKids: current node number',nodeNumber
			print defaultNodeDescr
			print 'processKids: current Node vector',nodeVec
		if nodeNumber < 0:
			termString = 'processKids (1): Node number ' + str(nodeNumber) + ' less than zero'
			abbyTerminate(termString)
		if nodeVec[DNNODENUM] == UNINIT:		# uninitialized down pointer
			if debug_processKids:
				print 'processKids: down is UNINIT'
			if nodeVec[NUMOFKIDS] == 0:			# node has no children
				if debug_processKids:
					print 'processKids: deal with end node, before'
					self.dumpAllNodeVals()
				self.endNode()
				if debug_processKids:
					print 'processKids: dealt with end node, after'
					self.dumpAllNodeVals()
			if nodeVec[NUMOFKIDS] > 0:		# initialize kids
				self.createChildNode()
				if debug_processKids:
					print 'processKids: created kids'
				self.changeNodeNumber(nodeNumber + 1)	# step down to the first kid
				return True
		elif nodeVec[NUMOFKIDS] == DONE:
			if debug_processKids:
				print 'processKids: * * * * not sure if the node has kids or not'
			return False
		if nodeVec[FILEOFFST] >= 0 and nodeVec[NUMOFKIDS] == UNINIT:
			if debug_processKids:
				print 'processKids: fixing up length and kid counts, etc'
			nodeList[nodeNumber][METALENGTH] = inputList[nodeVec[FILEOFFST] + 1]
			nodeList[nodeNumber][NUMOFKIDS] = inputList[nodeVec[FILEOFFST]]
			if nodeList[nodeNumber][NUMOFKIDS] == 0:
				nodeList[nodeNumber][DNNODENUM] = DONE
				nodeList[nodeNumber][METAOFFST] = nodeVec[FILEOFFST] + 2
			return True
		if nodeVec[CURRCHNUM] != DONE:
			if debug_processKids:
				print 'processKids: CURRCHNUM case node number',nodeNumber
			if (nodeList[nodeVec[CURRCHNUM]][NODECOMPL] == True) and (nodeList[nodeVec[CURRCHNUM]][RTNODENUM] == -1):
				nodeList[nodeNumber][NODECOMPL] = True
			if nodeNumber > 0:
				if debug_processKids:
					print 'processKids: changing node number'
				self.changeNodeNumber(nodeList[nodeNumber][UPNODENUM])
				if debug_processKids:
					print 'processKids (2): node number',nodeNumber
				else:
					return False
			return True	# fill in as I go along
		if debug_processKids:
			self.dumpAllNodeVals()
		else:
			# self.dumpNodeVals(nodeNumber)
			# termString = 'processKids: exiting at node number = ' + str(nodeNumber)
			# abbyTerminate(termString)
			return False	# fill in as I go along
		
	def checkSister(self):
		"""checkSister: check to see if the current kid is done
		If the current children are done then find the next sister
		and move to the next sister
		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----		
		"""
		global currentNodeNumber
		global nodeList
		debug_checkSister = True
		if debug_checkSister:
			print 'checkSister: reached function'
		parentNode = nodeList[currentNodeNumber][UPNODENUM]
		if debug_checkSister:
			print 'checkSister: current node number',currentNodeNumber
			print 'checkSister: parent node number',parentNode
		if nodeList[currentNodeNumber][DNNODENUM] == UNINIT:
			if debug_checkSister:
				print 'checkSister: No down vector is populated'
			return False
		if debug_checkSister:
			print 'checkSister: there is a down node'
			print 'checkSister: sister count',nodeList[currentNodeNumber][SISTERCNT]
			print 'checkSister: number of kids',nodeList[currentNodeNumber][NUMOFKIDS]
			self.dumpAllNodeVals()
		if nodeList[currentNodeNumber][SISTERCNT] == nodeList[currentNodeNumber][NUMOFKIDS]:
			pass
			if debug_checkSister:
				print '\n\ncheckSister: all the sisters are in the house'
				self.dumpAllNodeVals()
			childNodeNum = nodeList[currentNodeNumber][SISTERCNT]
			childMetaEnd = nodeList[childNodeNum][METAOFFST] + nodeList[childNodeNum][METALENGTH] + 1
			if debug_checkSister:
				print 'checkSister: currentNodeNumber',currentNodeNumber
				print 'checkSister: child node',childNodeNum
				print 'checkSister: childMetaEnd',childMetaEnd
			nodeList[currentNodeNumber][METAOFFST] = childMetaEnd
			nodeList[parentNode][SISTERCNT] = nodeList[currentNodeNumber][DNNODENUM]
			nodeList[parentNode][NODECOMPL] = False
			nodeList[parentNode][CURRCHWIP] = True
			self.changeNodeNumber(nodeList[currentNodeNumber][UPNODENUM])
			if debug_checkSister:
				print 'checkSister: moved to node',currentNodeNumber
				print 'checkSister: after the meta is loaded'
				self.dumpAllNodeVals()
			if currentNodeNumber < 0:
				abbyTerminate("Bad stuff")
				exit()
			return True
		if nodeList[currentNodeNumber][NODECOMPL] == False:
			daughterDoneNodeNum = nodeList[currentNodeNumber][CURRCHNUM]
			if debug_checkSister:
				print 'checkSister: node',currentNodeNumber
				self.dumpNodeVals(currentNodeNumber)
			if nodeList[daughterDoneNodeNum][RTNODENUM] == UNINIT:
				print 'checkSister: node',currentNodeNumber
				print 'checkSister: right isnt initialized'
				exit()
			nodeList[currentNodeNumber][CURRCHNUM] = nodeList[daughterDoneNodeNum][RTNODENUM]
			self.changeNodeNumber(nodeList[daughterDoneNodeNum][RTNODENUM])
			if debug_checkSister:
				print 'checkSister: Need to advance node to next node to right of dau'
				print 'checkSister: node to right is',nodeList[currentNodeNumber][CURRCHNUM]
			return True
		if nodeList[currentNodeNumber][SISTERCNT] < nodeList[currentNodeNumber][NUMOFKIDS]:
			pass
			if debug_checkSister:
				print 'checkSister: need to make a sister node'
			self.createSister()
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
		debug_processNode = False
		nodeVec = nodeList[nodeNumber]
		atLeastOneNodeDidSomething = False
		if debug_processNode:
			print 'processNode: nodeNumber',nodeNumber
			print 'processNode: vector',nodeVec
		if self.processKids() == True:
			atLeastOneNodeDidSomething = True
		if debug_processNode:
			print 'processNode: back from processKids'
		if self.checkSister() == True:
			atLeastOneNodeDidSomething = True
		if debug_processNode:
			print 'processNode: completed checkSister'
		if self.checkAnotherCase() == True:
			atLeastOneNodeDidSomething = True		
		if debug_processNode:
			print 'processNode: completed checkAnotherCase'
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

inFileName = 'input2.txt'

InputListHandler = filer()
InputListHandler.loadListFromFile(inFileName)

NodeHandler = NodeFunctions()
NodeHandler.addFirstNode()

coreCode()

print 'main: processing is done'
print NodeHandler.dumpAllNodeVals()
print 'wtf'

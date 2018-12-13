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
inputListPtr = 0

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
		
	def getInputPair(self,fileOffset):
		"""Get the input pair at inputListPtr
		"""
		global inputList
		pair = [inputList[fileOffset],inputList[fileOffset+1]]
		return pair
	
	def setInputListPtr(self,pointer):
		global inputListPtr		# global so other functions can set the pointer
		inputListPtr = pointer
		return True
	
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
UPNODENUM = 0	# Up node number (DONE, UNINT, number) points to the index for the node above
DNNODENUM = 1	# Down node number (DONE, UNINT, number) points to the index for the node above
LFNODENUM = 2	# Left node number (DONE, UNINT, number) points to the index for the node above
RTNODENUM = 3	# Right node number (DONE, UNINT, number) points to the index for the node above
NUMOFKIDS = 4	# The number of children of the node
FILEOFFST = 5	# Offset in the input file to the start of the node (child number)
METAOFFST = 6	# Offset in the input file to the start of the metadata
METALENGTH = 7	# Number of elements in the metadata
NODECOMPL = 8	# Node complete flag (True = all daughters below are completely resolved, False = work to do)
CURRCHDONE = 9	# Current Channel is Done (False = current channel is being worked on, True = Done)
CURRCHNN = 10	# Node number of the Current Channel that is being processed 
CHILDNUM = 11	# Number of child in the sisters list

defaultNode = [0,0,0,0,0,0,0,0,0,0,0,0]
defaultNodeDescr = '[UP,DN,LT,RT,KDS,FILOF,METOF,METCT,NDCMPL,CURCHDN,CURCHNM,CHNUM]'

DONE = -1
UNINIT = -2
WIP = -3

# Tree status
TREE_DONE = -4
TREE_IN_PROGRESS = -5
GET_NEXT_NODE = -6

CURRENT_POINT_DONE = 1
NEED_TO_MOVE_DOWN = 2
NEED_TO_MOVE_RIGHT = 3
NEED_TO_MOVE_DOWN_THEN_RIGHT = 4
NEED_TO_MOVE_UP = 5
NEED_TO_MOVE_TO_CURRENT_DAUGHTER = 6
NODE_COMPLETED = 7
TREE_COMPLETED = 8
EARLY_EXIT_FOR_DEBUG = 9

class NodeFunctions():

	def dumpAllNodeVals(self):
		"""
		"""
		i = 0
		print '*** Node table ***'
		print 'dumpAllNodeVals: nodes in table - length is',len(nodeList)
		print 'node,',defaultNodeDescr
		for i in xrange(len(nodeList)):
			print i,nodeList[i]
		return
	
	def dumpBitVal(self,myStr,nodeNumber,theFieldVal):
		"""
		"""
		print '', myStr,
		if nodeList[nodeNumber][theFieldVal] == UNINIT:
			print 'is uninitialized'
		elif nodeList[nodeNumber][theFieldVal] == DONE:
			print 'is done'
		elif nodeList[nodeNumber][theFieldVal] == WIP:
			print 'is WIP'
		else:
			print 'value =', nodeList[nodeNumber][theFieldVal]
		
	def dumpNodeVals(self,nodeNumber):
		"""dumpNodeVals
		
		:param: nodeNumber the offset to the node in array
		"""
		debug_dumpNodeVals = False
		print 'dumpNodeVals: at node',nodeNumber
		print nodeList[nodeNumber]
		if nodeNumber > len(nodeList) - 1:
			abbyTerminate('dumpNodeVals: Offset is not in list, exiting...')
		nodeVec = nodeList[nodeNumber]
		self.dumpBitVal('Up node number',nodeNumber,UPNODENUM)
		self.dumpBitVal('Down node number',nodeNumber,DNNODENUM)
		self.dumpBitVal('Left node number',nodeNumber,LFNODENUM)
		self.dumpBitVal('Sister to right',nodeNumber,RTNODENUM)
		self.dumpBitVal('Number of kids',nodeNumber,NUMOFKIDS)
		self.dumpBitVal('File Offset',nodeNumber,FILEOFFST)
		self.dumpBitVal('Metadata offset',nodeNumber,METAOFFST)
		self.dumpBitVal('Metadata count',nodeNumber,METALENGTH)
		self.dumpBitVal('Node done status',nodeNumber,NODECOMPL)
		self.dumpBitVal('Current Child Done status',nodeNumber,CURRCHDONE)
		self.dumpBitVal('Current child number being processed',nodeNumber,CURRCHNN)
		self.dumpBitVal('Total Number of Children',nodeNumber,CHILDNUM)
		
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
		
	def getNodeNumber(self):
		"""getNodeNumber
		"""
		return currentNodeNumber
		
	def changeNodeNumber(self,newNodeNumber):
		global currentNodeNumber
		debug_changeNodeNumber = False
		if debug_changeNodeNumber:
			print 'changeNodeNumber: old node number',currentNodeNumber,'new node number',newNodeNumber
		currentNodeNumber = newNodeNumber
		
	def createNewNode(self,childOffsetInList,theNodeNumber):
		"""createNewNode - add the first node
		Initialize the pointers for the first node
		Special values for pointers are
		DONE dead end (will not be updated later)
		UNINIT uninitialized but will be later set to something
		
		:param nodeList: the pair [numberKids,lengthOfMetaData] from the input file
		:returns: True when done
		"""
		global nodeList
		debug_createNewNode = False
		node = [0,0,0,0,0,0,0,0,0,0,0,0]
		if theNodeNumber == 0:
			node[UPNODENUM] = DONE
		else:
			node[UPNODENUM] = theNodeNumber
		if inputList[childOffsetInList] == 0:	# Number of Children = 0 case
			node[DNNODENUM] = DONE
			node[METAOFFST] = childOffsetInList + 2
			node[NODECOMPL] = True
			node[CURRCHDONE] = True
		else:
			node[DNNODENUM] = UNINIT
			node[METAOFFST] = UNINIT
			node[NODECOMPL] = False
			node[CURRCHDONE] = False
		if theNodeNumber == 0:
			node[METAOFFST] = len(inputList) - inputList[childOffsetInList+1] 
		node[CURRCHNN] = len(nodeList)	# CURRCHNN is the node number of the item being inserted
		node[CHILDNUM] = inputList[childOffsetInList]
		node[LFNODENUM] = DONE
		node[RTNODENUM] = DONE
		node[NUMOFKIDS] = inputList[childOffsetInList]
		node[METALENGTH] = inputList[childOffsetInList+1]
		node[FILEOFFST] = childOffsetInList
		self.pushNode(node)
		if debug_createNewNode:
			print 'createNewNode: created node',node
		return
	
	def addChildrenToNodeList(self,inPair,inputListOffset,nodeNumber):
		""" creates a list of kids in the nodeList and returns the offset to the first kid
		Other observations about child creation
		- Nodes 1 and 2 should have had the meta count set when the children were set up
		- Node 1 should have had the File Offset set up when the file was read in
		- Node 1 has the wrong METOF in it - looks like it got loaded with the address of the meta off rather than the content
		"""
		global nodeList
		debug_addChildrenToNodeList = False
		numberOfKids = inPair[0]
		metaCountAdr = inPair[1]
		if debug_addChildrenToNodeList:
			print '\naddChildrenToNodeList: reached function'
			print 'addChildrenToNodeList: numberOfKids',numberOfKids
			print 'addChildrenToNodeList: metaCountAdr,',metaCountAdr
		kidNum = 1
		endOfNodes = len(nodeList)		# add to end of the current nodes
		parentNum = nodeNumber
		while kidNum <= numberOfKids:
			node = [0,0,0,0,0,0,0,0,0,0,0,0]	# manual  copy of default node
			node[UPNODENUM] = parentNum
			node[DNNODENUM] = UNINIT
			if kidNum == numberOfKids:
				node[RTNODENUM] = DONE
			else:
				node[RTNODENUM] = kidNum + 1
			if kidNum == 1:
				node[METALENGTH] = inputList[inputListOffset + 3]
				node[FILEOFFST] = inputListOffset + 2
				node[LFNODENUM] = DONE
				node[NUMOFKIDS] = inputList[inputListOffset+2]
			else:
				node[METALENGTH] = UNINIT
				node[LFNODENUM] = kidNum - 1
				node[FILEOFFST] = UNINIT
				node[NUMOFKIDS] = UNINIT
			node[METAOFFST] = UNINIT
			node[NODECOMPL] = False
			node[CURRCHDONE] = False
			node[CURRCHNN] = len(nodeList)
			node[CHILDNUM] = kidNum
			self.pushNode(node)
			kidNum += 1
		return endOfNodes				# node number of first added child
	
	def doMovement(self,theNodeNumber,actionFlag):
		"""doMovement
		Look around the node and figure out where to move
		Assumption is that everything that can be done at the location was already done
		UPNODENUM = 0	# Up node number (DONE, UNINT, number) points to the index for the node above
		DNNODENUM = 1	# Down node number (DONE, UNINT, number) points to the index for the node above
		LFNODENUM = 2	# Left node number (DONE, UNINT, number) points to the index for the node above
		RTNODENUM = 3	# Right node number (DONE, UNINT, number) points to the index for the node above
		NUMOFKIDS = 4	# The number of children of the node
		FILEOFFST = 5	# Offset in the input file to the start of the node (child number)
		METAOFFST = 6	# Offset in the input file to the start of the metadata
		METALENGTH = 7	# Number of elements in the metadata
		NODECOMPL = 8	# Node complete flag (True = all daughters below are completely resolved, False = work to do)
		CURRCHDONE = 9	# Current Channel is Work in Progress (True = current channel is being worked on, False = Done)
		CURRCHNN = 10	# Current Channel number that is being processed 
		CHILDNUM = 11	# Number of child in the sisters list
		
		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----

		# Flags to operate on - first three lines of the input file
		# node,[UP, DN, LT, RT,KDS,FILOF,METOF,METCT,NDCMPL,CURCHIP,CURCHNM,CHNUM]
		# 	 0 [-1,  1, -1, -1,  2,    0,   -2,    3, False,     -2,     -2,    1]
		#	 1 [0,  -2, -1,  2,  0,    2,   -2,    3, False,     -2,     -2,    1]
		#	 2 [0,  -2,  1, -1, -2,   -2,   -2,   -2, False,     -2,     -2,    2]
		
		:returns: the new node number
		"""
		global nodeList
		debug_doMovement = True
		if debug_doMovement:
			print 'doMovement: theNodeNumber',theNodeNumber
		if debug_doMovement:
			print 'doMovement: actionFlag',actionFlag
		if actionFlag == NEED_TO_MOVE_DOWN:
			if debug_doMovement:
				print 'doMovement: Moving down to node',nodeList[theNodeNumber][DNNODENUM]
			return nodeList[theNodeNumber][DNNODENUM]
		elif actionFlag == NEED_TO_MOVE_UP:
			if debug_doMovement:
				print 'doMovement: Moving up to node',nodeList[theNodeNumber][UPNODENUM]
			return nodeList[theNodeNumber][UPNODENUM]
		elif actionFlag == NEED_TO_MOVE_DOWN_THEN_RIGHT:
			if debug_doMovement:
				print 'doMovement: Moving down and right to node',nodeList[theNodeNumber][RTNODENUM]
			downNode = nodeList[theNodeNumber][DNNODENUM]
			startingNode = nodeList[downNode][RTNODENUM]
			numberOfNodes = nodeList[downNode][CHILDNUM]
			if debug_doMovement:
				print 'doMovement: Moving down and right to node',nodeList[theNodeNumber][RTNODENUM]
				print 'doMovement: startingNode',startingNode
				print 'doMovement: numberOfNodes',numberOfNodes
				exit()
			return nodeList[theNodeNumber][RTNODENUM]
		elif actionFlag == NEED_TO_MOVE_RIGHT:
			if debug_doMovement:
				print 'doMovement: Moving right to node',nodeList[theNodeNumber][RTNODENUM]
			return nodeList[theNodeNumber][RTNODENUM]
		elif actionFlag == NEED_TO_MOVE_TO_CURRENT_DAUGHTER:
			if debug_doMovement:
				print 'doMovement: Moving up to current daughter',nodeList[theNodeNumber][CURRCHNN]
			return nodeList[theNodeNumber][CURRCHNN]
		elif actionFlag == CURRENT_POINT_DONE:
			return theNodeNumber
		else:
			exit()
		
	def processTree(self,inFileOffset,theNodeNumber):
		"""If anything can be done, do it
		determineAction based on state of currentNodeNumber
		:returns: [flag,fileOffset,currentNodeNumber]
		flag = DONE when tree is completed, UNINIT when tree is not completed
		fileOffset is the location in the input file that the next string will come from
		"""
		debug_processTree = False
		if debug_processTree:
			print '\nprocessTree: reached function'
			print 'processTree: theNodeNumber',theNodeNumber
			print 'processTree: inFileOffset',inFileOffset
		if debug_processTree:
			self.dumpNodeVals(theNodeNumber)
		if debug_processTree:
			print 'processTree: nodeList[theNodeNumber]',nodeList[theNodeNumber]
		currentActionsFlag = self.doAllActionsAtCurrentPoint(theNodeNumber)
		if currentActionsFlag == EARLY_EXIT_FOR_DEBUG:
			print 'processTree: early exit for debug'
			return [EARLY_EXIT_FOR_DEBUG,inFileOffset,theNodeNumber]
		elif currentActionsFlag == TREE_COMPLETED:
			return [TREE_DONE,inFileOffset,theNodeNumber]
		theNodeNumber = self.doMovement(theNodeNumber,currentActionsFlag)
		if debug_processTree:
			print 'processTree: doMovement moving to node',theNodeNumber
		return [TREE_IN_PROGRESS,inFileOffset,theNodeNumber]
		
	def doAllActionsAtCurrentPoint(self,theNodeNumber):
		"""Look around the node and find all of the actions that can be done at the node.
		Does not do any movement but does as much as possible to the cells in the row, the row above and the row below
		UPNODENUM = 0	# Up node number (DONE, UNINT, number) points to the index for the node above
		DNNODENUM = 1	# Down node number (DONE, UNINT, number) points to the index for the node above
		LFNODENUM = 2	# Left node number (DONE, UNINT, number) points to the index for the node above
		RTNODENUM = 3	# Right node number (DONE, UNINT, number) points to the index for the node above
		NUMOFKIDS = 4	# The number of children of the node
		FILEOFFST = 5	# Offset in the input file to the start of the node (child number)
		METAOFFST = 6	# Offset in the input file to the start of the metadata
		METALENGTH = 7	# Number of elements in the metadata
		NODECOMPL = 8	# Node complete flag (True = all daughters below are completely resolved, False = work to do)
		CURRCHDONE = 9	# Current Channel is Work in Progress (True = current channel is being worked on, False = Done)
		CURRCHNN = 10	# Current Channel number that is being processed 
		CHILDNUM = 11	# Offset number of child currently being processed in the sisters list starting at 1
		return when completed
		
		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----
		
		Observations about node 0
		- Node is not complete
		- Current Channel is not yet in process
		- Node has a down value
		- Node has two children
		- Node is not processing a child at the moment
		- Node has two kids (side effect of the reading in of a child pair)
		- Node child that needs work is node 1
		- Node 0 is already solved for the meta offset
		Other observations about child creation
		- Node 0 should not have METOF yet - Fixed
		- Node 1 should have the meta count set when the children were set up - Fixed
		- Node 1 should have had the File Offset set up when the file was read in - Fixed
		- Node 1 should have had the child count set when the children were set up - Fixed
		- Node 1 has the wrong METOF in it - fixed
		- Node 1 meta offset should be unknown - it's only known in this case since the child count is zero - made unknown
		
		# Flags to operate on - first three lines of the input file
		# node,[UP, DN, LT, RT,KDS,FILOF,METOF,METCT,NDCMPL,CURCHIP,CURCHNM,CHNUM]
		# 	 0 [-1,  1, -1, -1,  2,    0,   -2,    3, False,     -2,     -2,    1]
		#	 1 [ 0, -2, -1,  2,  0,    2,   -2,    3, False,     -2,     -2,    1]
		#	 2 [ 0, -2,  1, -1, -2,   -2,   -2,   -2, False,     -2,     -2,    2]
		
		"""
		global nodeList
		debug_doAllActionsAtCurrentPoint = True
		if debug_doAllActionsAtCurrentPoint:
			print '\ndoAllActionsAtCurrentPoint: Reached function, node',theNodeNumber
		if not nodeList[theNodeNumber][NODECOMPL]:					# Current node has not completed
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: Node is not yet completed'
			if not (nodeList[theNodeNumber][CURRCHDONE]):			# still processing a daughter
				if debug_doAllActionsAtCurrentPoint:
					print 'doAllActionsAtCurrentPoint: possibly still active children'
					print 'doAllActionsAtCurrentPoint: table before any action'
					self.dumpAllNodeVals()
				if nodeList[theNodeNumber][NUMOFKIDS] == 0:
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: zero kids case'
						self.dumpNodeVals(theNodeNumber)
					nodeList[theNodeNumber][CURRCHDONE] = True
#					nodeList[theNodeNumber][CURRCHNN] = 1
					## TBD
					nodeList[theNodeNumber][NODECOMPL] = True
					nodeList[theNodeNumber][METAOFFST] = nodeList[theNodeNumber][FILEOFFST] + 2
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: after dealing with the no kids case'
						self.dumpAllNodeVals()
					return NEED_TO_MOVE_UP
				elif nodeList[theNodeNumber][DNNODENUM] >= 0:
					## TBD check and see if the children are actually done
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: there are kids not done so nav down case'
						self.dumpNodeVals(theNodeNumber)
					## The latest problem is ----
					## should not be going down to the down node since this will always go to the first node
					## need the node number of the current child number
					## should have either stuffed it away earlier or scan over to it now
					## scan by as many nodes as the CURRCHNN starting at the DNNODENUM
#					nodeList[theNodeNumber][CURRCHNN] = nodeList[theNodeNumber][DNNODENUM]
					## need to move to the node pointed to by the pointer in the previous node
					nodeList[theNodeNumber][CURRCHDONE] = False
					return NEED_TO_MOVE_DOWN_THEN_RIGHT
				else: # the first child below current node needs to be created
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: need to create the first child below this node'
						self.dumpNodeVals(theNodeNumber)
					childOffsetInList = nodeList[theNodeNumber][FILEOFFST] + 2
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: child offset into inList ',childOffsetInList
					self.createNewNode(childOffsetInList,theNodeNumber)
					childNodeNum = len(nodeList)-1
					nodeList[theNodeNumber][DNNODENUM] = childNodeNum
					nodeList[childNodeNum][CHILDNUM] = 1
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: Before making the new node moving to node',childNodeNum
						self.dumpNodeVals(theNodeNumber)
					return NEED_TO_MOVE_DOWN	# move down into the child
			# combined with WIP code
				if debug_doAllActionsAtCurrentPoint:
					print 'doAllActionsAtCurrentPoint: WIP case - node',theNodeNumber
					print 'doAllActionsAtCurrentPoint: before changes'
					self.dumpAllNodeVals()
				downNode = nodeList[theNodeNumber][DNNODENUM]
				endOfDownNodeInListPlusOne = nodeList[downNode][METAOFFST] + nodeList[downNode][METALENGTH]
				if debug_doAllActionsAtCurrentPoint:
					print 'doAllActionsAtCurrentPoint: down node number',downNode
					print 'doAllActionsAtCurrentPoint: endOfDownNodeInList',endOfDownNodeInListPlusOne
					self.dumpAllNodeVals()
				if (nodeList[downNode][NODECOMPL] == True) and (nodeList[theNodeNumber][CURRCHNN] == nodeList[theNodeNumber][CHILDNUM]):
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: finished a node moving up'
						print 'doAllActionsAtCurrentPoint: do the meta calc here'
						print 'doAllActionsAtCurrentPoint: this is the last node in the list - downNode',downNode
						self.dumpAllNodeVals()
						self.dumpNodeVals(downNode)
					metaStartAddress = nodeList[downNode][METAOFFST] + nodeList[downNode][METALENGTH]
					nodeList[theNodeNumber][METAOFFST] = metaStartAddress
					if debug_doAllActionsAtCurrentPoint:
						print 'for node',theNodeNumber,'setting METAOFFST to ',nodeList[theNodeNumber][METAOFFST]
					if nodeList[theNodeNumber][CHILDNUM] == nodeList[theNodeNumber][CURRCHNN]:
						nodeList[theNodeNumber][NODECOMPL] = True
					else:
						nodeList[theNodeNumber][NODECOMPL] = False
					return NEED_TO_MOVE_UP
				# advance to the next siser if there is one
				else:
					sisterInputFilePair = InputListHandler.getInputPair(endOfDownNodeInListPlusOne)
					sistersNodeNumber = nodeList[downNode][RTNODENUM]
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: sisterInputFilePair',sisterInputFilePair
						print 'doAllActionsAtCurrentPoint: sistersNodeNumber',sistersNodeNumber
					nodeList[sistersNodeNumber][FILEOFFST] = endOfDownNodeInListPlusOne
					nodeList[sistersNodeNumber][METALENGTH] = sisterInputFilePair[1]
					nodeList[sistersNodeNumber][NUMOFKIDS] = sisterInputFilePair[0]
					nodeList[theNodeNumber][CURRCHDONE] = True
					if nodeList[theNodeNumber][CHILDNUM] < nodeList[theNodeNumber][NUMOFKIDS]:
						nodeList[theNodeNumber][CHILDNUM] = nodeList[theNodeNumber][CHILDNUM] + 1
					elif nodeList[theNodeNumber][CHILDNUM] == nodeList[theNodeNumber][NUMOFKIDS]:
						nodeList[theNodeNumber][NODECOMPL] = True
					if debug_doAllActionsAtCurrentPoint:
						self.dumpAllNodeVals()
					return CURRENT_POINT_DONE
			elif (nodeList[theNodeNumber][CURRCHDONE]):
				if debug_doAllActionsAtCurrentPoint:
					print 'doAllActionsAtCurrentPoint: Current channel is done'
					self.dumpNodeVals(theNodeNumber)
				if nodeList[theNodeNumber][CURRCHNN] < nodeList[theNodeNumber][CHILDNUM]:
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: Move to the next daughter'
					nodeList[theNodeNumber][CURRCHNN] = nodeList[theNodeNumber][CURRCHNN] + 1
					return NEED_TO_MOVE_TO_CURRENT_DAUGHTER
				if nodeList[theNodeNumber][CHILDNUM] == nodeList[theNodeNumber][CURRCHNN]:
					nodeList[theNodeNumber][NODECOMPL] = True
				## broken because the current channel number was broken earlier (was originally set up)
				# get the offset here
				if debug_doAllActionsAtCurrentPoint:
					print 'doAllActionsAtCurrentPoint: set node complete to true'
					self.dumpNodeVals(theNodeNumber)
				if theNodeNumber > 0:
					return NEED_TO_MOVE_UP
				else:
					if debug_doAllActionsAtCurrentPoint:
						print 'doAllActionsAtCurrentPoint: got to the top node'				
					return CURRENT_POINT_DONE
			else:
				pass
				print 'doAllActionsAtCurrentPoint: wtf-1'
				self.dumpNodeVals(theNodeNumber)
		else:	# node is complete at the point
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: node is complete'
			if theNodeNumber == 0:
				return TREE_COMPLETED
			else:	# node is complete but the parent may not be done yet
				parentNodeNumber = nodeList[theNodeNumber][UPNODENUM]
				if debug_doAllActionsAtCurrentPoint:
					print 'doAllActionsAtCurrentPoint: parentNodeNumber',parentNodeNumber
					print 'doAllActionsAtCurrentPoint: parents node flags'
					self.dumpNodeVals(parentNodeNumber)
				parentOffset = nodeList[theNodeNumber][METAOFFST] + nodeList[theNodeNumber][METALENGTH]
				nodeList[parentNodeNumber][METAOFFST] = parentOffset
				nodeList[parentNodeNumber][CURRCHNN] = nodeList[parentNodeNumber][CURRCHNN] + 1
				nodeList[parentNodeNumber][CURRCHDONE] = False
				if debug_doAllActionsAtCurrentPoint:
					print 'doAllActionsAtCurrentPoint: parentOffset set to',nodeList[theNodeNumber][METAOFFST]
					self.dumpAllNodeVals()
				return NEED_TO_MOVE_UP
			self.dumpNodeVals(theNodeNumber)
			self.dumpAllNodeVals()
			exit()
			return EARLY_EXIT_FOR_DEBUG
	
########################################################################
## Code

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	NodeHandler.dumpAllNodeVals()
	exit()

def moveInListToTree(currentNodePtr,inputListOffset):
	"""Get the input file stream data pair at inputListOffset
	pair is [childCount,metaoffset]
	Create the kids based on the pairs
	This method sits outside of the list and node handlers since it spans both
	"""
	debug_moveInListToTree = False
	inPair = InputListHandler.getInputPair(inputListOffset)
	if debug_moveInListToTree:
		print "moveInListToTree: read inPair",inPair
	childNodeNum = NodeHandler.addChildrenToNodeList(inPair,inputListOffset,currentNodePtr)	# pass the child count and meta count to the creator
	if debug_moveInListToTree:
		print "moveInListToTree: added childNodeNum",childNodeNum
		print 'moveInListToTree: currentNodePtr',currentNodePtr
	nodeList[currentNodePtr][DNNODENUM] = childNodeNum
	return

def newCoreCode():
	"""Creates the initial parent and child
	Calls processTree to handle nodes
	Operates on return value
	"""
	global nodeList
	debug_newCoreCode = False
	inputFileOffset = 0
	theNodeNumber = 0
	NodeHandler.changeNodeNumber(theNodeNumber)
	InputListHandler.setInputListPtr(inputFileOffset)
	NodeHandler.createNewNode(inputFileOffset,theNodeNumber)
	nodeToGet = [TREE_IN_PROGRESS,inputFileOffset,theNodeNumber]
	inFileOffset = 0
	if debug_newCoreCode:
		print 'newCoreCode: calling moveInListToTree'
	moveInListToTree(theNodeNumber,inFileOffset)
	if debug_newCoreCode:
		print 'newCoreCode: starting loop'
	while True:
		nodeToGet = NodeHandler.processTree(inFileOffset,theNodeNumber)
		if debug_newCoreCode:
			print 'newCoreCode: nodeToGet returned ',nodeToGet,
		if (nodeToGet[0] == TREE_DONE):
			if debug_newCoreCode:
				print 'tree done'
			return
		elif nodeToGet[0] == EARLY_EXIT_FOR_DEBUG:
			if debug_newCoreCode:
				print 'newCoreCode: nodeToGet returned ',nodeToGet,
				print 'newCoreCode: early exit for debugging at node',nodeToGet[2]
			return
		elif nodeToGet[0] == GET_NEXT_NODE:
			if debug_newCoreCode:
				print 'newCoreCode: pull next address'
			pass
		elif nodeToGet[0] == TREE_IN_PROGRESS:
			pass
		if debug_newCoreCode:
			NodeHandler.dumpAllNodeVals()
		theNodeNumber = nodeToGet[2]

def sumTheMetaStuff():
	accumMetaRecLens = 0
	for node in nodeList:
		startSpan = node[METAOFFST]
		endSpan = node[METAOFFST] + node[METALENGTH]
		print startSpan,endSpan-1
		while(startSpan < endSpan):
			accumMetaRecLens += inputList[startSpan]
			startSpan += 1
	print '\nSum =',accumMetaRecLens

##############################################################################
## Code follows

print 'Reading in file',time.strftime('%X %x %Z')

inFileName = 'input.txt'

InputListHandler = filer()
InputListHandler.loadListFromFile(inFileName)

print 'Processing Nodes',time.strftime('%X %x %Z')

NodeHandler = NodeFunctions()

newCoreCode()

print 'main: processing is done'
print 'node at the end was',NodeHandler.getNodeNumber()
NodeHandler.dumpAllNodeVals()

sumTheMetaStuff()

exit()

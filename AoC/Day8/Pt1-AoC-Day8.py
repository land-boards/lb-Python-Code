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
CURRCHWIP = 9	# Current Channel is Work in Progress (True = current channel is being worked on, False = Done)
CURRCHNUM = 10	# Current Channel number that is being processed 
CHILDNUM = 11	# Number of child in the sisters list

defaultNode = [0,0,0,0,0,0,0,0,0,0,0,0]
defaultNodeDescr = '[UP,DN,LT,RT,KDS,FILOF,METOF,METCT,NDCMPL,CURCHIP,CURCHNM,CHNUM]'

DONE = -1
UNINIT = -2
WIP = -3

# Tree status
TREE_DONE = 0
TREE_IN_PROGRESS = 1
GET_NEXT_NODE = 2

CURRENT_POINT_DONE = 1
NEED_TO_MOVE_DOWN = 2
NEED_TO_MOVE_RIGHT = 3
NEED_TO_MOVE_UP = 4
NODE_COMPLETED = 5
TREE_COMPLETED = 6
EARLY_EXIT_FOR_DEBUG = 7

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
		self.dumpBitVal('File Offset',FILEOFFST)
		self.dumpBitVal('Metadata offset',METAOFFST)
		self.dumpBitVal('Node done status',NODECOMPL)
		self.dumpBitVal('Current Child WIP status',CURRCHWIP)
		self.dumpBitVal('Current child number being processed',CURRCHNUM)
		self.dumpBitVal('Current child number being processed',CHILDNUM)
		
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
			print '\nendNode: reached function'
			print 'endNode: end node number is',currentNodeNumber,'before'
			self.dumpAllNodeVals()
			print 'endNode: parent node number is',parentNode
			print 'endNode: contents of parent before change'
			self.dumpNodeVals(parentNode)
		nodeVec[DNNODENUM] = DONE			# node is an endpoint down
		nodeList[currentNodeNumber][NODECOMPL] = True	# mark node complete
		nodeList[currentNodeNumber][CURRCHWIP] = UNINIT
		nodeList[currentNodeNumber][METAOFFST] = nodeList[currentNodeNumber][FILEOFFST] + 2
		if debug_endNode:
			print 'endNode: after updating the nodeList values for end node'
			self.dumpAllNodeVals()
		if nodeList[parentNode][NUMOFKIDS] == 1:
			if debug_endNode:
				print 'endNode: IS THIS AT THE WRONG POINT???'
			nodeList[parentNode][METAOFFST] = nodeList[currentNodeNumber][METAOFFST] + nodeList[currentNodeNumber][METALENGTH]
			nodeList[parentNode][CURRCHWIP] = UNINIT
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
		node[METAOFFST] = UNINIT
		node[METALENGTH] = inputList[1]
		node[FILEOFFST] = 0
		node[NODECOMPL] = False
		node[CURRCHWIP] = UNINIT
		node[CURRCHNUM] = UNINIT
		node[CHILDNUM] = 1
		self.pushNode(node)
		if debug_addFirstNode:
			print 'Added first node',node
			self.dumpAllNodeVals()
		return
	
	def addChildrenToNodeList(self,inPair,inputListOffset):
		""" creates a list of kids in the nodeList and returns the offset to the first kid
		Other observations about child creation
		- Nodes 1 and 2 should have had the meta count set when the children were set up
		- Node 1 should have had the File Offset set up when the file was read in
		- Node 1 has the wrong METOF in it - looks like it got loaded with the address of the meta off rather than the content
		"""
		global nodeList
		global currentNodeNumber
		debug_addChildrenToNodeList = False
		numberOfKids = inPair[0]
		metaCountAdr = inPair[1]
		if debug_addChildrenToNodeList:
			print '\naddChildrenToNodeList: reached function'
			print 'addChildrenToNodeList: numberOfKids',
			print 'addChildrenToNodeList: metaCountAdr,',metaCountAdr
		kidNum = 1
		endOfNodes = len(nodeList)		# add to end of the current nodes
		parentNum = currentNodeNumber
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
			node[CURRCHWIP] = UNINIT
			node[CURRCHNUM] = UNINIT
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
		CURRCHWIP = 9	# Current Channel is Work in Progress (True = current channel is being worked on, False = Done)
		CURRCHNUM = 10	# Current Channel number that is being processed 
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
			print actionFlag
		if actionFlag == NEED_TO_MOVE_DOWN:
			return nodeList[theNodeNumber][DNNODENUM]
		else:
			exit()
		
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
		CURRCHWIP = 9	# Current Channel is Work in Progress (True = current channel is being worked on, False = Done)
		CURRCHNUM = 10	# Current Channel number that is being processed 
		CHILDNUM = 11	# Node number of child currently being processed in the sisters list
		return when completed
		
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
		"""
		debug_doAllActionsAtCurrentPoint = True
		currentNodeVec = nodeList[theNodeNumber]
		if debug_doAllActionsAtCurrentPoint:
			self.dumpNodeVals(theNodeNumber)
		if currentNodeVec[NODECOMPL]:						# Current node has completed
			if (theNodeNumber == 0):
				if debug_doAllActionsAtCurrentPoint:
					print 'Tree is done!'
				return TREE_COMPLETED						# Tree is done!!!
			elif (theNodeNumber > 0):
				return NEED_TO_MOVE_UP						# Need to move up the tree
		if not currentNodeVec[NODECOMPL]:					# Current node has not completed
			if currentNodeVec[CURRCHWIP] == UNINIT:			# kick off processing lower node
				currentNodeVec[CURRCHWIP] = WIP
				currentNodeVec[CURRCHNUM] = currentNodeVec[DNNODENUM]
				# currentNodeVec[CHILDNUM] should have been set by the initial setup
				return NEED_TO_MOVE_DOWN
			elif currentNodeVec[CURRCHWIP] == WIP:			# Node is WIP but 
				pass										## TBD
			elif currentNodeVec[CURRCHWIP] == DONE:
				pass										## TBD
		return EARLY_EXIT_FOR_DEBUG
	
	def processTree(self,inFileOffset,theNodeNumber):
		"""If anything can be done, do it
		determineAction based on state of currentNodeNumber
		:returns: [flag,fileOffset,currentNodeNumber]
		flag = DONE when tree is completed, UNINIT when tree is not completed
		fileOffset is the location in the input file that the next string will come from
		"""
		debug_processTree = True
		if debug_processTree:
			print '\nprocessTree: reached function'
			print 'processTree: theNodeNumber',theNodeNumber
			print 'processTree: inFileOffset',inFileOffset
		currentNodeVec = nodeList[theNodeNumber]
		self.dumpNodeVals(theNodeNumber)
		if debug_processTree:
			print 'processTree: currentNodeVec',currentNodeVec
		currentActionsFlag = self.doAllActionsAtCurrentPoint(theNodeNumber)
		if currentActionsFlag == EARLY_EXIT_FOR_DEBUG:
			return [EARLY_EXIT_FOR_DEBUG,inFileOffset,theNodeNumber]
		elif currentActionsFlag == TREE_COMPLETED:
			return [TREE_DONE,inFileOffset,theNodeNumber]
		theNodeNumber = self.doMovement(theNodeNumber,currentActionsFlag)
		if (currentNodeVec[DNNODENUM] != DONE) and (CURRCHWIP != DONE):
			return [TREE_IN_PROGRESS,inFileOffset,theNodeNumber]
		else:
			return [TREE_DONE,inFileOffset,theNodeNumber]
		
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
	debug_moveInListToTree = True
	inPair = InputListHandler.getInputPair(inputListOffset)
	if debug_moveInListToTree:
		print "moveInListToTree: read inPair",inPair
	childNodeNum = NodeHandler.addChildrenToNodeList(inPair,inputListOffset)	# pass the child count and meta count to the creator
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
	debug_newCoreCode = True
	inputFileOffset = 0
	theNodeNumber = 0
	NodeHandler.changeNodeNumber(theNodeNumber)
	InputListHandler.setInputListPtr(inputFileOffset)
	NodeHandler.addFirstNode()
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
				print 'tree done'
				return
			elif nodeToGet[0] == EARLY_EXIT_FOR_DEBUG:
				print 'early exit for debugging'
				return
			elif nodeToGet[0] == TREE_IN_PROGRESS:
				print 'tree in progress'
			elif nodeToGet[0] == GET_NEXT_NODE:
				print 'pull next address'
		NodeHandler.dumpAllNodeVals()
		if nodeToGet[0] == TREE_DONE:
			return
		elif nodeToGet[0] == TREE_IN_PROGRESS:
			pass
		elif nodeToGet[0] == GET_NEXT_NODE:
			moveInListToTree(nodeToGet[1],nodeToGet[2])

##############################################################################
## Code follows

print 'Reading in file',time.strftime('%X %x %Z')

inFileName = 'input2.txt'

InputListHandler = filer()
InputListHandler.loadListFromFile(inFileName)

print 'Processing Nodes',time.strftime('%X %x %Z')

NodeHandler = NodeFunctions()

newCoreCode()

print 'main: processing is done'
NodeHandler.dumpAllNodeVals()
exit()

# Pt1-AoCDay8.py
# 2018 Advent of Code
# Day 8
# Part 1
# https://adventofcode.com/2018/day/8

import time
import re
import os
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

0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5

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
		global debugAllModules
		if debugAllModules:
			debug_getInputPair = True
		else:
			debug_getInputPair = False
		global debugAllModules
		if debugAllModules:
			debug_getInputPair = True
		else:
			debug_getInputPair = False
		pair = [inputList[fileOffset],inputList[fileOffset+1]]
		if debug_getInputPair:
			print 'getInputPair: getting pair at file offset',fileOffset,'returned pair',pair
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
CHANNELIP = 10	# Count of the Current Channel that is being processed

defaultNode = [0,0,0,0,0,0,0,0,0,0,0]
defaultNodeDescr = '[UP,DN,LT,RT,KDS,FILOF,METOF,METCT,NDCMPL,CURCHDN,CHIP]'

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
NODE_COMPLETED = 6
TREE_COMPLETED = 6
EARLY_EXIT_FOR_DEBUG = 8

debugAllModules = False

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
	
	def dumpFormattedAllNodeVals(self):
		"""
		"""
		print '*** Node table ***'
		print 'dumpAllNodeVals: nodes in table - length is',len(nodeList)
		print 'node,',defaultNodeDescr
		i = 0
		for item in nodeList:
			if i < 10:
				print '  ',
			elif i< 100:
				print ' ',
			print i,
			for element in item:
				if element == UNINIT:
					print ' UN',
				elif element == DONE:
					print ' DN',
				elif element >= 10:
					print element,
				elif element >= 0:
					print ' ',element,
				elif element == False:
					print ' F',
				elif element == True:
					print ' T',
				else:
					print element,
			print
			i += 1
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
		self.dumpBitVal('Right node number',nodeNumber,RTNODENUM)
		self.dumpBitVal('Number of kids',nodeNumber,NUMOFKIDS)
		self.dumpBitVal('File Offset',nodeNumber,FILEOFFST)
		self.dumpBitVal('Metadata offset',nodeNumber,METAOFFST)
		self.dumpBitVal('Metadata count',nodeNumber,METALENGTH)
		self.dumpBitVal('Node done status',nodeNumber,NODECOMPL)
		self.dumpBitVal('Current Child Done status',nodeNumber,CURRCHDONE)
		self.dumpBitVal('Current child number being processed',nodeNumber,CHANNELIP)
		
	def pushNode(self,node):
		"""pushNode - 
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_pushNode = True
		else:
			debug_pushNode = False
		print len(nodeList)
		if len(nodeList) > 200:
			self.dumpAllNodeVals()
			exit()
		debug_pushNode = False
		if debug_pushNode:
			print 'pushNode: node is',node,'previous offset',len(nodeList)-1
		nodeList.append(node)
		if debug_pushNode:
			self.dumpAllNodeVals()
		
	def createSingleNodeBelowCurrentNode(self,childOffsetInList,theNodeNumber):
		"""createSingleNodeBelowCurrentNode - add a node
		Initialize the pointers for the first node
		Special values for pointers are
		DONE dead end (will not be updated later)
		UNINIT uninitialized but will be later set to something
		
		:param nodeList: the pair [numberKids,lengthOfMetaData] from the input file
		:returns: True when done
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_createSingleNodeBelowCurrentNode = True
		else:
			debug_createSingleNodeBelowCurrentNode = False
		if debug_createSingleNodeBelowCurrentNode:
			print 'createSingleNodeBelowCurrentNode: childOffsetInList',childOffsetInList
			print 'createSingleNodeBelowCurrentNode: theNodeNumber',theNodeNumber
		node = [0,0,0,0,0,0,0,0,0,0,0]
		node[RTNODENUM] = DONE
		if theNodeNumber == 0:
			node[UPNODENUM] = DONE
			node[NODECOMPL] = False
		else:
			node[UPNODENUM] = theNodeNumber
			node[NODECOMPL] = True
		if inputList[childOffsetInList] == 0:	# Number of Children = 0 case
			node[DNNODENUM] = DONE
			node[METAOFFST] = childOffsetInList + 2
			node[CURRCHDONE] = True
		else:
			node[DNNODENUM] = UNINIT
			node[METAOFFST] = UNINIT
			node[CURRCHDONE] = False
		if theNodeNumber == 0:
			node[METAOFFST] = len(inputList) - inputList[childOffsetInList+1] 
		node[CHANNELIP] = 1
		node[LFNODENUM] = DONE
		node[NUMOFKIDS] = inputList[childOffsetInList]
		node[METALENGTH] = inputList[childOffsetInList+1]
		node[FILEOFFST] = childOffsetInList
		self.pushNode(node)
		if debug_createSingleNodeBelowCurrentNode:
			print 'createSingleNodeBelowCurrentNode: created node',node
		return
		
	def addChildrenToNodeList(self,inPair,inputListOffset,nodeNumber):
		""" creates a list of kids in the nodeList and returns the offset to the first kid
		Other observations about child creation
		- Nodes 1 and 2 should have had the meta count set when the children were set up
		- Node 1 should have had the File Offset set up when the file was read in
		- Node 1 has the wrong METOF in it - looks like it got loaded with the address of the meta off rather than the content
		"""
		global debugAllModules
		global nodeList
		if debugAllModules:
			debug_addChildrenToNodeList = True
		else:
			debug_addChildrenToNodeList = False
		numberOfKids = inPair[0]
		metaCountAdr = inPair[1]
		if debug_addChildrenToNodeList:
			print '\naddChildrenToNodeList: reached function'
			print 'addChildrenToNodeList: numberOfKids',numberOfKids
			print 'addChildrenToNodeList: metaCountAdr,',metaCountAdr
		kidNum = 1
		firstNewNodeNumber = len(nodeList)		# add to end of the current nodes
		parentNum = nodeNumber
		while kidNum <= numberOfKids:
			node = [0,0,0,0,0,0,0,0,0,0,0]	# manual  copy of default node
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
			node[CHANNELIP] = 1
			self.pushNode(node)
			kidNum += 1
		if debug_addChildrenToNodeList:
			print 'addChildrenToNodeList: returning firstNewNodeNumber',firstNewNodeNumber
			self.dumpAllNodeVals()
		return firstNewNodeNumber				# node number of first added child
	
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
		CHANNELIP = 10	# Current Channel number that is being processed 
		
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
		global debugAllModules
		retVal = -1
		if debugAllModules:
			debug_doMovement = True
		else:
			debug_doMovement = True
		if actionFlag == NEED_TO_MOVE_DOWN:
			if debug_doMovement:
				print 'doMovement: Moving from node',theNodeNumber,'down to node',nodeList[theNodeNumber][DNNODENUM]
			return nodeList[theNodeNumber][DNNODENUM]
		elif actionFlag == NEED_TO_MOVE_UP:
			if debug_doMovement:
				print 'doMovement: Moving from node',theNodeNumber,'up to node',nodeList[theNodeNumber][UPNODENUM]
			return nodeList[theNodeNumber][UPNODENUM]
		elif actionFlag == NEED_TO_MOVE_RIGHT:
			if debug_doMovement:
				print 'doMovement: Moving from node',theNodeNumber,'right to node',nodeList[theNodeNumber][RTNODENUM]
			return nodeList[theNodeNumber][RTNODENUM]
		elif actionFlag == CURRENT_POINT_DONE:
			return theNodeNumber
		else:
			print 'wtf-550pm'
			exit()
		
	def prepForRightMove(self,theNodeNumber):
		"""prepForRightMove
		returns true or false
		and returns a number
		not good
		wtf-613pm
		"""
		global debugAllModules
		if debugAllModules:
			debug_prepForRightMove = True
		else:
			debug_prepForRightMove = False
		parentNode = nodeList[theNodeNumber][UPNODENUM]
		if debug_prepForRightMove:
			print 'prepForRightMove: parent still has children to handle'
		if nodeList[theNodeNumber][RTNODENUM] < 0:
			if debug_prepForRightMove:
				print 'prepForRightMove: when children list was created this node was only partly populated'
				print 'prepForRightMove: need to create a new node to the right of this node before moving to the node'
				print 'prepForRightMove: will need to pass the sibling the address and my node number'
				print 'repForRightMove: it would be better to move up a level and let the parent make siblings'
				self.dumpAllNodeVals()
			newNodeNum = self.doMovement(theNodeNumber,NEED_TO_MOVE_UP)		# have to go up to create uncle
			if debug_prepForRightMove:
				print 'prepForRightMove: the new node number will be',newNodeNum
			return False
#		os.system("pause")
		## should ONLY increment the CHANNELIP when it completes the channel
		print 'prepForRightMove: wtf-1235'
		nodeList[parentNode][CHANNELIP] = nodeList[parentNode][CHANNELIP] + 1
		nodeList[parentNode][NODECOMPL] = False
		if debug_prepForRightMove:
			print 'prepForRightMove: before moving right, set up sister'
		rightNode = nodeList[theNodeNumber][RTNODENUM]
		if debug_prepForRightMove:
			print 'prepForRightMove: right node number is',rightNode
			print 'prepForRightMove: need to find sister offset address'
		sisterFileOffset = nodeList[theNodeNumber][FILEOFFST] + nodeList[theNodeNumber][METALENGTH] + 2
		if debug_prepForRightMove:
			print 'prepForRightMove: sisters file offset is',sisterFileOffset
		nodeList[rightNode][FILEOFFST] = sisterFileOffset
		if debug_prepForRightMove:
			print 'prepForRightMove: the pair at sisters file offset in the list is the child count and metaoffset'
		inPair = InputListHandler.getInputPair(sisterFileOffset)
		if debug_prepForRightMove:
			print 'prepForRightMove: sisters pair is',inPair
			print 'prepForRightMove: sisters child count',inPair[0]
			print 'prepForRightMove: metadata count',inPair[1]
		nodeList[rightNode][NUMOFKIDS] = inPair[0]
		nodeList[rightNode][METALENGTH] = inPair[1]
		if debug_prepForRightMove:
			print 'prepForRightMove: node tree after action'
			#self.dumpNodeVals(theNodeNumber)
			self.dumpAllNodeVals()
		return True
				
	def doIncompleteChannelNotDone(self,theNodeNumber):
		"""
		doIncompleteChannelNotDone
		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----
		"""
		global debugAllModules
		if debugAllModules:
			debug_doIncompleteChannelNotDone = True
		else:
			debug_doIncompleteChannelNotDone = True
		if debug_doIncompleteChannelNotDone:
			print '\n**************************\ndoIncompleteChannelNotDone: possibly still active children, at node',theNodeNumber
			self.dumpAllNodeVals()
		## if my child count is not exhausted and the child below me has UNINIT as the pointer then create a child to the right 
		if nodeList[theNodeNumber][DNNODENUM] != -2:
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: Move down to the child already below this node'
				#self.dumpNodeVals(theNodeNumber)
			return self.doMovement(theNodeNumber,NEED_TO_MOVE_DOWN)
		elif nodeList[theNodeNumber][NUMOFKIDS] == 0:
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: No node below and number of kids is zero here'
				print 'doIncompleteChannelNotDone: node tree before action'
				#self.dumpNodeVals(theNodeNumber)
				self.dumpAllNodeVals()
				print 'doIncompleteChannelNotDone: no children below node so metadata follows'
			nodeList[theNodeNumber][METAOFFST] = nodeList[theNodeNumber][FILEOFFST] + 2
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: meta offset for node starts at',nodeList[theNodeNumber][METAOFFST]
				print 'doIncompleteChannelNotDone: should be able to make the node complete'
			## deal with all of the things that relate to this node
			nodeList[theNodeNumber][NODECOMPL] = True
			nodeList[theNodeNumber][CURRCHDONE] = True
			nodeList[theNodeNumber][DNNODENUM] = DONE
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: move to parent is next'
			parentNode = nodeList[theNodeNumber][UPNODENUM]
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: parent node number',parentNode
			if nodeList[theNodeNumber][CHANNELIP] == nodeList[theNodeNumber][NUMOFKIDS]:
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: parent has reached the last child'
				nodeList[theNodeNumber][NODECOMPL] = True
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: node tree after action'
					#self.dumpNodeVals(theNodeNumber)
					self.dumpAllNodeVals()
				## TBD should I move up or right here? 
				## If there's a right to do then I should move right. 
				## If the node is completed then I can move up
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: wtf-1209pm node',theNodeNumber
					self.dumpNodeVals(theNodeNumber)
					self.dumpFormattedAllNodeVals()
				pause
				return self.doMovement(theNodeNumber,NEED_TO_MOVE_UP)
			else:	# node below is done and there's a sister to the right
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: wtf-542pm'
				if not self.prepForRightMove(theNodeNumber):
					if debug_doIncompleteChannelNotDone:
						print 'doIncompleteChannelNotDone: prepForRightMove returned False'
					return self.doMovement(theNodeNumber,CURRENT_POINT_DONE)
				else:
					if debug_doIncompleteChannelNotDone:
						print 'doIncompleteChannelNotDone:  prepForRightMove returned True'
						self.dumpAllNodeVals()
					return self.doMovement(theNodeNumber,NEED_TO_MOVE_RIGHT)
		elif nodeList[theNodeNumber][NUMOFKIDS] != 0: # the first child below current node needs to be created			
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: need to create the first child below this node'
				self.dumpNodeVals(theNodeNumber)
			childOffsetInList = nodeList[theNodeNumber][FILEOFFST] + 2
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: child offset into inList ',childOffsetInList
			inPair = InputListHandler.getInputPair(childOffsetInList)
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: the input pair was',inPair
			if inPair[0] != 0:
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: the input pair [0] was',inPair[0]
				nextChildNodeNumber = len(nodeList)
				self.addChildrenToNodeList(inPair,childOffsetInList,theNodeNumber)
				nodeList[theNodeNumber][DNNODENUM] = nextChildNodeNumber	# down should only point to first in the list not the last in the list
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: Before making the new node moving to node nextChildNodeNumber',nextChildNodeNumber
					self.dumpNodeVals(theNodeNumber)
			elif inPair[0] == 0:
				childOffsetInList = nodeList[theNodeNumber][FILEOFFST] + 2
				newNodeNum = len(nodeList)
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: got zero kids - need to fix up stufffff'
					print 'doIncompleteChannelNotDone: childOffsetInList',childOffsetInList
				self.createSingleNodeBelowCurrentNode(childOffsetInList,theNodeNumber)
				nodeList[theNodeNumber][METAOFFST] = nodeList[newNodeNum][METAOFFST] + nodeList[newNodeNum][METALENGTH]
				nodeList[theNodeNumber][DNNODENUM] = newNodeNum
				nodeList[theNodeNumber][NODECOMPL] = True
				nodeList[theNodeNumber][CURRCHDONE] = True
				if debug_doIncompleteChannelNotDone:
					self.dumpAllNodeVals()
				return self.doMovement(theNodeNumber,CURRENT_POINT_DONE)
			return self.doMovement(theNodeNumber,NEED_TO_MOVE_DOWN)	# move down into the child
		else:
			print 'wtf-725am'
			exit()

	def doNodeIncompleteChannelDone(self,theNodeNumber):
		global debugAllModules
		if debugAllModules:
			debug_doNodeIncompleteChannelDone = True
		else:
			debug_doNodeIncompleteChannelDone = False
		if debug_doNodeIncompleteChannelDone:
			print 'doNodeIncompleteChannelDone: Current channel is done'
			self.dumpNodeVals(theNodeNumber)
		nodeList[theNodeNumber][NODECOMPL] = True
		if debug_doNodeIncompleteChannelDone:
			print 'doNodeIncompleteChannelDone: set node complete to true'
			self.dumpNodeVals(theNodeNumber)
		if theNodeNumber > 0:
			if debug_doNodeIncompleteChannelDone:
				print 'doNodeIncompleteChannelDone: wft-1215pm'
				self.dumpNodeVals(theNodeNumber)
			## why move up here?
#			os.system("pause")
			return self.doMovement(theNodeNumber,NEED_TO_MOVE_UP)
		else:
			if debug_doNodeIncompleteChannelDone:
				print 'doNodeIncompleteChannelDone: got to the top node'				
			return self.doMovement(theNodeNumber,CURRENT_POINT_DONE)
			
	def doNodeIncompleteNode(self,theNodeNumber):
		"""
		## Three possible direction to move
		## Prefer to move down then right then up
		## If the current node is not complete, can it be made complete?
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_doNodeIncompleteNode = True
		else:
			debug_doNodeIncompleteNode = True
		if debug_doNodeIncompleteNode:
			print '\n**********************************\ndoNodeIncompleteNode: Node is not yet completed, at node',theNodeNumber
		if not (nodeList[theNodeNumber][CURRCHDONE]):
			if debug_doNodeIncompleteNode:
				print 'doNodeIncompleteNode: calling doIncompleteChannelNotDone function'
			return self.doIncompleteChannelNotDone(theNodeNumber)
		elif (nodeList[theNodeNumber][CURRCHDONE]):
			if debug_doNodeIncompleteNode:
				print 'doNodeIncompleteNode: calling doNodeIncompleteChannelDone function'
			return self.doNodeIncompleteChannelDone(theNodeNumber)
		else:
			pass
			print 'doNodeIncompleteNode: wtf-1'
			self.dumpNodeVals(theNodeNumber)
		
	def doNodeCompleteNode(self,theNodeNumber):
		"""doNodeCompleteNode
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_doNodeCompleteNode = True
		else:
			debug_doNodeCompleteNode = True
		if debug_doNodeCompleteNode:
			print '\n*************************\ndoNodeCompleteNode: node is complete, node',theNodeNumber
			if theNodeNumber < 0:
				print 'doNodeCompleteNode: wtf-259pm'
				exit()
			# print 'doNodeCompleteNode: table before'
			# self.dumpAllNodeVals()
		# node is complete but the parent may not be done yet
		parentNodeNumber = nodeList[theNodeNumber][UPNODENUM]
		if debug_doNodeCompleteNode:
			print 'doNodeCompleteNode: parentNodeNumber',parentNodeNumber
		parentOffset = nodeList[theNodeNumber][METAOFFST] + nodeList[theNodeNumber][METALENGTH]
		nodeList[parentNodeNumber][METAOFFST] = parentOffset
		if nodeList[parentNodeNumber][CHANNELIP] == nodeList[parentNodeNumber][NUMOFKIDS]:
			nodeList[parentNodeNumber][NODECOMPL] = True
			nodeList[parentNodeNumber][CURRCHDONE] = True
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: Marked Parent Complete'
				print 'doNodeCompleteNode: wtf-1219`'
				self.dumpAllNodeVals()
			#	os.system("pause")
			nextNodeVal = self.doMovement(theNodeNumber,NEED_TO_MOVE_UP)
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: Next Node number is',nextNodeVal
			return nextNodeVal
		elif nodeList[parentNodeNumber][CHANNELIP] < nodeList[parentNodeNumber][NUMOFKIDS]:
			if nodeList[theNodeNumber][RTNODENUM] < 0:	## uninitialized node to the right
				## wtf-227 I think these will be eliminated since I'm going to be creating lists as I go down
				if debug_doNodeCompleteNode:
					print 'doNodeCompleteNode: need a node to the right of me'
					print 'doNodeCompleteNode: nodeList[parentNodeNumber][CHANNELIP]',nodeList[parentNodeNumber][CHANNELIP]
					print 'doNodeCompleteNode: nodeList[parentNodeNumber][NUMOFKIDS]',nodeList[parentNodeNumber][NUMOFKIDS]
					#os.system("pause")
				offsetInFile = nodeList[theNodeNumber][METAOFFST] + nodeList[theNodeNumber][METALENGTH]
				inPair = InputListHandler.getInputPair(offsetInFile)
				nextChildNodeNumber = len(nodeList)
				self.addChildrenToNodeList(inPair,offsetInFile,theNodeNumber)
				nodeList[theNodeNumber][DNNODENUM] = nextChildNodeNumber	# down should only point to first in the list not the last in the list
				if debug_doNodeCompleteNode:
					self.dumpAllNodeVals()
				nodeList[parentNodeNumber][CHANNELIP] = nodeList[parentNodeNumber][CHANNELIP] + 1
				if debug_doNodeCompleteNode:
					print 'doNodeCompleteNode: staying at the same node but causing re-run'
					self.dumpAllNodeVals()
				return theNodeNumber
			nodeList[theNodeNumber][RTNODENUM] = DONE	# Don't really have to do this but do it anyway
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: still kids to the right of the parent'
				print 'wtf-1039am'
				if self.prepForRightMove(theNodeNumber) == False:
					return theNodeNumber
				else:
					return theNodeNumber
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: table after right move prep'
				self.dumpAllNodeVals()
			return self.doMovement(theNodeNumber,NEED_TO_MOVE_UP)
		elif nodeList[parentNodeNumber][NUMOFKIDS] < 0:		## parent is missing siblings
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: parent is missing siblings move up and hope it works?'
				print 'doNodeCompleteNode: current node before the uncle is created'
				self.dumpNodeVals(theNodeNumber)
				print 'doNodeCompleteNode: uncle node before the uncle is created'
				self.dumpNodeVals(parentNodeNumber)
			## problem with just moving up is that the parent doesn't know this node number without scanning the from the start
			## either add a function to scan the list or hook up the parent with a new sibling node
			## create a new sibling for the parent
			##
			## siblings need to be created relative to the existing parent offset
			## otherwise they get put in "parallel" with the current node
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: creating an uncle node'
			offsetInFile = nodeList[theNodeNumber][METAOFFST] + nodeList[theNodeNumber][METALENGTH]
			inPair = InputListHandler.getInputPair(offsetInFile)
			self.addChildrenToNodeList(inPair,offsetInFile,theNodeNumber)
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: wtf-1216'
				self.dumpNodeVals(theNodeNumber)
				#os.system("pause")
			if debug_doNodeCompleteNode:
				print 'doNodeCompleteNode: '
				print 'doNodeCompleteNode: current node after the uncle is created'
				self.dumpNodeVals(theNodeNumber)
				print 'doNodeCompleteNode: parent node after the uncle is created'
				self.dumpNodeVals(parentNodeNumber)
#			exit()
			return self.doMovement(theNodeNumber,NEED_TO_MOVE_UP)
		else:
			print 'doNodeCompleteNode: fell past all of the if and elif clauses node',theNodeNumber
			print 'doNodeCompleteNode: , parent channel pointer',nodeList[parentNodeNumber][CHANNELIP]
			print 'doNodeCompleteNode: , nodeList[parentNodeNumber][CHANNELIP]',nodeList[parentNodeNumber][CHANNELIP]
			print 'doNodeCompleteNode: , nodeList[parentNodeNumber][NUMOFKIDS]',nodeList[parentNodeNumber][NUMOFKIDS]
			self.dumpNodeVals(theNodeNumber)
			print 'doNodeCompleteNode: nodeList[parentNodeNumber][CHANNELIP]',nodeList[parentNodeNumber][CHANNELIP]
			self.dumpFormattedAllNodeVals()
			print 'doNodeCompleteNode: parentNodeNumber',parentNodeNumber
			print 'doNodeCompleteNode: parent vector'
			self.dumpNodeVals(parentNodeNumber)
			print 'doNodeCompleteNode: wtf-120pm'
			exit()
	
	def processTree(self,inFileOffset,theNodeNumber):
		"""If anything can be done, do it
		determineAction based on state of currentNodeNumber
		:returns: [flag,fileOffset,currentNodeNumber]
		flag = DONE when tree is completed, UNINIT when tree is not completed
		fileOffset is the location in the input file that the next string will come from
		"""
		global debugAllModules
		if debugAllModules:
			debug_processTree = True
		else:
			debug_processTree = False
		if debug_processTree:
			print '\nprocessTree: reached function'
			print 'processTree: theNodeNumber',theNodeNumber
			print 'processTree: inFileOffset',inFileOffset
		if debug_processTree:
			self.dumpNodeVals(theNodeNumber)
			self.dumpNodeVals(theNodeNumber)
		if debug_processTree:
			print 'processTree: nodeList[theNodeNumber]',nodeList[theNodeNumber]
		theNodeNumber = self.doAllActionsAtCurrentPoint(theNodeNumber)
		if theNodeNumber < 0:
			print 'wtf-538pm'
			exit()
		if theNodeNumber == 0:
				return [TREE_DONE,inFileOffset,theNodeNumber]
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
		CHANNELIP = 10	# Current Channel number that is being processed 
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
		dumpAllNodeVals: nodes in table - length is 4
		node, [UP, DN, LT, RT,KDS,FILOF,METOF,METCT,NDCMPL,CURCHDN,CHIP]
		0  [-1,  1, -1, -1,  2,    0,   13,    3,  True,   True,      2]
		1   [0, -1, -1,  2,  0,    2,    4,    3,  True,   True,      1]
		2   [0,  3, 1,  -1,  1,    7,   12,    1,  True,   True,      1]
		3   [2, -1, -1, -1,  0,    9,   11,    1,  True,   True,      1]
		13 15
		4 6
		12 12
		11 11
		Sum = 138		
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_doAllActionsAtCurrentPoint = True
		else:
			debug_doAllActionsAtCurrentPoint = False
		if debug_doAllActionsAtCurrentPoint:
			print 'doAllActionsAtCurrentPoint: Reached function, node,',theNodeNumber
			if theNodeNumber < 0:
				print '\ndoAllActionsAtCurrentPoint: wtf-300pm - boy that went really bad'
				exit()
			if theNodeNumber >= len(nodeList):
				print 'doAllActionsAtCurrentPoint: wtf-533pm the node number is out of sync with the list'
				exit()
				## seems like a count got off by an add
		if not nodeList[theNodeNumber][NODECOMPL]:		# Current node has not completed
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: not complete'
			return self.doNodeIncompleteNode(theNodeNumber)
		else:											# node is complete at the point
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: complete'
			if theNodeNumber == 0:
				return TREE_COMPLETED
			return self.doNodeCompleteNode(theNodeNumber)
	
########################################################################
## Code

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	NodeHandler.dumpAllNodeVals()
	exit()

def newCoreCode():
	"""Creates the initial parent and child
	Calls processTree to handle nodes
	Operates on return value
	"""
	global nodeList
	debug_newCoreCode = False
	inputFileOffset = 0
	theNodeNumber = 0
	InputListHandler.setInputListPtr(inputFileOffset)
	NodeHandler.createSingleNodeBelowCurrentNode(inputFileOffset,theNodeNumber)
	nextNodeNum = len(nodeList)
	nodeList[0][DNNODENUM] = nextNodeNum
	inPair = InputListHandler.getInputPair(inputFileOffset)
	NodeHandler.addChildrenToNodeList(inPair,inputFileOffset,theNodeNumber)
	nodeToGet = [TREE_IN_PROGRESS,inputFileOffset,theNodeNumber]
	inFileOffset = 0
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

inFileName = 'input2.txt'

InputListHandler = filer()
InputListHandler.loadListFromFile(inFileName)

print 'Processing Nodes',time.strftime('%X %x %Z')

NodeHandler = NodeFunctions()

newCoreCode()

print 'main: processing is done'
print 'node at the end was',currentNodeNumber
NodeHandler.dumpAllNodeVals()

sumTheMetaStuff()

exit()

# Pt2-AoCDay8.py
# 2018 Advent of Code
# Day 8
# Part 2
# https://adventofcode.com/2018/day/8

import time
import re
import os
"""
--- Part Two ---
The second check is slightly more complicated: you need to find the value of the root node (A in the example above).

The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata entries. So, the value of node B is 10+11+12=33, 
and the value of node D is 99.

However, if a node does have child nodes, the metadata entries become indexes which refer to those child nodes. 
A metadata entry of 1 refers to the first child node, 2 to the second, 3 to the third, and so on. 
The value of this node is the sum of the values of the child nodes referenced by the metadata entries. 
If a referenced child node does not exist, that reference is skipped. 
A child node can be referenced multiple time and counts each time it is referenced. 
A metadata entry of 0 does not refer to any child node.

For example, again using the above nodes:

Node C has one metadata entry, 2. Because node C has only one child node, 
2 references a child node which does not exist, and so the value of node C is 0.
Node A has three metadata entries: 1, 1, and 2. The 1 references node A's first child node, B, 
and the 2 references node A's second child node, C. 
Because node B has a value of 33 and node C has a value of 0, the value of node A is 33+33+0=66.
So, in this example, the value of the root node is 66.

What is the value of the root node?
"""

debugAllModules = False

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
		
	def moveToNextPair(self):
		"""Move the input list pointer up by 2 (assumes children being created)
		"""
		global inputListPtr
		global debugAllModules
		if debugAllModules:
			debug_getInputPair = True
		else:
			debug_getInputPair = False
		inputListPtr += 2
			
	def getInputPair(self,fileOffset):
		"""Get the input pair at inputListPtr
		"""
		global inputList
		global debugAllModules
		if debugAllModules:
			debug_getInputPair = True
		else:
			debug_getInputPair = False
		pair = [inputList[fileOffset],inputList[fileOffset+1]]
		if debug_getInputPair:
			print 'getInputPair: getting pair at file offset',fileOffset,'returned pair',pair
		return pair
	
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

	def setCurrentFileInputOffset(self,offset):
		"""
		"""
		if debugAllModules:
			debug_doIncompleteChannelNotDone = True
		else:
			debug_setCurrentFileInputOffset = False
		global inputListPtr
		inputListPtr = offset
		if debug_setCurrentFileInputOffset:
			print 'setCurrentFileInputOffset: Set the input list pointer to',inputListPtr
		return
	
	def getCurrentFileInputOffset(self):
		"""
		"""
		if debugAllModules:
			debug_getCurrentFileInputOffset = True
		else:
			debug_getCurrentFileInputOffset = False
		global inputListPtr
		if debug_getCurrentFileInputOffset:
			print 'getCurrentFileInputOffset: Returning input list pointer =',inputListPtr
		return inputListPtr
		
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
defaultNodeDescr = ' Node  UP  DOWN  LEFT RIGHT  KIDS FILOF METOF METCT NDCMP  CHDN  CHIP'

# Tree and other status values - negative enums essentially
DONE 					= -1
UNINIT 					= DONE 					- 1
TREE_DONE				= UNINIT 				- 1
TREE_IN_PROGRESS 		= TREE_DONE 			- 1
CURRENT_POINT_DONE		= TREE_IN_PROGRESS 		- 1
NEED_TO_MOVE_DOWN 		= CURRENT_POINT_DONE 	- 1
NEED_TO_MOVE_RIGHT		= NEED_TO_MOVE_DOWN 	- 1
NEED_TO_MOVE_UP			= NEED_TO_MOVE_RIGHT 	- 1
TREE_COMPLETED 			= NEED_TO_MOVE_UP 		- 1
EARLY_EXIT_FOR_DEBUG 	= TREE_COMPLETED 		- 1

class NodeFunctions():

	def dumpAllNodeVals(self):
		"""dumpAllNodeVals - Dumps out all of the node values.
		"""
		global nodeList
		self.dumpPartOfNodeList(0)
		return
		
	def dumpBitVal(self,myStr,nodeNumber,theFieldVal):
		"""
		"""
		global nodeList
		print '', myStr,
		if nodeList[nodeNumber][theFieldVal] == UNINIT:
			print 'Uninitialized'
		elif nodeList[nodeNumber][theFieldVal] == DONE:
			print 'Done'
		else:
			print nodeList[nodeNumber][theFieldVal]
		
	def dumpNodeVals(self,nodeNumber):
		"""dumpNodeVals
		
		:param: nodeNumber the offset to the node in array
		"""
		global nodeList
		debug_dumpNodeVals = False
		print 'dumpNodeVals: at node',nodeNumber
#		print nodeList[nodeNumber]
		if nodeNumber > len(nodeList) - 1:
			abbyTerminate('dumpNodeVals: Offset is not in list, exiting...')
		nodeVec = nodeList[nodeNumber]
		self.dumpBitVal('Up ....',nodeNumber,UPNODENUM)
		self.dumpBitVal('Down ..',nodeNumber,DNNODENUM)
		self.dumpBitVal('Left ..',nodeNumber,LFNODENUM)
		self.dumpBitVal('Right .',nodeNumber,RTNODENUM)
		self.dumpBitVal('Kids ..',nodeNumber,NUMOFKIDS)
		self.dumpBitVal('FilOf .',nodeNumber,FILEOFFST)
		self.dumpBitVal('MetOf .',nodeNumber,METAOFFST)
		self.dumpBitVal('MetCt .',nodeNumber,METALENGTH)
		self.dumpBitVal('NodDn .',nodeNumber,NODECOMPL)
		self.dumpBitVal('ChDn ..',nodeNumber,CURRCHDONE)
		self.dumpBitVal('ChNum .',nodeNumber,CHANNELIP)
		
	def dumpPartOfNodeList(self,nodeListStart):
		global nodeList
		print '*** Node table length =',len(nodeList),'***'
		print defaultNodeDescr
		i = nodeListStart
		for item in nodeList[nodeListStart:]:
			print '%3d' % (i),
			for element in item:
				if element == UNINIT:
					print '%5s' % ('UN'),
				elif element == DONE:
					print '%5s' % ('DN'),
				elif element >= 0:
					print '%5d' % (element),
				elif element == False:
					print '%5s' % ('F'),
				elif element == True:
					print '%5s' % ('T'),
				elif element >= 0:
					print '%5d' % (element),
			print
			i += 1
		return
	
	def pushNode(self,node):
		"""pushNode - Pushes nodes into the node list
		Does not mess with any counters, etc.
		Constant - stopLength is to keep the list from running away
		
		:param: node - the node vector
		:returns: no return value
		"""
		global nodeList
		global debugAllModules
		stopLength = 10000
		if debugAllModules:
			debug_pushNode = True
		else:
			debug_pushNode = False
		print '.',		# print a dot for every node that gets pushed - fairly low overhead cost
		if len(nodeList) > stopLength:		# stop if the list runs away
			self.dumpAllNodeVals()
			exit()
		nodeList.append(node)
		if debug_pushNode:
			print 'pushNode: list length after push =',len(nodeList)
			print 'pushNode: node is',node,'previous offset',len(nodeList)-1
			self.dumpAllNodeVals()
		
	def createSingleNodeBelowCurrentNode(self,theNodeNumber):
		"""createSingleNodeBelowCurrentNode - add a node
		The first node is always a single node and is identified by theNodeNumber being zero
		The other time this is called is for a node which has no children
		Initialize the pointers for a single node
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
		node = [0,0,0,0,0,0,0,0,0,0,0]
		# these next items come from the input file stream
		nextNodeNum = len(nodeList)
		node[NUMOFKIDS] = inputList[InputListHandler.getCurrentFileInputOffset()]		# number of kids = first number in inList
		node[METALENGTH] = inputList[InputListHandler.getCurrentFileInputOffset()+1]	# metadata length = second number in inList
		node[FILEOFFST] = InputListHandler.getCurrentFileInputOffset()					# where the inList pointer was at
		if len(nodeList) == 0:								# special case for the first node
			node[METAOFFST] = len(inputList) - node[METALENGTH]	# known a priori
#			print 'createSingleNodeBelowCurrentNode: (1) setting METAOFFST to',node[METAOFFST]
			node[UPNODENUM] = DONE			# no up for first nodeList
			node[NODECOMPL] = False			# node is definitely not completed
			node[CURRCHDONE] = False		# Current channel is not yet done
			node[DNNODENUM] = UNINIT		# will be 1 later
		else:								# singleton nodes
			node[METAOFFST] = InputListHandler.getCurrentFileInputOffset() + 2		# always the next locations
#			print 'createSingleNodeBelowCurrentNode: (2) setting METAOFFST to',node[METAOFFST]
			node[UPNODENUM] = theNodeNumber				# the current node is always the parent
			node[NODECOMPL] = True						# Since it's a single node, it is always done already
			node[CURRCHDONE] = True						# Channel is done
			node[DNNODENUM] = DONE						# No down node since it's an endpoint
			nodeList[theNodeNumber][DNNODENUM] = nextNodeNum	# parent should point to this node when done
			if debug_createSingleNodeBelowCurrentNode:
				print 'createSingleNodeBelowCurrentNode: the offset address is',newOffsetAddress
		node[RTNODENUM] = DONE			# no right hand node
		node[LFNODENUM] = DONE			# no left hand node
		node[CHANNELIP] = 1				# There's only one channel anyway
		self.pushNode(node)
		if debug_createSingleNodeBelowCurrentNode:
			print 'createSingleNodeBelowCurrentNode: theNodeNumber',theNodeNumber
			print 'createSingleNodeBelowCurrentNode: created node',node
			self.dumpNodeVals(len(nodeList)-1)
		return
		
	def addChildrenToNodeList(self,parentNodeNum):
		""" creates a list of kids in the nodeList.
		
		:param: parentNodeNum - node number of the parent = the UPNODENUM value
		:returns: node number of the first new child that was just added
		"""
		global debugAllModules
		global nodeList
		if debugAllModules:
			debug_addChildrenToNodeList = True
		else:
			debug_addChildrenToNodeList = False
		childAndMetaCounts = InputListHandler.getInputPair(InputListHandler.getCurrentFileInputOffset())		# pulls the child count and meta count pair from the input file
		firstNewNodeNumber = len(nodeList)		# new node is always just past the end of the current list
		kidNum = firstNewNodeNumber 			# start at first and move up as the row gets processed
		childCount = childAndMetaCounts[0]
		terminalKidNumber = firstNewNodeNumber + childCount
		if debug_addChildrenToNodeList:
			print '\naddChildrenToNodeList: reached function, parentNodeNum',parentNodeNum
			print 'addChildrenToNodeList: childCount',childCount
			print 'addChildrenToNodeList: firstNewNodeNumber',firstNewNodeNumber
			print 'addChildrenToNodeList: kidNum',kidNum
			print 'addChildrenToNodeList: terminalKidNumber',terminalKidNumber
		while kidNum <= terminalKidNumber-1:	# Number of children
			node = [0,0,0,0,0,0,0,0,0,0,0]		# manual  copy of default node
			node[UPNODENUM] = parentNodeNum
			node[DNNODENUM] = UNINIT
			if kidNum == terminalKidNumber-1:	# last child
				node[RTNODENUM] = DONE			# no right pointer in the last child
			else:
				node[RTNODENUM] = kidNum + 1	# not the last child point to the next child
			if kidNum == firstNewNodeNumber:
				node[METALENGTH] = inputList[InputListHandler.getCurrentFileInputOffset() + 3]
				node[FILEOFFST] = InputListHandler.getCurrentFileInputOffset() + 2
				node[LFNODENUM] = DONE
				node[NUMOFKIDS] = inputList[InputListHandler.getCurrentFileInputOffset()+2]
				nodeList[parentNodeNum][DNNODENUM] = firstNewNodeNumber
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
			print '\naddChildrenToNodeList: Number Of Kids',childAndMetaCounts[0]
			print 'addChildrenToNodeList: Meta Count Address,',childAndMetaCounts[1]
			print 'addChildrenToNodeList: Added to nodeList'
			self.dumpPartOfNodeList(firstNewNodeNumber)
			print 'addChildrenToNodeList: Returning first new node number',firstNewNodeNumber
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
			debug_doMovement = False
		routingMessagesOnly = False
		if actionFlag == NEED_TO_MOVE_DOWN:
			if debug_doMovement or routingMessagesOnly:
				print 'doMovement: Moving from node',theNodeNumber,'down to node',nodeList[theNodeNumber][DNNODENUM]
			retVal = nodeList[theNodeNumber][DNNODENUM]
		elif actionFlag == NEED_TO_MOVE_UP:
			if debug_doMovement or routingMessagesOnly:
				print 'doMovement: Moving from node',theNodeNumber,'up to node',nodeList[theNodeNumber][UPNODENUM]
			if theNodeNumber > 0:
				retVal =  nodeList[theNodeNumber][UPNODENUM]
			else:
				retVal = 0
		elif actionFlag == NEED_TO_MOVE_RIGHT:
			if debug_doMovement or routingMessagesOnly:
				print 'doMovement: Moving from node',theNodeNumber,'right to node',nodeList[theNodeNumber][RTNODENUM]
			retVal =  nodeList[theNodeNumber][RTNODENUM]
		elif actionFlag == CURRENT_POINT_DONE:
			if debug_doMovement or routingMessagesOnly:
				print 'doMovement: Staying at node',theNodeNumber
			retVal = theNodeNumber
		return retVal
		
	def prepForRightMove(self,theNodeNumber):
		"""prepForRightMove
		:returns: true or false
		True = can make the move to the right
		False = cant make the move to the right - should be designed out by fixes to calling routines
		"""
		global nodeList
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
				print 'prepForRightMove: it would be better to move up a level and let the parent make siblings'
				self.dumpAllNodeVals()
			newNodeNum = self.doMovement(theNodeNumber,NEED_TO_MOVE_UP)		# have to go up to create uncle
			if debug_prepForRightMove:
				print 'prepForRightMove: the new node number will be',newNodeNum
				print 'prepForRightMove: returning false'
			return False
		if debug_prepForRightMove:
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
	
	def askForDirections(self,theNodeNumber):
		"""Function looks around a particular node to try and determine the best direction to move.
		Preference for movement is 
		1 - down (highest priority)
		2 - right
		3 - up (lowest priority)
		Function does not do the movement.
		:param: theNodeNumber - look around from a node to determine where best to go next.
		:returns: direction to go next
		NEED_TO_MOVE_DOWN
		NEED_TO_MOVE_RIGHT
		NEED_TO_MOVE_UP	
		
		UPNODENUM
		DNNODENUM
		LFNODENUM
		RTNODENUM
		NUMOFKIDS
		FILEOFFST
		METAOFFST
		METALENGTH
		NODECOMPL
		CURRCHDONE
		CHANNELIP
		"""
		global nodeList
		global debugAllModules
		#os.system('pause')
		if debugAllModules:
			debug_askForDirections = True
		else:
			debug_askForDirections = False
		if debug_askForDirections:
			print '\n**************************\nCall askForDirections: figure out which way to go for node',theNodeNumber
			self.dumpAllNodeVals()
		# Can I move to node below?
		if (nodeList[theNodeNumber][DNNODENUM] >= 0) and (nodeList[theNodeNumber][NUMOFKIDS] > 0) and (not nodeList[theNodeNumber][NODECOMPL]):
			if debug_askForDirections:
				print 'Call askForDirections: moving down'
			return NEED_TO_MOVE_DOWN
		if nodeList[theNodeNumber][METAOFFST] == UNINIT:
			return CURRENT_POINT_DONE		
		if (nodeList[theNodeNumber][NUMOFKIDS] > 0) and (not nodeList[theNodeNumber][NODECOMPL]):
			return CURRENT_POINT_DONE
		# can I move to node to the right?
		if (nodeList[theNodeNumber][RTNODENUM] >= 0):
			if debug_askForDirections:
				print 'doaskForDirections: moving right'
			return NEED_TO_MOVE_RIGHT
		# up movement is the last resort
		if debug_askForDirections:
			print 'doaskForDirections: moving up'
		return NEED_TO_MOVE_UP
	
	def findLastNodeHorizontally(self,startingNodeNumber):
		"""

		:returns: with [foundNodeNumber,count]		
		"""
		i = 1
		currentNode = startingNodeNumber
		while i < 99:
			if nodeList[currentNode][RTNODENUM] > 0:
				i += 1
				currentNode = nodeList[currentNode][RTNODENUM]
			else:
				return [currentNode,i]
		
	def checkParentDone(self,theNodeNumber):
		"""After finishing a node
		Increment the parent channel number
		If the parent channel number was already at the terminal count then mark it as completed
		
		Need to make this smart
		Increment node number in parent
		Set the node done of the parent if the count is terminal
		Set the channel in progress
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_checkParentDone = True
		else:
			debug_checkParentDone = False
		if debug_checkParentDone:
			print 'checkParentDone: reached function, node',theNodeNumber,'tree before'
			self.dumpAllNodeVals()
		nodeList[theNodeNumber][NODECOMPL] = True
		nodeList[theNodeNumber][CURRCHDONE] = True
		nextNodeStart = nodeList[theNodeNumber][METAOFFST] + nodeList[theNodeNumber][METALENGTH]
		InputListHandler.setCurrentFileInputOffset(nextNodeStart)
		if debug_checkParentDone:
			print 'checkParentDone: nextNodeStart',nextNodeStart
		# Do stuff to the parent
		parentNode = nodeList[theNodeNumber][UPNODENUM]
		if nodeList[parentNode][CHANNELIP] < nodeList[parentNode][NUMOFKIDS]:
			nodeList[parentNode][CHANNELIP] = nodeList[parentNode][CHANNELIP] + 1
		else:		# at the last node
			nodeList[parentNode][METAOFFST] = nodeList[theNodeNumber][METAOFFST] + nodeList[theNodeNumber][METALENGTH]
			nodeList[parentNode][NODECOMPL] = True
			if debug_checkParentDone:
				print 'checkParentDone: Set parent node',parentNode,'meta offset',nodeList[parentNode][METAOFFST]	
				print 'checkParentDone: Last Child is completed, set the parents node complete to True'
				print 'checkParentDone: Dont need to increment the child counter since it is already at term ct'
		nodeList[parentNode][CURRCHDONE] = True
		if debug_checkParentDone:
			print 'checkParentDone: parent node number',parentNode
			print 'checkParentDone: incremented current channel in process'
		if debug_checkParentDone:
			print 'checkParentDone: completed function, node',theNodeNumber,'tree after'
			self.dumpAllNodeVals()
	
	def doIncompleteChannelNotDone(self,theNodeNumber):
		"""
		doIncompleteChannelNotDone: Acts on the basis of the number of children of the current node.
		
		0 0 0 0  0  0  0 0 0 0 1  1 1 1 1 1
		0 1 2 3  4  5  6 7 8 9 0  1 2 3 4 5
		
		2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
		A----------------------------------
			B----------- C-----------
							 D-----
		
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_doIncompleteChannelNotDone = True
		else:
			debug_doIncompleteChannelNotDone = False
		if debug_doIncompleteChannelNotDone:
			print '\n***********************************************************\n'
			print 'doIncompleteChannelNotDone: possibly still active children, at node',theNodeNumber
			self.dumpAllNodeVals()
		if nodeList[theNodeNumber][NUMOFKIDS] == 0:		# No children below current node
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: Zero children below node'
				print 'doIncompleteChannelNotDone: no children below node so metadata follows'
			nodeList[theNodeNumber][METAOFFST] = nodeList[theNodeNumber][FILEOFFST] + 2
			nodeList[theNodeNumber][DNNODENUM] = DONE	# There's no child below this node so mark it DONE
#			print 'doIncompleteChannelNotDone (1): setting METAOFFST to',nodeList[theNodeNumber][METAOFFST]
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: meta offset for node',theNodeNumber,'starts at',nodeList[theNodeNumber][METAOFFST]
			self.checkParentDone(theNodeNumber)
			nextNodeStart = nodeList[theNodeNumber][METAOFFST] + nodeList[theNodeNumber][METALENGTH]
			InputListHandler.setCurrentFileInputOffset(nextNodeStart)
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: nextNodeStart',nextNodeStart		
			# single children have no siblings so the only move is up
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: zero children so move back to parent is next'
			parentNode = nodeList[theNodeNumber][UPNODENUM]
			return self.doMovement(theNodeNumber,self.askForDirections(theNodeNumber))
		elif nodeList[theNodeNumber][NUMOFKIDS] > 0: 	# There are kids below the current node
			if nodeList[theNodeNumber][DNNODENUM] == UNINIT:	# kids are not yet created
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: No down pointer, so create children below this parent'
				## address of the child should be off the parent's address if it's a child directly below
				nextChildNodeNumber = self.addChildrenToNodeList(theNodeNumber)
				InputListHandler.moveToNextPair()
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: Next node below will be',nextChildNodeNumber
					#self.dumpNodeVals(theNodeNumber)
				return self.doMovement(theNodeNumber,self.askForDirections(theNodeNumber))	# move down into the child
			else:		# kids were already created
				if nodeList[theNodeNumber][FILEOFFST] >= 0:
					## scan right on my children to find the last one
					## use that to get the offset and mark the node done
					## assuming that the other nodes are all solved
					## alternately could remember where the last one ended or use the ending of the last one to my advantage???
					lastPair = self.findLastNodeHorizontally(nodeList[theNodeNumber][DNNODENUM])
					print 'lastPair',lastPair
					print 'kids',nodeList[theNodeNumber][NUMOFKIDS]
					if lastPair[1] == nodeList[theNodeNumber][NUMOFKIDS]:
						print 'kid count matched'
						lastNodeAddr = nodeList[lastPair[0]][METALENGTH] + nodeList[lastPair[0]][METAOFFST]
						nodeList[theNodeNumber][METAOFFST] = lastNodeAddr
						nodeList[theNodeNumber][CURRCHDONE] = True
						nodeList[theNodeNumber][NODECOMPL] = True
						print 'lastNodeAddr',lastNodeAddr
#					abbyTerminate('fileoff known')
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: There should already be a child below this node'
					self.dumpAllNodeVals()
				if nodeList[theNodeNumber][LFNODENUM] > 0:
					offsetNode = nodeList[theNodeNumber][LFNODENUM]
					childOffsetInList = nodeList[offsetNode][METALENGTH] + nodeList[offsetNode][METAOFFST]
					if debug_doIncompleteChannelNotDone:
						print 'doIncompleteChannelNotDone: setting offsetNode from the left node',offsetNode,'to value',childOffsetInList
				else:
					childOffsetInList = nodeList[theNodeNumber][FILEOFFST] + 2
					if debug_doIncompleteChannelNotDone:
						print 'doIncompleteChannelNotDone: setting offsetNode from the parent',offsetNode
				InputListHandler.setCurrentFileInputOffset(childOffsetInList)
				if debug_doIncompleteChannelNotDone:
					print 'doIncompleteChannelNotDone: child offset into inList ',childOffsetInList
				if InputListHandler.getInputPair(childOffsetInList) == 0:	# no children below the next node
					childOffsetInList = nodeList[theNodeNumber][FILEOFFST]
					newNodeNum = len(nodeList)
					if debug_doIncompleteChannelNotDone:
						print 'doIncompleteChannelNotDone: got zero kids - need to fix up stufffff'
						print 'doIncompleteChannelNotDone: childOffsetInList',childOffsetInList
					self.createSingleNodeBelowCurrentNode(theNodeNumber)
					nodeList[theNodeNumber][METAOFFST] = nodeList[newNodeNum][METAOFFST] + nodeList[newNodeNum][METALENGTH]
#					print 'doIncompleteChannelNotDone (3): setting metaoffset to',nodeList[theNodeNumber][METAOFFST]
					nodeList[theNodeNumber][NODECOMPL] = True
					nodeList[theNodeNumber][CURRCHDONE] = True
					if debug_doIncompleteChannelNotDone:
						self.dumpAllNodeVals()
					return self.doMovement(theNodeNumber,self.askForDirections(theNodeNumber))
		elif nodeList[theNodeNumber][NUMOFKIDS] == UNINIT:	# somebody moved here without filling in the record
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: Need to fill in record the left'
			sisterNode = nodeList[theNodeNumber][LFNODENUM]
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: Sister node to the left is',sisterNode
			sisterRecordEnd = nodeList[sisterNode][METAOFFST] + nodeList[sisterNode][METALENGTH]
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: sister record end (plus 1) is node',sisterRecordEnd
				print 'doIncompleteChannelNotDone: my record starts at',sisterRecordEnd
				print 'doIncompleteChannelNotDone: compare this with InputListHandler.getCurrentFileInputOffset()',InputListHandler.getCurrentFileInputOffset()
			# if sisterRecordEnd != InputListHandler.getCurrentFileInputOffset():
				# print 'doIncompleteChannelNotDone: input file offset mismatch with calculated value from left node'
			if debug_doIncompleteChannelNotDone:
				print 'sister node'
				self.dumpNodeVals(sisterNode)
			inPair = InputListHandler.getInputPair(sisterRecordEnd)
			nodeList[theNodeNumber][NUMOFKIDS] = inPair[0]
			nodeList[theNodeNumber][METALENGTH] = inPair[1]
			nodeList[theNodeNumber][FILEOFFST] = sisterRecordEnd
			if debug_doIncompleteChannelNotDone:
				print 'doIncompleteChannelNotDone: the node list'
				self.dumpAllNodeVals()
			return self.doMovement(theNodeNumber,self.askForDirections(theNodeNumber))
		else:											# Should not be the case
			abbyTerminate('wft-810am')

	def doNodeIncompleteChannelDone(self,theNodeNumber):
		global nodeList
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
			return self.doMovement(theNodeNumber,self.askForDirections(theNodeNumber))
		else:
			if debug_doNodeIncompleteChannelDone:
				print 'doNodeIncompleteChannelDone: got to the top node'
			return self.doMovement(theNodeNumber,self.askForDirections(theNodeNumber))
	
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
			debug_doNodeIncompleteNode = False
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
		If you are done at a point then adjust the parent node
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_doNodeCompleteNode = True
		else:
			debug_doNodeCompleteNode = False
		if debug_doNodeCompleteNode:
			print '\n*******************************************\n'
			print 'doNodeCompleteNode: node is complete, node',theNodeNumber
			self.dumpAllNodeVals()
		if theNodeNumber < 0:
			abbyTerminate('doNodeCompleteNode: ERROR wtf-259pm')
		self.checkParentDone(theNodeNumber)
		return self.doMovement(theNodeNumber,self.askForDirections(theNodeNumber))
			
	def processTree(self,theNodeNumber):
		"""If anything can be done, do it
		determineAction based on state of currentNodeNumber
		
		:param: theNodeNumber - the current node number that is being processed
		:returns: [flag,fileOffset,currentNodeNumber]
		flag = DONE when tree is completed, UNINIT when tree is not completed
		
		"""
		global debugAllModules
		global nodeList
		if debugAllModules:
			debug_processTree = True
		else:
			debug_processTree = False
		if debug_processTree:
			print '\nprocessTree: reached function - node',theNodeNumber
			self.dumpNodeVals(theNodeNumber)
		theNodeNumber = self.doAllActionsAtCurrentPoint(theNodeNumber)
		if (theNodeNumber == 0) and (nodeList[theNodeNumber][NODECOMPL]):
			return [TREE_DONE,theNodeNumber]
		if theNodeNumber < 0:
			abbyTerminate('processTree: Moved to a negative node number')
		return [TREE_IN_PROGRESS,theNodeNumber]
	
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
			self.dumpAllNodeVals()
		if theNodeNumber < 0:				## debug error condition node number less than zero
			abbyTerminate('doAllActionsAtCurrentPoint: wtf-300pm - boy that went really bad')
		if theNodeNumber >= len(nodeList):	## debug error condition node number past the end of the list
			abbyTerminate('doAllActionsAtCurrentPoint: wtf-533pm the node number is out of sync with the list')
		if (theNodeNumber == 0) and (nodeList[theNodeNumber][NODECOMPL]):
			abbyTerminate('doAllActionsAtCurrentPoint: wtf-702pm this should have been enough to make it stop')
			return TREE_COMPLETED
		if not nodeList[theNodeNumber][NODECOMPL]:		# Current node has not completed
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: not complete, calling doNodeIncompleteNode'
			return self.doNodeIncompleteNode(theNodeNumber)
		else:											# node is complete at the point
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: node',theNodeNumber,'is complete, calling doNodeCompleteNode'
			if (theNodeNumber == 0) and (nodeList[0][NODECOMPL]):
				return TREE_COMPLETED
			else:
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
	theNodeNumber = 0	# initial value is the first node
	NodeHandler.createSingleNodeBelowCurrentNode(theNodeNumber)
	nodeToGet = [TREE_IN_PROGRESS,0,theNodeNumber]
	InputListHandler.setCurrentFileInputOffset(0)	# initial value - gets overriden by function
	if debug_newCoreCode:
		print 'newCoreCode: starting loop'
	while True:
		nodeToGet = NodeHandler.processTree(theNodeNumber)
		if debug_newCoreCode:
			print 'newCoreCode: nodeToGet returned ',nodeToGet,
		if (nodeToGet[0] == TREE_DONE):
			if debug_newCoreCode:
				print 'tree done'
			return
		elif nodeToGet[0] == EARLY_EXIT_FOR_DEBUG:
			if debug_newCoreCode:
				print 'newCoreCode: nodeToGet returned ',nodeToGet,
				print 'newCoreCode: early exit for debugging at node',nodeToGet[1]
			return
		elif nodeToGet[0] == TREE_IN_PROGRESS:
			pass
		if debug_newCoreCode:
			NodeHandler.dumpAllNodeVals()
		theNodeNumber = nodeToGet[1]

def sumTheMetaStuff():
	accumMetaRecLens = 0
	for node in nodeList:
		startSpan = node[METAOFFST]
		endSpan = node[METAOFFST] + node[METALENGTH]
#		print startSpan,endSpan-1
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
print 'node at the end was',currentNodeNumber
NodeHandler.dumpAllNodeVals()

sumTheMetaStuff()

exit()

# 12,13,15

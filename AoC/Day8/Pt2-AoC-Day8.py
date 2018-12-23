# Pt2-AoCDay8.py
# Pt2-AoCDay8.py
# 2018 Advent of Code
# Day 8
# Part 2
# https://adventofcode.com/2018/day/8

# Implemented a Depth First Search without recursion
# https://en.wikipedia.org/wiki/Depth-first_search
#
# 7003 is not the right answer.

import time
import re
import os
"""
--- Part Two ---
The second check is slightly more complicated: you need to find the value of the root node (A in the example above).

The value of a node depends on whether it has child nodes.

If a node has no child nodes, its value is the sum of its metadata entries. 
So, the value of node B is 10+11+12=33, and the value of node D is 99.

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

input4 example solution from MJG code = 53

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
NODEVALUE = 11	# Value of the metadata at this point

defaultNode = [0,0,0,0,0,0,0,0,0,0,0,0]
defaultNodeDescr = ' Node  UP  DOWN  LEFT RIGHT  KIDS FILOF METOF METCT NDCMP  CHDN  CHIP  NVAL'

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

	def dumpTopOfNodeList(self):
		global nodeList
		print '*** Node table length =',len(nodeList),'***'
		print defaultNodeDescr
		i = 0
		for item in nodeList:
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
			if i >= 100:
				return
		return
		
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
		
		:param: node - the node vector
		:returns: no return value
		"""
		global nodeList
		global debugAllModules
		if debugAllModules:
			debug_pushNode = True
		else:
			debug_pushNode = False
		#print '.',		# print a dot for every node that gets pushed - fairly low overhead cost
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
		node = [0,0,0,0,0,0,0,0,0,0,0,0]
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
		node[RTNODENUM] = DONE			# no right hand node
		node[LFNODENUM] = DONE			# no left hand node
		node[CHANNELIP] = 1				# There's only one channel anyway
		node[NODEVALUE] = UNINIT		# Will fill in value at a later time
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
			node = [0,0,0,0,0,0,0,0,0,0,0,0]		# manual  copy of default node
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
			node[NODEVALUE] = UNINIT
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
		elif actionFlag == NEED_TO_MOVE_RIGHT:
			if debug_doMovement or routingMessagesOnly:
				print 'doMovement: Moving from node',theNodeNumber,'right to node',nodeList[theNodeNumber][RTNODENUM]
			retVal =  nodeList[theNodeNumber][RTNODENUM]
		elif actionFlag == CURRENT_POINT_DONE:
			if debug_doMovement or routingMessagesOnly:
				print 'doMovement: Staying at node',theNodeNumber
			retVal = theNodeNumber
		return retVal
		
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
		# can I move to node to the right?
		if (nodeList[theNodeNumber][RTNODENUM] >= 0):
			if debug_askForDirections:
				print 'doaskForDirections: moving right'
			return NEED_TO_MOVE_RIGHT
		# up movement is the last resort
		if debug_askForDirections:
			print 'doaskForDirections: moving up'
		return NEED_TO_MOVE_UP
		
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
		if not nodeList[theNodeNumber][NODECOMPL]:		# Current node has not completed
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: not complete, calling doNodeIncompleteNode'
			return self.doNodeIncompleteNode(theNodeNumber)
		else:											# node is complete at the point
			if debug_doAllActionsAtCurrentPoint:
				print 'doAllActionsAtCurrentPoint: node',theNodeNumber,'is complete, calling doNodeCompleteNode'
			return self.doNodeCompleteNode(theNodeNumber)
	
	def resolveNodes_NodesWithZeroChildren(self):
		"""If a node has no children set the meta sum for that node
		Otherwise, leave the node alone
		
		:returns: No return
		"""
		global nodeList
		if debugAllModules:
			debug_sumMetaDataEntries = True
		else:
			debug_sumMetaDataEntries = False
		unSolvedNodes = []
		for node in nodeList:
			if node[NUMOFKIDS] == 0:
				pointerToMetaData = node[METAOFFST]
				metaDataCount = node[METALENGTH]
				end = pointerToMetaData + metaDataCount
				if debug_sumMetaDataEntries:
					print 'resolveNodes_NodesWithZeroChildren: node has no children'
					print 'start',pointerToMetaData
					print 'count',metaDataCount
					print 'end',end
				sum = 0
				while pointerToMetaData < end:
					if debug_sumMetaDataEntries:
						print pointerToMetaData,
						print 'data value',inputList[pointerToMetaData]
					sum += inputList[pointerToMetaData]
					pointerToMetaData += 1
				node[NODEVALUE] = sum

	def resolveNodes_AllOutOfRangeKids(self):
		"""Another quick pass as resolving nodes
		If the node has no children in range then move it to a new unresolved nodes list.
		Since python is by reference even making a new list will still do the changes to the nodeList
		"""
		global nodeList
		for node in nodeList:
			if node[NODEVALUE] == UNINIT:	# See which nodes can be eliminated
				nodeMetaStart = node[METAOFFST]
				nodeMetaLength = node[METALENGTH]
				nodeChildCount = node[NUMOFKIDS]
				noNodesInRange = True
				for metaOffset in xrange(nodeMetaLength):
					metaValue = inputList[nodeMetaStart]
					if metaValue > 0 and metaValue <= nodeChildCount:
						noNodesInRange = False
				if noNodesInRange:
					node[NODEVALUE] = 0
		
	def getUninitNodeCount(self):
		"""Count the number of nodes which do have an uninitialized metadata value
		"""
		nodeCount = 0
		for node in nodeList:
			if node[NODEVALUE] == UNINIT:
				nodeCount += 1
		return nodeCount
	
	def getChildNodeNumber(self,parentNodeNumber,childOffset):
		"""Get the node number of the child that is pointed to the passed items
		
		:param parentNodeNumber:
		:param childOffset:
		:returns: node number of the child at the childOffset (numbered 1...)
		"""
		debug_getChildNodeNumber = False
		currentChildOffsetCount = 0
		childNodeNumber = nodeList[parentNodeNumber][DNNODENUM]
		if debug_getChildNodeNumber:
			print 'getChildNodeNumber: parentNodeNumber',parentNodeNumber
			print 'getChildNodeNumber: number of kids of parent',nodeList[parentNodeNumber][NUMOFKIDS]
			print 'getChildNodeNumber: childOffset',childOffset
			print 'getChildNodeNumber: first childNodeNumber',childNodeNumber
			if childOffset > nodeList[parentNodeNumber][NUMOFKIDS]:
				abbyTerminate('getChildNodeNumber: asked for a child past the child count')
		while currentChildOffsetCount < childOffset - 1:
			childNodeNumber = nodeList[childNodeNumber][RTNODENUM]
			currentChildOffsetCount+= 1
		if debug_getChildNodeNumber:
			print 'getChildNodeNumber: returning childNodeNumber',childNodeNumber
		return childNodeNumber

	
	def iterativeResolveNodes(self):
		"""Go through the list resolving as many nodes as possible
		These nodes are all nodes which have not yet been solved
		The intention is to repeately call this function until all nodes have been solved
		Next node to check could be done more intelligently but there are 500ish nodes to solve
		Tree is also not all that deep so this could go quickly - we'll see
		
		:returns: list of nodes it could not solve
		"""
		debug_iterativeResolveNodes = True
		nodeNumber = 0
		for node in nodeList:
			if node[NODEVALUE] == UNINIT:	# Only work on nodes which are unsolved
				if debug_iterativeResolveNodes:
					print '\niterativeResolveNodes: checking node number',nodeNumber
				if debug_iterativeResolveNodes:
					print 'iterativeResolveNodes: node itself has uninitialized value'
				unresolvedNodeFlag = False	# if any of the children cannot be determined (later pass will get it)
				nodeSum = 0					# sum of the values of the children pointed to by the metadata
				nodeMetaStart = node[METAOFFST]
				nodeMetaLength = node[METALENGTH]
				nodeChildCount = node[NUMOFKIDS]
				if debug_iterativeResolveNodes:
					#print 'iterativeResolveNodes: unresolvedNodeFlag',unresolvedNodeFlag
					#print 'iterativeResolveNodes: nodeSum (zero at start)',nodeSum
					print 'iterativeResolveNodes: nodeMetaStart',nodeMetaStart
					print 'iterativeResolveNodes: nodeMetaLength',nodeMetaLength
					print 'iterativeResolveNodes: nodeChildCount',nodeChildCount
				for metaOffset in xrange(nodeMetaLength):
					metaValue = inputList[nodeMetaStart+metaOffset]
					if debug_iterativeResolveNodes:
						print 'iterativeResolveNodes: nodeMetaStart+metaOffset',nodeMetaStart+metaOffset
						print 'iterativeResolveNodes: metaValue',metaValue
					if metaValue > 0 and metaValue <= nodeChildCount:
						childNodeNumber = self.getChildNodeNumber(nodeNumber,metaValue)
						if debug_iterativeResolveNodes:
							print 'iterativeResolveNodes: value is in range of children'
							print 'iterativeResolveNodes: childNodeNumber',childNodeNumber
						if nodeList[childNodeNumber][NODEVALUE] == UNINIT:
							unresolvedNodeFlag = True
							if debug_iterativeResolveNodes:
								print 'iterativeResolveNodes: node is not yet valued'
								print 'iterativeResolveNodes: unresolvedNodeFlag',unresolvedNodeFlag
								print 'iterativeResolveNodes: breaking out of the loop'
							break
						else:
							nodeSum += nodeList[childNodeNumber][NODEVALUE]
							if debug_iterativeResolveNodes:
								print 'iterativeResolveNodes: node',childNodeNumber,
								print ' is valued at',nodeList[childNodeNumber][NODEVALUE],
								print 'new sum',nodeSum
					else:
						pass
						if debug_iterativeResolveNodes:
							print 'iterativeResolveNodes: metaValue is not in range of children',metaValue
						
				if unresolvedNodeFlag == False:
					node[NODEVALUE] = nodeSum
					if debug_iterativeResolveNodes:
						print 'iterativeResolveNodes: all subnodes were resolved, sum was',nodeSum
					#os.system('pause')
			nodeNumber += 1
	
	def processPart2(self):
		""" Do Part 2
		"""
		global nodeList
		debug_processPart2 = True
		# Populate the node value (sum of meta data) for nodes with zero children
		if debug_processPart2:
			print 'processPart2: Nodes before processing =',self.getUninitNodeCount()
		self.resolveNodes_NodesWithZeroChildren()
		if debug_processPart2:
			print 'processPart2: Un-solved nodes after resolveNodes_NodesWithZeroChildren',self.getUninitNodeCount()
		self.resolveNodes_AllOutOfRangeKids()
		if debug_processPart2:
			print 'processPart2: Un-solved nodes after resolveNodes_AllOutOfRangeKids',self.getUninitNodeCount()
		self.dumpTopOfNodeList()
		while self.getUninitNodeCount() > 0:
			self.iterativeResolveNodes()
			print 'processPart2: Un-solved nodes after pass through iterativeResolveNodes =',self.getUninitNodeCount()
		if debug_processPart2:
			print 'processPart2: First node values are'
			print nodeList[0]
		#for node in nodeList:
		#	print node
		
		#os.system('pause')
		print 'reached end'
		value = 99
		return value
	
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

#print 'main: processing is done'
#print 'node at the end was',currentNodeNumber
#NodeHandler.dumpAllNodeVals()

#print 'Part 1 solution',
#sumTheMetaStuff()

print ''

valPart2 = NodeHandler.processPart2()
print '\nPart 2 value is',valPart2


exit()

# 12,13,15

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

"""


def stringOfNumbersToList(str):
	theList = []
	num = 0
	for letter in str:
		if letter >= '0' and letter <= '9':
			num = num*10 + ord(letter)-ord('0')
		else:
			theList.append(num)
			num = 0
	return theList

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
	
def pushNodeAtPoint(listOffset):
	global nodeList
	endNode = False
	currentChildCountOffset = listOffset
	currentChildCount = myList[listOffset]
	if currentChildCount == 0:
		currentMetaCountOffset = listOffset+2
		endNode = True
	else:
		currentMetaCountOffset = -1
	currentMetaCount = myList[listOffset + 1]
	newNode = [currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount]
	nodeList.append(newNode)
	print 'pushNodeAtPoint',newNode
	return endNode
	
def isNodeStored(listOffset):
	global nodeList
	currentChildCountOffset = listOffset
	currentChildCount = myList[listOffset]
	currentMetaCountOffset = listOffset + 1
	currentMetaCount = myList[listOffset + 1]
	nodeVal = [currentChildCountOffset,currentChildCount,currentMetaCountOffset,currentMetaCount]
	for nodeVal in nodeList:
		if nodeVal[0] == currentChildCountOffset and nodeVal[1] == currentChildCount and nodeVal[3] == currentMetaCount:
			#print 'isNodeStored: was already stored',nodeVal
			return True
	#print 'isNodeStored: was not stored',nodeVal
	return False

def getNode(nodeNum):
	global nodeList
	return nodeList[nodeNum]

def getNodeCount():
	global nodeList
	return len(nodeList)
	
def getChildCount(nodeNum):
	return nodeList[nodeNum][0]

def putMetaDataOffset(nodeCount,nodeOffset):
	nodeList[nodeCount][2] = nodeOffset+2

def dumpNodes():
	global nodeList
	print 'dumpNodes: length of nodes',len(nodeList)
	for node in nodeList:
		print '[chOff,chCt,metaOff,metaCount] =',
		print node
	#print 'done dumpNodes'

textList = readTextFileToList('input2.txt')
#print textList

myList = stringOfNumbersToList(textList)
#print 'main:',myList

nodeList = []

listOffset = 0
listLength = len(myList)
#print 'main: listLength',listLength

streamStates = ['qtyChildren','qtyMetadata']
streamState = 'qtyChildren'

pushNodeAtPoint(listOffset)	# prime with the first node
# print 'main: initial nodes',
# dumpNodes()

nodeOffset = 0
loopEnd = 5
setEndNode = False
storedNodeFlag = True
while storedNodeFlag:
	storedNodeFlag = False
	nodeCount = getNodeCount()
	while nodeCount > 0:
		nodeVals = getNode(nodeOffset)
		print 'main: checking node with nodeVals',nodeVals
		nodeOffset = nodeVals[0] + 2
		if not isNodeStored(nodeOffset):
			if pushNodeAtPoint(nodeOffset):
				lastNode = getNode(nodeCount)
				print 'main: pushing Node relative to end node',lastNode
				pushNodeAtPoint(lastNode[2]+lastNode[3])
			storedNodeFlag = True
		print 'main: was last node an end node?',setEndNode,'nodeCount',nodeCount,'nodeCount actual',getNodeCount()
		nodeCount -= 1
		nodeOffset = 0
	dumpNodes()

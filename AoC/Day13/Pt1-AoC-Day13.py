# Pt1-AoCDay12.py
# 2018 Advent of Code
# Day 12
# Part 1
# https://adventofcode.com/2018/day/13

import time
import re
import os

"""



"""

#####################################################################################
## Functions which operate on the input file and node lists

class InputFileHandler():

	def readTextFileLinesToList(self,fileName):
		"""readTextFileAndSrtToList - open file and read the content to a list
		File is sorted to produce a date/time ordered file
		:returns: the list sorted list
		"""
		textFile = ''
		with open(fileName, 'r') as filehandle:  
			textFile = filehandle.readlines()
		inList = []
		for row in textFile:
			inList.append(row.strip('\n\r'))
		return inList

#####################################################################################
## Functions which operate on the node list

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	exit()


def makeMapArray(theTextList):
	"""Go through the input list and make an array from the lines of textFile
	"""
	print 'makeMapArray: make an array from the text lines'
	mapArray = []
	for row in theTextList:
		rowList = list(row)
		mapArray.append(rowList)
	return mapArray
	
def padMapArray(mapArray):
	"""Pad the area around the map with spaces
	The reason for padding is that scanning the map for surrounding cells
	would be complicated if the adjacent cells were outside of the array.
	Having an array that has padding removes this complication.
	
	:param mapArray: the x,y file that is the map
	:returns: newMapArray - map array padded
	"""
	debug_padMapArray = False
	columnCount = len(mapArray[0])
	rowCount = len(mapArray)
	if debug_padMapArray:
		print 'padMapArray: columnCount',columnCount
		print 'padMapArray: rowCount',rowCount
	newMapArray = []
	endRows = []
	for column in range(columnCount+2):
		endRows.append(' ')
	newMapArray.append(endRows)
	for row in xrange(rowCount):
		newCol = []
		newCol.extend(' ')
		for column in xrange(columnCount):
			newCol.extend(mapArray[row][column])
		newCol.extend(' ')
		newMapArray.append(newCol)
	newMapArray.append(endRows)
	return newMapArray
	
	
def sortElfList(elfList):
	"""Sort the elf lists.
	"""
	print 'sortElfList: Sorting list of elves in x,y order'
	elfList = sorted(elfList, key = lambda errs: errs[1])		# sort by first column
	elfList = sorted(elfList, key = lambda errs: errs[0])		# sort by first column
	return elfList

def dumpMapList(mapList):
	"""Dump the elf list
	"""
	print 'dumpMapList:'
	columnCount = len(mapList[0])
	rowCount = len(mapList)
	for row in xrange(rowCount):
		for column in range(columnCount):
			print mapList[row][column],
		print


def determineReplacementCellValue(mineMap,x,y):
	"""Determine what the cell gets replaced with.
	The type of track depends on the surrounding cells

	Some of the examples:
	S = space
	 S  \
	-X-  > Insert a -
	 S  /
	 
	 |  \
	SXS  > Insert a -
	 |  /	
	
	 |  \
	-X-  > Insert a +
	 |  /
	 
	:returns: replacement cell value
	"""
	# Implement as a bunch of deep if statements
	lV = mineMap[x-1][y]
	rV = mineMap[x+1][y]
	uV = minedMap[x][y+1]
	dV = mineMap[x][y-1]
	SP = ' '
	ulC = '/'
	lrC = '/'
	urC = '\\'
	llC = '\\'
	
	
	return replacementCell

def makeCleanMap(mineMap):
	"""Go through the mine map and replace the elves with tracks
	Complicated by the tracks can be at the edge of the arrays
	Could pad the entire tracks with spaces - probably the easiest choice
	"""
	return mineMap

def findElves(mineMap):
	"""Go through the map and find the elves.
	
	:param mineMap: the map file
	:returns: list of [x,y,travel,nextDirection]
	"""
	debug_findElves = True
	print 'findElves'
	print mineMap
	exit()
	elfList = []
	columnCount = len(mineMap[0])
	rowCount = len(mineMap)
	for row in xrange(rowCount):
		for column in range(columnCount):
			if mineMap[row][column] == '>' or mineMap[row][column] == '<' or mineMap[row][column] == '^' or mineMap[row][column] == 'v':
				elfXY = [column,row,mineMap[row][column],'left']
				elfList.append(elfXY)
	if debug_findElves:
		print 'findElves: Number of elves',len(elfList)
		for elf in elfList:
			print elf
	return elfList

direction = ['left','straight','right']

########################################################################
## This is the workhorse of this assignment


########################################################################
## Code
## Read in the map
## Remove the elves from the map and bring them into a list
## Move in the list
## Determine action based on the updated map
## Keep a map without elves for directional choices
## May have to make an array that tracks just the elves
## Coordinate the two arrays

inFileName = 'input2.txt'

debug_main = False
print 'Reading in file',time.strftime('%X %x %Z')
InputFileClass = InputFileHandler()
textList = InputFileClass.readTextFileLinesToList(inFileName)
if debug_main:
	print '\ntextList',textList

unpaddedMineMap = makeMapArray(textList)
mineMap = padMapArray(unpaddedMineMap)
dumpMapList(mineMap)

exit()

elfList = findElves(mineMap)
print 'elfList',elfList
dumpMapList(elfList)
elfList = sortElfList(elfList)


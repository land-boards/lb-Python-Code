# Pt2-AoCDay18.py
# 2018 Advent of Code
# Day 18
# Part 2
# https://adventofcode.com/2018/day/18

import time
import re
import os

"""
--- Day 18: Settlers of The North Pole ---
On the outskirts of the North Pole base construction project, many Elves are collecting lumber.

The lumber collection area is 50 acres by 50 acres; each acre can be either open ground (.), trees (|), or a lumberyard (#). 
You take a scan of the area (your puzzle input).

Strange magic is at work here: each minute, the landscape looks entirely different. 
In exactly one minute, an open acre can fill with trees, a wooded acre can be converted to a lumberyard, 
or a lumberyard can be cleared to open ground (the lumber having been sent to other projects).

The change to each acre is based entirely on the contents of that acre as well as the number of open, 
wooded, or lumberyard acres adjacent to it at the start of each minute. Here, "adjacent" means any of the eight acres surrounding that acre. 
(Acres on the edges of the lumber collection area might have fewer than eight adjacent acres; the missing acres aren't counted.)

In particular:

An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard 
and at least one acre containing trees. Otherwise, it becomes open.
These changes happen across all acres simultaneously, each of them using the state of all acres at the beginning of the minute 
and changing to their new form by the end of that same minute. Changes that happen during the minute don't affect each other.

For example, suppose the lumber collection area is instead only 10 by 10 acres with this initial configuration:

Initial state:
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.

After 1 minute:
.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.

After 2 minutes:
.......#..
......|#..
.|.|||....
..##|||..#
..###|||#|
...#|||||.
|||||||||.
||||||||||
||||||||||
.|||||||||

After 3 minutes:
.......#..
....|||#..
.|.||||...
..###|||.#
...##|||#|
.||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 4 minutes:
.....|.#..
...||||#..
.|.#||||..
..###||||#
...###||#|
|||##|||||
||||||||||
||||||||||
||||||||||
||||||||||

After 5 minutes:
....|||#..
...||||#..
.|.##||||.
..####|||#
.|.###||#|
|||###||||
||||||||||
||||||||||
||||||||||
||||||||||

After 6 minutes:
...||||#..
...||||#..
.|.###|||.
..#.##|||#
|||#.##|#|
|||###||||
||||#|||||
||||||||||
||||||||||
||||||||||

After 7 minutes:
...||||#..
..||#|##..
.|.####||.
||#..##||#
||##.##|#|
|||####|||
|||###||||
||||||||||
||||||||||
||||||||||

After 8 minutes:
..||||##..
..|#####..
|||#####|.
||#...##|#
||##..###|
||##.###||
|||####|||
||||#|||||
||||||||||
||||||||||

After 9 minutes:
..||###...
.||#####..
||##...##.
||#....###
|##....##|
||##..###|
||######||
|||###||||
||||||||||
||||||||||

After 10 minutes:
.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||
After 10 minutes, there are 37 wooded acres and 31 lumberyards. 
Multiplying the number of wooded acres by the number of lumberyards gives the total resource value after ten minutes: 37 * 31 = 1147.

What will the total resource value of the lumber collection area be after 10 minutes?

Your puzzle answer was 560091.

The first half of this puzzle is complete! It provides one gold star: *
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
		for yValueNum in textFile:
			inList.append(yValueNum.strip('\n\r'))
		return inList
	
	def writeOutMapFile(self,mapList):
		"""writeOutMapFile - Write out the map file so that it can be read by an editor.
		The map file is too big to print in a 80 xValueNum DOS CMD window.
		newline between each line
		"""
		mapAsList = self.mapToList(mapList)
		with open('SnapMap.txt', 'w') as f:
			for item in mapAsList:
				f.write(item)
				f.write('\n')
		
	def mapToList(self,mapList):
		"""Write out the mapList to a file because it is too big to see on the screen
		"""
		debug_mapToList = False
		if debug_mapToList:
			print 'writeOutMapFile: newLine',mapList[0]
			print 'writeOutMapFile: mapList has line count',len(mapList)
		outList = []
		for line in mapList:
			newLine = ''.join(line)
			outList.append(newLine)
		if debug_mapToList:
			print 'mapToList: outList',
		return outList

#####################################################################################
## Functions which deal in general with programming tasks

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	exit()

#####################################################################################

def makeEmptyMap(theMap):
	"""Make a copy of the map without anything in it.
	"""
	yValueNumCount = len(theMap)
	xValueNumCount = len(theMap[0])
	newMap = []
	for yValueNum in xrange(yValueNumCount):
		xList = []
		for xValueNum in xrange(xValueNumCount):
			xList.append('0')
		newMap.append(xList)
	return newMap

#####################################################################################
## Functions which operate on the map list

def makeMapArray(theTextList):
	"""Go through the input list and make an array from the lines of textFile
	
	:param theTextList: The text file as a list of strings. 
	Each string is a line of the file.
	:returns: map turned into 2D list (more or less an array) 
	"""
	debug_makeMapArray = False
	if debug_makeMapArray:
		print 'makeMapArray: make an array from the text lines'
	mapArray = []
	for yValueNum in theTextList:
		yValueNumList = list(yValueNum)
		mapArray.append(yValueNumList)
	return mapArray
	
def determineNextSymbols(map):
	newMap = makeEmptyMap(map)	# copy the current map size as a new map
	xValueNumCount = len(map[0])
	yValueNumCount = len(map)
	for yValueNum in xrange(yValueNumCount):
		for xValueNum in xrange(xValueNumCount):
			if map[yValueNum][xValueNum] == '.':		# Open Ground
				if countObjectsAround('|',xValueNum,yValueNum,map) >= 3:
					newMap[yValueNum][xValueNum] = '|'
				else:
					newMap[yValueNum][xValueNum] = map[yValueNum][xValueNum]
			elif map[yValueNum][xValueNum] == '|':	# Trees
				if countObjectsAround('#',xValueNum,yValueNum,map) >= 3:
					newMap[yValueNum][xValueNum] = '#'
				else:
					newMap[yValueNum][xValueNum] = map[yValueNum][xValueNum]
			elif map[yValueNum][xValueNum] == '#':	# Lumberyard
				if countObjectsAround('#',xValueNum,yValueNum,map) >= 1 and countObjectsAround('|',xValueNum,yValueNum,map) >= 1:
					newMap[yValueNum][xValueNum] = '#'
				else:
					newMap[yValueNum][xValueNum] = '.'
	return newMap

def countObjectsAround(lookingForChar,xValueNum,yValueNum,map):
	debug_countObjectsAround = False
	charCount = 0
	if getVal(-1,-1,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if getVal(0,-1,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if getVal(1,-1,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if getVal(-1,0,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if getVal(1,0,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if getVal(-1,1,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if getVal(0,1,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if getVal(1,1,xValueNum,yValueNum,map) == lookingForChar:
		charCount += 1
	if debug_countObjectsAround:
		print 'countObjectsAround: at x y',xValueNum,yValueNum,'counted',charCount,'of char',lookingForChar
	return charCount

def getVal(xOffset,yOffset,xValueNum,yValueNum,map):
	"""getVal - Get the value of the character at a position with offset.
	
	:param xOffset:
	:param yOffset:
	:param xValueNum:
	:param yValueNum:
	:param map:	
	:returns: the character if in the map, otherwise char zero '0'
	"""
	if (xValueNum + xOffset) < 0:
		return '0'
	if (xValueNum + xOffset) > (len(map[0]) - 1):
		return '0'
	if (yValueNum + yOffset) < 0:
		return '0'
	if (yValueNum + yOffset) > (len(map[0]) - 1):
		return '0'
	return map[yValueNum+yOffset][xValueNum+xOffset]

def dumpMapList(map):
	"""Dump the elf list
	"""
	print 'dumpMapList:'
	xValueNumCount = len(map[0])
	yValueNumCount = len(map)
	for yValueNum in xrange(yValueNumCount):
		for xValueNum in range(xValueNumCount):
			print map[yValueNum][xValueNum],
		print

def valueForest(forestMap):
	numberOfTrees = 0
	numberOfLumbermills = 0
	xValueNumCount = len(forestMap[0])
	yValueNumCount = len(forestMap)
	for yValueNum in xrange(yValueNumCount):
		for xValueNum in xrange(xValueNumCount):
			if forestMap[yValueNum][xValueNum] == '|':
				numberOfTrees += 1
			elif forestMap[yValueNum][xValueNum] == '#':
				numberOfLumbermills += 1
	return numberOfTrees*numberOfLumbermills

########################################################################
## This is the workhorse of this assignment


########################################################################
## Code

inFileName = 'input.txt'

debug_main = False
print 'Reading in file',time.strftime('%X %x %Z')
InputFileClass = InputFileHandler()
textList = InputFileClass.readTextFileLinesToList(inFileName)
if debug_main:
	print '\ntextList',textList
forestMap = makeMapArray(textList)				# Get the map from the file
dumpMapList(forestMap)
loopCount = 1
while loopCount <= 10:
	print 'After',loopCount,'mins'
	newForestMap = determineNextSymbols(forestMap)
	dumpMapList(newForestMap)
	forestMap = newForestMap
	loopCount += 1
	
forestValue = valueForest(forestMap)

print 'forest value is',forestValue


print 'Finished processing',time.strftime('%X %x %Z')

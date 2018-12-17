# Pt1-AoCDay12.py
# 2018 Advent of Code
# Day 12
# Part 1
# https://adventofcode.com/2018/day/13

import time
import re
import os

"""
--- Day 13: Mine Cart Madness ---
A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be making this up as they go along. They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/
Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/
Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current location: carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |
First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart. The first cart moves down, then the second cart moves up - right into the first cart, colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/-->\        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/   

/---v        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/   

/---\        
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/   

/---\        
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/   

/---\        
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/   

/---\        
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/   

/---\        
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/   

/---\        
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/   
After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0:

           111
 0123456789012
0/---\        
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/   
In this example, the location of the first crash is 7,3.

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
	
	def writeOutMapFile(self,mapList):
		mapAsList = self.mapToList(mapList)
		
		print mapAsList

		
	def mapToList(self,mapList):
		"""Write out the mapList to a file because it is too big to see on the screen
		"""
		print 'writeOutMapFile: newLine',mapList[0]
		print 'writeOutMapFile: mapList has line count',len(mapList)
		outList = []
		for line in mapList:
			newLine = ''.join(line)
			outList.append(newLine)
		return outList

#####################################################################################
## Functions which operate on the map list

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	exit()

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
	debug_sortElfList = False
	if debug_sortElfList:
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
	debug_determineReplacementCellValue = False
	# Implement as a bunch of deep if statements
	if debug_determineReplacementCellValue:
		print '\ndetermineReplacementCellValue: x,y',x,y
		print 'determineReplacementCellValue: columns in map',len(mineMap[0])
		print 'determineReplacementCellValue: rows in map',len(mineMap)
		print 'determineReplacementCellValue: element in cell already',mineMap[y][x]
	lV = mineMap[y][x-1]
	rV = mineMap[y][x+1]
	uV = mineMap[y+1][x]
	dV = mineMap[y-1][x]
	SP = ' '
	HL = '-'
	PL = '+'
	VL = '|'
	ulC = '/'
	lrC = '/'
	urC = '\\'
	llC = '\\'
	if lV == SP and rV == SP:
		return(VL)
	elif uV == SP and dV == SP:
		return(HL)
	elif lV == HL and rV == HL and uV == VL and dV == VL:
		return('+')
	elif lV == SP and rV == VL and uV == VL and dV == VL:
		return(VL)
	elif lV == VL and rV == SP and uV == PL and dV == VL:
		return(VL)
	elif lV == VL and rV == VL and uV == PL and dV == VL:
		return(VL)
	elif lV == SP and rV == VL and uV == VL and dV == PL:
		return(VL)
	elif lV == VL and rV == VL and uV == VL and dV == VL:
		return(VL)
	elif lV == SP and rV == VL and uV == PL and dV == VL:
		return(VL)
	elif lV == VL and rV == SP and uV == ulC and dV == PL:
		return(VL)
	elif lV == HL and rV == HL and uV == HL and dV == HL:
		return(HL)
	elif lV == VL and rV == SP and uV == VL and dV == VL:
		return(VL)
	else:
		print '\ndetermineReplacementCellValue: '
		print 'lV',lV
		print 'rV',rV
		print 'uV',uV
		print 'dV',dV
		exit()

def makeCleanMap(mineMap,elfList):
	"""Go through the mine map and replace the elves with tracks
	Complicated by the tracks can be at the edge of the arrays
	Could pad the entire tracks with spaces - probably the easiest choice
	elfList has list of elements which are [x,y,currentDirection,nextDirection]
	"""
	debug_makeCleanMap = True
	newMineMap = mineMap
	for elf in elfList:
		x = elf[0]
		y = elf[1]
		newMineMap[y][x] = determineReplacementCellValue(mineMap,x,y)
	return newMineMap

def findElves(mineMap):
	"""Go through the map and find the elves.
	
	:param mineMap: the map file
	:returns: list of elves - [x,y,currentDirection,nextDirection]
	"""
	debug_findElves = False
	if debug_findElves:
		print 'findElves'
		print mineMap
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

inFileName = 'input.txt'

debug_main = False
print 'Reading in file',time.strftime('%X %x %Z')
InputFileClass = InputFileHandler()
textList = InputFileClass.readTextFileLinesToList(inFileName)
if debug_main:
	print '\ntextList',textList

unpaddedMineMap = makeMapArray(textList)
mineMap = padMapArray(unpaddedMineMap)
#dumpMapList(mineMap)

elfList = findElves(mineMap)
elfList = sortElfList(elfList)
print 'main: there are',len(elfList),'elves'
print 'main: list of elves',elfList

cleanMap = makeCleanMap(mineMap,elfList)
#dumpMapList(cleanMap)

InputFileClass.writeOutMapFile(cleanMap)
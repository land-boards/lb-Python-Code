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
A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. 
The Elves are very busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, 
the Elves seem to be making this up as they go along. They haven't even figured out how to avoid xValuelisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). 
Curves connect exactly two perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/
Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, 
turning right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/
Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). 
(On your initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, 
goes straight the second time, turns right the third time, and then repeats those directions starting again with left the fourth time, straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. 
They do this based on their current location: carts on the top yValueNum move first (acting from left to right), 
then carts on the second yValueNum move (again from left to right), then carts on the third yValueNum, and so on. 
Once each cart has moved one step, the process repeats; each of these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |
First, the top cart moves. It is facing down (v), so it moves down one square. 
Second, the bottom cart moves. It is facing up (^), so it moves up one square. 
Because all carts have moved, the first tick ends. Then, the process repeats, starting with the first cart. 
The first cart moves down, then the second cart moves up - right into the first cart, xValueliding with it! 
(The location of the crash is marked with an X.) This ends the second and last tick.

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
After following their respective paths for a while, the carts eventually crash. 
To help prevent crashes, you'd like to know the location of the first crash. 
Locations are given in X,Y coordinates, where the furthest left xValueNum is X=0 and the furthest top yValueNum is Y=0:

           111
 0123456789012
0/---\        
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/   
In this example, the location of the first crash is 7,3.

Your puzzle answer was 26,92.

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
## Functions which deal with elves

def sortElfList(elfList):
	"""Sort the elf lists.
	Is this list backwards?
	"""
	debug_sortElfList = False
	if debug_sortElfList:
		print 'sortElfList: Sorting list of elves in x,y order'
	elfList = sorted(elfList, key = lambda errs: errs[0])		# sort by first xValueNum
	elfList = sorted(elfList, key = lambda errs: errs[1])		# sort by first xValueNum
	return elfList

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
	xValueNumCount = len(mineMap[0])
	yValueNumCount = len(mineMap)
	for yValueNum in xrange(yValueNumCount):
		for xValueNum in xrange(xValueNumCount):
			if debug_findElves:
				print 'xValueNum,yValueNum',xValueNum,yValueNum
			if (mineMap[yValueNum][xValueNum] == '>') or (mineMap[yValueNum][xValueNum] == '<') or (mineMap[yValueNum][xValueNum] == '^') or (mineMap[yValueNum][xValueNum] == 'v'):
				elfXY = [xValueNum,yValueNum,mineMap[yValueNum][xValueNum],'left']
				elfList.append(elfXY)
	if debug_findElves:
		print 'findElves: Number of elves',len(elfList)
		for elf in elfList:
			print elf
	return elfList

def makeEmptyElfField(tracksMap):
	"""Make a copy of the tracksMap without tracks.
	"""
	yValueNumCount = len(tracksMap)
	xValueNumCount = len(tracksMap[0])
	elfsMap = []
	for yValueNum in xrange(yValueNumCount):
		xList = []
		for xValueNum in xrange(xValueNumCount):
			xList.append(' ')
		elfsMap.append(xList)
	return elfsMap

def putElvesIntoElfField(elfList,elfsMap):
	"""
	:param elfList: list of elves - [x,y,currentDirection,nextDirection]
	"""
	for elf in elfList:
		elfX = elf[0]
		elfY = elf[1]
		elfArrowValue = elf[2]
		elfsMap[elfY][elfX] = elfArrowValue
	return elfsMap

def moveElf(elf,tracksMap,elvesInField):
	"""Move the particular elf through the tracks map.
	
	:parm elf: The elf vector - [x,y,currentDirection,nextDirection]
	Example: [2, 0, '>', 'left']
	nextDirection moves through left,straight,right
	
	:parm tracksMap: The tracks map
	:returns: newElf vector
	"""
	debug_moveElf = False
	if debug_moveElf:
		printElfCurrentStatus(elf)
	currentElfX = elf[0]
	currentElfY = elf[1]
	currentElfArrowValue = elf[2]
	nextDirectionChange = elf[3]
	newElfList = []
	newXY = getNextXY(currentElfX,currentElfY,currentElfArrowValue)
	newX = newXY[0]
	newY= newXY[1]
	if elvesInField[newY][newX] != ' ':
		print 'moveElf: Collision will be at x y',newX,newY
		exit()
	if debug_moveElf:
		print 'moveElf: Elf moving from x y',currentElfX,currentElfY,'to x y',newX,newY
	symbolAtMovePosition = tracksMap[newY][newX]
	newArrowChar = currentElfArrowValue
	newDirection = nextDirectionChange
	if symbolAtMovePosition == '+':	# at an intersection - circles through left, straight, right
		if debug_moveElf:
			print 'moveElf: Elf is at an intersection'
		## Need to do stuff with direction
		if nextDirectionChange == 'left':
			if currentElfArrowValue == '<':
				newArrowChar = 'v'
			elif currentElfArrowValue == '>':
				newArrowChar = '^'
			elif currentElfArrowValue == 'v':
				newArrowChar = '>'
			elif currentElfArrowValue == '^':
				newArrowChar = '<'
			newDirection = 'straight'
		elif nextDirectionChange == 'right':
			if currentElfArrowValue == '<':
				newArrowChar = '^'
			elif currentElfArrowValue == '>':
				newArrowChar = 'v'
			elif currentElfArrowValue == 'v':
				newArrowChar = '<'
			elif currentElfArrowValue == '^':
				newArrowChar = '>'
			newDirection = 'left'
		elif nextDirectionChange == 'straight':
			newArrowChar = currentElfArrowValue
			newDirection = 'right'
	elif symbolAtMovePosition == ulC_val and currentElfArrowValue == '<':
		newArrowChar = 'v'
	elif symbolAtMovePosition == ulC_val and currentElfArrowValue == '^':
		newArrowChar = '>'
	elif symbolAtMovePosition == urC_val and currentElfArrowValue == '>':
		newArrowChar = 'v'
	elif symbolAtMovePosition == urC_val and currentElfArrowValue == '^':
		newArrowChar = '<'
	elif symbolAtMovePosition == lrC_val and currentElfArrowValue == 'v':
		newArrowChar = '<'
	elif symbolAtMovePosition == lrC_val and currentElfArrowValue == '>':
		newArrowChar = '^'
	elif symbolAtMovePosition == llC_val and currentElfArrowValue == '<':
		newArrowChar = '^'
	elif symbolAtMovePosition == llC_val and currentElfArrowValue == 'v':
		newArrowChar = '>'
	retVal = [newX,newY,newArrowChar,newDirection]
	if debug_moveElf:
		print 'retVal',retVal
	return retVal

def moveElves(elfList,tracksMap):
	"""moveElves
	Two options:
	Option 1 - Create an map the same size as the track map that only has elves on it.
	Move the elves in that map and look for collisions as I am going along.
	Disadvantages: Will need to keep rescanning the entire array every time to find the elves positions.
	Advantages: Don't have to keep track of the elves by position.
	Don't need to sort the elves list.
	Option 2 - Deal with elves as a modified elves list.
	If I move elves in their own elements I could do the move and then figure out
	if any two elves occupy the same location or not.
	Will need to sort the elves list after every move since their x,y positions will shift relative to each other.
	If more than two elves collide at one time
	Disadvantages: Sorting the list
	Advantages: there are a lot less elves than there are x,y positions so this should be a lot faster
	
	:param elfList: list of elves - [x,y,currentDirection,nextDirection]
	:param tracksMap: 
	
	:returns: True if move results in a collision
	"""
	debug_moveElves = False
	if debug_moveElves:
		print 'moveElves: Move the elves and look for collisions'
	collided = False
	while not collided:
		elfList = sortElfList(elfList)
		emptyElfField = makeEmptyElfField(tracksMap)
		elvesInField = putElvesIntoElfField(elfList,emptyElfField)
		newElfList = []
		for elf in elfList:
			elfList = moveElf(elf,tracksMap,elvesInField)
			if debug_moveElves:
				print 'moveElves: made it back from moveElf function'
			newElfList.append(elfList)
			if newElfList == []:
				abbyTerminate('moveElves: moveElf Returned empty list')
		if debug_moveElves:
			print 'moveElves: newElfList',newElfList
		elfList = newElfList
		drawElvesInMap(elfList,tracksMap)
		# os.system('pause')
		# os.system('cls')
	
def drawElvesInMap(elfList,traks):
	"""drawElvesInMap
	
	:param elfList: list of elves - [x,y,currentDire ction,nextDirection]
	:param traks: 
	"""
	debug_drawElvesInMap = False
	newMap = map(list, traks)	# 2D list copy that really does a copy
	for elf in elfList:
		x = elf[0]
		y = elf[1]
		newMap[elf[1]][elf[0]] = elf[2]
	if debug_drawElvesInMap:
		dumpMapList(newMap)
	return

def printElfCurrentStatus(elf):
	currentElfX = elf[0]
	currentElfY = elf[1]
	print 'moveElf: elf at x y',currentElfX,currentElfY,'is moving',
	currentElfArrowValue = elf[2]
	if currentElfArrowValue == '>':
		print 'right',
	elif currentElfArrowValue == 'v':
		print 'down',
	elif currentElfArrowValue == '<':
		print 'left',
	elif currentElfArrowValue == '^':
		print 'up',
	nextDirectionChange = elf[3]
	print 'move at next intersection will be',nextDirectionChange
	print 'moveElf: map at x y',currentElfX,currentElfY,'is',tracksMap[currentElfY][currentElfX]
	return
	
def getNextXY(x,y,currentElfArrowValue):
	"""Given an x,y location and a movement direction, return the next x,y value.
	Note that the assumption is that the elf is always pointing in the right direction.
	If the previous move of the elf was to an intersection the direction was already updated.
	"""
	nextX = 0
	nextY = 0
	if currentElfArrowValue == '>':
		nextX = x + 1
		nextY = y + 0
	elif currentElfArrowValue == 'v':
		nextX = x + 0
		nextY = y + 1
	elif currentElfArrowValue == '<':
		nextX = x - 1
		nextY = y + 0
	elif currentElfArrowValue == '^':
		nextX = x + 0
		nextY = y - 1	
	return [nextX,nextY]
	
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
	
def unPadMapArray(mapArray):
	"""unPadMapArray - the function padMapArray added spaces around the array
	This function removes the spaces from around the array.
	"""
	debug_unPadMapArray = False
	xValueNumCount = len(mapArray[0])
	yValueNumCount = len(mapArray)
	if debug_unPadMapArray:
		print 'unPadMapArray: xValueNumCount',xValueNumCount
		print 'unPadMapArray: yValueNumCount',yValueNumCount
	newMapArray = []
	for row in mapArray[1:-1]:
		newXValue = row[1:-1]
		newMapArray.append(newXValue)
	return newMapArray
	
def padMapArray(mapArray):
	"""Pad the area around the map with spaces
	The reason for padding is that scanning the map for surrounding cells
	would be complicated if the adjacent cells were outside of the array.
	Having an array that has padding removes this complication.
	
	:param mapArray: the x,y file that is the map
	:returns: newMapArray - map array padded
	"""
	debug_padMapArray = False
	xValueNumCount = len(mapArray[0])
	yValueNumCount = len(mapArray)
	if debug_padMapArray:
		print 'padMapArray: xValueNumCount',xValueNumCount
		print 'padMapArray: yValueNumCount',yValueNumCount
	newMapArray = []
	endRows = []
	for xValueNum in range(xValueNumCount+2):
		endRows.append(' ')
	newMapArray.append(endRows)
	for yValueNum in xrange(yValueNumCount):
		newXValue = []
		newXValue.extend(' ')
		for xValueNum in xrange(xValueNumCount):
			newXValue.extend(mapArray[yValueNum][xValueNum])
		newXValue.extend(' ')
		newMapArray.append(newXValue)
	newMapArray.append(endRows)
	return newMapArray
	
def dumpMapList(map):
	"""Dump the elf list
	"""
	print 'dumpMapList:'
	xValueNumCount = len(map[0])
	yValueNumCount = len(map)
	for yValueNumNum in xrange(yValueNumCount):
		for xValueNum in range(xValueNumCount):
			print map[yValueNumNum][xValueNum],
		print

def determineReplacementCellValue(mineMap,x,y):
	"""Determine what the cell gets replaced with.
	Problem states a simplifying assumption:
	'On your initial map, the track under each cart is a straight path matching the direction the cart is facing'
	Interpret 'under' as the next piece of track adjacent to the current direction.
	Should verify this assumption.
	:returns: replacement cell value
	"""
	debug_determineReplacementCellValue = False
	directionSymbol = mineMap[y][x]
	newSymbol = ''
	if debug_determineReplacementCellValue:
		print '\ndetermineReplacementCellValue: x,y',x,y
		print 'determineReplacementCellValue: xValueNums in map',len(mineMap[0])
		print 'determineReplacementCellValue: yValueNums in map',len(mineMap)
		print 'determineReplacementCellValue: element in cell before replacement',mineMap[y][x]
	if directionSymbol == '>':
		newSymbol = '-'
	elif directionSymbol == 'v':
		newSymbol = '|'
	elif directionSymbol == '<':
		newSymbol = '-'
	elif directionSymbol == '^':
		newSymbol = '|'
	else:
		if debug_determineReplacementCellValue:
			print '\ndetermineReplacementCellValue: Unexpected symbol'
	if debug_determineReplacementCellValue:
		print 'determineReplacementCellValue: New symbol is',newSymbol
	return newSymbol
	
def replaceElvesWithTrack(mineMap,elfList):
	"""Go through the mine map and replace the elves with tracks
	Complicated by the tracks can be at the edge of the arrays
	Could pad the entire tracks with spaces - probably the easiest choice
	elfList has list of elements which are [x,y,currentDirection,nextDirection]
	"""
	debug_replaceElvesWithTrack = False
	if debug_replaceElvesWithTrack:
		print 'replaceElvesWithTrack: reached function'
	newMineMap = mineMap
	for elf in elfList:
		x = elf[0]
		y = elf[1]
		newMineMap[y][x] = determineReplacementCellValue(mineMap,x,y)
	return newMineMap

ulC_val = '0'
urC_val = '1'
lrC_val = '2'
llC_val = '3'
	
def figureOutCorners(mineMap):
	"""The mine map has corners which make sense visually but don't actually correspond to directions.
	This will be a challenge when a corner is reached to determine which direction the track goes in.
	It could be possible to calculate that when navigating the maze but it would be easier to replace
	the corners with a different symbol depending on which direction the corner is going.
	Replace the two symbols for the four corner types with enumerated numbers.
	/---\ >	0---1
	|   | 	|   |
	|   |	|   |
	\---/	3---2
	
	:param: mineMap - The original mine map 
	:returns: newMineMap - with corners transformed into numbers
	"""
	debug_figureOutCorners = False
	newMap = []
	for yValueNumNum in range(len(mineMap)):
		newRow = []
		for xValueNum in range(len(mineMap[0])):
			if debug_figureOutCorners:
				oldVal = mineMap[yValueNumNum][xValueNum]
			if mineMap[yValueNumNum][xValueNum] == '/':
				if (mineMap[yValueNumNum+1][xValueNum] == '|' or mineMap[yValueNumNum+1][xValueNum] == '+') and (mineMap[yValueNumNum][xValueNum+1] == '-' or mineMap[yValueNumNum][xValueNum+1] == '+'):
					mineMap[yValueNumNum][xValueNum] = ulC_val
				elif (mineMap[yValueNumNum-1][xValueNum] == '|' or mineMap[yValueNumNum-1][xValueNum] == '+') and (mineMap[yValueNumNum][xValueNum-1] == '-' or mineMap[yValueNumNum][xValueNum-1] == '+'):
					mineMap[yValueNumNum][xValueNum] = lrC_val
				else:
					print 'figureOutCorners: stuck at',mineMap[yValueNumNum][xValueNum]
					print 'mineMap[yValueNumNum-1][xValueNum]',mineMap[yValueNumNum-1][xValueNum]
					print 'mineMap[yValueNumNum+1][xValueNum]',mineMap[yValueNumNum+1][xValueNum]
					print 'mineMap[yValueNumNum][xValueNum-1]',mineMap[yValueNumNum][xValueNum-1]
					print 'mineMap[yValueNumNum][xValueNum+1]',mineMap[yValueNumNum][xValueNum+1]
					abbyTerminate('figureOutCorners - Fell through / case') 
				if debug_figureOutCorners:
					print 'figureOutCorners: replaced',oldVal,'at x,y',xValueNum,yValueNumNum,'with',mineMap[yValueNumNum][xValueNum]
			elif mineMap[yValueNumNum][xValueNum] == '\\':
				if (mineMap[yValueNumNum-1][xValueNum] == '|' or mineMap[yValueNumNum-1][xValueNum] == '+') and (mineMap[yValueNumNum][xValueNum+1] == '-' or mineMap[yValueNumNum][xValueNum+1] == '+'):
					mineMap[yValueNumNum][xValueNum] = llC_val
				elif (mineMap[yValueNumNum+1][xValueNum] == '|' or mineMap[yValueNumNum+1][xValueNum] == '+') and (mineMap[yValueNumNum][xValueNum-1] == '-' or mineMap[yValueNumNum][xValueNum-1] == '+'):
					mineMap[yValueNumNum][xValueNum] = urC_val
				else:
					print 'figureOutCorners: stuck at',mineMap[yValueNumNum][xValueNum]
					print 'mineMap[yValueNumNum-1][xValueNum]',mineMap[yValueNumNum-1][xValueNum]
					print 'mineMap[yValueNumNum+1][xValueNum]',mineMap[yValueNumNum+1][xValueNum]
					print 'mineMap[yValueNumNum][xValueNum-1]',mineMap[yValueNumNum][xValueNum-1]
					print 'mineMap[yValueNumNum][xValueNum+1]',mineMap[yValueNumNum][xValueNum+1]
					abbyTerminate('figureOutCorners - Fell through \\ case') 
				if debug_figureOutCorners:
					print 'figureOutCorners: replaced',oldVal,'at x,y',xValueNum,yValueNumNum,'with',mineMap[yValueNumNum][xValueNum]
			newRow.append(mineMap[yValueNumNum][xValueNum])
		newMap.append(newRow)
	return newMap
			
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
unpaddedMineMap = makeMapArray(textList)				# Get the map from the file
elfList = findElves(unpaddedMineMap)					# Find the elves on the map
elfList = sortElfList(elfList)							# Sort the elves in 'reading' order
if debug_main:
	print 'main: there are',len(elfList),'elves'
	print 'main: list of elves',elfList
mapWithoutElves = replaceElvesWithTrack(unpaddedMineMap,elfList)	# Remove the elves from the map
paddedMap = padMapArray(mapWithoutElves)				# Pad the map with spaces all around
cornersFixedMap = figureOutCorners(paddedMap)			# Replace corners with corner numbers
tracksMap = unPadMapArray(cornersFixedMap)				# Unpad the map
InputFileClass.writeOutMapFile(tracksMap)				# Write out the new map
if debug_main:
	dumpMapList(mapWithoutElves)
moveElves(elfList,tracksMap)
print 'Finished processing',time.strftime('%X %x %Z')

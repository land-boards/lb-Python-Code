# Pt2-AoCDay13.py
# 2018 Advent of Code
# Day 13
# Part 2
# https://adventofcode.com/2018/day/13

## TODO
## Tried case with three elves all 1 away from each other.
## Only 2 should be cleared not all three.
## Problem happens in moveElves since it does the move and then checks to see which elves collided after the move
## If three elves collide it removes all three not just the first two that collided.
## Can't check the move that way. Need to check as I go along.
## Trouble is removing nodes from the list breaks the loop.
## Alternate is to use a loop counter and increment by two if there are two removed but the two may not be near.
## Need to move the elves within an array and do the checking in the array.
## Will need functions to operate on the array instead of the elvesList,


import time
import re
import os

"""
--- Part Two ---
There isn't much you can do to prevent crashes in this ridiculous system. 
However, by predicting the crashes, the Elves know where to be in advance 
and instantly remove the two crashing carts the moment any crash occurs.

They can proceed like this for a while, but eventually, they're going to run out of carts. 
It could be useful to figure out where the last cart that hasn't crashed will end up.

For example:

/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\  
|   |  
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\  
|   |  
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\  
|   |  
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/
After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.

What is the location of the last cart at the end of the first tick where it is the only cart left?

That's not the right answer. 
If you're stuck, there are some general tips on the about page, or you can ask for hints on the subreddit. 
Please wait one minute before trying again. (You guessed 125,37.)

"""

#####################################################################################
## Functions which operate on the input file and node lists

class InputFileHandler():
	"""Class which contains the methods to handle reading and writing files.
	"""
	
	def readTextFileLinesToList(self,fileName):
		"""readTextFileLinesToList - open file and read the content to a list
		First read in the file into a text file.
		Then turn the lines of the text file into a list of lines of the text file
		:returns: the list
		"""
		debug_readTextFileLinesToList = False
		textFile = ''
		with open(fileName, 'r') as filehandle:  
			textFile = filehandle.readlines()
		inList = []
		if debug_readTextFileLinesToList:
			print 'readTextFileLinesToList: the input text file contents by rows'
		for row in textFile:
			inList.append(row.strip('\n\r'))
			if debug_readTextFileLinesToList:
				print row.strip('\n\r')
		return inList
	
	def writeOutMapFile(self,mapList):
		"""writeOutMapFile - Write out the map file so that it can be read by an editor.
		The map file is too big to print in a 80 xValueNum DOS CMD window.
		newline between each line.
		Stores result into the directory that the program was in.
		Stores result as name 'SnapMap.txt'.
		
		:returns: no return value
		"""
		debug_writeOutMapFile = False
		mapAsList = self.mapToList(mapList)
		with open('SnapMap.txt', 'w') as f:
			for item in mapAsList:
				if debug_writeOutMapFile:
					print 'item'
				f.write(item)
				f.write('\n')
		
	def mapToList(self,mapList):
		"""Write out the mapList to a file because it is too big to see on the screen
		"""
		debug_mapToList = False
		if debug_mapToList:
			print 'mapToList: newLine',mapList[0]
			print 'mapToList: mapList has line count',len(mapList)
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

def runElves(elvesList,tracksMap,elfArrayAsList):
	"""runElves - Takes the elves through their paces.
	
	:param elvesList: the original elves list
	:param tracksMap: field of tracks without elves
	"""
	debug_runElves = False
	while len(elvesList) > 1:
		elfArrayAsList = clearElvesMap(elfArrayAsList)						# Set the elves positions to uninitialized
		for elf in elvesList:
			newElfPosition = getNextElfPosition(elf,tracksMap)
			elfNumber = elf[0]
			newElfX = newElfPosition[1]
			newElfY = newElfPosition[2]
			if elfArrayAsList[newElfY][newElfX] == -1:		# There is no elf there yet
				elfArrayAsList[newElfY][newElfX] = elfNumber
				if debug_runElves:
					print 'runElves: There was no elf there so placing elf into array'
			else:											
				elfArrayAsList[newElfY][newElfX] = -1		# Remove the conflicting elf
				if debug_runElves:
					print 'runElves: Elf conflict - removing both elves'
		elvesList = getElvesFromMap(elvesList,elfArrayAsList)
		elvesList = sortElfList(elvesList)					# need a sorted list to get the reading order to work (maybe reading order doesn't matter in Part 2)
		if debug_runElves:
			os.system('pause')
			os.system('cls')
	return elvesList
	
def getElvesFromMap(elvesList,elfArrayAsList):
	"""getElvesFromMap - Go through the elfArrayAsList and get the elf in each cell
	Put the elves found into a new elvesList
	
	:param elvesList: List of all of the elves
	:param elfArrayAsList: The array that the elves were placed into
	:returns: newElvesList which has 
	"""
	debug_getElvesFromMap = True
	newElvesList = []
	for yVal in elfArrayAsList:
		for xVal in yVal:
			if elfArrayAsList[yVal][xVal] != -1:	# Found an elf
				if debug_getElvesFromMap:
					print 'getElvesFromMap: found elf at',xVal,yVal
				elfNumberInMap = elfArrayAsList[yVal][xVal]
				elfVector = findElfNumberInElvesList(elfNumberInMap,elvesList)
				newElvesList.append(elfVector)
	if debug_getElvesFromMap:
		print 'getElvesFromMap: newElvesList',newElvesList
	return newElvesList

def getNextElfPosition(elf,tracksMap):
	"""Move the particular elf through the tracks map.
	
	:parm elf: The elf vector - [elfNumber,x,y,currentDirection,nextDirection]
	Example: [2, 0, '>', 'left']
	nextDirection moves through left,straight,right
	
	:parm tracksMap: The tracks map
	:returns: newElf vector - [x,y,currentDirection,nextDirection]
	x,y is the new position of the elf
	currentDirection is the arrow character after the resulting movement.
	"""
	debug_getNextElfPosition = False
	if debug_getNextElfPosition:
		print 'getNextElfPosition: elf',elf
		printElfCurrentStatus(elf,tracksMap)
	currentElfNumber = elf[0]
	currentElfX = elf[1]
	currentElfY = elf[2]
	currentElfArrowValue = elf[3]
	nextDirectionChange = elf[4]
	newElfList = []
	newXY = getNextXY(currentElfX,currentElfY,currentElfArrowValue)
	newX = newXY[0]
	newY= newXY[1]
	if debug_getNextElfPosition:
		print 'getNextElfPosition: Elf moving from x y',currentElfX,currentElfY,'to x y',newX,newY
	symbolAtMovePosition = tracksMap[newY][newX]
	newArrowChar = currentElfArrowValue
	newDirection = nextDirectionChange
	if symbolAtMovePosition == '+':
		if debug_getNextElfPosition:
			print 'getNextElfPosition: Elf is at an intersection'
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
	retVal = [currentElfNumber,newX,newY,newArrowChar,newDirection]
	if debug_getNextElfPosition:
		print 'getNextElfPosition: retVal',retVal
	return retVal

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
	
def sortElfList(elvesList):
	"""Sort the elf lists.
	Is this list backwards?
	"""
	debug_sortElfList = False
	if debug_sortElfList:
		print 'sortElfList: Sorting list of elves in x,y order'
	elvesList = sorted(elvesList, key = lambda errs: errs[1])		# sort by first xValueNum
	elvesList = sorted(elvesList, key = lambda errs: errs[2])		# sort by first xValueNum
	return elvesList

def findElves(mineMap):
	"""Go through the map and find the elves.
	
	:param mineMap: the map file
	:returns: list of elves - [elfNumber,x,y,currentDirection,nextDirection]
	"""
	debug_findElves = False
	if debug_findElves:
		print 'findElves'
		print 'mineMap',mineMap
	elvesList = []
	elfNumber = 0
	for yValueNum in xrange(len(mineMap)):
		for xValueNum in xrange(len(mineMap[0])):
			if (mineMap[yValueNum][xValueNum] == '>') or (mineMap[yValueNum][xValueNum] == '<') or (mineMap[yValueNum][xValueNum] == '^') or (mineMap[yValueNum][xValueNum] == 'v'):
				elfXY = [elfNumber,xValueNum,yValueNum,mineMap[yValueNum][xValueNum],'left']
				elvesList.append(elfXY)
				if debug_findElves:
					print 'findElves: found new elf',elfNumber,'at xValueNum,yValueNum',xValueNum,yValueNum,'char',mineMap[yValueNum][xValueNum]
				elfNumber += 1
	if debug_findElves:
		print 'findElves: Number of elves',len(elvesList)
		for elf in elvesList:
			print elf
	return elvesList
	
def clearElvesMap(elfArrayAsList):
	"""clearElvesMap - Clear the elves list
	
	:param elfArrayAsList: The array that the elves get placed into.
	:return: nothing
	"""
	print 'elfArrayAsList',elfArrayAsList
	for yVal in xrange(len(elfArrayAsList)):		# clear out the elfArrayAsList to empty
		for xVal in xrange(len(elfArrayAsList[0])):
			#print 'x y',xVal,yVal
			elfArrayAsList[yVal][xVal] = -1
	return elfArrayAsList

def printElfCurrentStatus(elf,tracksMap):
	"""Elf vector is [elfNumber,x,y,currentDirection,nextDirection]
	"""
	currentElfX = elf[1]
	currentElfY = elf[2]
	debug_printElfCurrentStatus = False
	if debug_printElfCurrentStatus:
		print 'printElfCurrentStatus getNextElfPosition passed elf at x y',currentElfX,currentElfY,'is moving',
	currentElfArrowValue = elf[3]
	if debug_printElfCurrentStatus:
		if currentElfArrowValue == '>':
			print 'right,',
		elif currentElfArrowValue == 'v':
			print 'down,',
		elif currentElfArrowValue == '<':
			print 'left,',
		elif currentElfArrowValue == '^':
			print 'up,',
	nextDirectionChange = elf[4]
	if debug_printElfCurrentStatus:
		print 'turn at next intersection will be',nextDirectionChange
		print 'printElfCurrentStatus: map value at x y',currentElfX,currentElfY,'is',tracksMap[currentElfY][currentElfX]
	return
	
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
	
def makeElfArray(unpaddedMineMap):
	"""Make an empty map for the elves that is the same size as the map
	
	:param unpaddedMineMap: The unpadded version of the map (used for sizing)
	:returns: 2D list the same size as the map
	"""
	debug_makeMapArray = False
	if debug_makeMapArray:
		print 'makeMapArray: make an array from the text lines'
	mapArray = []
	for yVal in xrange(len(unpaddedMineMap)):
		mapRow = []
		for xVal in xrange(len(unpaddedMineMap[0])):
			mapRow.append(-1)
		mapArray.append(mapRow)
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
			if map[yValueNumNum][xValueNum] == '0':
				print '/',
			elif map[yValueNumNum][xValueNum] == '1':
				print '\\',
			elif map[yValueNumNum][xValueNum] == '2':
				print '/',
			elif map[yValueNumNum][xValueNum] == '3':
				print '\\',
			else:
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
	
def replaceElvesWithTrack(mineMap,elvesList):
	"""Go through the mine map and replace the elves with tracks
	Complicated by the tracks can be at the edge of the arrays
	Could pad the entire tracks with spaces - probably the easiest choice
	elvesList has list of elements which are [x,y,currentDirection,nextDirection]
	"""
	debug_replaceElvesWithTrack = False
	if debug_replaceElvesWithTrack:
		print 'replaceElvesWithTrack: reached function'
	newMineMap = mineMap
	for elf in elvesList:
		x = elf[1]
		y = elf[2]
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

#inFileName = 'input.txt'
#inFileName = 'input_Part2_Example.txt'
#inFileName = 'input_1Elf_3Tracks.txt'
#inFileName = 'input_2Elves_1Track.txt'
#inFileName = 'input_3Elves_4Tracks.txt'
inFileName = 'input_3Elves_1 Corner.txt'

debug_main = True
print 'Reading in file',time.strftime('%X %x %Z')
InputFileClass = InputFileHandler()
textList = InputFileClass.readTextFileLinesToList(inFileName)
# if debug_main:
	# print 'main: input file as a textList'
	# print textList
unpaddedMineMap = makeMapArray(textList)				# Get the map from the file
print 'unPadMapArray',unpaddedMineMap
elfArrayAsList = makeElfArray(unpaddedMineMap)					# Make an array for the elves to populate
elvesList = findElves(unpaddedMineMap)					# Find the elves on the map
if debug_main:
	print 'main: elvesList before sort',elvesList
elvesList = sortElfList(elvesList)						# Sort the elves in 'reading' order
if debug_main:
	print 'main: sorted elvesList',elvesList
	print 'main: there are',len(elvesList),'elves'
mapWithoutElves = replaceElvesWithTrack(unpaddedMineMap,elvesList)	# Remove the elves from the map
paddedMap = padMapArray(mapWithoutElves)				# Pad the map with spaces all around
cornersFixedMap = figureOutCorners(paddedMap)			# Replace corners with corner numbers
tracksMap = unPadMapArray(cornersFixedMap)				# Unpad the map
InputFileClass.writeOutMapFile(tracksMap)				# Write out the new map
if debug_main:
	dumpMapList(mapWithoutElves)
lastElf = runElves(elvesList,tracksMap,elfArrayAsList)
print 'Finished processing',time.strftime('%X %x %Z')

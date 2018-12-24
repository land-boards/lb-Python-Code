# Pt2-AoCDay13.py
# 2018 Advent of Code
# Day 13
# Part 2
# https://adventofcode.com/2018/day/13

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

	def readTextFileLinesToList(self,fileName):
		"""readTextFileAndSrtToList - open file and read the content to a list
		:returns: the list
		"""
		textFile = ''
		with open(fileName, 'r') as filehandle:  
			textFile = filehandle.readlines()
		inList = []
		for row in textFile:
			inList.append(row.strip('\n\r'))
		return inList
	
	def writeOutMapFile(self,mapList):
		"""writeOutMapFile - Write out the map file so that it can be read by an editor.
		The map file is too big to print in a 80 xValueNum DOS CMD window.
		newline between each line
		"""
		debug_writeOutMapFile = False
		if debug_writeOutMapFile:
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

def runElves(elvesList,tracksMap):
	"""runElves - takes the elves through their paces.
	
	:param elvesList: the original elves list
	:param tracksMap: field of tracks without elves
	"""
	debug_runElves = False
	# print 'runElves: elvesList'
	# for elf in elvesList:
		# print elf
	if debug_runElves:
		drawElvesInMap(elvesList,tracksMap)
	while len(elvesList) > 1:
		if debug_runElves:
			print 'runElves: running the',len(elvesList),'Elves through their paces before'
			for elf in elvesList:
				print elf
		elvesList = sortElfList(elvesList)					# need a sorted list to get the reading order to work (maybe reading order doesn't matter in Part 2)
		newElvesList = moveElves(elvesList,tracksMap)
		removeElvesList = compareNewVsOldElvesList(elvesList,newElvesList)
		elvesList = removeTheElves(removeElvesList,newElvesList)
		if len(elvesList) == 1:
			print '\n*****\nrunElves: Reached the last elf number',elvesList[0][0],'at x y',elvesList[0][1],elvesList[0][2],'\n*****\n'
			if debug_runElves:
				drawElvesInMap(elvesList,tracksMap)
				exit()
		if len(elvesList) == 0:
			print '\n*****\nrunElves: Last two elves collided - there are no surviving elves'
			if debug_runElves:
				drawElvesInMap(elvesList,tracksMap)
				exit()
		if debug_runElves:
			os.system('pause')
			os.system('cls')
			drawElvesInMap(elvesList,tracksMap)
		
def removeTheElves(removeElvesList,newElvesList):
	"""removeTheElves(removeElvesList,newElvesList)
	
	:parm removeElvesList: list of elves IDs which need to be removed
	:parm newElvesList: The list of elves
	"""
	debug_removeTheElves = True
	repairedElvesList = []
	if removeElvesList == []:	# Shortcut return if there are no removals
		return newElvesList		
	else:
		pass
		if debug_removeTheElves:
			print 'removeTheElves: removing these elf numbers',removeElvesList
	for elf in newElvesList:
		if elf[0] not in removeElvesList:
			repairedElvesList.append(elf)
	if debug_removeTheElves:
		print 'removeTheElves: remaining elves are'
		for elf in repairedElvesList:
			print elf
	return repairedElvesList

def compareNewVsOldElvesList(oldElvesList,newElvesList):
	"""compareNewVsOldElvesList(oldElvesList,newElvesList)
	"""
	debug_compareNewVsOldElvesList = True
	removeElfList = []
	for oldElf in oldElvesList:
		for newElf in newElvesList:
			if oldElf[0] != newElf[0]:
				if oldElf[1] == newElf[1] and oldElf[2] == newElf[2]:
					if oldElf[0] not in removeElfList:
						removeElfList.append(oldElf[0])
					if newElf[0] not in removeElfList:
						removeElfList.append(newElf[0])
					if debug_compareNewVsOldElvesList:
						print 'compareNewVsOldElvesList: removing old elf',oldElf[0],'and new elf',newElf[0]
	newElfCount = len(newElvesList)
	elfCount = 0
	while elfCount < newElfCount:
		nextElfCount = elfCount + 1
		while nextElfCount < newElfCount:
			if newElvesList[elfCount][1] == newElvesList[nextElfCount][1] and newElvesList[elfCount][2] == newElvesList[nextElfCount][2]:
				if newElvesList[elfCount][0] not in removeElfList:
					removeElfList.append(newElvesList[elfCount][0])
				if newElvesList[nextElfCount][0] not in removeElfList:
					removeElfList.append(newElvesList[nextElfCount][0])
				if debug_compareNewVsOldElvesList:
					print 'compareNewVsOldElvesList: removing elves',newElvesList[elfCount][0],'and',newElvesList[nextElfCount][0],'from new elves list'
			nextElfCount += 1
		elfCount += 1
	if debug_compareNewVsOldElvesList:
		if removeElfList != []:
			print 'compareNewVsOldElvesList: removeElfList',removeElfList
	return removeElfList

def moveElves(elvesList,tracksMap):
	"""moveElves - Go through the elves in the elf list and move each of them one at a time.
	Returns a list of elves which had collisions in the move.
	
	:param elvesList: list of elves - [elfNumber,x,y,currentDirection,nextDirection]
	:param tracksMap: 
	:returns: List of elf numbers for collided elves
	"""
	debug_moveElves = False
	elfCollisionList = []
	if debug_moveElves:
		print 'moveElves: reached function'
	for elf in elvesList:		# go through each of the elves
		if elf[0] not in elfCollisionList;
			newElfValue = moveElf(elf,tracksMap)
			collisionsOnPass = checkElfValueInElfList(newElfValue,elvesList,elfCollisionList)
			if collisionsOnPass != []:
				print 'elves collided',checkVal
				elfCollisionList.append(collisionsOnPass[0],collisionsOnPass[1])
	if not newElfList:
		abbyTerminate('moveElves: moveElf Returned empty list')
	if debug_moveElves:
		print ''
		os.system('pause')
		#os.system('cls')
		print 'moveElves: the new elves list after the move',newElfList
	return newElfList
	
def checkElfValueInElfList(elfIn,elfList,elfCollisionList):
	elfNumber = elfIn[0]
	for elf in elfList:
		if elfNumber != elf[0]:
			if elf not in elfCollisionList:
				if elfNumber[1] == elfIn[1] and elfNumber[2] == elfIn[2]:
					# collision at this point
					print 'elves collided',elfNumber[0],elf[0]
					return [elfNumber[0], elf[0]]


def moveElf(elf,tracksMap):
	"""Move the particular elf through the tracks map.
	
	:parm elf: The elf vector - [elfNumber,x,y,currentDirection,nextDirection]
	Example: [2, 0, '>', 'left']
	nextDirection moves through left,straight,right
	
	:parm tracksMap: The tracks map
	:returns: newElf vector - [x,y,currentDirection,nextDirection]
	x,y is the new position of the elf
	currentDirection is the arrow character after the resulting movement.
	"""
	debug_moveElf = False
	if debug_moveElf:
		print 'moveElf: elf',elf
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
	if debug_moveElf:
		print 'moveElf: Elf moving from x y',currentElfX,currentElfY,'to x y',newX,newY
	symbolAtMovePosition = tracksMap[newY][newX]
	newArrowChar = currentElfArrowValue
	newDirection = nextDirectionChange
	if symbolAtMovePosition == '+':
		if debug_moveElf:
			print 'moveElf: Elf is at an intersection'
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
	if debug_moveElf:
		print 'moveElf: retVal',retVal
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

def makeEmptyElfField(tracksMap):
	"""Make a copy of the tracksMap without tracks.
	"""
	yValueNumCount = len(tracksMap)
	xValueNumCount = len(tracksMap[0])
	elfsMap = []
	print 'makeEmptyElfField: Making an empty Elf Field'
	for yValueNum in xrange(yValueNumCount):
		xList = []
		for xValueNum in xrange(xValueNumCount):
			xList.append(' ')
		elfsMap.append(xList)
	return elfsMap

def putElvesIntoElfField(elvesList,elfsMap):
	"""
	:param elvesList: list of elves - [x,y,currentDirection,nextDirection]
	"""
	for elf in elvesList:
		elfX = elf[1]
		elfY = elf[2]
		elfArrowValue = elf[3]
		elfsMap[elfY][elfX] = elfArrowValue
	return elfsMap

def getOtherElfAtLocation(elfVal,elvesList):
	"""Remove two elves at a particular point.
	The elf that was passed is the elf that caused the collision
	Look for the elf that it collided with and return that elf value
	The other elf should be at the same location as the current elf
	"""
	debug_getOtherElfAtLocation = True
	if debug_getOtherElfAtLocation:
		print 'elfVal',elfVal
	myElfNumber = elfVal[0]
	myElfX = elfVal[1]
	myElfY = elfVal[2]
	for elf in elvesList:
		if myElfNumber != elf[0]:	# always need to ignore yourself
			if myElfX == elf[1] and myElfY == elf[2]:
				return elf
	abbyTerminate('not sure why but the colliding elf was not located')

def checkCollisions(elvesList):
	"""checkCollisions - Check the elves list to see if any two elves are at the same position
	If the elves are at the same position then remove them from the list of elves.
	
	"""
	collidedElves = []
	numberOfElves = len(elvesList)-1
	debug_checkCollisions = False
	if debug_checkCollisions:
		print 'checkCollisions: checking elves',numberOfElves
	for i in xrange(numberOfElves):
		if (elvesList[i][0] == elvesList[i+1][0]) and (elvesList[i][1] == elvesList[i+1][1]):
			#if debug_checkCollisions:
			print 'checkCollisions: elves collided at x y',elvesList[i][0],elvesList[i][1]
			if elvesList[i] not in collidedElves:
				collidedElves.append(elvesList[i])
			if elvesList[i+1] not in collidedElves:
				collidedElves.append(elvesList[i+1])
			if debug_checkCollisions:
				print 'checkCollisions: removing a collided case from the list of elves'
	if collidedElves != []:
		for collidedElf in collidedElves:
			elvesList.remove(collidedElf)
	if len(elvesList) == 1:
		print elvesList
		print 'final elf at'
	return elvesList
			
def drawElvesInMap(elvesList,traks):
	"""drawElvesInMap
	
	:param elvesList: list of elves - [elfNumber,x,y,currentDire ction,nextDirection,collision]
	:param traks: 
	"""
	debug_drawElvesInMap = True
	newMap = map(list, traks)	# 2D list copy that really does a copy
	for elf in elvesList:
		x = elf[1]
		y = elf[2]
		newMap[elf[2]][elf[1]] = elf[3]
	if debug_drawElvesInMap:
		dumpMapList(newMap)
	return

def printElfCurrentStatus(elf,tracksMap):
	"""Elf vector is [elfNumber,x,y,currentDirection,nextDirection]
	"""
	currentElfX = elf[1]
	currentElfY = elf[2]
	debug_printElfCurrentStatus = True
	if debug_printElfCurrentStatus:
		print 'printElfCurrentStatus moveElf passed elf at x y',currentElfX,currentElfY,'is moving',
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
inFileName = 'input_3Elves_4Tracks.txt'

debug_main = False
print 'Reading in file',time.strftime('%X %x %Z')
InputFileClass = InputFileHandler()
textList = InputFileClass.readTextFileLinesToList(inFileName)
if debug_main:
	print '\ntextList',textList
unpaddedMineMap = makeMapArray(textList)				# Get the map from the file
elvesList = findElves(unpaddedMineMap)					# Find the elves on the map
if debug_main:
	print 'elvesList',elvesList
elvesList = sortElfList(elvesList)							# Sort the elves in 'reading' order
if debug_main:
	print 'sorted elvesList',elvesList
if debug_main:
	print 'main: there are',len(elvesList),'elves'
	print 'main: list of elves',elvesList
mapWithoutElves = replaceElvesWithTrack(unpaddedMineMap,elvesList)	# Remove the elves from the map
paddedMap = padMapArray(mapWithoutElves)				# Pad the map with spaces all around
cornersFixedMap = figureOutCorners(paddedMap)			# Replace corners with corner numbers
tracksMap = unPadMapArray(cornersFixedMap)				# Unpad the map
InputFileClass.writeOutMapFile(tracksMap)				# Write out the new map
if debug_main:
	dumpMapList(mapWithoutElves)
runElves(elvesList,tracksMap)
print 'Finished processing',time.strftime('%X %x %Z')

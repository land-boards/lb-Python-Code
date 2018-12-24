# Pt1-AoCDay13.py
# 2018 Advent of Code
# Day 14
# Part 1
# https://adventofcode.com/2018/day/14

import time
import re
import os

"""
--- Day 14: Chocolate Charts ---
You finally have a chance to look at all of the produce moving around. 
Chocolate, cinnamon, mint, chili peppers, nutmeg, vanilla... 
the Elves must be growing these plants to make hot chocolate! 
As you realize this, you hear a conversation in the distance. 
When you go to investigate, you discover two Elves in what appears to be a makeshift underground kitchen/laboratory.

The Elves are trying to come up with the ultimate hot chocolate recipe; 
they're even maintaining a scoreboard which tracks the quality score (0-9) of each recipe.

Only two recipes are on the board: the first recipe got a score of 3, the second, 7. 
Each of the two Elves has a current recipe: the first Elf starts with the first recipe, 
and the second Elf starts with the second recipe.

To create new recipes, the two Elves combine their current recipes. 
This creates new recipes from the digits of the sum of the current recipes' scores. 
With the current recipes' scores of 3 and 7, their sum is 10, and so two new recipes would be created: 
the first with score 1 and the second with score 0. If the current recipes' scores were 2 and 3, the sum, 5, 
would only create one recipe (with a score of 5) with its single digit.

The new recipes are added to the end of the scoreboard in the order they are created. 
So, after the first round, the scoreboard is 3, 7, 1, 0.

After all new recipes are added to the scoreboard, each Elf picks a new current recipe. 
To do this, the Elf steps forward through the scoreboard a number of recipes equal to 1 
plus the score of their current recipe. So, after the first round, the first Elf moves forward 1 + 3 = 4 times, 
while the second Elf moves forward 1 + 7 = 8 times. If they run out of recipes, they loop back around to the beginning. 
After the first round, both Elves happen to loop around until they land on the same recipe that they had in the beginning; 
in general, they will move to different recipes.

Drawing the first Elf as parentheses and the second Elf as square brackets, they continue this process:

(3)[7]
(3)[7] 1  0 
 3  7  1 [0](1) 0 
 3  7  1  0 [1] 0 (1)
(3) 7  1  0  1  0 [1] 2 
 3  7  1  0 (1) 0  1  2 [4]
 3  7  1 [0] 1  0 (1) 2  4  5 
 3  7  1  0 [1] 0  1  2 (4) 5  1 
 3 (7) 1  0  1  0 [1] 2  4  5  1  5 
 3  7  1  0  1  0  1  2 [4](5) 1  5  8 
 3 (7) 1  0  1  0  1  2  4  5  1  5  8 [9]
 3  7  1  0  1  0  1 [2] 4 (5) 1  5  8  9  1  6 
 3  7  1  0  1  0  1  2  4  5 [1] 5  8  9  1 (6) 7 
 3  7  1  0 (1) 0  1  2  4  5  1  5 [8] 9  1  6  7  7 
 3  7 [1] 0  1  0 (1) 2  4  5  1  5  8  9  1  6  7  7  9 
 3  7  1  0 [1] 0  1  2 (4) 5  1  5  8  9  1  6  7  7  9  2 
The Elves think their skill will improve after making a few recipes (your puzzle input). 
However, that could take ages; you can speed this up considerably by identifying the scores of the ten recipes after that.
For example:

If the Elves think their skill will improve after making 9 recipes, the scores of the ten recipes 
after the first nine on the scoreboard would be 5158916779 (highlighted in the last line of the diagram).
After 5 recipes, the scores of the next ten would be 0124515891.
After 18 recipes, the scores of the next ten would be 9251071085.
After 2018 recipes, the scores of the next ten would be 5941429882.
What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?

Your puzzle input is 110201.

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

# Pt2-AoCDay18.py
# 2018 Advent of Code
# Day 18
# Part 2
# https://adventofcode.com/2018/day/18

import time
import re
import os

"""

--- Part Two ---
This important natural resource will need to last for at least thousands of years. Are the Elves collecting this lumber sustainably?

What will the total resource value of the lumber collection area be after 1000000000 minutes?
That's not the right answer; your answer is too low. 
If you're stuck, there are some general tips on the about page, or you can ask for hints on the subreddit. 
Please wait one minute before trying again. (You guessed 196959.)

length of singletons 416
offset to start of repeated pattern 416
length of repeated 40
point to start looking at 999999585
modulusValue 25
positionInOriginalList 441
value at that point 197054

Wrong values are all singletons so I should not have tried them.

195305
196959
197054

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

def workThroughUnsortedForestValues(forestValues,pointInTimeToValue):
	"""Solve the value at a point in time past the list for a repeated list. 
	Example: Find the value at time of 10 in the list (should be 11)
	1 2 3 4 5 6  7  8  9  10 11 12 13 14 	- time
	0 1 2 3 4 5  6  7  8   9 10 11 12 13 	- Offset in list
	0 1 2 3 4 10 11 12 10 11 12 10 11 12 	- Values
	+ + + + + 								- Singleton values
	          R  R  R						- Repeated values
	0 1 2 3 4 are the singletons - length = 5
	10 11 12 is the repeated pattern - length of repeat pattern is the same as the number of elements in the list
	10 11 12 pattern starts at offset 5 just past the end of the singletons
	repeated pattern length - len(repeatedPattern)
	
	Go through values list. 
	If the value is in neither list, put it into the singletons list
	If the value is in the singletons list, remove it from the singletons list and put it into the valueRepeats
	Want to have two lists in the end. One list has the singletons and the other list has the repeated values.
	The offset to the first repeated pattern is the length of the singletons list
	The repeat count is the length of the repeats list
	To find the value at a particular time deal with offset and number of repeats
	
	:param forestValues:
	:param pointInTimeToValue:
	"""
	valueRepeats = []
	valueSingletons = []
	print 'passed time to check',pointInTimeToValue
	checkAtTime = pointInTimeToValue - 1
	print 't=0 compensation',checkAtTime
	for value in forestValues:
		if value not in valueRepeats and value not in valueSingletons:
			valueSingletons.append(value)
		elif value in valueSingletons:
			valueSingletons.remove(value)
			valueRepeats.append(value)
	print 'singletons',valueSingletons
	print 'repeated',valueRepeats
	offsetToStartOfRepeatedPattern = len(valueSingletons)
	print 'length of singletons',offsetToStartOfRepeatedPattern
	print 'offset to start of repeated pattern',offsetToStartOfRepeatedPattern
	#print 'the last singleton value',valueSingletons[-1]
	patternLength = len(valueRepeats)
	print 'length of repeated',patternLength
	lookInPatternOffset = checkAtTime - offsetToStartOfRepeatedPattern
	print 'point to start looking at',lookInPatternOffset
	modulusValue = lookInPatternOffset % patternLength
	print 'modulusValue',modulusValue
	positionInOriginalList = offsetToStartOfRepeatedPattern + modulusValue
	print 'positionInOriginalList',positionInOriginalList
	print 'value at that point',forestValues[positionInOriginalList]

########################################################################
## Code

## Game of life problem
## At what point does the pattern repeat?
## modulus math to figure out the solution past that point
## Running loop for 1000 iterations shows repeated forest values
## As an example in 1000 loops, the number 199732 repeats 20 times:
##	199732, 199732, 199732, 199732, 199732, 199732, 199732, 199732, 199732, 199732, 
##	199732, 199732, 199732, 199732, 199732, 199732, 199732, 199732, 199732, 199732
## Or picking number
## 208420, 208420, 208420, 208420, 208420, 208420, 208420, 208420, 208420, 208420, 
## 208420, 208420, 208420, 208420, 208420, 208420, 208420, 208420, 208420, 208420,
## This also repeats 20 times.
## So for 1000 items dividing by the 20 implies that the repeat pattern is somewhere
##	around 50 inputs (after the initial run into the pattern)
## It seems like this is a two pronged problem
## 	Find first repeat point then find repeat offset
## 	Can I just operate on the iteration list?

# testList = [0,1,2,3,4,10,11,12,10,11,12,10,11,12,10,11,12]
# workThroughUnsortedForestValues(testList,12)
# abbyTerminate('testing done')

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
forestValues = []
while loopCount <= 500:
	print 'After',loopCount,'mins'
	newForestMap = determineNextSymbols(forestMap)
	#dumpMapList(newForestMap)
	forestMap = newForestMap
	forestValue = valueForest(forestMap)
	forestValues.append(forestValue)
	loopCount += 1
	
#dumpMapList(newForestMap)
print 'unsofted forestValues',forestValues
workThroughUnsortedForestValues(forestValues,1000000000)
# forestValues.sort()
# print 'sorted forestValues',forestValues

# print 'forest value is',forestValue

print 'Finished processing',time.strftime('%X %x %Z')

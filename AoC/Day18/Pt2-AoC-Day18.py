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
This important natural resource will need to last for at least thousands of years. 
Are the Elves collecting this lumber sustainably?

What will the total resource value of the lumber collection area be after 1000000000 minutes?
That's not the right answer; your answer is too low. 
If you're stuck, there are some general tips on the about page, or you can ask for hints on the subreddit. 
Please wait one minute before trying again. (You guessed 196959.)

202301

That's the right answer! You are one gold star closer to fixing the time stream.

General Notes about the solution.
This is the first problem I have ever done with looking through data for patterns.
The good part is that the data is really well ordered.
The data that repeats happens a couple of times before the pattern but the pattern repeated a lot of times.
I ran with 600 data points.
The front end until the repeat was the first 0-441 values.
The pattern was 28 elements long.
Stimulus of 600 elements was enough to get 5-6 repeats. 
Fortunately, there was not too much of the repeated pattern elements earlier.
What I did:
Read forest value data (from part A) into list
Create frequency bins for the data.
Take the two highest runners for frequency.
Taking 1 isn't enough since the data stops mid bin.
This data was convenient since it wasn't very random and the two top bins were good.
Put the data found into a dictionary.

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

def makeFrequencyBins(listOfDuplicates,originalList):
	"""Create a dictionary with the number of times a number has been hit
	The most frequent numbers are the repeated ones if the pattern is long enough.
	List scan could be ob1 due to where the scan ends (test case doesn't take that into account)
	
	:returns: dictionary of the frequency counts of each item
	"""
	freqBins = {}
	for dupListItem in listOfDuplicates:
		for origListItem in originalList:
			if dupListItem == origListItem:
				if dupListItem in freqBins:		# The item is in the list so increase the count
					freqBins[dupListItem] = freqBins[dupListItem] + 1
				else:							# The item is not in the list so add it to the list
					freqBins[dupListItem] = 1
	return freqBins

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
	
	ISSUE: Not accounting for some early repeats.
	Need to find the offset to the last singleton and go from there.
	
	:param forestValues:
	:param pointInTimeToValue:
	"""
	valueRepeats = []
	valueSingletons = []
	workThroughUnsortedForestValues = False
	if workThroughUnsortedForestValues:
		print 'passed time to check',pointInTimeToValue
	checkAtTime = pointInTimeToValue - 1
	if workThroughUnsortedForestValues:
		print 't=0 compensation',checkAtTime
	for value in forestValues:
		if (value not in valueRepeats) and (value not in valueSingletons):	# first time seeing a valueForest
			valueSingletons.append(value)
		elif value in valueSingletons:										# seen value before
			valueSingletons.remove(value)
			valueRepeats.append(value)
	if workThroughUnsortedForestValues:
		print 'singletons list',valueSingletons
		print 'repeated',valueRepeats
	lastSingletonValue = valueSingletons[-1]
	if workThroughUnsortedForestValues:
		print 'the last singleton value',lastSingletonValue
	listOff = 0
	for singleton in forestValues:
		if singleton == lastSingletonValue:
			offsetToLastSingletonInForestValues = listOff
		listOff += 1
	if workThroughUnsortedForestValues:
		print 'offset to last singleton in the original list',offsetToLastSingletonInForestValues
	offsetToStartOfRepeatedPattern = offsetToLastSingletonInForestValues + 1
	if workThroughUnsortedForestValues:
		print 'last singleton value from singleton list',valueSingletons[-1]
		print 'make Frequency bins'
	freqBins = makeFrequencyBins(valueRepeats,forestValues)
	freqList = []
	for x, y in freqBins.items():
		if workThroughUnsortedForestValues:
			print(x, y)
		freqList.append(y)
	freqList.sort()
	if workThroughUnsortedForestValues:
		print 'frequency list',freqList
	maxFreqVal = freqList[-1]
	if workThroughUnsortedForestValues:
		print 'maxFreqVal',maxFreqVal
	# if the count is at maxFreqVal or maxFreqVal -1 the leave it in the dictionary
	maxFreqMinusOne = maxFreqVal - 1
	if workThroughUnsortedForestValues:
		print 'maxFreqMinusOne',maxFreqMinusOne
	for x, y in freqBins.items():
		if y != maxFreqVal and y != maxFreqMinusOne:
			freqBins.pop(x)
	if workThroughUnsortedForestValues:
		print 'the selected list of repeat values'
	if workThroughUnsortedForestValues:
		for x, y in freqBins.items():
			print(x, y)
	
	if workThroughUnsortedForestValues:
		print 'Find the first value in the original list that is in the dictionary'
	offsetInList = 0
	matchCount = 0
	for item in forestValues:
		if workThroughUnsortedForestValues:
			print 'checking item in bin at offset',offsetInList,'value',forestValues[offsetInList]
		if item in freqBins:
			matchCount += 1
			if workThroughUnsortedForestValues:
				print 'Item in forestValues was in the frequently found bins'
			if matchCount == len(freqBins):
				if workThroughUnsortedForestValues:
					print 'Found a match to the entire list'
				break
		else:
			matchCount = 0
		offsetInList += 1
	if workThroughUnsortedForestValues:
		print 'Offset in forestValues list to the end of the first repeated pattern element is',offsetInList
	patternLength = len(freqBins)
	if workThroughUnsortedForestValues:
		print 'The length of the repeat pattern is',len(freqBins)
		print 'Last item in repeated item list is',forestValues[offsetInList]
	firstItemInRepeatList = offsetInList - len(freqBins) + 1
	if workThroughUnsortedForestValues:
		print 'offset to first repeated item',firstItemInRepeatList 
		print 'element at the first repeated item',forestValues[firstItemInRepeatList]
	
	lookInPatternOffset = checkAtTime - firstItemInRepeatList
	if workThroughUnsortedForestValues:
		print 'point to start looking at',lookInPatternOffset
	modulusValue = lookInPatternOffset % patternLength
	if workThroughUnsortedForestValues:
		print 'modulusValue',modulusValue
	positionInOriginalList = firstItemInRepeatList + modulusValue
	if workThroughUnsortedForestValues:
		print 'positionInOriginalList',positionInOriginalList,
	print '\n*** Value at solution point',forestValues[positionInOriginalList],'***\n'

########################################################################
## Code

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
#dumpMapList(forestMap)
loopCount = 1
forestValues = []
while loopCount <= 600:			# this number could be autodetected if there was sufficient time to pull signal/noise ratio
	#print 'After',loopCount,'mins'
	newForestMap = determineNextSymbols(forestMap)
	forestMap = newForestMap
	forestValue = valueForest(forestMap)
	forestValues.append(forestValue)
	loopCount += 1

## The following is the workhorse for this part of the problem	
workThroughUnsortedForestValues(forestValues,1000000000)

print 'Finished processing',time.strftime('%X %x %Z')

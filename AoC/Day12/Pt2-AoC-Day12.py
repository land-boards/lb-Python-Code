# Pt1-AoCDay12.py
# 2018 Advent of Code
# Day 12
# Part 1
# https://adventofcode.com/2018/day/12

import time
import re
import os

"""

--- Part Two ---
You realize that 20 generations aren't enough. 
After all, these plants will need to last another 1500 years to even reach your timeline, 
not to mention your future.

After fifty billion (50000000000) generations, 
what is the sum of the numbers of all pots which contain a plant?

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
			inList.append(row.strip())
		return inList

#####################################################################################
## Functions which operate on the node list

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	exit()

def dumpStateValuesList(theList):
	for row in theList:
		print row
	return

def dumpPlantHistory(plantHistoryArray):
	i = 1
	for plants in plantHistoryArray:
		print i,plants
		i += 1

def makeStringExtendedCopy(string,copies):
	copyCount = copies
	newString = ''
	while (copyCount > 0):
		newString += string
		copyCount -= 1
	#print newString
	return newString

def convertStateValueStringsIntoLists(stateValuesList):
	debug_convertStateValueStringsIntoLists = False
	thelist = []
	for listItem in stateValuesList:
		newList = listItem.split()
		hlist = []
		hlist.append(newList[0])
		hlist.append(newList[2])
		thelist.append(hlist)
	if debug_convertStateValueStringsIntoLists:
		print 'convertStateValueStringsIntoLists: re-format table'
		for row in thelist:
			print row
		#os.system('pause')
	return thelist
	
def padOutStateString(stateString,padCount):
	debug_padOutStateString = False
	if debug_padOutStateString:
		print 'padOutStateString: padding out state vector with no plants "dot"'
		print 'padOutStateString: input state vector',stateString
		print 'padOutStateString: pad to number of padCount',padCount
	stateString = stateString
	if debug_padOutStateString:
		print 'padOutStateString: stateString',stateString
	concatString = makeStringExtendedCopy('.',padCount)
	if debug_padOutStateString:
		print 'padOutStateString: concatString',concatString
	newStateString = concatString
	newStateString = newStateString + stateString
	newStateString = newStateString + concatString
	if debug_padOutStateString:
		print 'padOutStateString: resulting string',newStateString
	return newStateString

def getBitForString(currentString,stateTable):
	"""getBitForString - look up the current string in the string table and return the new bit
	
	:param: currentString = 5 character long string
	:param: stateTable - table of the states and the results for those states
	"""
	debug_getBitForString = False
	if debug_getBitForString:
		print 'getBitForString: currentString',currentString
	if len(currentString) != 5:
		
		abbyTerminate('getBitForString: halt and catch fire')
	bit = '.'	# sample case has an assumed return value
	for value in stateTable:
		if value[0] == currentString:
			bit = value[1]
	return bit

def makeNewStringFromCurrentString(oldString,stateTable):
	"""Function slices out 5 bits at a time to pass to getBitForString()
	Requires 2 field padding on both ends to avoid contraction of the list
	
	:param: oldString - the entire line worth of data
	:param: stateTable - Passed through to the next level down routine
	
	"""
	debug_makeNewStringFromCurrentString = False
	padString = '....'
	oldStringLength = len(oldString)
	if debug_makeNewStringFromCurrentString:
		print 'makeNewStringFromCurrentString: oldStringLength',oldStringLength
		print 'oldString',oldString
	newString = padString
	oldStringCount = 2
	while oldStringCount < oldStringLength-4:
		newString += getBitForString(oldString[oldStringCount:oldStringCount+5],stateTable)
		oldStringCount += 1
	newString += '..'
	if debug_makeNewStringFromCurrentString:
		print 'makeNewStringFromCurrentString: newString',newString
	return newString

def sumAcrossLine(plantSnapshot):
	"""sumAcrossLine - 
	"""
	print plantSnapshot
	i = -3
	sum = 0
	for char in plantSnapshot:
		if char == '#':
			print i
			sum += i
		i += 1
	return sum

def productAcrossLine(plantSnapshot):
	"""productAcrossLine - Turn the plants into a binary number
	"""
	print plantSnapshot
	i = 1
	product = 0
	for char in plantSnapshot:
		if char == '#':
			print 2*i
			product += 2*i
		i = i*i
	return product

def iterateThroughPlants(stateTable,initialStateVector,generations):
	print 'iterateThroughPlants: stateTable',stateTable
	print 'iterateThroughPlants: initialStateVector',initialStateVector
	print 'iterateThroughPlants: generations',generations
	loopCount = 0
	resultingStateVector = initialStateVector
	plantList = []
	while loopCount < generations:
		resultingStateVector = makeNewStringFromCurrentString(resultingStateVector,stateTable)
#		print 'gen',loopCount+1,': ',resultingStateVector
		plantList.append(resultingStateVector)
		loopCount += 1
#		os.system('pause')
	return plantList

def stripPlantHistory(plantHistory):
	newList = []
	for row in plantHistory:
		newList.append(row[padValue-3:])
	return newList

########################################################################
## This is the workhorse of this assignment


########################################################################
## Code
## This is a fairly deep set of nested loops

print 'Reading in file',time.strftime('%X %x %Z')

InputFileClass = InputFileHandler()

textList = InputFileClass.readTextFileLinesToList('input.txt')
#print '\ntextList',textList

padValue = 32

initialState = textList[0]
#print '\ninitialState',initialState
firstList = initialState.split()
#print 'firstList',firstList
stateString = firstList[2]
print '\nmain: stateString',stateString
initialStateVector = padOutStateString(stateString,padValue)
print 'Pmain: added out string - initialStateVector',initialStateVector

stateValuesList = textList[2:]
stateTable = convertStateValueStringsIntoLists(stateValuesList)

## test the modules

print 'test cases'
if getBitForString('...##',stateTable) == '#' and getBitForString('.....',stateTable) == '.':
	print 'main: getBitForString() - sample data test case passed'
else:
	print 'main: getBitForString() - sample data test case failed'

# getBitForString('...##d',stateTable)	# deliberately causes a failure

testString = '......#..#.#..##......###...###......'
expect = '....#...#....#.....#..#..#..#......'
if makeNewStringFromCurrentString(testString,stateTable) != expect:
	print 'main: makeNewStringFromCurrentString() - sample data test case failed'
else:
	print 'main: makeNewStringFromCurrentString() - sample data test case passed'

generations = 20
plantHistory = iterateThroughPlants(stateTable,initialStateVector,generations)
#dumpPlantHistory(plantHistory)
strippedPlantHistory = stripPlantHistory(plantHistory)
dumpPlantHistory(strippedPlantHistory)

print ' \nsum',sumAcrossLine(strippedPlantHistory[19])

print ' \nproduct',productAcrossLine(strippedPlantHistory[19])

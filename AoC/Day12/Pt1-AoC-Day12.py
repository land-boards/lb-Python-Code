# Pt1-AoCDay12.py
# 2018 Advent of Code
# Day 12
# Part 1
# https://adventofcode.com/2018/day/12

import time
import re
import os

"""

--- Day 12: Subterranean Sustainability ---
The year 518 is significantly more underground than your history books implied. 
Either that, or you've arrived in a vast cavern network under the North Pole.

After exploring a little, you discover a long tunnel that contains a row of small pots 
as far as you can see to your left and right. A few of them contain plants - 
someone is trying to grow things in these geothermally-heated caves.

The pots are numbered, with 0 in front of you. 
To the left, the pots are numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... 
Your puzzle input contains a list of pots from 0 to the right and whether they do (#) or do not (.) currently contain a plant, the initial state. (No other pots currently contain plants.) For example, an initial state of #..##.... indicates that pots 0, 3, and 4 currently contain plants.

Your puzzle input also contains some notes you find on a nearby table: 
someone has been trying to figure out how these plants spread to nearby pots. 
Based on the notes, for each generation of plants, a given pot has or 
does not have a plant based on whether that pot (and the two pots on either side of it) 
had a plant in the last generation. 
These are written as LLCRR => N, where L are pots to the left, 
C is the current pot being considered, R are the pots to the right, 
and N is whether the current pot will have a plant in the next generation. 

For example:

A note like ..#.. => . means that a pot that contains a plant but with 
no plants within two pots of it will not have a plant in it during the next generation.
A note like ##.## => . means that an empty pot with two plants on each side of it 
will remain empty in the next generation.
A note like .##.# => # means that a pot has a plant in a given generation if, 
in the previous generation, there were plants in that pot, the one immediately to the left, and the one two pots to the right, but not in the ones immediately to the right and two to the left.
It's not clear what these plants are for, but you're sure it's important, 
so you'd like to make sure the current configuration of plants is sustainable 
by determining what will happen after 20 generations.

For example, given the following input:

initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
For brevity, in this example, only the combinations which do produce a plant are listed. (Your input includes all possible combinations.) Then, the next 20 generations will look like this:

                 1         2         3     
       0         0         0         0     
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.
The generation is shown along the left, where 0 is the initial state. 
The pot numbers are shown along the top, where 0 labels the center pot, 
negative-numbered pots extend to the left, and positive pots extend toward the right. 
Remember, the initial state begins at pot 0, which is not the leftmost pot used in this example.

After one generation, only seven plants remain. 
The one in pot 0 matched the rule looking for ..#.., the one in pot 4 matched the rule 
looking for .#.#., pot 9 matched .##.., and so on.

In this example, after 20 generations, the pots shown as # contain plants, 
the furthest left of which is pot -2, and the furthest right of which is pot 34. 
Adding up all the numbers of plant-containing pots after the 20th generation produces 325.

After 20 generations, what is the sum of the numbers of all pots which contain a plant?


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
	"""
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

textList = InputFileClass.readTextFileLinesToList('input2.txt')
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

print ' \n',sumAcrossLine(strippedPlantHistory[19])

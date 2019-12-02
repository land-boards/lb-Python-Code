# Pt1-AoCDay7.py
# 2018 Advent of Code
# Day 7
# Part 1
# https://adventofcode.com/2018/day/7

import time
import re

"""
--- Day 7: The Sum of Its Parts ---
You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?

Your puzzle answer was DFOQPTELAYRVUMXHKWSGZBCJIN.

The first half of this puzzle is complete! It provides one gold star: *


"""

def readTextFileAndSortToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce an ordered file
	:returns: the list sorted list
	"""
	textFile = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textFile.append(line.strip())
		textFile.sort()
	return textFile

def parseInFile(inFileList):
	"""parseInFile - 
	"""
	inLists = []
	for record in inFileList:
		inListListed = record.split()
		#print 'inListListed =',inListListed
		inLine = []
		inLine.append(inListListed[1])
		inLine.append(inListListed[7])
		inLists.append(inLine)
		
	#print inLists
	return inLists

def removePair(sL,nL,originalListCopy):
	"""go through firstLL and find the appropriate second letter
	"""
#	print 'removing',sL,nL
	newList = []
	for line in originalListCopy:
		if sL == line[0] and nL == line[1]:
#			print 'skipping',sL,nL
			continue
		else:
			newList.append(line)
	return newList
	
def getNextLetter(sL,theList):
	nextLettersList = []
	for pair in originalListCopy:
		if pair[0] == startingLetter:
			nextLetter = pair[1]
			nextLettersList.append(pair[1])
	nextLettersList.sort()
	nextLetter1 = nextLettersList[0]
	return nextLetter1

def addLetterToResultList(firstLetterList,secondLetterList):
	sll = []
	for letter in firstLetterList:
		if letter not in secondLetterList:
			sll.append(letter)
	sll.sort()
	return sll

def fillFirstLetterList(originalListCopy):
	firstLetterList = []
	for pair in originalListCopy:
		if pair[0] not in firstLetterList:
			firstLetterList.append(pair[0])
	firstLetterList.sort()
	return firstLetterList
	
def fillSecondLetterList(originalListCopy):
	secondLetterList = []
	for pair in originalListCopy:
		if pair[1] not in secondLetterList:
			secondLetterList.append(pair[1])
	secondLetterList.sort()
	return secondLetterList

###########################################
## Code
###########################################

print 'Reading in file',time.strftime('%X %x %Z')
inFileList = readTextFileAndSortToList('input.txt')
parsedInList = parseInFile(inFileList)
originalListCopy = parsedInList

workers = 5
timeStep = 60

choseString = ''
while len(originalListCopy) > 0:
	firstLetterList = fillFirstLetterList(originalListCopy)
	secondLetterList = fillSecondLetterList(originalListCopy)
	startingLetterList = addLetterToResultList(firstLetterList,secondLetterList)
	startingLetter = startingLetterList[0]
	if startingLetter not in choseString:
		choseString += startingLetter
	if len(firstLetterList) == 1 and len(secondLetterList) == 1:
		choseString += secondLetterList[0]
	nextLetter1 = getNextLetter(startingLetter,originalListCopy)
	originalListCopy = removePair(startingLetter,nextLetter1,originalListCopy)
print 'Completed processing',time.strftime('%X %x %Z')
print choseString

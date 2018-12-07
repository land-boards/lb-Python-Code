# Pt2-AoCDay7.py
# 2018 Advent of Code
# Day 7
# Part 2
# https://adventofcode.com/2018/day/7

import time
import re

"""

--- Part Two ---
As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .        
   1        C          .        
   2        C          .        
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE
Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?

"""

def readTextFileAndSortToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
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

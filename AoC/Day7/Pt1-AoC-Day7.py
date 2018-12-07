# Pt1-AoCDay7.py
# 2018 Advent of Code
# Day 7
# Part 1
# https://adventofcode.com/2018/day/7

import time
import re

"""


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
	
###########################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')
inFileList = readTextFileAndSortToList('input.txt')
parsedInList = parseInFile(inFileList)
print parsedInList
originalListCopy = parsedInList

choseString = ''
while len(originalListCopy)>0:
	firstLetterList = []
	secondLetterList = []
	for pair in originalListCopy:
		if pair[0] not in firstLetterList:
			firstLetterList.append(pair[0])
		if pair[1] not in secondLetterList:
			secondLetterList.append(pair[1])
	firstLetterList.sort()
	secondLetterList.sort()
	sll = []
	for letter in firstLetterList:
		if letter not in secondLetterList:
			sll.append(letter)
	sll.sort()
	startingLetter = sll[0]
	if startingLetter not in choseString:
		choseString += startingLetter
	if len(firstLetterList) == 1 and len(secondLetterList) == 1:
		choseString += secondLetterList[0]
		print 'lastLetter',secondLetterList[0]
	nextLettersList = []
	for pair in originalListCopy:
		if pair[0] == startingLetter:
			nextLetter = pair[1]
			nextLettersList.append(pair[1])
	nextLettersList.sort()
	originalListCopy = removePair(startingLetter,nextLettersList[0],originalListCopy)
print choseString
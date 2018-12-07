# Pt1-AoC-Day6.py
# 2017 Advent of Code
# Day 6
# Part 1
# Problem
# https://adventofcode.com/2017/day/6
# Dataset
# https://adventofcode.com/2017/day/6/input

import time
import re

"""
You notice a progress bar that jumps to 50% completion. Apparently, the door isn't yet satisfied, but it did emit a star as encouragement. The instructions change:

Now, instead of considering the next digit, it wants you to consider the digit halfway around the circular list. That is, if your list contains 10 items, only include a digit in your sum if the digit 10/2 = 5 steps forward matches it. Fortunately, your list has an even number of elements.

For example:

1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
1221 produces 0, because every comparison is between a 1 and a 2.
123425 produces 4, because both 2s match each other, but no other digit has a match.
123123 produces 12.
12131415 produces 4.
What is the solution to your new captcha?

Your puzzle answer was 1054.

"""

def readTextFileToString(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a string
	:returns: the string
	"""
	with open(fileName, 'r') as filehandle:
		inString = filehandle.read().strip()
	return inString

def findMaxValue(valueList):
	foundMax = 0
	foundOff = 0
	currentOff = 0
	for item in valueList:
		if item > foundMax:
			foundMax = item
			foundOff = currentOff
		currentOff += 1
	return [foundMax,foundOff]
	
def loopyListInLoopList(loopyList):
	print 'loopyList',loopyList
	print 'loopList',loopList
	for vector in loopList:
		loopyListOff = 0
		for vectElement in vector:
			if vectElement != loopyList[loopyListOff]:
				return False
	else:
		return True

def addToLoopList(loopyList):
	if loopyListInLoopList(loopyList) == True:
		return False
	else:
		return True
	
###############################################################################
## Code
###############################################################################

print 'Reading in file',time.strftime('%X %x %Z')
vector = readTextFileToString('input2.txt').split()
vectorList = []
for element in vector:
	vectorList.append(int(element))
print vectorList
vectorCount = len(vectorList)
#print 'vectorCount',vectorCount

loopList = []
loopList.append(vectorList)
timesThrough = 0
while timesThrough < 20:
	maxValOff = findMaxValue(vectorList)
	blksToRedistr = maxValOff[0]
	blkOffset = maxValOff[1]
	#print 'blksToRedistr',blksToRedistr
	#print 'blkOffset',blkOffset
	blockSize = blksToRedistr/(vectorCount-1)
	#print 'blockSize',blockSize
	blocksToRedistribute = blockSize
	vectorList[blkOffset] = 0
	blkOffset += 1
	if blkOffset >= vectorCount:
		blkOffset = 0
	while blksToRedistr > 0:
		#print vectorList,'blksToRedistr',blksToRedistr,'blkOffset',blkOffset
		if blksToRedistr < blockSize:
			#print 'shortage'
			vectorList[blkOffset] = vectorList[blkOffset] + blksToRedistr
		else:
			#print 'unlimited'
			vectorList[blkOffset] = vectorList[blkOffset] + blockSize
		blkOffset += 1
		if blkOffset >= vectorCount:
			blkOffset = 0
		blksToRedistr -= blockSize
	print vectorList
	timesThrough += 1
	if addToLoopList(vectorList) == False:
		break
print timesThrough

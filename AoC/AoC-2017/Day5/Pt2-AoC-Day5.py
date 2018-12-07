# Pt2-AoCDay5.py
# 2017 Advent of Code
# Day 5
# Part 2
# Problem
# https://adventofcode.com/2017/day/5
# Dataset
# https://adventofcode.com/2017/day/5/input

import time
import re

"""

--- Part Two ---
Now, the jumps are even stranger: after each jump, if the offset was three or more, instead decrease it by 1. Otherwise, increase it by 1 as before.

Using this rule with the above example, the process now takes 10 steps, and the offset values after finding the exit are left as 2 3 2 3 -1.

How many steps does it now take to reach the exit?

Your puzzle answer was 25136209.

Reading in file 22:47:42 12/06/18 Eastern Standard Time
length of dataArray 1044
Completed 22:48:09 12/06/18 Eastern Standard Time
done in  25136209

"""

def readTextFileToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
	:returns: the list sorted list
	"""
	textFile = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textFile.append(line.strip())
	return textFile

print 'Reading in file',time.strftime('%X %x %Z')
strArray = readTextFileToList('input.txt')		# replace filename string as needed
dataArray = []
for element in strArray:
	dataArray.append(int(element))
print 'length of dataArray',len(dataArray)
#print 'dataArray'
programCounter = 0
programStepsExecuted = 0
while True:
	#print dataArray,'PC =',programCounter
	nextAddr = dataArray[programCounter] + programCounter
	if dataArray[programCounter] >= 3:
		dataArray[programCounter] = dataArray[programCounter] - 1
	else:
		dataArray[programCounter] = dataArray[programCounter] + 1
	programCounter = nextAddr
	programStepsExecuted += 1
	if programCounter >= len(dataArray) or programCounter < 0:
		print 'Completed',time.strftime('%X %x %Z')
		print 'done in ',programStepsExecuted
		exit()

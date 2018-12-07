# Pt1-AoCDay5.py
# 2017 Advent of Code
# Day 5
# Part 1
# Problem
# https://adventofcode.com/2017/day/5
# Dataset
# https://adventofcode.com/2017/day/5/input

import time
import re

"""

Our sponsors help make Advent of Code possible:
Formlabs - We make powerful, affordable 3D printers for professionals.
--- Day 5: A Maze of Twisty Trampolines, All Alike ---
An urgent interrupt arrives from the CPU: it's trapped in a maze of jump instructions, and it would like assistance from any programs with spare cycles to help find the exit.

The message includes a list of the offsets for each jump. Jumps are relative: -1 moves to the previous instruction, and 2 skips the next one. Start at the first instruction in the list. The goal is to follow the jumps until one leads outside the list.

In addition, these instructions are a little strange; after each jump, the offset of that instruction increases by 1. So, if you come across an offset of 3, you would move three instructions forward, but change it to a 4 for the next time it is encountered.

For example, consider the following list of jump offsets:

0
3
0
1
-3
Positive jumps ("forward") move downward; negative jumps move upward. For legibility in this example, these offset values will be written all on one line, with the current instruction marked in parentheses. The following steps would be taken before an exit is found:

(0) 3  0  1  -3  - before we have taken any steps.
(1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all). Fortunately, the instruction is then incremented to 1.
 2 (3) 0  1  -3  - step forward because of the instruction we just modified. The first instruction is incremented again, now to 2.
 2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.
 2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.
 2  5  0  1  -2  - jump 4 steps forward, escaping the maze.
In this example, the exit is reached in 5 steps.

How many steps does it take to reach the exit?

Your puzzle answer was 342669.

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

#print 'Reading in file',time.strftime('%X %x %Z')
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
	dataArray[programCounter] = dataArray[programCounter] + 1
	programCounter = nextAddr
	programStepsExecuted += 1
	if programCounter >= len(dataArray) or programCounter < 0:
		print 'done in ',programStepsExecuted
		exit()

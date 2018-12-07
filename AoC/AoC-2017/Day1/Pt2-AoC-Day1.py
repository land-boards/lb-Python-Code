# Pt1-AoCDay1.py
# 2017 Advent of Code
# Day 1
# Part 2
# Problem
# https://adventofcode.com/2017/day/1
# Dataset
# https://adventofcode.com/2017/day/1/input

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
		string = filehandle.read().strip()
	return string

print 'Reading in file',time.strftime('%X %x %Z')
captchaString = readTextFileToString('input2.txt')		# replace filename string as needed
print 'captchaString',captchaString
captchaList = []
for inChar in captchaString:
	captchaList.append(int(inChar))
print 'captchaList',captchaList
originalListLength = len(captchaList)
print 'List Length',originalListLength
sum = 0
loopCount = 0
loopMatchCount = 1
lastNum = 0
currentNum = 0
halfListLen = originalListLength/2
while loopCount < halfListLen:
	num1 = captchaList[loopCount]
	num2 = captchaList[loopCount + halfListLen]
	if num1 == num2:
		sum += 2 * num1
	loopCount += 1
print 'sum',sum

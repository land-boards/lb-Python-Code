# Pt1-AoCDay1.py
# 2017 Advent of Code
# Day 1
# Part 1
# Problem
# https://adventofcode.com/2017/day/1
# Dataset
# https://adventofcode.com/2017/day/1/input

import time
import re

"""
The captcha requires you to review a sequence of digits (your puzzle input) and find the sum of all digits that match the next digit in the list. The list is circular, so the digit after the last digit is the first digit in the list.

For example:

1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit and the third digit (2) matches the fourth digit.
1111 produces 4 because each digit (all 1) matches the next.
1234 produces 0 because no digit matches the next.
91212129 produces 9 because the only digit that matches the next one is the last digit, 9.
What is the solution to your captcha?

Your puzzle answer was 1044.

"""

def readTextFileToString(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a string
	:returns: the string
	"""
	with open(fileName, 'r') as filehandle:
		string = filehandle.read().strip()
	return string

print 'Reading in file',time.strftime('%X %x %Z')
captchaString = readTextFileToString('input.txt')		# replace filename string as needed
print 'captchaString',captchaString
captchaList = list(captchaString)
captchaList = []
for inChar in captchaString:
	captchaList.append(int(inChar))
lastNumInList = captchaList[0]			# add the first digit to the end
captchaList.append(lastNumInList)
captchaList.append(0)
print 'captchaList',captchaList
sum = 0
loopCount = 0
loopMatchCount = 1
lastNum = 0
currentNum = 0
while loopCount < len(captchaList):
	currentNum = captchaList[loopCount]
	#print 'currentNum',currentNum,
	if currentNum == lastNum:
		#print 'matched last',lastNum,'to current',currentNum
		loopMatchCount += 1
	else:
		print 'changed digit from',lastNum,'to',currentNum,
		print 'loopMatchCount',loopMatchCount
		if loopMatchCount == 2:
			sum += lastNum
		elif loopMatchCount > 2:
			print 'loopMatchCount',loopMatchCount
			sum += lastNum * (loopMatchCount-1)
		#print 'sum',sum
		loopMatchCount = 1
	lastNum = currentNum
	loopCount += 1
print 'sum',sum

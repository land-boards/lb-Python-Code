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
"""

def readTextFileToString(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a string
	:returns: the string
	"""
	with open(fileName, 'r') as filehandle:
		string = filehandle.read().strip()
	return string

print 'Reading in file',time.strftime('%X %x %Z')
captchaString = readTextFileToString('input2.txt')
print captchaString
lastChar = captchaString[0]
if captchaString[0] == captchaString[1]:
	accum = int(captchaString[0])
else:
	accum = 0
stringOff = 1
reachedEnd = False
while True:
	currentChar = captchaString[stringOff]
	print 'lastChar',lastChar,'currentChar',currentChar
	if lastChar == currentChar:
		accum += int(currentChar)
		stringOff += 1
	elif reachedEnd:
		print 'accum',accum
		exit()
	else:
		lastChar = currentChar
		stringOff += 1
	if stringOff == len(captchaString):
		stringOff = 0
		reachedEnd = True

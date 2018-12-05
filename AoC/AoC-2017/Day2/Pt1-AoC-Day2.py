# Pt1-AoCDay2.py
# 2017 Advent of Code
# Day 2
# Part 1
# Problem
# https://adventofcode.com/2017/day/2
# Dataset
# https://adventofcode.com/2017/day/2/input

import time
import re

"""
--- Day 2: Corruption Checksum ---
As you walk through the door, a glowing humanoid shape yells in your direction. "You there! Your state appears to be idle. Come help us repair the corruption in this spreadsheet - if we take another millisecond, we'll have to display an hourglass cursor!"

The spreadsheet consists of rows of apparently-random numbers. To make sure the recovery process is on the right track, they need you to calculate the spreadsheet's checksum. For each row, determine the difference between the largest value and the smallest value; the checksum is the sum of all of these differences.

For example, given the following spreadsheet:

5 1 9 5
7 5 3
2 4 6 8
The first row's largest and smallest values are 9 and 1, and their difference is 8.
The second row's largest and smallest values are 7 and 3, and their difference is 4.
The third row's difference is 6.
In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.

What is the checksum for the spreadsheet in your puzzle input?

Your puzzle answer was 43074.

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
dataArray = readTextFileToList('input.txt')		# replace filename string as needed
print 'dataArray',dataArray
totalCount = 0
for row in dataArray:
	rowMin = 9999
	rowMax = 0
	column = row.split()
	print 'column',column
	for element in column:
		if int(element) > rowMax:
			rowMax = int(element)
		if int(element) < rowMin:
			rowMin = int(element)
	rowSum = rowMax - rowMin
	totalCount += rowSum
print 'totalCount',totalCount

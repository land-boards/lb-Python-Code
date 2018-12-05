# Pt2-AoCDay2.py
# 2017 Advent of Code
# Day 2
# Part 2
# Problem
# https://adventofcode.com/2017/day/2
# Dataset
# https://adventofcode.com/2017/day/2/input

import time
import re

"""
"Great work; looks like we're on the right track after all. Here's a star for your effort." However, the program seems a little worried. Can programs be worried?

"Based on what we're seeing, it looks like all the User wanted is some information about the evenly divisible values in the spreadsheet. Unfortunately, none of us are equipped for that kind of calculation - most of us specialize in bitwise operations."

It sounds like the goal is to find the only two numbers in each row where one evenly divides the other - that is, where the result of the division operation is a whole number. They would like you to find those numbers on each line, divide them, and add up each line's result.

For example, given the following spreadsheet:

5 9 2 8
9 4 7 3
3 8 6 5
In the first row, the only two numbers that evenly divide are 8 and 2; the result of this division is 4.
In the second row, the two numbers are 9 and 3; the result is 3.
In the third row, the result is 2.
In this example, the sum of the results would be 4 + 3 + 2 = 9.

What is the sum of each row's result in your puzzle input?

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

def isDivisible(num1,num2):
	"""isDivisible - If the two numbers are evenly divisible between each other
	"""
	print 'comparing',num1,num2,
	division = num1/num2
	product = num2*division
	if product == num1:
		print 'divisible returning',division
		return division
	division = num2/num1
	product = num1*division
	if product == num2:
		print 'divisible returning',division
		return division
	print 'not divisible'
	return 0
	
def checkNumbersInRow(row):
	"""
	"""
	num = 0
	column = row.split()
	print 'cells in the row',column
	numColumns = len(column)
	print 'number of cells in the row',numColumns
	currentColumn = 1
	currCol2 = 0
	for element in column:
		print 'checking element',element
		element1 = int(element)
		currCol2 += 1
		currentColumn = currCol2
		while currentColumn < numColumns:
			element2 = int(column[currentColumn])
			isDiv = isDivisible(element1,element2)
			if isDiv != 0:
				return(isDiv)
			currentColumn += 1

print 'Reading in file',time.strftime('%X %x %Z')
dataArray = readTextFileToList('input.txt')		# replace filename string as needed
print 'dataArray',dataArray
totalCount = 0
for row in dataArray:
	foundNum = checkNumbersInRow(row)
	print 'foundNum',foundNum
	totalCount += foundNum
print 'totalCount',totalCount

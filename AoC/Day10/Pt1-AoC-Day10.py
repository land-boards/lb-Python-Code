# Pt1-AoCDay9.py
# 2018 Advent of Code
# Day 9
# Part 1
# https://adventofcode.com/2018/day/9

import time
import re

"""



"""


def readTextFileToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
	:returns: the list sorted list
	"""
	textFile = ''
	with open(fileName, 'r') as filehandle:  
		for char in filehandle:
			textFile += char
	return textFile
	
def stringOfNumbersToList(str):
	"""stringOfNumbersToList - Take the input file which is a really long list and turn it into a python list
	"""
	theList = []
	num = 0
	for letter in str:
		if letter >= '0' and letter <= '9':
			num = num*10 + ord(letter)-ord('0')
		else:
			theList.append(num)
			num = 0
	return theList

#####################################################################################
## Functions which operate on the input file and node lists


#####################################################################################
## Functions which operate on the node list


########################################################################
## This is the workhorse of this assignment


########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

textList = readTextFileToList('input2.txt')

myList = stringOfNumbersToList(textList)


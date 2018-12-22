# Pt1-AoCDay16.py
# 2018 Advent of Code
# Day 16
# Part 1
# https://adventofcode.com/2018/day/16

import time
import re
import os

"""

"""


def readTextFileToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
	:returns: the list sorted list
	"""
	textList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textList.append(line.strip())
	for line in textList:
		print line
	exit()
	return textList
	
def textFileToList(textFile):
	"""Convert the text file into a list
	
	"""
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

textList = readTextFileToList('input.txt')

myList = textFileToList(textList)

print 'myList',myList
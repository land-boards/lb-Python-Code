# Pt1-AoCDay4.py
# 2017 Advent of Code
# Day 4
# Part 1
# Problem
# https://adventofcode.com/2017/day/2
# Dataset
# https://adventofcode.com/2017/day/2/input

import time
import re

"""
--- Day 4: High-Entropy Passphrases ---
A new system policy has been put in place that requires all accounts to use a passphrase instead of simply a password. A passphrase consists of a series of words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

aa bb cc dd ee is valid.
aa bb cc dd aa is not valid - the word aa appears more than once.
aa bb cc dd aaa is valid - aa and aaa count as different words.
The system's full passphrase list is available as your puzzle input. How many passphrases are valid?
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
rowVals = []
totalPassphrases = len(dataArray)
badPassphrases = 0
for row in dataArray:
	rowVals = re.split('[\W]+',row)
	newRowList = []
	for phrases in rowVals:
		if phrases not in newRowList:
			newRowList.append(phrases)
		else:
			print phrases
			badPassphrases += 1
			break
print 'total passphrases',totalPassphrases
print 'bad passphrases',badPassphrases
print 'good passphrases',totalPassphrases-badPassphrases

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
--- Part Two ---
For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two words that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged to form any other word in the passphrase.

For example:

abcde fghij is a valid passphrase.
abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
iiii oiii ooii oooi oooo is valid.
oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
Under this new system policy, how many passphrases are valid?
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

def checkRowForAnnagrams(rowVals):
	print 'row',rowVals
	newRowList = []
	offset = 1
	for phrases in rowVals:
		print phrases

print 'Reading in file',time.strftime('%X %x %Z')
dataArray = readTextFileToList('input2.txt')		# replace filename string as needed
print 'dataArray',dataArray
rowVals = []
totalPassphrases = len(dataArray)
badPassphrases = 0
for row in dataArray:
	rowVals = re.split('[\W]+',row)
	if checkRowForAnnagrams(rowVals):
		print 'got an annagram'
	else:
		print 'was not an annagram'
		
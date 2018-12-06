# Pt2-AoCDay4.py
# 2017 Advent of Code
# Day 4
# Part 2
# Problem
# https://adventofcode.com/2017/day/4
# Dataset
# https://adventofcode.com/2017/day/4/input

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

Your puzzle answer was 167.

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

def areWordsAnnagrams(word1,word2):
	wordList1 = list(word1)
	wordList1.sort()
	wordList2 = list(word2)
	wordList2.sort()
	#print 'wordList1',wordList1
	#print 'wordList2',wordList2
	if wordList1 == wordList2:
		return True
	return False
	
def checkRowForAnnagrams(rowVals):
	#print 'row',rowVals
	newRowList = []
	wordOffset = 1
	for word in rowVals:
		offset = wordOffset
		while offset < len(rowVals):
			if areWordsAnnagrams(word,rowVals[offset]):
				return True
			offset += 1
		wordOffset += 1
	return False

#print 'Reading in file',time.strftime('%X %x %Z')
dataArray = readTextFileToList('input.txt')		# replace filename string as needed
#print 'dataArray',dataArray
rowVals = []
valid = 0
invalid = 0
for row in dataArray:
	rowVals = re.split('[\W]+',row)
	if checkRowForAnnagrams(rowVals):
		invalid += 1
		#print 'got an annagram'
	else:
		#print 'was not an annagram'
		valid += 1

print 'valid',valid
print 'not valid',invalid

# Pt1-AoCDay5.py
# 2018 Advent of Code
# Day 5
# Part 1
# https://adventofcode.com/2018/day/5

import time
import re

"""

--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab. The Elves are making decent progress, but are still struggling with the suit's size reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their problem eventually, you can do better. You scan the chemical composition of the suit's material and discover that it is formed by extremely long polymers (one of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each other such that two adjacent units of the same type and opposite polarity are destroyed. Units' types are represented by letters; units' polarity is represented by capitalization. For instance, r and R are units with the same type but opposite polarity, whereas r and s are entirely different types and do not react.

For example:

In aA, a and A react, leaving nothing behind.
In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
In abAB, no two adjacent units are of the same type, and so nothing happens.
In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
Now, consider a larger example, dabAcCaCBAcCcaDA:

dabAcCaCBAcCcaDA  The first 'cC' is removed.
dabAaCBAcCcaDA    This creates 'Aa', which is removed.
dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
dabCBAcaDA        No further actions can be taken.
After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned? (Note: in this puzzle and others, the input is large; if you copy/paste your input, make sure you get the whole thing.)

Your puzzle answer was 477.
"""

def readTextFileToString(fileName):
	"""readTextFileToList - Turn a text file into a list.
	Every line is an element in the list.
	"""
	textFile = []
	# open file and read the content into an accumulated sum
	#print 'Reading in file',time.strftime('%X %x %Z')
	with open(fileName, 'r') as filehandle: 
		string = filehandle.read().strip()
	return string

def matchCheck(char1, char2):
	#print 'checking',char1,char2
	if char1.isupper() and char2.isupper():
		#print 'mismatch1'
		return False
	if char1.islower() and char2.islower():
		#print 'mismatch2'
		return False
	if char1.upper() != char2.upper():
		#print 'mismatch3'
		return False
	#print 'match',char1,char2
	return True
	
polymereString = readTextFileToString('input2.txt')
print 'polymereString',polymereString
print 'len of polymereString before',len(polymereString)
currentColumn = 0
newString = ''
changesFound = True
while changesFound:
	changesFound = False
	while True:
		if matchCheck(polymereString[currentColumn],polymereString[currentColumn+1]):
			currentColumn += 2
			changesFound = True
		else:
			newString += polymereString[currentColumn]
			#print 'newString',newString
			currentColumn += 1
		if currentColumn == len(polymereString)-1:
			newString += polymereString[currentColumn]
			break
	#print 'reached end of string'
	polymereString = newString
	newString = ''
	currentColumn = 0
	#print 'polymereString',polymereString
print 'polymereString',polymereString
print 'len of polymereString after',len(polymereString)


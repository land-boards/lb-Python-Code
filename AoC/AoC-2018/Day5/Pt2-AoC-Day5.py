# Pt2-AoCDay5.py
# 2018 Advent of Code
# Day 5
# Part 2
# https://adventofcode.com/2018/day/5

import time
import re
import string

"""

--- Part Two ---
Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from collapsing as much as it should. Your goal is to figure out which unit type is causing the most problems, remove all instances of it (regardless of polarity), fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer produces dbCBcD, which has length 6.
Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer produces daCAcaDA, which has length 8.
Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer produces daDA, which has length 4.
Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer produces abCBAc, which has length 6.
In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units of exactly one type and fully reacting the result?

Your puzzle answer was 6484.

"""

def readTextFileToString(fileName):
	"""readTextFileToString - Turn a text file into a string.
	Every character is an element in the string.
	"""
	textFile = []
	with open(fileName, 'r') as filehandle: 
		string = filehandle.read()
	return string.strip()
	
def removeLetterFromString(char1,stringToFix):
	newString = ''
	for letter in stringToFix:
		if letter.upper() != char1.upper():
			newString += letter
	return newString

def matchCheck(char1, char2):
	"""matchCheck - Check if two adjacent characters are the same but different case
	Returns True if the characters are the same
	"""
	if char1.isupper() and char2.isupper():	# both are uppers
		return False
	if char1.islower() and char2.islower():	# both are lowers
		return False
	if char1.upper() != char2.upper():		# one is upper, one is lower but they are not the same char
		return False
	return True								# only thing left is same chars different cases
	
def reduceString(polymereString):
	"""reduceString - Go through the string and eliminate case switching adjacent characters.
	Removes aA or Aa.
	Doesn't remove aa or AA.
	Repeatedly goes through the string until no more reductions can be made
	returns shortened string
	"""
	currentColumn = 0
	newString = ''
	changesFound = True
	while changesFound:
		changesFound = False
		while currentColumn < len(polymereString):
			if matchCheck(polymereString[currentColumn],polymereString[currentColumn+1]):
				currentColumn += 2
				changesFound = True
			else:
				newString += polymereString[currentColumn]
				currentColumn += 1
			if currentColumn == len(polymereString)-1:	# can't go past 1 from the last element
				newString += polymereString[currentColumn]
				break
		polymereString = newString
		newString = ''
		currentColumn = 0
	return polymereString
	
polymereString = readTextFileToString('input2.txt')
print 'Length of polymere before processing =',len(polymereString)
alphabet = list(string.ascii_lowercase)
newList = []
for letterInAlpha in alphabet:
	testString = removeLetterFromString(letterInAlpha,polymereString)
	newTestString = reduceString(testString)
	print letterInAlpha, len(newTestString)
	newListLine = []
	newListLine.append(letterInAlpha)
	newListLine.append(len(newTestString))
	newList.append(newListLine)
minVal = len(polymereString)
minLetter = ''
for line in newList:
	if line[1] < minVal:
		minVal = line[1]
		minLetter = line[0]
	
print 'Letter that results in the shortest polymer =',minLetter
print 'Shortest polymere with letter removed =',minVal

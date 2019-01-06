# Pt2-AoCDay14.py
# 2018 Advent of Code
# Day 14
# Part 2
# https://adventofcode.com/2018/day/14

import time
import re
import os

"""
--- Part Two ---

As it turns out, you got the Elves' plan backwards. 
They actually want to know how many recipes appear on the scoreboard to the left of the first recipes whose scores are the digits from your puzzle input.

    51589 first appears after 9 recipes.
    01245 first appears after 5 recipes.
    92510 first appears after 18 recipes.
    59414 first appears after 2018 recipes.

How many recipes appear on the scoreboard to the left of the score sequence in your puzzle input?

"""

#####################################################################################
## Functions which deal in general with programming tasks

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	exit()

#####################################################################################
## 

########################################################################
## This is the workhorse of this assignment

def checkForEndCondition(endString,recipeList):
	debug_checkForEndCondition = False
	if debug_checkForEndCondition:
		print '\ncheckForEndCondition: reached function'
	if len(recipeList) < len(endString):
		if debug_checkForEndCondition:
			print 'checkForEndCondition: too short to compare'
		return False
	offsetToLastRecipeCharacters = len(recipeList) - len(endString)
	if debug_checkForEndCondition:
		print 'checkForEndCondition: Checking for endString',endString
		print 'checkForEndCondition: recipe list',recipeList
		print 'checkForEndCondition: offsetToLastRecipeCharacters',offsetToLastRecipeCharacters
	for offset in xrange(len(endString)):
		#print 'checkForEndCondition: comparing',endString[offset],'to',recipeList[offsetToLastRecipeCharacters]
		if int(endString[offset]) != int(recipeList[offsetToLastRecipeCharacters]):
			if debug_checkForEndCondition:
				print 'checkForEndCondition: mismatch',offsetToLastRecipeCharacters
			return False
		offsetToLastRecipeCharacters += 1
	if debug_checkForEndCondition:
		print 'checkForEndCondition: matched'
	return True

########################################################################
## Code

print 'Starting Processing',time.strftime('%X %x %Z')

elf1Offset = 0
elf2Offset = 1

#lookingForString = '51589'
#lookingForString = '01245'
#lookingForString = '59414'
#lookingForString = '92510'
lookingForString = '110201'

recipeList = [3,7]
keepLooping = True
while keepLooping:
	newRecipe = recipeList[elf1Offset] + recipeList[elf2Offset]
	if newRecipe >= 10:
		recipe10sDigit = newRecipe/10
		recipe1sDigit = newRecipe % 10
		recipeList.append(recipe10sDigit)
		recipeList.append(recipe1sDigit)
	else:
		recipeList.append(newRecipe)
	listLength = len(recipeList)
	elf1Offset = (elf1Offset + 1 + recipeList[elf1Offset]) % listLength
	elf2Offset = (elf2Offset + 1 + recipeList[elf2Offset]) % listLength

	if checkForEndCondition(lookingForString,recipeList):
		print 'Input',lookingForString,'reached at',listLength-len(lookingForString),'recipes'
		break

print 'Finished processing',time.strftime('%X %x %Z')


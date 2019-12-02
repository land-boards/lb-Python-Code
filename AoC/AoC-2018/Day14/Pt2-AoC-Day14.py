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

Your puzzle answer was 20291131.

That's the right answer! You are one gold star closer to fixing the time stream.

Code below produces a result 1 too high.

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

def checkForEndCondition(endString,recipeList,ob1):
	debug_checkForEndCondition = False
	if len(recipeList) < len(endString):
		if debug_checkForEndCondition:
			print 'checkForEndCondition: too short to compare'
		return False
	offsetToLastRecipeCharacters = len(recipeList) - len(endString) + ob1
	if debug_checkForEndCondition:
		print '\ncheckForEndCondition: reached function ob1',ob1
		print 'checkForEndCondition: Checking for endString',endString
		print 'checkForEndCondition: recipe list',recipeList
		print 'checkForEndCondition: offsetToLastRecipeCharacters',offsetToLastRecipeCharacters
	for offset in xrange(len(endString)):
		if debug_checkForEndCondition:
			print 'checkForEndCondition: comparing',endString[offset],'to',recipeList[offsetToLastRecipeCharacters]
		if int(endString[offset]) != int(recipeList[offsetToLastRecipeCharacters]):
			if debug_checkForEndCondition:
				print 'checkForEndCondition: mismatch',offsetToLastRecipeCharacters
			return False
		offsetToLastRecipeCharacters += 1
	if debug_checkForEndCondition:
		print 'checkForEndCondition: matched'
	return True

def findPatternInRecipes(lookingForString):
	"""findPatternInRecipes - Make the recipes and call function to look for end condition
	
	:param lookingForString: The test string I am looking for
	"""
	elf1Offset = 0
	elf2Offset = 1

	recipeList = [3,7]		# seed of the list
	listLength = 2
	while True:
		newRecipe = recipeList[elf1Offset] + recipeList[elf2Offset]
		if newRecipe < 10:
			recipeList.append(newRecipe)
			listLength += 1
		else:
			recipeList.append(newRecipe/10)
			recipeList.append(newRecipe % 10)
			listLength += 2
		elf1Offset = (elf1Offset + 1 + recipeList[elf1Offset]) % listLength
		elf2Offset = (elf2Offset + 1 + recipeList[elf2Offset]) % listLength

		if checkForEndCondition(lookingForString,recipeList,0):
			print 'Input',lookingForString,'reached at',listLength-len(lookingForString),'recipes'
			return listLength-len(lookingForString)

		if checkForEndCondition(lookingForString,recipeList,-1):
			print 'Input',lookingForString,'reached at',listLength-len(lookingForString),'recipes'
			return listLength-len(lookingForString)-1

########################################################################
## Code

print 'Starting Processing',time.strftime('%X %x %Z')

lookingForString = '110201'

if findPatternInRecipes('01245') != 5:
	print 'main: test case 01245 failed'
	exit()
if findPatternInRecipes('51589') != 9:
	print 'main: test case 51589 failed'
	exit()
if findPatternInRecipes('59414') != 2018:
	print 'main: test case 59414 failed'
	exit()
if findPatternInRecipes('92510') != 18:
	print 'main: test case 92510 failed'
	exit()
print 'main: all example tests passed'
findPatternInRecipes('110201')

print 'Finished processing',time.strftime('%X %x %Z')


# Pt2-AoCDay3.py
# 2019 Advent of Code
# Day 3
# Part 2

"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 125730-579381.
6655 is too high
2081 is the right answer

--- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
How many different passwords within the range given in your puzzle input meet all of the criteria?

1015 is too low
val 566777 should have been ok
val 566688 should have been ok

1862 is too high
577999 should have been OK since there is a pair in there

1063 is too low

1167 is not right

1652 is not right

1411 is correct

"""
from __future__ import print_function

def makeListFromInt(val):
	""" Turn an integer into a list of digits
	"""
	digitString=str(val)
	resultList = []
	for charVal in digitString:
		resultList.append(charVal)
	return resultList

def hasAscendingChars(digitString):
	""" All of the digits should be the same or ascending
	:returns: False if any digits is descending
	"""
	for i in range(len(digitString)-1):
		if digitString[i]>digitString[i+1]:
			return False
	return True
	
def countPairs(stringVal):
	""" Precisely count the exact number of pairs where pairs are two adjacent same with no other same of the number.
	There can be multiple pairs that are different numbers.
	"""
	pairCount = 0
	if                                    ((stringVal[0] == stringVal[1]) and (stringVal[1] != stringVal[2])):
		pairCount = pairCount + 1
	if ((stringVal[0] != stringVal[1]) and (stringVal[1] == stringVal[2]) and (stringVal[2] != stringVal[3])):
		pairCount = pairCount + 1
	if ((stringVal[1] != stringVal[2]) and (stringVal[2] == stringVal[3]) and (stringVal[3] != stringVal[4])):
		pairCount = pairCount + 1
	if ((stringVal[2] != stringVal[3]) and (stringVal[3] == stringVal[4]) and (stringVal[4] != stringVal[5])):
		pairCount = pairCount + 1
	if ((stringVal[3] != stringVal[4]) and (stringVal[4] == stringVal[5])):
		pairCount = pairCount + 1
	return pairCount
	
###################################################################################

startVal = 125730
endVal = 579381

passwordsCount = 0
val = startVal
while (val < endVal):
	myList = makeListFromInt(val)
	if hasAscendingChars(myList):
		pairCount = countPairs(myList)
		if pairCount != 0:
			print("First pass possible value :",val)
			passwordsCount = passwordsCount + 1
	val = val + 1
print("Count :",passwordsCount)

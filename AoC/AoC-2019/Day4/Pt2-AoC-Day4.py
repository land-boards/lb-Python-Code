# Pt2-AoCDay3.py
# 2019 Advent of Code
# Day 3
# Part 1
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
1862 is too high

val 566777 should have been ok
val 566688 should have been ok
"""
from __future__ import print_function

def makeListFromInt(val):
	digitString=str(val)
	resultList = []
	for charVal in digitString:
		resultList.append(charVal)
	return resultList

def checkPassword(digitString):
	if (digitString[0]>digitString[1]):
		return False
	if (digitString[1]>digitString[2]):
		return False
	if (digitString[2]>digitString[3]):
		return False
	if (digitString[3]>digitString[4]):
		return False
	if (digitString[4]>digitString[5]):
		return False

	if (digitString[0]==digitString[1]):
		return True
	if (digitString[1]==digitString[2]):
		return True
	if (digitString[2]==digitString[3]):
		return True
	if (digitString[3]==digitString[4]):
		return True
	if (digitString[4]==digitString[5]):
		return True
		
	return False
		
def checkLonger(stringVal):
	if ((stringVal[0] == stringVal[1]) and (stringVal[1] == stringVal[2])):
		print("Failed first three digits the same")
		return False
	if ((stringVal[1] == stringVal[2]) and (stringVal[2] == stringVal[3])):
		print("Failed second three digits the same")
		return False
	if ((stringVal[2] == stringVal[3]) and (stringVal[3] == stringVal[4])):
		print("Failed third three digits the same")
		return False
	if ((stringVal[3] == stringVal[4]) and (stringVal[4] == stringVal[5])):
		print("Failed third three digits the same")
		return False
	return True

def checkForPair(stringVal):
	if ((stringVal[0] == stringVal[1]) and (stringVal[1] != stringVal[2])):
		print("Found pair at first position")
		return True
	if ((stringVal[1] == stringVal[2]) and (stringVal[2] != stringVal[3])):
		print("Found pair at second position")
		return True
	if ((stringVal[2] == stringVal[3]) and (stringVal[3] != stringVal[4])):
		print("Found pair at third position")
		return True
	if ((stringVal[3] == stringVal[4]) and (stringVal[4] != stringVal[5])):
		print("Found pair at 4th position")
		return True
	return False

###################################################################################

startVal = 125730
endVal = 579381

passwordsCount = 0
val = startVal
while (val < endVal):
	myList = makeListFromInt(val)
	if checkPassword(myList):
		print("First pass value",val)
		if checkLonger(myList):
			passwordsCount = passwordsCount + 1
		else:
			if checkForPair(myList):
				passwordsCount = passwordsCount + 1				
	val = val + 1
print("Count :",passwordsCount)

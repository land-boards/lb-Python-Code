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

"""
from __future__ import print_function

def checkPassword(val):
	digitString=str(val)
	
	digit0=int(digitString[0])
	#print("digit0",digit0)
	digit1=int(digitString[1])
	#print("digit1",digit1)
	digit2=int(digitString[2])
	#print("digit2",digit2)
	digit3=int(digitString[3])
	#print("digit3",digit3)
	digit4=int(digitString[4])
	#print("digit4",digit4)
	digit5=int(digitString[5])
	#print("digit5",digit5)
	
	if (digit0>digit1):
		return False
	if (digit1>digit2):
		return False
	if (digit2>digit3):
		return False
	if (digit3>digit4):
		return False
	if (digit4>digit5):
		return False

	if (digit0==digit1):
		return True
	if (digit1==digit2):
		return True
	if (digit2==digit3):
		return True
	if (digit3==digit4):
		return True
	if (digit4==digit5):
		return True
		
	return False
		
###################################################################################

startVal = 125730
endVal = 579381

passwordsCount = 0
val = startVal
while (val < endVal):
	if checkPassword(val):
		print("pass value",val)
		passwordsCount = passwordsCount + 1
	val = val + 1
print("Count :",passwordsCount)
	
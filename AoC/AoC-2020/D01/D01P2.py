# D01P2.py
# 2020 Advent of Code
# Day 1
# Part 2

"""
"""

import time

startTime = time.time()

# open file and read the content into an accumulated sum
newList = []
with open('input.txt', 'r') as filehandle:
	for lineIn in filehandle:
		newList.append(int(lineIn.strip()))
print('newList',newList)

desiredNumber = 2020

for numVal in newList:
	lookingFor = desiredNumber - numVal
	for x in newList:
		for y in newList:
			if x+y == lookingFor:
				print(numVal*x*y)
				endTime = time.time()
				print('time',endTime-startTime)
				exit()
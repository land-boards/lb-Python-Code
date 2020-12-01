# D01P1.py
# 2020 Advent of Code
# Day 1
# Part 1

"""
"""

# open file and read the content into an accumulated sum
newList = []
with open('input.txt', 'r') as filehandle:  
	for lineIn in filehandle:
		newList.append(int(lineIn.strip()))
print('newList',newList)

desiredNumber = 2020

for numVal in newList:
	lookingFor = desiredNumber-numVal
	for checkVal in newList:
		if checkVal == lookingFor:
			print(numVal*checkVal)

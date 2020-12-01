# D01P2.py
# 2020 Advent of Code
# Day 1
# Part 2

"""
"""

def product2(x,y):
	return x+y

# open file and read the content into an accumulated sum
newList = []
with open('input.txt', 'r') as filehandle:  
	for lineIn in filehandle:
		newList.append(int(lineIn.strip()))
print('newList',newList)

desiredNumber = 2020

for numVal in newList:
	lookingFor = desiredNumber-numVal
	for x in newList:
		for y in newList:
			checkVal = product2(x,y)
			if checkVal == lookingFor:
				print(numVal*x*y)

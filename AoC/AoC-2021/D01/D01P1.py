# D01P1.py
# 2021 Advent of Code
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

incrCount = 0
for numOffset in range(len(newList)-1):
	currNum = newList[numOffset]
	nextNum = newList[numOffset+1]
	if nextNum > currNum:
		incrCount += 1
print("incrCount",incrCount)
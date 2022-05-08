# D01P2.py
# 2021 Advent of Code
# Day 1
# Part 2

"""
"""

import time

# At start
startTime = time.time()

# open file and read the content into an accumulated sum
newList = []
with open('input.txt', 'r') as filehandle:  
	for lineIn in filehandle:
		newList.append(int(lineIn.strip()))
#print('newList',newList)

avgList = []
for numOffset in range(len(newList)-2):
	firstNum = newList[numOffset]
	secondNum = newList[numOffset+1]
	thirdNum = newList[numOffset+2]
	sumOfNums = firstNum + secondNum + thirdNum
	avgList.append(sumOfNums)
print("avgList",avgList)
incrCount = 0
for numOffset in range(len(avgList)-1):
	if avgList[numOffset+1] > avgList[numOffset]:
		incrCount += 1
print("incrCount",incrCount)

# At end
endTime = time.time()
print('time',endTime-startTime)

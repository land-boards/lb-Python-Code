# DXXP1.py
# 2021 Advent of Code
# Day XX
# Part 1

import time

# At start
startTime = time.time()

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings('input.txt')
print(inList)
for row in inList:
	print(row)


endTime = time.time()
print('time',endTime-startTime)

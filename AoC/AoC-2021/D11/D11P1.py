# D11P1.py
# 2021 Advent of Code
# Day 11
# Part 1

def readFileToList(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	return inList

inList = readFileToList("input.txt")

# print("inList",inList)

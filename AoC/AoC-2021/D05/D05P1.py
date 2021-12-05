# D04P1.py
# 2021 Advent of Code
# Day 4
# Part 1

# readFileOfStringsToListOfLists
def readFileOfStringsToListOfLists():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(list(inLine))
	return inList


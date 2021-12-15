# DXXP1.py
# 2021 Advent of Code
# Day XX
# Part 1

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



# D08P1.py
# 2021 Advent of Code
# Day 8
# Part 1
# 499 is too high

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings('input.txt')
# print(inList)
# for row in inList:
	# print(row)

newList = []
for row in inList:
	row1 = row.replace(' | ','|')
	newRow = row1.split('|')
	# print("newRow",newRow)
	newList.append(newRow)

print("newList")
countVals = 0
for row in newList:
	#print(row[1])
	newRow = row[1].split(' ')
	print("newRow",newRow)
	for rowElement in newRow:
		rowLen = len(rowElement)
		if (rowLen == 2) or (rowLen == 4) or (rowLen == 3) or (rowLen == 7):
			countVals += 1
print("countVals",countVals)

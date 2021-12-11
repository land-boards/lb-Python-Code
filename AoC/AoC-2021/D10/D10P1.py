# D10P1.py
# 2021 Advent of Code
# Day 10
# Part 1
# 323634 is too low

def readFileOfStringsToListOfLists(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	return inList

def reduceList(inStr):
	# First cut at removing paired reductions
	# Loop until no more paired reductions can be done
	moreToDo = True
	while moreToDo:
		beforeLen = len(inStr)
		inStr = inStr.replace("()","")
		inStr = inStr.replace("[]","")
		inStr = inStr.replace("{}","")
		inStr = inStr.replace("<>","")
		afterLen = len(inStr)
		if beforeLen == afterLen:
			moreToDo = False
	return inStr

inList = readFileOfStringsToListOfLists("input.txt")

# print("inList",inList)

total = 0
for inLine in inList:
	print(inLine)
	curveCount = 0
	curlyCount = 0
	squareCount = 0
	ltgtCount = 0
	inLine1 = reduceList(inLine)
	for charIn in inLine1:
		print(charIn,end='')
		gotClosing = False
		if charIn == ')':
			total += 3
			gotClosing = True
		elif charIn == ']':
			total += 57
			gotClosing = True
		elif charIn == '}':
			total += 1197
			gotClosing = True
		elif charIn == '>':
			ltgtCount -= 1
			total += 25137
			gotClosing = True
		if gotClosing:
			break

print("\ntotal",total)

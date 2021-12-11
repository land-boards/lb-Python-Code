# D10P2.py
# 2021 Advent of Code
# Day 10
# Part 2
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

def reverseString(x):
  return x[::-1]

def scoreString(inStr):
	total = 0
	for inChar in inStr:
		total *= 5
		if inChar == ')':
			total += 1
		elif inChar == ']':
			total += 2
		elif inChar == '}':
			total += 3
		elif inChar == '>':
			total += 4
	return total

inList = readFileOfStringsToListOfLists("input.txt")

# print("inList",inList)

newList = []
for inLine in inList:
	#print(inLine)
	inLine1 = reduceList(inLine)
	for charIn in inLine1:
		gotClosing = False
		if charIn == ')':
			gotClosing = True
		elif charIn == ']':
			gotClosing = True
		elif charIn == '}':
			gotClosing = True
		elif charIn == '>':
			gotClosing = True
		if gotClosing:
			break
	if not gotClosing:
		newList.append(inLine1)

print("newList")
score = []
for line in newList:
	# print(line)
	revStr = reverseString(line)
	revStr = revStr.replace('(',')')
	revStr = revStr.replace('[',']')
	revStr = revStr.replace('{','}')
	revStr = revStr.replace('<','>')
	print(revStr)
	scoreVal = scoreString(revStr)
	score.append(scoreVal)
score.sort()
print(score)
scoreLen = len(score)
print(scoreLen)
median = int(scoreLen/2)
print("median",median)
print("score median",score[median])

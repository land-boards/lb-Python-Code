# D20P1.py
# 2021 Advent of Code
# Day 2P
# Part 1

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList


def padArray(arrayIn,padChar):
	arrayOut = []
	arrayWidthPlusPad = len(arrayIn[0]) + 2
	arrayHeight = len(arrayIn)
	newRow = []
	for charVal in range(arrayWidthPlusPad):
		newRow.append(padChar)
	arrayOut.append(newRow)
	for row in arrayIn:
		newRow = []
		newRow.append(padChar)
		for charVal in row:
			newRow.append(charVal)
		newRow.append(padChar)
		arrayOut.append(newRow)
	newRow = []
	for charVal in range(arrayWidthPlusPad):
		newRow.append(padChar)
	arrayOut.append(newRow)
	return arrayOut	

def convertPointToNumber(charVal):
	if charVal == '.':
		return 0
	elif charVal == '#':
		return 1
	
def getValAtPoint(xLoc,yLoc,arrayIn):
	val = 0
	for yVal in range(-1,2):
		for xVal in range(-1,2):
			val = val * 2 + convertPointToNumber(arrayIn[yLoc+yVal][xLoc+xVal])
	# print(xVal,yVal,val)
	return val

inList = readFileToListOfStrings('input.txt')

decoder = inList[0]
puzzleRaw = inList[2:]
puzzle = []
for row in puzzleRaw:
	newRow = []
	for char in row:
		newRow.append(char)
	puzzle.append(newRow)

# print("decoder",decoder)
# print("puzzle")
# for row in puzzle:
	# print(row)

paddedPuzzle = padArray(puzzle,'.')
paddedPuzzle = padArray(paddedPuzzle,'.')
paddedPuzzle = padArray(paddedPuzzle,'.')
paddedPuzzle = padArray(paddedPuzzle,'.')

print("paddedPuzzle")
for row in paddedPuzzle:
	print(row)

count = 0
loopCount = 2
while loopCount > 0:
	newPuzzle = []
	for yVal in range(1,len(paddedPuzzle)-1):
		puzzleRow = []
		for xVal in range(1,len(paddedPuzzle[0])-1):
			val = getValAtPoint(xVal,yVal,paddedPuzzle)
			newVal = decoder[val]
			# print("x,y,val",xVal,yVal,val,newVal)
			puzzleRow.append(newVal)
		newPuzzle.append(puzzleRow)
	print("newPuzzle")
	for row in newPuzzle:
		for  charVal in row:
			print(charVal,end='')
		print()
	paddedPuzzle = newPuzzle
	loopCount -= 1
	
for row in newPuzzle:
	for  charVal in row:
		print(charVal,end='')
		if charVal == '#':
			count += 1
	print()

print("count",count)

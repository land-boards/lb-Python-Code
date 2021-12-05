# D04P2.py
# 2021 Advent of Code
# Day 4
# Part 2

# readFileToListOfStrings
def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def checkNumOnBoards(checkVal):
	for boardNum in range(len(allBoards)):
		for lineNum in range(5):
			for colNum in range(5):
				if allBoards[boardNum][lineNum][colNum] == checkVal:
					solvedBoardArray[boardNum][lineNum][colNum] = 'yes'

def checkSolvedYet():
	for boardNum in range(len(allBoards)):
		for lineNum in range(5):
			lineSolved = True
			for colNum in range(5):
				if solvedBoardArray[boardNum][lineNum][colNum] != 'yes':
					lineSolved = False
			if lineSolved:
				if boardNum not in listOfSolvedBoards:
					listOfSolvedBoards.append(boardNum)
		for colNum in range(5):
			colSolved = True
			for lineNum in range(5):
				if solvedBoardArray[boardNum][lineNum][colNum] != 'yes':
					colSolved = False
			if colSolved:
				if boardNum not in listOfSolvedBoards:
					listOfSolvedBoards.append(boardNum)

def sumBoard(boardNum):
	sum = 0
	for lineNum in range(5):
		for colNum in range(5):
			if solvedBoardArray[boardNum][lineNum][colNum] == 'no':
				sum += int(allBoards[boardNum][lineNum][colNum])
	return sum

inList = readFileToListOfStrings('input.txt')
# print(inList)
# for row in inList:
	# print(row)

pulledNums = inList[0].split(',')
print("pulledNums")
print(pulledNums)

boardNum = 0
# print("boardNum",boardNum)

board = []
solvedBoard = []
allBoards = []
solvedBoardArray = []
for row in inList[2:]:
	if row == '':
		allBoards.append(board)
		solvedBoardArray.append(solvedBoard)
		board = []
		solvedBoard = []
		boardNum += 1
	else:
		if row[0] == ' ':
			row = row[1:]
		row = row.replace('  ',' ')
		newRow = row.split(' ')
		board.append(newRow)
		solvedBoard.append(['no','no','no','no','no'])
print("Each board ")
print("allBoards",allBoards)
print("Boards",len(allBoards))
lastNumChecked = 0
listOfSolvedBoards = []
for checkNum in pulledNums:
	print("Checking number",checkNum)
	checkNumOnBoards(checkNum)
	checkSolvedYet()
	lastNumChecked = int(checkNum)
	# Run once without the next three lines to find the last winning board
	# Pull last solved board then hardcode below to stop when solved
	if listOfSolvedBoards != []:
		if listOfSolvedBoards[-1]== 31:
			break

print(listOfSolvedBoards)
print("Solved, last number checked",lastNumChecked,"board",listOfSolvedBoards)

lastSolvedBoard = listOfSolvedBoards[-1]
print("lastSolvedBoards",lastSolvedBoard)

print("solvedBoardArray",solvedBoardArray[lastSolvedBoard])

sum = sumBoard(lastSolvedBoard)
print("sum",sum)
product = sum * lastNumChecked
print("product",product)

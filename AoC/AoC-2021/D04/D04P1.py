# D04P1.py
# 2021 Advent of Code
# Day 4
# Part 1
# 4608 is too low

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
				print("BINGO: ",end='')
				return boardNum
		for colNum in range(5):
			colSolved = True
			for lineNum in range(5):
				if solvedBoardArray[boardNum][lineNum][colNum] != 'yes':
					colSolved = False
			if colSolved:
				print("BINGO: ",end='')
				return boardNum
	#print("Not yet BINGO",)
	return -1

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
for checkNum in pulledNums:
	print("Checking number",checkNum)
	checkNumOnBoards(checkNum)
	boardNumber = checkSolvedYet()
	if boardNumber != -1:
		lastNumChecked = int(checkNum)
		break
print("Solved, last number checked",lastNumChecked,"board",boardNumber)
for row in range(5):
	print(solvedBoardArray[boardNumber][row])
for row in range(5):
	print(allBoards[boardNumber][row])

sum = sumBoard(boardNumber)
print("sum",sum)
product = sum * lastNumChecked
print("product",product)

# D23P2.py
# 2021 Advent of Code
# Day 23
# Part 2
# 41213 is too low
# Clear B column first didn't work

import random

# print(random.randrange(1, 10))

def readFileOfStringsToListOfLists(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip('\n')
			inList.append(list(inLine))
	return inList

def printBoard(inList):
	colNum = 0
	print("\n   ",end='')
	for col in range(len(inList[0])):
		print(int(col/10),end='')
	print("\n   ",end='')
	for col in range(len(inList[0])):
		print(col%10,end = '')
	print()
	rowNum = 0
	for row in inList:
		print(rowNum,end='  ')
		for col in row:
			print(col,end='')
		print()
		rowNum += 1

def findAllMovablePieces(board):
	moveablePieces = []
	yVal = 1
	for xVal in range(1,12):
		if 'A' <= board[yVal][xVal] <= 'D':
			if board[yVal][xVal-1] == '.' or board[yVal][xVal+1] == '.':
				char = board[yVal][xVal]
				moveablePieces.append([char,xVal,yVal])
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					char = board[yVal][xVal]
					moveablePieces.append([char,xVal,yVal])
	return moveablePieces

def findLegalMovesToHomeRow(x,y,list):
	legalMovesToHomeRow = []
	if y > 1:
		xPos = x-1
		while list[1][xPos] == '.':
			# print("xPos(1)",xPos)
			legalMovesToHomeRow.append([xPos,1])
			if xPos > 3:
				xPos -= 2
			elif xPos == 2:
				xPos = 1
			else:
				break
	if y > 1:
		xPos = x+1
		while list[1][xPos] == '.':
			# print("xPos(2)",xPos)
			legalMovesToHomeRow.append([xPos,1])
			if xPos == 10:
				xPos = 11
			elif xPos > 3 and xPos < 11:
				xPos += 2
			else:
				break
	return legalMovesToHomeRow

def findLegalMovesToDestColumns(x,y,list):
	   # 0123456789012
	# 0  #############
	# 1  #...........#
	# 2  ###B#B#D#D###
	# 3    #D#C#B#A#
	# 4    #D#B#A#C#
	# 5    #C#A#A#C#
	# 6    #########
	checkLetter = list[y][x]
	if checkLetter == 'A':
		xOffset = 3
	elif checkLetter == 'B':
		xOffset = 5
	elif checkLetter == 'C':
		xOffset = 7
	elif checkLetter == 'D':
		xOffset = 9
	else:
		assert False,"Huh?"
	# print("xOffset",xOffset)
	if list[5][xOffset] == '.':
		return [[xOffset,5]]
	if list[5][xOffset] != checkLetter:
		return []
	if list[4][xOffset] == '.':
		return [[xOffset,4]]
	if list[4][xOffset] != checkLetter:
		return []
	if list[3][xOffset] == '.':
		return [[xOffset,y]]
	if list[3][xOffset] != checkLetter:
		return []
	if list[2][xOffset] == '.':
		return [[xOffset,2]]
	if list[2][xOffset] != checkLetter:
		return []
	assert False,"weirdness"

def findAllLegalMoves(x,y,list):
	legalMovesToDestColumns = findLegalMovesToDestColumns(x,y,list)
	if legalMovesToDestColumns != []:
		print("findAllLegalMoves: found legal moves to dest columns")
		return legalMovesToDestColumns
	legalMovesToHomeRow = findLegalMovesToHomeRow(x,y,list)
	if legalMovesToHomeRow == []:
		# print("findAllLegalMoves: No legal moves for ",list[y][x])
		return []
	return legalMovesToHomeRow

def checkBoardLocked(inList):
	allMoveablePieces = findAllMovablePieces(inList)
	if allMoveablePieces == []:
		return False
	# print("checkBoardLocked: Still have pieces that can be moved")
	for pieceToMove in allMoveablePieces:
		x = pieceToMove[1]
		y = pieceToMove[2]
		legalMoves = findAllLegalMoves(x,y,inList)
		if legalMoves != []:
			# print("checkBoardLocked: Legal moves",legalMoves)
			return False
	# print("checkBoardLocked: Board is Locked up for moves")
	return True

def checkBoardSolved(inList):
	return

boardSolved = False
while not boardSolved:
	inList = readFileOfStringsToListOfLists('input.txt')
	score = 0
	moveablePieces = findAllMovablePieces(inList)
	print("Before moves")
	printBoard(inList)
	boardLocked = False
	while not boardLocked:
		printBoard(inList)
		pieceToMoveOffset = random.randrange(0,len(moveablePieces))
		
		# print("main: Moving from",moveablePieces[pieceToMoveOffset])
		x = moveablePieces[pieceToMoveOffset][1]
		y = moveablePieces[pieceToMoveOffset][2]
		legalMoves = findAllLegalMoves(x,y,inList)
		if legalMoves != []:
			print("main: legalMoves",legalMoves)
			destOffset = random.randrange(0,len(legalMoves))
			# print("main: moving to",legalMoves[destOffset])
			moveablePieces[pieceToMoveOffset][1]
			pickUpPiece = inList[y][x]
			inList[y][x] = '.'
			inList[legalMoves[destOffset][1]][legalMoves[destOffset][0]] = pickUpPiece
			moveablePieces = findAllMovablePieces(inList)
			# print("moveablePieces",moveablePieces,"\n")
		boardLocked = checkBoardLocked(inList)
	print("After moves")
	printBoard(inList)
	print("***********************************************")
	# quit()

print("score",score)

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

def findMoveablePiecesInHomeRow(board):
	moveablePieces = []
	yVal = 1
	for xVal in range(1,12):
		if 'A' <= board[yVal][xVal] <= 'D':
			if board[yVal][xVal-1] == '.' or board[yVal][xVal+1] == '.':
				char = board[yVal][xVal]
				moveablePieces.append([char,xVal,yVal])
	return moveablePieces

def isValTopAlreadyAtDestTop(xVal,yVal,board):
	print("isValTopAlreadyAtDestTop: xVal,yVal",xVal,yVal)
	charTestVal = board[yVal][xVal]
	if xVal == 3:
		charExectedVal = 'A'
	elif xVal == 5:
		charExectedVal = 'B'
	elif xVal == 7:
		charExectedVal = 'C'
	elif xVal == 9:
		charExectedVal = 'D'
	for yOff in range(yVal,6):
		if board[yOff] != charExectedVal:
			return False
	return True

def shouldPieceBeMovedFromColumn(xVal,yVal,board):
	# print("shouldPieceBeMovedFromColumn: xVal,yVal",xVal,yVal)
	charMovingMaybe = board[yVal][xVal]
	if (charMovingMaybe == 'A') and (yVal != 3):
		return True
	if (charMovingMaybe == 'B') and (yVal != 5):
		return True
	if (charMovingMaybe == 'C') and (yVal != 7):
		return True
	if (charMovingMaybe == 'D') and (yVal != 9):
		return True
	if isValTopAlreadyAtDestTop(xVal,yVal,board):
		return False
	return True

def findMoveablePiecesInLowerColumns(board):
	moveablePieces = []
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					if shouldPieceBeMovedFromColumn(xVal,yVal,board):
						# print("findMoveablePiecesInLowerColumns: adding xVal,yVal",xVal,yVal)
						char = board[yVal][xVal]
						moveablePieces.append([char,xVal,yVal])
	return moveablePieces

def findAllMovablePieces(board):
	moveablePieces = findMoveablePiecesInLowerColumns(board)
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
		return [[xOffset,3]]
	if list[3][xOffset] != checkLetter:
		return []
	if list[2][xOffset] == '.':
		return [[xOffset,2]]
	if list[2][xOffset] != checkLetter:
		return []
	assert False,"weirdness"

def findAllLegalMoves(x,y,list):
	if y == 1:
		return findLegalMovesToDestColumns(x,y,list)
	else:
		return findLegalMovesToHomeRow(x,y,list)

def checkBoardLocked(board):
	print("checkBoardLocked: reached function")
	moveableHomeRowPieces = findMoveablePiecesInHomeRow(board)
	if moveableHomeRowPieces == []:
		print("checkBoardLocked: No moveable pieces in the home row")
	else:
		print("checkBoardLocked: Moveable pieces in the home row",moveableHomeRowPieces)
		noDestsForHome = True
		for moveablePiece in moveableHomeRowPieces:
			if findLegalMovesToDestColumns(moveablePiece[1],moveablePiece[2],board) != []:
				print("checkBoardLocked: Still can move from home row")
				return False
		print("checkBoardLocked: No place to move home row pieces")
	moveableColumnPieces = findMoveablePiecesInLowerColumns(board)
	if moveableColumnPieces == []:
		print("checkBoardLocked: No moveable pieces in column")
	else:
		print("checkBoardLocked: Moveable pieces in column",moveableColumnPieces)
		for moveablePiece in moveableColumnPieces:
			if findLegalMovesToHomeRow(moveablePiece[1],moveablePiece[2],board) != []:
				print("checkBoardLocked: Still can move from columns")
				return False
		print("checkBoardLocked: No place to move column pieces")
	return True
		
def checkBoardSolved(inList):
	if inList == []:
		return False
	if inList[3][2] != 'A':
		return False
	elif inList[3][3] != 'A':
		return False
	elif inList[3][4] != 'A':
		return False
	elif inList[3][5] != 'A':
		return False
		
	if inList[5][2] != 'B':
		return False
	elif inList[5][3] != 'B':
		return False
	elif inList[5][4] != 'B':
		return False
	elif inList[5][5] != 'B':
		return False
	
	if inList[7][2] != 'C':
		return False
	elif inList[7][3] != 'C':
		return False
	elif inList[7][4] != 'C':
		return False
	elif inList[7][5] != 'C':
		return False
	
	if inList[9][2] != 'D':
		return False
	elif inList[9][3] != 'D':
		return False
	elif inList[9][4] != 'D':
		return False
	elif inList[9][5] != 'D':
		return False
		
	return True

def moveAllHomeRowPiecesToColumns(board):
	movedAPieceFromHomeRow = False
	moveablePieces = findMoveablePiecesInHomeRow(board)
	if moveablePieces == []:
		return movedAPieceFromHomeRow,board
	for pieceToMove in moveablePieces:
		print("moveAllHomeRowPiecesToColumns: Piece to move",pieceToMove)
		allLegalDest = 1(pieceToMove[1],pieceToMove[2],board)
		print("All dests",allLegalDest)
		if allLegalDest != []:
			board[allLegalDest[1]][allLegalDest[0]] = pieceToMove[0]
			board[pieceToMove[2]][pieceToMove[1]] = '.'
			movedAPieceFromHomeRow = True
	return movedAPieceFromHomeRow,board
	# quit()

def moveRandomPieceFromColumns(board):
	moveablePieces = findAllMovablePieces(board)
	# print("moveRandomPieceFromColumns: moveablePieces",moveablePieces)
	pieceToMoveOffset = random.randrange(0,len(moveablePieces))
	# print("moveRandomPieceFromColumns: Moving from",moveablePieces[pieceToMoveOffset])
	x = moveablePieces[pieceToMoveOffset][1]
	y = moveablePieces[pieceToMoveOffset][2]
	legalMoves = findAllLegalMoves(x,y,board)
	if legalMoves != []:
		# print("moveRandomPieceFromColumns: legalMoves",legalMoves)
		destOffset = random.randrange(0,len(legalMoves))
		# print("moveRandomPieceFromColumns: moving to",legalMoves[destOffset])
		moveablePieces[pieceToMoveOffset][1]
		pickUpPiece = board[y][x]
		board[y][x] = '.'
		board[legalMoves[destOffset][1]][legalMoves[destOffset][0]] = pickUpPiece
		moveablePieces = findAllMovablePieces(board)
	return board

# main follows
inList = []
while not checkBoardSolved(inList):
	inList = readFileOfStringsToListOfLists('input.txt')
	score = 0
	# print("Before moves")
	# printBoard(inList)
	while not checkBoardLocked(inList):
		printBoard(inList)
		movedAPieceFromHomeRow,inList = moveAllHomeRowPiecesToColumns(inList)
		inList = moveRandomPieceFromColumns(inList)
		
	print("After moves")
	printBoard(inList)
	print("***********************************************")
	# input("hit key")
	# quit()
	
printBoard(inList)
print("score",score)

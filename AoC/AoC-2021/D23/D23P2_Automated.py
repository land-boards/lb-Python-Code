# D23P2.py
# 2021 Advent of Code
# Day 23
# Part 2
# 41213 is too low
# Clear B column first didn't work

import random
import os
import time

# print(random.randrange(1, 10))

def readFileOfStringsToListOfLists(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip('\n')
			inList.append(list(inLine))
	return inList

def printBoard(inList):
	# os.system("cls")
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

def checkBoardLocked(board):
	# print("checkBoardLocked: reached function")
	moveableHomeRowPieces = findMoveablePiecesInHomeRow(board)
	if moveableHomeRowPieces == []:
		# print("checkBoardLocked: No moveable pieces in the home row")
		pass
	else:
		# print("checkBoardLocked: Moveable pieces in the home row",moveableHomeRowPieces)
		noDestsForHome = True
		for moveablePiece in moveableHomeRowPieces:
			if findLegalMovesToDestColumns(moveablePiece[1],moveablePiece[2],board) != []:
				# print("checkBoardLocked: Still can move from home row")
				return False
		# print("checkBoardLocked: No place to move home row pieces")
	moveableColumnPieces = findTopPiecesInColumns(board)
	if moveableColumnPieces == []:
		# print("checkBoardLocked: No moveable pieces in column")
		pass
	else:
		# print("checkBoardLocked: Moveable pieces in column",moveableColumnPieces)
		for moveablePiece in moveableColumnPieces:
			if findLegalMovesToHomeRow(moveablePiece[1],moveablePiece[2],board) != []:
				# print("checkBoardLocked: Still can move from columns")
				return False
		# print("checkBoardLocked: No place to move column pieces")
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
	# movedAPieceFromHomeRow = False
	moveablePieces = findMoveablePiecesInHomeRow(board)
	if moveablePieces == []:
		return board
		# return movedAPieceFromHomeRow,board
	for pieceToMove in moveablePieces:
		# print("moveAllHomeRowPiecesToColumns: Piece to move",pieceToMove)
		allLegalDest = findLegalMovesToDestColumns(pieceToMove[1],pieceToMove[2],board)
		# print("All dests",allLegalDest)
		if allLegalDest != []:
			for legalDests in allLegalDest:
				board[legalDests[1]][legalDests[0]] = pieceToMove[0]
				board[pieceToMove[2]][pieceToMove[1]] = '.'
				# movedAPieceFromHomeRow = True
	return board

def isColumnAtLeastPartlySolved(charExpectedVal,xOff,board):
	for yOff in range(2,6):
		charAtSpot = board[yOff][xOff]
		if (charAtSpot != charExpectedVal) and (charAtSpot != '.'):
			return False
	return True

valCharDict = {3:'A',5:'B',7:'C',9:'D'}

def isValAlreadyAtTop(xVal,yVal,board):
	# print("isValAlreadyAtTop: xVal,yVal",xVal,yVal)
	charExpectedVal = valCharDict[xVal]
	colPartlySolved = isColumnAtLeastPartlySolved(charExpectedVal,xVal,board)
	if colPartlySolved:
		# print("isValAlreadyAtTop: Partly solved char,xVal,yVal",board[yVal][xVal],xVal,yVal)
		return True
	else:
		# print("isValAlreadyAtTop: Not partly solved char,xVal,yVal",board[yVal][xVal],xVal,yVal)
		return False

charVal = {'A':3,'B':5,'C':7,'D':9}

def shouldPieceBeMovedFromColumn(xVal,yVal,board):
	# print("shouldPieceBeMovedFromColumn: xVal,yVal",xVal,yVal)
	# charMovingMaybe = board[yVal][xVal]
	# print("shouldPieceBeMovedFromColumn: charMovingMaybe",charMovingMaybe)
	# if charMovingMaybe != charVal[charMovingMaybe]:
		# print("shouldPieceBeMovedFromColumn: returning True (1)")
		# return True
	if isValAlreadyAtTop(xVal,yVal,board):
		# print("shouldPieceBeMovedFromColumn: returning False")
		return False
	# print("shouldPieceBeMovedFromColumn: returning True (2)")
	return True

def findTopPiecesInColumns(board):
	# Find the top elements in all the columns on the board
	# Doesn't validate that the element should or can be moved
	# Returns list of [char,xVal,yVal] elements
	topColumnValList = []
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					if shouldPieceBeMovedFromColumn(xVal,yVal,board):
						# print("findTopPiecesInColumns: adding xVal,yVal",xVal,yVal)
						char = board[yVal][xVal]
						topColumnValList.append([char,xVal,yVal])
	# print("findTopPiecesInColumns: topColumnValList",topColumnValList)
	return topColumnValList

def moveRandomPieceFromColumns(board):
	moveablePieces = findTopPiecesInColumns(board)
	# print("moveRandomPieceFromColumns: All top pieces",moveablePieces)
	if moveablePieces == []:
		# assert False,"moveRandomPieceFromColumns: no moveable pieces"
		return board
	pieceToMoveOffset = random.randrange(0,len(moveablePieces))
	# print("moveRandomPieceFromColumns: Moving from",moveablePieces[pieceToMoveOffset])
	x = moveablePieces[pieceToMoveOffset][1]
	y = moveablePieces[pieceToMoveOffset][2]
	legalMoves = findLegalMovesToHomeRow(x,y,board)
	if legalMoves != []:
		# print("moveRandomPieceFromColumns: legalMoves",legalMoves)
		randomDestOffset = random.randrange(0,len(legalMoves))
		# print("moveRandomPieceFromColumns: moving to",legalMoves[randomDestOffset])
		moveablePieces[pieceToMoveOffset][1]
		pickUpPiece = board[y][x]
		board[y][x] = '.'
		board[legalMoves[randomDestOffset][1]][legalMoves[randomDestOffset][0]] = pickUpPiece
	return board

def printMoves(movesList):
	print("movesList")
	for board in movesList:
		printBoard(board)

# main follows
board = readFileOfStringsToListOfLists('input.txt')
movesList = []
while not checkBoardSolved(board):
	board = readFileOfStringsToListOfLists('input.txt')
	score = 0
	movesList = []
	movesList.append(board)
	# printMoves(movesList)
	# print("Before moves")
	# printBoard(board)
	while not checkBoardLocked(board):
		# printBoard(board)
		# time.sleep(0.1)
		# Always move all pieces from home row if possible
		# movedAPieceFromHomeRow,board = moveAllHomeRowPiecesToColumns(board)
		board = moveAllHomeRowPiecesToColumns(board)
		# print("main: moved all home row pieces")
		# printBoard(board)
		if movesList[-1] != board:
			movesList.append(list(board))
		# printMoves(movesList)
		# Move a single piece from the columns to the home row
		board = moveRandomPieceFromColumns(board)
		# print("main: moved all column pieces")
		# printBoard(board)
		if movesList[-1] != board:
			movesList.append(list(board))
		# printMoves(movesList)
	# print("After moves")
	# printBoard(board)
	# time.sleep(0.5)
	# print("*****")
	# input("hit key")
	# quit()
	# printMoves(movesList)
	
print("\nmovesList")
for board in movesList:
	printBoard(board)
# print(movesList)
print("score",score)

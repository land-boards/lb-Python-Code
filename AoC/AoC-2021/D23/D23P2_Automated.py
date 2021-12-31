# D23P2.py
# 2021 Advent of Code
# Day 23
# Part 2
# 41213 is too low

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

def findAllPiecesInHomeRow(board):
	allPiecesInTopRow = []
	yVal = 1
	for xVal in range(1,12):
		if 'A' <= board[yVal][xVal] <= 'D':
			if board[yVal][xVal-1] == '.' or board[yVal][xVal+1] == '.':
				char = board[yVal][xVal]
				allPiecesInTopRow.append([char,xVal,yVal])
	return allPiecesInTopRow

letterToColDestDict = {'A':3,'B':5,'C':7,'D':9}

def pathIsOpen(piece,board):
	# piece [char,xVal,yVal]
	destCol = letterToColDestDict[piece[0]]
	startCol = piece[1]
	if startCol < destCol:
		for xOff in range(startCol+1,destCol+1):
			# print("pathIsOpen: ",board[1][xOff])
			if board[1][xOff] != '.':
				return False
		return True
	elif startCol > destCol:
		for xOff in range(startCol-1,destCol-1,-1):
			if board[1][xOff] != '.':
				return False
	else:
		assert False,"pathIsOpen: weirdness"

def findMoveablePiecesInHomeRow(board):
	allPiecesInTopRow = findAllPiecesInHomeRow(board)
	moveablePieces = []
	for piece in allPiecesInTopRow:
		if pathIsOpen(piece,board):
			moveablePieces.append(piece)
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
	if inList[2][3] != 'A':
		return False
	elif inList[3][3] != 'A':
		return False
	elif inList[4][3] != 'A':
		return False
	elif inList[5][3] != 'A':
		return False
		
	if inList[2][5] != 'B':
		return False
	elif inList[3][5] != 'B':
		return False
	elif inList[4][5] != 'B':
		return False
	elif inList[5][5] != 'B':
		return False
	
	if inList[2][7] != 'C':
		return False
	elif inList[3][7] != 'C':
		return False
	elif inList[4][7] != 'C':
		return False
	elif inList[5][7] != 'C':
		return False
	
	if inList[2][9] != 'D':
		return False
	elif inList[3][9] != 'D':
		return False
	elif inList[4][9] != 'D':
		return False
	elif inList[5][9] != 'D':
		return False
		
	return True

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
	xOffset = letterToColDestDict[checkLetter]
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

def moveAllHomeRowPiecesToColumns(board):
	moveablePieces = findMoveablePiecesInHomeRow(board)
	if moveablePieces == []:
		return board
	for pieceToMove in moveablePieces:
		# print("moveAllHomeRowPiecesToColumns: Piece to move",pieceToMove)
		allLegalDest = findLegalMovesToDestColumns(pieceToMove[1],pieceToMove[2],board)
		# print("All dests",allLegalDest)
		if allLegalDest != []:
			for legalDests in allLegalDest:
				board[legalDests[1]][legalDests[0]] = pieceToMove[0]
				board[pieceToMove[2]][pieceToMove[1]] = '.'
	return board

valCharDict = {3:'A',5:'B',7:'C',9:'D'}

def isValAlreadyAtTop(xVal,yVal,board):
	# print("isValAlreadyAtTop: xVal,yVal",xVal,yVal)
	charExpectedVal = valCharDict[xVal]
	for yOff in range(2,6):
		charAtSpot = board[yOff][xVal]
		if (charAtSpot != charExpectedVal) and (charAtSpot != '.'):
			return False
	return True
	colPartlySolved = isColumnAtLeastPartlySolved(charExpectedVal,xVal,board)
	if colPartlySolved:
		# print("isValAlreadyAtTop: Partly solved char,xVal,yVal",board[yVal][xVal],xVal,yVal)
		return True
	else:
		# print("isValAlreadyAtTop: Not partly solved char,xVal,yVal",board[yVal][xVal],xVal,yVal)
		return False

def findTopPiecesInColumns(board):
	# Find the top elements in all the columns on the board
	# Doesn't validate that the element should or can be moved
	# Returns list of [char,xVal,yVal] elements
	topColumnValList = []
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					if not isValAlreadyAtTop(xVal,yVal,board):
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

def printMoves():
	global movesList
	print("movesList")
	for board in movesList:
		printBoard(board)

def clearMovesList(board):
	global movesList
	movesList = []
	newBoard = []
	for row in board:
		newRow = []
		for col in row:
			newRow.append(col)
		newBoard.append(newRow)
	movesList.append(newBoard)

def addToMovesList(board):
	global movesList
	if board == movesList[-1]:
		return
	newBoard = []
	for row in board:
		newRow = []
		for col in row:
			newRow.append(col)
		newBoard.append(newRow)
	movesList.append(newBoard)

# main follows
board = readFileOfStringsToListOfLists('input.txt')
movesList = []
while not checkBoardSolved(board):
	board = readFileOfStringsToListOfLists('input.txt')
	score = 0
	clearMovesList(board)
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
		addToMovesList(board)
		# printMoves(movesList)
		# Move a single piece from the columns to the home row
		board = moveRandomPieceFromColumns(board)
		# print("main: moved all column pieces")
		# printBoard(board)
		addToMovesList(board)
		# printMoves(movesList)
	# print("After moves")
	# if board[5][3] == 'A' or board[5][5] == 'B' or board[5][7] == 'C' or board[5][9] == 'D':
		# print("Val in end")
		# printBoard(board)
	# print("*****")
	# time.sleep(1)
	# input("hit key")
	# quit()
	# printMoves()
	# break
	
printMoves()
# print(movesList)
print("score",score)

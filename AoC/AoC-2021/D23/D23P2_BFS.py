# D23P2.py
# 2021 Advent of Code
# Day 23
# Part 2
# 41213 is too low
# One of four pieces can get moved from rooms into hallways
# There are 7 positions in the hallways pieces can be moved into (at most)
# There are 16 pieces to move
# All pieces get moved twice

import random
import os
import time
import time
from collections import deque

# At start
startTime = time.time()

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
print(time_string,"started")

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

# Board check functions

def checkBoardLocked(board):
	# Check to see if the board has any possible moves
	# Returns True if the board has possible moves
	# Returns False if the board is not yet solved
	# print("checkBoardLocked: reached function")
	debugCheckBoardLocked = True
	moveableHallwayPieces = findAllPiecesInHallwayWithOpenPaths(board)
	if moveableHallwayPieces != []:
		if debugCheckBoardLocked:
			print("checkBoardLocked: Moveable pieces in the hallway",moveableHallwayPieces)
		noDestsForHome = True
		for moveablePiece in moveableHallwayPieces:
			if findOpenRooms(moveablePiece[1],moveablePiece[2],board) != []:
				if debugCheckBoardLocked:
					print("checkBoardLocked: Still can move from home row")
				return False
		if debugCheckBoardLocked:
			print("checkBoardLocked: No place to move home row pieces")
			print("checkBoardLocked: No moveable pieces in the hallway")
	moveableColumnPieces = findTopPiecesInRooms(board)
	if moveableColumnPieces == []:
		if debugCheckBoardLocked:
			print("checkBoardLocked: No moveable pieces in column")
	else:
		if debugCheckBoardLocked:
			print("checkBoardLocked: Moveable pieces in column",moveableColumnPieces)
		for moveablePiece in moveableColumnPieces:
			if findLegalMovesToHallways(moveablePiece[1],moveablePiece[2],board) != []:
				if debugCheckBoardLocked:
					print("checkBoardLocked: Still can move from columns")
				return False
		if debugCheckBoardLocked:
			print("checkBoardLocked: No place to move column pieces")
	return True
		
def checkBoardSolved(board):
	# Check to see if the board is solved
	# Returns True if the board is solved
	# Returns False if the board is not yet solved
	# print(board[2])
	debugCheckBoardSolved = False
	if debugCheckBoardSolved:
		print("checkBoardSolved: board")
		printBoard(board)
	if board[0][2] == ['#', '#', '#', 'A', '#', 'B', '#', 'C', '#', 'D', '#', '#', '#']:
		if debugCheckBoardSolved:
			print("checkBoardSolved: board is solved")
		quit()
		return True
	if debugCheckBoardSolved:
		print("checkBoardSolved: board is not solved")
	return False

pieceValDict = {'A':1,'B':10,'C':100,'D':1000}
def movePieceAndKeepCount(xFrom,yFrom,xTo,yTo,board):
	# Move the piece from (xFrom,yFrom) to (xTo,yTo) and keep score
	debugMovePieceAndKeepCount = False
	if debugMovePieceAndKeepCount:
		print("movePieceAndKeepCount: xFrom,yFrom,xTo,yTo",xFrom,yFrom,xTo,yTo)
		print("movePieceAndKeepCount: board (before)")
		printBoard(board)
	pickedUp = board[yFrom][xFrom]
	board[yTo][xTo] = pickedUp
	board[yFrom][xFrom] = '.'
	if debugMovePieceAndKeepCount:
		print("movePieceAndKeepCount: pickedUp",pickedUp)
	pieceVal = pieceValDict[pickedUp]
	# Update score
	score = pieceVal*abs(xFrom-xTo)
	score += pieceVal*abs(yFrom-yTo)
	if debugMovePieceAndKeepCount:
		print("movePieceAndKeepCount: pieceVal",pieceVal)
		print("movePieceAndKeepCount: score (before move)",score)
	if debugMovePieceAndKeepCount:
		print("movePieceAndKeepCount: board (after)")
		printBoard(board)
		print("movePieceAndKeepCount: ",score)
	return board,score

# Hallway to Room movement functions

def findAnyHallwayPieceToMoveToRoom(board):
	# if board[1] == ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#']:
		# return board
	debugFindHallwayPiecesToMoveToRoom = False
	hallwayMoves = []
	if debugFindHallwayPiecesToMoveToRoom:
		print("findAnyHallwayPieceToMoveToRoom: board",board)
		printBoard(board)
	moveablePiecesInHallways = findAllPiecesInHallwayWithOpenPaths(board)
	if moveablePiecesInHallways == []:
		if debugFindHallwayPiecesToMoveToRoom:
			print("findAnyHallwayPieceToMoveToRoom: Nothing to move in hallways")
		return []
	if debugFindHallwayPiecesToMoveToRoom:
		print("findAnyHallwayPieceToMoveToRoom: ",moveablePiecesInHallways)
	for pieceToMove in moveablePiecesInHallways:
		if debugFindHallwayPiecesToMoveToRoom:
			print("findAnyHallwayPieceToMoveToRoom: Piece to move",pieceToMove)
		allLegalDest = findOpenRooms(pieceToMove[1],pieceToMove[2],board)
		if debugFindHallwayPiecesToMoveToRoom:
			print("All dests",allLegalDest)
		if allLegalDest != []:
			hallwayMoves.append([pieceToMove[0],pieceToMove[1],pieceToMove[2],allLegalDest[0][0],allLegalDest[0][1]])
			return hallwayMoves
	return []

legalHallwayXLocations = [1,2,4,6,8,10,11]
def findAllPiecesInHallwayWithOpenPaths(board):
	debugFindAllPiecesInHallwayWithOpenPaths = False
	moveablePiecesInHallways = []
	for xVal in legalHallwayXLocations:
		if 'A' <= board[1][xVal] <= 'D':
			char = board[1][xVal]
			if pathIsOpenFromHallwayToOutsideRoom([char,xVal],board):
				moveablePiecesInHallways.append([char,xVal,1])
	return moveablePiecesInHallways

letterToColDestDict = {'A':3,'B':5,'C':7,'D':9}
def pathIsOpenFromHallwayToOutsideRoom(piece,board):
	# piece [char,xVal]
	destCol = letterToColDestDict[piece[0]]
	# print("destCol",destCol)
	startCol = piece[1]
	# print("startCol",startCol)
	if startCol < destCol:
		for xOff in range(startCol+1,destCol+1):
			# print("pathIsOpenFromHallwayToOutsideRoom: ",board[1][xOff])
			if board[1][xOff] != '.':
				return False
		return True
	elif startCol > destCol:
		for xOff in range(startCol-1,destCol-1,-1):
			# print("pathIsOpenFromHallwayToOutsideRoom: xOff",xOff, )
			if board[1][xOff] != '.':
				return False
		return True
	else:
		assert False,"pathIsOpenFromHallwayToOutsideRoom: weirdness"

def findOpenRooms(x,y,board):
	# 0123456789012
	# 0  #############
	# 1  #...........#
	# 2  ###B#B#D#D###
	# 3    #D#C#B#A#
	# 4    #D#B#A#C#
	# 5    #C#A#A#C#
	# 6    #########
	checkLetter = board[y][x]
	xOffset = letterToColDestDict[checkLetter]
	if board[5][xOffset] == '.':
		return [[xOffset,5]]
	if board[5][xOffset] != checkLetter:
		return []
	if board[4][xOffset] == '.':
		return [[xOffset,4]]
	if board[4][xOffset] != checkLetter:
		return []
	if board[3][xOffset] == '.':
		return [[xOffset,3]]
	if board[3][xOffset] != checkLetter:
		return []
	if board[2][xOffset] == '.':
		return [[xOffset,2]]
	if board[2][xOffset] != checkLetter:
		return []
	assert False,"weirdness"

# Rooms to Hallway movement functions

def getListOfMoveableRoomPieces(board):
	# allTopPiecesInRooms - [char,xVal,yVal]
	debugGetListOfMoveableRoomPieces = False
	if debugGetListOfMoveableRoomPieces:
		print("getListOfMoveableRoomPieces: board")
		printBoard(board)
	allTopPiecesInRooms = findTopPiecesInRooms(board)
	if debugGetListOfMoveableRoomPieces:
		print("(getListOfMoveableRoomPieces): All top pieces in rooms")
		for row in allTopPiecesInRooms:
			print(row)
	if allTopPiecesInRooms == []:
		# assert False,"(getListOfMoveableRoomPieces): no moveable pieces"
		return []
	legallyMoveablePieces = []
	for piece in allTopPiecesInRooms:
		xFrom = piece[1]
		yFrom = piece[2]
		if findLegalMovesToHallways(xFrom,yFrom,board) != []:
			legallyMoveablePieces.append(piece)
	if legallyMoveablePieces == []:
		if debugGetListOfMoveableRoomPieces:
			print("(getListOfMoveableRoomPieces): No pieces to move")
		return []
	if debugGetListOfMoveableRoomPieces:
		print("(getListOfMoveableRoomPieces): legallyMoveablePieces")
		for row in legallyMoveablePieces:
			print(row)
	return legallyMoveablePieces

def findAllMoves(pieceToMove,board):
	debugmoveOnePieceFromRoomToHallway = False
	if debugmoveOnePieceFromRoomToHallway:
		print("(findAllMoves): pieceToMove",pieceToMove)
	xFrom = pieceToMove[1]
	yFrom = pieceToMove[2]
	legalDestHallwaySpots = findLegalMovesToHallways(xFrom,yFrom,board)
	if debugmoveOnePieceFromRoomToHallway:
		print("(findAllMoves): legalDestHallwaySpots")
		for row in legalDestHallwaySpots:
			print(row)
	return legalDestHallwaySpots

def findTopPiecesInRooms(board):
	# Find the top elements in all the columns on the board
	# Doesn't validate that the element should or can be moved
	# Returns list of [char,xVal,yVal] elements
	debugFindTopPiecesInRooms = False
	topColumnValList = []
	if debugFindTopPiecesInRooms:
		print("findTopPiecesInRooms",board)
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					if not canRoomTakeCharFromHallway(xVal,yVal,board):
						if debugFindTopPiecesInRooms:
							print("findTopPiecesInRooms: adding xVal,yVal",xVal,yVal)
						char = board[yVal][xVal]
						topColumnValList.append([char,xVal,yVal])
	if debugFindTopPiecesInRooms:
		print("findTopPiecesInRooms: topColumnValList",topColumnValList)
	return topColumnValList

def findLegalMovesToHallways(x,y,board):
	# Make board of open spots in Hallway
	# Returns board of X, Y board
	debugFindLegalMovesToHallways = False
	if debugFindLegalMovesToHallways:
		print("findLegalMovesToHallways: x,y",x,y)
		printBoard(board)
	legalMovesToHomeRow = []
	xPos = x-1
	while board[1][xPos] == '.':
		if debugFindLegalMovesToHallways:
			print("findLegalMovesToHallways: xPos(1)",xPos)
		legalMovesToHomeRow.append((xPos,1))
		if xPos > 3:
			xPos -= 2
		elif xPos == 2:
			xPos = 1
		else:
			break
	xPos = x+1
	while board[1][xPos] == '.':
		if debugFindLegalMovesToHallways:
			 print("findLegalMovesToHallways: xPos(2)",xPos)
		legalMovesToHomeRow.append((xPos,1))
		if xPos == 10:
			xPos = 11
		elif xPos > 3 and xPos < 11:
			xPos += 2
		else:
			break
	# Always move to corner instead of adjucent to corner position if available
	return legalMovesToHomeRow

valCharDict = {3:'A',5:'B',7:'C',9:'D'}
def canRoomTakeCharFromHallway(xVal,yVal,board):
	# Returns True if the room can accept a transfer from the hallway
	# print("canRoomTakeCharFromHallway: xVal,yVal",xVal,yVal)
	charExpectedVal = valCharDict[xVal]	# Map letter to col 3=A,5=B,7=C,9=D
	for yOff in range(2,6):
		charAtSpot = board[yOff][xVal]
		if (charAtSpot != charExpectedVal) and (charAtSpot != '.'):
			return False
	return True

def copyBoard(board):
	newBoard = []
	for row in board:
		myRow = []
		for col in row:
			myRow.append(col)
		newBoard.append(myRow)
	return newBoard

# main follows

runNum = 0
count = 0
score = 0

movesList = []

openSpotInRoom = {3:-1,5:-1,7:-1,9:-1}

def findAllMovesFromRoomsToHallway(board):
	# Return list of moves [[piece,fromX,fromY,toX,toY],...]
	debugMakeRoomsToHallMovesList = False
	moveablePiecesInRooms = getListOfMoveableRoomPieces(board)
	allMovesFromTo = []
	if moveablePiecesInRooms != []:
		if debugMakeRoomsToHallMovesList:
			print("findAllMovesFromRoomsToHallway: moveablePiecesInRooms",moveablePiecesInRooms)
		for piece in moveablePiecesInRooms:
			fromX = piece[1]
			fromY = piece[2]
			if debugMakeRoomsToHallMovesList:
				print("findAllMovesFromRoomsToHallway: piece",piece)
			allMoves = findAllMoves(piece,board)
			if debugMakeRoomsToHallMovesList:
				print("findAllMovesFromRoomsToHallway: allMoves",allMoves)
			for move in allMoves:
				toX = move[0]
				toY = move[1]
				if debugMakeRoomsToHallMovesList:
					print("findAllMovesFromRoomsToHallway: move",piece[0],"from x,y",fromX,fromY,"to x,y",toX,toY)
				allMovesFromTo.append([piece[0],fromX,fromY,toX,toY])
	return allMovesFromTo

def doMovesOnBoard(board,movesList):
	debugDoMovesOnBoard = False
	if debugDoMovesOnBoard:
		print("doMovesOnBoard: movesList",movesList)
	newBoard = copyBoard(board)
	xFrom = movesList[1]
	yFrom = movesList[2]
	xTo = movesList[3]
	yTo = movesList[4]
	if debugDoMovesOnBoard:
		print("doMovesOnBoard: xFrom, yFrom, xTo, yTo",xFrom,yFrom,xTo,yTo)
		printBoard(board)
	newBoard,score = movePieceAndKeepCount(xFrom,yFrom,xTo,yTo,newBoard)
	if debugDoMovesOnBoard:
		print("doMovesOnBoard: score after move",score)
	return [newBoard,score]

def findNextMoves(board):
	# Return list of fromXY, toXY, piece
	# First, check hallway and if there is a piece select it, if more than one, select first only
	# Second, get a list of the pieces in the rooms that can be moved
	debugFindNeighbors = False
	if debugFindNeighbors:
		print("findNextMoves: board")
		printBoard(board)
	boardsList = []
	hallwayMoveablePieces = findAnyHallwayPieceToMoveToRoom(board)
	if hallwayMoveablePieces != []:
		return hallwayMoveablePieces
	movesList = findAllMovesFromRoomsToHallway(board)
	if debugFindNeighbors:
		print("findNextMoves: movesList",movesList)
		print("findNextMoves: len(movesList)",len(movesList))
	return movesList

inFileName = 'input.txt'		# My input
# inFileName = 'input-Part.txt'	# My input
# inFileName = 'input3.txt'		# My input
# inFileName = 'input1-2.txt'	# Example
# inFileName = 'input-SAG.txt'	# SAG example
print("(main): inFileName:",inFileName)
board1 = readFileOfStringsToListOfLists(inFileName)
debugMain = False
# Load the board,score into the deque\
tovisit = deque([[board1,0]])
while len(tovisit):
	current = tovisit.popleft()
	board = current[0]
	currentScore = current[1]
	if debugMain:
		print("main: currentScore",currentScore)
	neighbors=findNextMoves(board)
	if debugMain:
		print("main: neighbors",neighbors)
	if neighbors != []:
		for n in neighbors:
			if debugMain:
				print("main: n",n)
			newBoard = doMovesOnBoard(board,n)
			tovisit.append([newBoard[0],newBoard[1]+currentScore])
	if checkBoardSolved(board):
		print("main: solved currentScore",currentScore)

endTime = time.time()
print('time',endTime-startTime)

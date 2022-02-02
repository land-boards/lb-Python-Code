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
	debugCheckBoardLocked = False
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
		print("checkBoardSolved: board",board)
		printBoard(board)
	if board[0][2] != ['#', '#', '#', 'A', '#', 'B', '#', 'C', '#', 'D', '#', '#', '#']:
		if debugCheckBoardSolved:
			print("checkBoardSolved: board is not solved")
		return False
	if debugCheckBoardSolved:
		print("checkBoardSolved: board is solved")
	return True

pieceValDict = {'A':1,'B':10,'C':100,'D':1000}
def movePieceAndKeepCount(xFrom,yFrom,xTo,yTo,board):
	# Move the piece from (xFrom,yFrom) to (xTo,yTo) and keep score
	global score
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
	if debugMovePieceAndKeepCount:
		print("movePieceAndKeepCount: pieceVal",pieceVal)
		print("movePieceAndKeepCount: score (before move)",score)
	# Update score
	score += pieceVal*abs(xFrom-xTo)
	score += pieceVal*abs(yFrom-yTo)
	if debugMovePieceAndKeepCount:
		print("movePieceAndKeepCount: board (after)")
		printBoard(board)
	return board

# Hallway to Room movement functions

def findAnyHallwayPieceToMoveToRoom(board):
	# if board[1] == ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#']:
		# return board
	debugFindHallwayPiecesToMoveToRoom = True
	# if debugFindHallwayPiecesToMoveToRoom:
		# print("findAnyHallwayPieceToMoveToRoom: board",board)
		# printBoard(board[0])
	moveablePiecesInHallways = findAllPiecesInHallwayWithOpenPaths(board[0])
	if moveablePiecesInHallways == []:
		# if debugFindHallwayPiecesToMoveToRoom:
			# print("findAnyHallwayPieceToMoveToRoom: Nothing to move in hallways")
		return []
	# if debugFindHallwayPiecesToMoveToRoom:
		# print("findAnyHallwayPieceToMoveToRoom: ",moveablePiecesInHallways)
	for pieceToMove in moveablePiecesInHallways:
		# if debugFindHallwayPiecesToMoveToRoom:
			# print("findAnyHallwayPieceToMoveToRoom: Piece to move",pieceToMove)
		allLegalDest = findOpenRooms(pieceToMove[1],pieceToMove[2],board[0])
		# if debugFindHallwayPiecesToMoveToRoom:
			# print("All dests",allLegalDest)
		if allLegalDest != []:
			return [pieceToMove[0],pieceToMove[1],pieceToMove[2],allLegalDest[0][0],allLegalDest[0][1]]
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

def findAllMoves(pieceToMove):
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
	topColumnValList = []
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					if not canRoomTakeCharFromHallway(xVal,yVal,board):
						# print("findTopPiecesInRooms: adding xVal,yVal",xVal,yVal)
						char = board[yVal][xVal]
						topColumnValList.append([char,xVal,yVal])
	# print("findTopPiecesInRooms: topColumnValList",topColumnValList)
	return topColumnValList

def findLegalMovesToHallways(x,y,list):
	# Make list of open spots in Hallway
	# Returns list of X, Y list
	legalMovesToHomeRow = []
	xPos = x-1
	while list[1][xPos] == '.':
		# print("xPos(1)",xPos)
		legalMovesToHomeRow.append((xPos,1))
		if xPos > 3:
			xPos -= 2
		elif xPos == 2:
			xPos = 1
		else:
			break
	xPos = x+1
	while list[1][xPos] == '.':
		# print("xPos(2)",xPos)
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

def moveFourPiecesFromRoomsToCornersInHallway(board):
	# Move 4 random pieces to corners
	# dstX1 = 1
	# dstX2 = 2
	# dstX3 = 10
	# dstX4 = 11
	# Move a random piece to random corner
	# moveablePieces format [char,xVal,yVal]
	randoCorner = random.randrange(0,2)
	if randoCorner == 0:
		dstX1 = 1
	else:
		dstX1 = 11
	moveablePieces = findTopPiecesInRooms(board)
	pieceToMoveOffset = random.randrange(0,len(moveablePieces))
	xFrom = moveablePieces[pieceToMoveOffset][1]
	yFrom = moveablePieces[pieceToMoveOffset][2]
	board = movePieceAndKeepCount(xFrom,yFrom,dstX1,1,board)
	# # Move 2nd random piece to other corner
	# moveablePieces = findTopPiecesInRooms(board)
	# pieceToMoveOffset = random.randrange(0,len(moveablePieces))
	# xFrom = moveablePieces[pieceToMoveOffset][1]
	# yFrom = moveablePieces[pieceToMoveOffset][2]
	# movePieceAndKeepCount(xFrom,yFrom,dstX2,1,board)
	# # Move 3rd random piece to other corner
	# moveablePieces = findTopPiecesInRooms(board)
	# pieceToMoveOffset = random.randrange(0,len(moveablePieces))
	# xFrom = moveablePieces[pieceToMoveOffset][1]
	# yFrom = moveablePieces[pieceToMoveOffset][2]
	# movePieceAndKeepCount(xFrom,yFrom,dstX3,1,board)
	# # Move 4th random piece to other corner
	# moveablePieces = findTopPiecesInRooms(board)
	# pieceToMoveOffset = random.randrange(0,len(moveablePieces))
	# xFrom = moveablePieces[pieceToMoveOffset][1]
	# yFrom = moveablePieces[pieceToMoveOffset][2]
	# movePieceAndKeepCount(xFrom,yFrom,dstX4,1,board)
	return board

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
	debugMakeRoomsToHallMovesList = True
	moveablePiecesInRooms = getListOfMoveableRoomPieces(board[0])
	count = board[1]
	allMovesFromTo = []
	if moveablePiecesInRooms != []:
		# if debugFindNeighbors:
			# print("findNextMoves: moveablePiecesInRooms",moveablePiecesInRooms)
		for piece in moveablePiecesInRooms:
			fromX = piece[1]
			fromY = piece[2]
			if debugMakeRoomsToHallMovesList:
				print("findNextMoves: piece",piece)
			allMoves = findAllMoves(piece)
			if debugMakeRoomsToHallMovesList:
				print("findNextMoves: allMoves",allMoves)
			for move in allMoves:
				toX = move[0]
				toY = move[1]
				if debugMakeRoomsToHallMovesList:
					print("findNextMoves: move",piece[0],"from x,y",fromX,fromY,"to x,y",toX,toY)
				allMovesFromTo.append([piece[0],fromX,fromY,toX,toY])
	return allMovesFromTo

def doMovesOnBoard(board,movesList):
	global score
	debugDoMovesOnBoard = False
	newBoard = copyBoard(board)
	xFrom = movesList[1]
	yFrom = movesList[2]
	xTo = movesList[3]
	yTo = movesList[4]
	score = 0
	if debugDoMovesOnBoard:
		print("doMovesOnBoard: xFrom, yFrom, xTo, yTo",xFrom,yFrom,xTo,yTo)
	newBoard = movePieceAndKeepCount(xFrom,yFrom,xTo,yTo,newBoard)
	if debugDoMovesOnBoard:
		print("doMovesOnBoard: score after move",score)
	return [newBoard,score]

def findNextMoves(board):
	# Return list of fromXY, toXY, piece
	# First, check hallway and if there is a piece select it, if more than one, select first only
	# Second, get a list of the pieces in the rooms that can be moved
	global score
	debugFindNeighbors = True
	score = board[1]
	if debugFindNeighbors:
		print("findNextMoves: board",board[0])
		printBoard(board[0])
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
board = readFileOfStringsToListOfLists(inFileName)

# Load the board,score into the deque
tovisit = deque([[board,0]])
while len(tovisit):
	current = tovisit.popleft()
	if checkBoardSolved(current[0]):
		print("main: score",current[1])
		# quit()
	neighbors=findNextMoves(current)
	# print("main: neighbors\n",neighbors)
	if neighbors != []:
		for n in neighbors:
			print("n",n)
			newBoard = doMovesOnBoard(current[0],n)
			tovisit.append([newBoard[0],newBoard[1]])	# add score is 0
	print("main: made it through loop")
	# for thing in tovisit:
		# printBoard(thing[0])
		# print(thing[1])
	# quit()

endTime = time.time()
print('time',endTime-startTime)
print("score",score)

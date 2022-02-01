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

# Moves list functions

def printMoves():
	# printMoves
	global movesList
	print("movesList")
	for move in movesList:
		print(move)
	return

def clearMovesList():
	global movesList
	# print("(clearMovesList): Clearing moves list")
	movesList = []
	return
	
def addToMovesList(xFrom,yFrom,xTo,yTo,pickedUp):
	global movesList
	global movesCount
	# print("addToMovesList",xFrom,yFrom,xTo,yTo,pickedUp)
	movesList.append([xFrom,yFrom,xTo,yTo,pickedUp])
	movesCount += 1
	return

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
	if board[2] != ['#', '#', '#', 'A', '#', 'B', '#', 'C', '#', 'D', '#', '#', '#']:
		return False
	return True

pieceValDict = {'A':1,'B':10,'C':100,'D':1000}
def movePieceAndKeepCount(xFrom,yFrom,xTo,yTo,board):
	# Move the piece from (xFrom,yFrom) to (xTo,yTo) and keep score
	global score
	# print("(movePieceAndKeepCount): xFrom,yFrom,xTo,yTo",xFrom,yFrom,xTo,yTo)
	pickedUp = board[yFrom][xFrom]
	board[yTo][xTo] = pickedUp
	board[yFrom][xFrom] = '.'
	# print("(movePieceAndKeepCount): pickedUp",pickedUp)
	pieceVal = pieceValDict[pickedUp]
	# Update score
	score += pieceVal*abs(xFrom-xTo)
	score += pieceVal*abs(yFrom-yTo)
	addToMovesList(xFrom,yFrom,xTo,yTo,pickedUp)
	return board

# Hallway to Room movement functions

legalHallwayXLocations = [1,2,4,6,8,10,11]
def findAllPiecesInHallway(board):
	if board[1] == ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#']:
		return []
	allHallwayPieces = []
	for x in legalHallwayXLocations:
		if board[1][x] !=- '.':
			allHallwayPieces.append(x)
	return allHallwayPieces

def moveHallwayPiecesToRooms(board):
	# if board[1] == ['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#']:
		# return board
	moveablePiecesInHallways = findAllPiecesInHallwayWithOpenPaths(board)
	# print("moveablePiecesInHallways",moveablePiecesInHallways)
	if moveablePiecesInHallways == []:
		return board
	for pieceToMove in moveablePiecesInHallways:
		# print("moveHallwayPiecesToRooms: Piece to move",pieceToMove)
		allLegalDest = findOpenRooms(pieceToMove[1],pieceToMove[2],board)
		# print("All dests",allLegalDest)
		if allLegalDest != []:
			for legalDests in allLegalDest:
				board = movePieceAndKeepCount(pieceToMove[1],pieceToMove[2],legalDests[0],legalDests[1],board)
	return board

def findAllPiecesInHallwayWithOpenPaths(board):
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

# def moveOneRandomPieceFromRoomToHallway(board):
	# # allTopPiecesInRooms - [char,xVal,yVal]
	# debugMoveOneRandomPieceFromRoomToHallway = False
	# allTopPiecesInRooms = findTopPiecesInRooms(board)
	# if debugMoveOneRandomPieceFromRoomToHallway:
		# printBoard(board)
		# print("(moveOneRandomPieceFromRoomToHallway): All top pieces in rooms")
		# for row in allTopPiecesInRooms:
			# print(row)
	# if allTopPiecesInRooms == []:
		# # assert False,"(moveOneRandomPieceFromRoomToHallway): no moveable pieces"
		# return board
	# legallyMoveablePieces = []
	# for piece in allTopPiecesInRooms:
		# xFrom = piece[1]
		# yFrom = piece[2]
		# if findLegalMovesToHallways(xFrom,yFrom,board) != []:
			# legallyMoveablePieces.append(piece)
	# if legallyMoveablePieces == []:
		# if debugMoveOneRandomPieceFromRoomToHallway:
			# print("(moveOneRandomPieceFromRoomToHallway): No pieces to move")
		# return board
	# if debugMoveOneRandomPieceFromRoomToHallway:
		# print("(moveOneRandomPieceFromRoomToHallway): legallyMoveablePieces")
		# for row in legallyMoveablePieces:
			# print(row)
	# pieceToMoveOffset = random.randrange(0,len(legallyMoveablePieces))
	# pieceToMove = legallyMoveablePieces[pieceToMoveOffset]
	# if debugMoveOneRandomPieceFromRoomToHallway:
		# print("(moveOneRandomPieceFromRoomToHallway): pieceToMove",pieceToMove)
	# xFrom = pieceToMove[1]
	# yFrom = pieceToMove[2]
	# legalDestHallwaySpots = findLegalMovesToHallways(xFrom,yFrom,board)
	# if debugMoveOneRandomPieceFromRoomToHallway:
		# print("(moveOneRandomPieceFromRoomToHallway): legalDestHallwaySpots")
		# for row in legalDestHallwaySpots:
			# print(row)
	# destLocationOffset = random.randrange(0,len(legalDestHallwaySpots))
	# destLocation = legalDestHallwaySpots[destLocationOffset]
	# if debugMoveOneRandomPieceFromRoomToHallway:
		# print("(moveOneRandomPieceFromRoomToHallway): destLocation",destLocation)
	# xTo = destLocation[0]
	# yTo = destLocation[1]
	# legallyMoveablePieces[pieceToMoveOffset][1]
	# board = movePieceAndKeepCount(xFrom,yFrom,xTo,yTo,board)
	# # pickUpPiece = board[yFrom][xFrom]
	# # board[yFrom][xFrom] = '.'
	# # board[yTo][xTo] = pickUpPiece
	# if debugMoveOneRandomPieceFromRoomToHallway:
		# printBoard(board)
		# quit()
	# return board

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
	# destLocationOffset = random.randrange(0,len(legalDestHallwaySpots))
	# destLocation = legalDestHallwaySpots[destLocationOffset]
	# if debugmoveOnePieceFromRoomToHallway:
		# print("(findAllMoves): destLocation",destLocation)
	# xTo = destLocation[0]
	# yTo = destLocation[1]
	# legallyMoveablePieces[pieceToMoveOffset][1]
	# board = movePieceAndKeepCount(xFrom,yFrom,xTo,yTo,board)
	# if debugmoveOnePieceFromRoomToHallway:
		# printBoard(board)
		# quit()
	# return board

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

def testCode():
	global score
	debugTestCode = False
	# Test readFileOfStringsToListOfLists()
	inFileName = "input-Solved.TXT"
	board = readFileOfStringsToListOfLists(inFileName)
	if board != [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], 
	['#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#'], 
	['#', '#', '#', 'A', '#', 'B', '#', 'C', '#', 'D', '#', '#', '#'], 
	[' ', ' ', '#', 'A', '#', 'B', '#', 'C', '#', 'D', '#'], 
	[' ', ' ', '#', 'A', '#', 'B', '#', 'C', '#', 'D', '#'], 
	[' ', ' ', '#', 'A', '#', 'B', '#', 'C', '#', 'D', '#'], 
	[' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#']]:
		print("testCode(): readFileOfStringsToListOfLists() failed")
		return False
	# Test checkBoardSolved()
	if not checkBoardSolved(board):
		print("testCode(): readFileOfStringsToListOfLists() failed")
		return False
	# Test checkBoardSolved()
	if not checkBoardLocked(board):
		print("testCode():  checkBoardLocked() failed (1)")
		return False
	# Test moveHallwayPiecesToRooms
	inFileName = 'input-MoveToRoomTest.txt'
	board = readFileOfStringsToListOfLists(inFileName)
	if debugTestCode:
		printBoard(board)
	board = moveHallwayPiecesToRooms(board)
	if debugTestCode:
		printBoard(board)
	if not checkBoardSolved(board):
		print("testCode(): moveHallwayPiecesToRooms() failed")
		return False
	if score != 3:
		print("testCode(): Score failed")
		return False
	if debugTestCode:
		print("testCode(): score",score)
		print("testCode(): passed")
	board = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], 
	['#', 'D', 'D', '.', 'D', '.', 'B', '.', 'C', '.', 'A', 'C', '#'], 
	['#', '#', '#', '.', '#', '.', '#', '.', '#', '.', '#', '#', '#'], 
	[' ', ' ', '#', '.', '#', 'C', '#', '.', '#', '.', '#'], 
	[' ', ' ', '#', 'D', '#', 'B', '#', 'A', '#', 'C', '#'], 
	[' ', ' ', '#', 'B', '#', 'A', '#', 'B', '#', 'A', '#'], 
	[' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
	if not checkBoardLocked(board):
		print("testCode():  checkBoardLocked() failed (2)")
		return False
	inFileName = "input-Solved.TXT"
	board = readFileOfStringsToListOfLists(inFileName)
	topSpots = findTopPiecesInRooms(board)
	if topSpots != []:
		print("testCode():  findTopPiecesInRooms() failed (1)")
		return False
	inFileName = "input.TXT"
	board = readFileOfStringsToListOfLists(inFileName)
	topSpots = findTopPiecesInRooms(board)
	if topSpots != [['B', 3, 2], ['B', 5, 2], ['D', 7, 2], ['D', 9, 2]]:
		print("(testCode): findTopPiecesInRooms failed (2)")
		print(topSpots)
		return False
	if canRoomTakeCharFromHallway(3,0,board):
		print("(testCode): canRoomTakeCharFromHallway() failed")
		return False
	# print("testCode(): topSpots",topSpots)
	# quit()
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
movesCount = 0

openSpotInRoom = {3:-1,5:-1,7:-1,9:-1}

if not testCode():
	print("(main): Test code failed")
else:
	print("(main): Test code passed")

def findNeighbors(board):
	global count
	boardsList = []
	debugFindNeighbors = True
	moveablePiecesInRooms = getListOfMoveableRoomPieces(board[0])
	count = board[1]
	allMovesFromTo = []
	if moveablePiecesInRooms != []:
		# if debugFindNeighbors:
			# print("findNeighbors: moveablePiecesInRooms",moveablePiecesInRooms)
		for piece in moveablePiecesInRooms:
			fromX = piece[1]
			fromY = piece[2]
			print("findNeighbors: piece",piece)
			allMoves = findAllMoves(piece)
			print("findNeighbors: allMoves",allMoves)
			for move in allMoves:
				toX = move[0]
				toY = move[1]
				print("findNeighbors: move",piece[0],"from x,y",fromX,fromY,"to x,y",toX,toY)

inFileName = 'input.txt'		# My input
# inFileName = 'input-Part.txt'	# My input
# inFileName = 'input3.txt'		# My input
# inFileName = 'input1-2.txt'	# Example
# inFileName = 'input-SAG.txt'	# SAG example
print("(main): inFileName:",inFileName)
board1 = readFileOfStringsToListOfLists(inFileName)
board = copyBoard(board1)
movesCount = 0
mostMoves = 5
movesList = []

tovisit = deque([[board,0]])
while len(tovisit):
	current = tovisit.popleft()
	if checkBoardSolved(current[0]):
		print(current)
		quit()
	neighbors=findNeighbors(current)
	for n in neighbors:
		tovisit.append([n,current[1]+0])	# add score is 0
	

while not checkBoardSolved(board):	# Read/re-read the board from the file
	# board = readFileOfStringsToListOfLists(inFileName)
	board = copyBoard(board1)
	score = 0
	movesList = []
	movesCount = 0
	loopsCount = 0
	# openSpotInRoom = {3:-1,5:-1,7:-1,9:-1}
	# printMoves()
	# print("(main): Before moves")
	# printBoard(board)
	# Move 2 pieces to the two far corners
	# board = moveFourPiecesFromRoomsToCornersInHallway(board)
	while not checkBoardLocked(board):
		# Move a single piece from the columns to the home row
		board = moveOneRandomPieceFromRoomToHallway(board)
		# addToMovesList(board)
		# print("(main): moved all column pieces")
		# printBoard(board)
		# printMoves()
		# Always move all pieces from home row if possible
		# movedAPieceFromHomeRow,board = moveHallwayPiecesToRooms(board)
		board = moveHallwayPiecesToRooms(board)
		# addToMovesList(board)
		# print("(main): moved all home row pieces")
		# printBoard(board)
		# printMoves()
		# time.sleep(0.1)
		if movesCount > 32:
			printMoves()
			quit()
		loopsCount += 1
		if loopsCount > 32:
			printMoves()
			quit()
	runNum += 1
	# if runNum % 10000 == 0:
		# named_tuple = time.localtime() # get struct_time
		# time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
		# print(time_string,end=' ')
		# print(runNum,score)
	if movesCount > mostMoves:
		named_tuple = time.localtime() # get struct_time
		time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
		print(time_string,end=' ')
		print('Run',runNum,'score',score,'moves',movesCount)
		mostMoves = movesCount
		printMoves()
		printBoard(board)
	# if (board[5][3] == 'A') or (board[5][5] == 'B') or (board[5][7] == 'C') or (board[5][9] == 'D'):
		# printMoves()
		# printBoard(board)
		# input("hit key")
	# quit()
	# break
	
printMoves()
# print(movesList)
endTime = time.time()
print('time',endTime-startTime)

print("score",score)

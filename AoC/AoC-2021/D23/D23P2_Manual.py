# D23P2.py
# 2021 Advent of Code
# Day 23
# Part 2
# Clear B column first didn't work

import random
import time

# At start
startTime = time.time()

# print(random.randrange(1, 10))

def readFileOfStringsToListOfLists(inFileName):
	board = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip('\n')
			board.append(list(inLine))
	return board

def printBoard(board):
	colNum = 0
	print("\n   ",end='')
	for col in range(len(board[0])):
		print(int(col/10),end='')
	print("\n   ",end='')
	for col in range(len(board[0])):
		print(col%10,end = '')
	print()
	rowNum = 0
	for row in board:
		print(rowNum,end='  ')
		for col in row:
			print(col,end='')
		print()
		rowNum += 1

pieceValDict = {'A':1,'B':10,'C':100,'D':1000}
letterToColDestDict = {'A':3,'B':5,'C':7,'D':9}
legalHallwayXLocations = [1,2,4,6,8,10,11]
def findAllMovablePieces(board):
	moveablePieces = []
	yVal = 1
	for xVal in legalHallwayXLocations:
		if 'A' <= board[yVal][xVal] <= 'D':
			char = board[yVal][xVal]
			moveablePieces.append([char,xVal,yVal])
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					char = board[yVal][xVal]
					moveablePieces.append([char,xVal,yVal])
	return moveablePieces

# inFileName = 'input1-2.txt'
inFileName = 'input.txt'
board = readFileOfStringsToListOfLists(inFileName)
# quit()

def getNum(inStr):
	legalNum = True
	while legalNum:
		val = input(inStr)
		val = val.strip('\n')
		for charVal in val:
			if '0' <= charVal <= '9':
				pass
			else:
				legalNum = False
		if legalNum:
			return int(val)

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

def findHallwayDests(board):
	# legalHallwayXLocations = [1,2,4,6,8,10,11]
	legalHallwayXVals = []
	for x in legalHallwayXLocations:
		if board[1][x] == '.':
			legalHallwayXVals.append(x)
	return legalHallwayXVals

def getPickupPieceXY(board):
	moveablePieces = findAllMovablePieces(board)
	print("moveablePieces are:")
	for row in moveablePieces:
		print('Piece',row[0],'at',row[1],end='')
		print(',',row[2])
	legalPieceToPickup = False
	while not legalPieceToPickup:
		pieceX = getNum("Enter pick piece x > ")
		if pieceX == 99:
			print("score",score)
			print("Pick up locations")
			for row in pickedUpPieces:
				print(row)
			quit()
		pieceY = getNum("Enter pick piece y > ")
		for piece in moveablePieces:
			if piece[1] == pieceX and piece[2] == pieceY:
				return pieceX, pieceY
		print("************ Illegal coord *********")
		print("moveablePieces are:")
		for row in moveablePieces:
			print('Piece',row[0],'at',row[1],end='')
			print(',',row[2])
	
# def getDest(board):
	# legalDests = findAllLegalDesta(
	
# print("board",board)
score = 0
pickedUpPieces = []
while True:
	printBoard(board)
	print("score",score,'\n')
	print("Pick up piece (Enter x = 99 to stop game)")
	legalPiece = False
	fromX, fromY = getPickupPieceXY(board)
	pickedUp = board[fromY][fromX]
	pieceVal = pieceValDict[pickedUp]
	print("PieceVal =",pieceVal)
	pickedUpPieces.append(['picked up',pickedUp,'at x y',fromX,fromY])
	printBoard(board)
	# toX, toY = getDests(board)
	if fromY != 1:
		print("Legal hallway locations")
		for x in findHallwayDests(board):
			print('x, y =',x,end='')
			print(', 1')
	
	dir = ''
	while dir != 'q':
		dir = input("\nup/down/left/right/quit ")
		if dir == '':
			break
		if dir[0] == 'u':
			if board[fromY-1][fromX] != '.':
				print("*********Illegal move**********")
				board[fromY][fromX] = pickedUp
				break
			board[fromY][fromX] = '.'
			fromY -= 1
			board[fromY][fromX] = pickedUp
			score += pieceVal
		elif dir[0] == 'd':
			if board[fromY+1][fromX] != '.':
				print("*********Illegal move**********")
				board[fromY][fromX] = pickedUp
				break
			board[fromY][fromX] = '.'
			fromY += 1
			board[fromY][fromX] = pickedUp
			score += pieceVal
		elif dir[0] == 'l':
			if board[fromY][fromX-1] != '.':
				print("*********Illegal move**********")
				board[fromY][fromX] = pickedUp
				break
			board[fromY][fromX] = '.'
			fromX -= 1
			board[fromY][fromX] = pickedUp
			score += pieceVal
		elif dir[0] == 'r':
			if board[fromY][fromX+1] != '.':
				print("*********Illegal move**********")
				board[fromY][fromX] = pickedUp
				break
			board[fromY][fromX] = '.'
			fromX += 1
			board[fromY][fromX] = pickedUp
			score += pieceVal
#			elif dir == 'q':
			# if board[fromY][fromX] == 'X':
				# board[fromY][fromX] = pickedUp
		else:
			break
		pickedUpPieces.append(['  moved',pickedUp,dir[0],'to x y',fromX,fromY])
		print("score",score)
		printBoard(board)
		
endTime = time.time()
print('time',endTime-startTime)

print("score",score)

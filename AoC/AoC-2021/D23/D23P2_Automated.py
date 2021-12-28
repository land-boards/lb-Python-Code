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

def findAllLegalMoves(x,y,list):
	allLegalMoves = []
	# legalPossibleHomeRowLegalXValues = [1,2,4,6,8,10,11]
	# print("x,y",x,y)
	if y > 1:
		xPos = x-1
		while list[1][xPos] == '.':
			# print("xPos(1)",xPos)
			allLegalMoves.append([xPos,1])
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
			allLegalMoves.append([xPos,1])
			if xPos == 10:
				xPos = 11
			elif xPos > 3 and xPos < 11:
				xPos += 2
			else:
				break
	
	# print("allLegalMoves",allLegalMoves)
	return allLegalMoves

inList = readFileOfStringsToListOfLists('input.txt')
score = 0
moveablePieces = findAllMovablePieces(inList)
while moveablePieces != []:
	printBoard(inList)
	pieceToMoveOffset = random.randrange(0,len(moveablePieces))
	
	print("Moving from",moveablePieces[pieceToMoveOffset])
	x = moveablePieces[pieceToMoveOffset][1]
	y = moveablePieces[pieceToMoveOffset][2]
	legalMoves = findAllLegalMoves(x,y,inList)
	print("legalMoves",legalMoves)
	destOffset = random.randrange(0,len(legalMoves))
	print("Moving to",legalMoves[destOffset])
	# fromX = 
	# fromY = 
	moveablePieces[pieceToMoveOffset][1]
	pickUpPiece = inList[y][x]
	inList[y][x] = '.'
	inList[legalMoves[destOffset][1]][legalMoves[destOffset][0]] = pickUpPiece
	moveablePieces = findAllMovablePieces(inList)
	print("\nmoveablePieces",moveablePieces)

print("score",score)

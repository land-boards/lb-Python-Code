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
			char = board[yVal][xVal]
			moveablePieces.append([char,xVal,yVal])
	for xVal in range(3,10,2):
		for yVal in range(2,6):
			if 'A' <= board[yVal][xVal] <= 'D':
				if board[yVal-1][xVal] == '.':
					char = board[yVal][xVal]
					moveablePieces.append([char,xVal,yVal])
	return moveablePieces

inFileName = 'input1-2.txt'
inList = readFileOfStringsToListOfLists(inFileName)
# moveablePieces = findAllMovablePieces(inList)
# print("moveablePieces")
# for row in moveablePieces:
	# print(row)
# quit()


# print("inList",inList)
score = 0
pickedUpPieces = []
while True:
	printBoard(inList)
	print("score",score,'\n')
	print("Pick up piece (Enter x = 99 to stop game)")
	legalPiece = False
	legalCoord = False
	while not legalPiece and not legalCoord:
		legalCoord = False
		pieceXVal = input("Pick piece x ")
		if '0' <= pieceXVal[0] <= '9':
			pieceX = int(pieceXVal)
			if pieceX == 99:
				print("score",score)
				print("Pick up locations")
				for row in pickedUpPieces:
					print(row)
				quit()
			if 1 <= pieceX <= 11:
				legalCoord = True
			else:
				legalCoord = False
				print("************ Illegal coord *********")
		if legalCoord:
			pieceYVal = input("Pick piece y ")
			if '0' <= pieceYVal[0] <= '9':
				pieceY = int(pieceYVal)
				if 1 <= pieceY <= 5:
					legalCoord = True
				else:
					legalCoord = False
					print("************ Illegal coord *********")
			else:
				legalCoord = False
				print("************ Illegal coord *********")
		if legalCoord:
			pickedUp = inList[pieceY][pieceX]
			if 'A' <= pickedUp <= 'D':
				legalPiece = True
				print("Picked up ",pickedUp)
				# inList[pieceY][pieceX] = 'X'
			else:
				print("Tried to pick up Illegal piece",pickedUp,"at x y",pieceX,pieceY)
				legalPiece = False
				break
	if legalPiece:
		if pickedUp == 'A':
			pieceVal = 1
		elif pickedUp == 'B':
			pieceVal = 10
		elif pickedUp == 'C':
			pieceVal = 100
		elif pickedUp == 'D':
			pieceVal = 1000
		print("PieceVal =",pieceVal)
		pickedUpPieces.append(['picked up',pickedUp,'at x y',pieceXVal,pieceYVal])
#		inList[pieceY][pieceX] = 'X'
		printBoard(inList)
		dir = ''
		while dir != 'q':
			dir = input("\nup/down/left/right/quit ")
			if dir == '':
				break
			if dir[0] == 'u':
				if inList[pieceY-1][pieceX] != '.':
					print("*********Illegal move**********")
					inList[pieceY][pieceX] = pickedUp
					break
				inList[pieceY][pieceX] = '.'
				pieceY -= 1
				inList[pieceY][pieceX] = pickedUp
				score += pieceVal
			elif dir[0] == 'd':
				if inList[pieceY+1][pieceX] != '.':
					print("*********Illegal move**********")
					inList[pieceY][pieceX] = pickedUp
					break
				inList[pieceY][pieceX] = '.'
				pieceY += 1
				inList[pieceY][pieceX] = pickedUp
				score += pieceVal
			elif dir[0] == 'l':
				if inList[pieceY][pieceX-1] != '.':
					print("*********Illegal move**********")
					inList[pieceY][pieceX] = pickedUp
					break
				inList[pieceY][pieceX] = '.'
				pieceX -= 1
				inList[pieceY][pieceX] = pickedUp
				score += pieceVal
			elif dir[0] == 'r':
				if inList[pieceY][pieceX+1] != '.':
					print("*********Illegal move**********")
					inList[pieceY][pieceX] = pickedUp
					break
				inList[pieceY][pieceX] = '.'
				pieceX += 1
				inList[pieceY][pieceX] = pickedUp
				score += pieceVal
#			elif dir == 'q':
				# if inList[pieceY][pieceX] == 'X':
					# inList[pieceY][pieceX] = pickedUp
			else:
				break
			pickedUpPieces.append(['  moved',pickedUp,dir[0],'to x y',pieceX,pieceY])
			print("score",score)
			printBoard(inList)
		
endTime = time.time()
print('time',endTime-startTime)

print("score",score)

# D23P1.py
# 2021 Advent of Code
# Day 23
# Part 1
# 10625 is too high
# 10607
# 9927  is too low

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

inList = readFileOfStringsToListOfLists('input.txt')
# print("inList",inList)
score = 0
while True:
	print("score",score)
	print("Pick up piece (Enter x = 99 to stop game)")
	printBoard(inList)
	legalPiece = False
	while not legalPiece:
		pieceX = int(input("Pick piece x "))
		if pieceX == 99:
			print("score",score)
			quit()
		pieceY = int(input("Pick piece y "))
		pickedUp = inList[pieceY][pieceX]
		if 'A' <= pickedUp <= 'D':
			legalPiece = True
		else:
			print("Tried to pick up Illegal piece")
	print("Picked up ",pickedUp)
	if pickedUp == 'A':
		pieceVal = 1
	elif pickedUp == 'B':
		pieceVal = 10
	elif pickedUp == 'C':
		pieceVal = 100
	elif pickedUp == 'D':
		pieceVal = 1000
	print("PieceVal =",pieceVal)
	inList[pieceY][pieceX] = 'X'
	printBoard(inList)
	dir = ''
	while dir != 'q':
		dir = input("\nup/down/left/right/quit ")[0]
		if dir == 'u':
			if inList[pieceY-1][pieceX] == '#':
				print("Illegal move")
				inList[pieceY][pieceX] = pickedUp
				break
			inList[pieceY][pieceX] = '.'
			pieceY -= 1
			inList[pieceY][pieceX] = pickedUp
			score += pieceVal
		elif dir == 'd':
			if inList[pieceY+1][pieceX] == '#':
				print("Illegal move")
				inList[pieceY][pieceX] = pickedUp
				break
			inList[pieceY][pieceX] = '.'
			pieceY += 1
			inList[pieceY][pieceX] = pickedUp
			score += pieceVal
		elif dir == 'l':
			if inList[pieceY][pieceX-1] == '#':
				print("Illegal move")
				inList[pieceY][pieceX] = pickedUp
				break
			inList[pieceY][pieceX] = '.'
			pieceX -= 1
			inList[pieceY][pieceX] = pickedUp
			score += pieceVal
		elif dir == 'r':
			if inList[pieceY][pieceX+1] == '#':
				print("Illegal move")
				inList[pieceY][pieceX] = pickedUp
				break
			inList[pieceY][pieceX] = '.'
			pieceX += 1
			inList[pieceY][pieceX] = pickedUp
			score += pieceVal
		elif dir == 'q':
			if inList[pieceY][pieceX] == 'X':
				inList[pieceY][pieceX] = pickedUp
		else:
			break
		print("score",score)
		printBoard(inList)
		

print("score",score)

'''
D17P1.py
Tetris
3639 is too high
3170 is too high
'''

'''
Shapes

....
....
....
####

....
.#..
###.
.#..

....
..#.
..#.
###.

#...
#...
#...
#...

....
....
##..
##..

'''

import time

# At start
startTime = time.time()

def getNextDir():
	global inLine
	global dirOffset
	global manualIn
	if manualIn:
		print('getNextDir Got here')
		while True:
			inStr = input('Direction (<,v,>)')
			print('char',inStr[0])
			if inStr[0] == '<':
				return '<'
			elif inStr[0] == 'v':
				return 'v'
			elif inStr[0] == '>':
				return '>'
			
	debug_getNextDir = False
	if debug_getNextDir:
		if dirOffset ==  0:
			print('getNextDir: Start of directions')
	nextDir = inLine[dirOffset]
	dirOffset += 1
	if dirOffset == len(inLine):
		dirOffset = 0
	return nextDir

def parseInList(inList):
	parsedList = inList
	return parsedList

def readInFile(fileName):
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
	return inLine
	
def getNextShape():
	global shapeOffset
	global manualIn
	if manualIn:
		keepLooping = True
		while keepLooping:
			keepLooping = False
			inStr = input('Shape (0-5)')
			print(inStr)
			if inStr[0] == '0':
				shapeOffset = 0
			elif inStr[0] == '1':
				shapeOffset = 1
			elif inStr[0] == '2':
				shapeOffset = 2
			elif inStr[0] == '3':
				shapeOffset = 3
			elif inStr[0] == '4':
				shapeOffset =  4
			else:
				keepLooping = True
	else:
		debug_getNextShape= False
		if shapeOffset == 0:
			if debug_getNextShape:
				print('First offset')
	currentShape = shapes[shapeOffset]
	shapeWidth = shapeHorizSize[shapeOffset]
	shapeHeight = shapeVertSize[shapeOffset]
	shapeOffset += 1
	if shapeOffset == len(shapes):
		shapeOffset = 0
	return currentShape,shapeWidth,shapeHeight

def printTopField():
	global manualIn
	debug_printField = True
	if len(field)> 16:
		last = len(field)-16
	else:
		last = -1
	if debug_printField or manualIn:
		for row in range(len(field)-1,last,-1):
			print(field[row])

def printField():
	global manualIn
	debug_printField = True
	if debug_printField or manualIn:
		for row in range(len(field)-1,-1,-1):
			print(field[row])

def insert3BlankRowsIntoField():
	blankFieldLine = '|.......|'
	field.append(blankFieldLine)
	field.append(blankFieldLine)
	field.append(blankFieldLine)

def addNextShapeToField(shapeHeight,shapeYPos):
	debug_addNextShapeToField = False
	if debug_addNextShapeToField:
		print('addNextShapeToField: len(fieldLen)',len(field))
		printField()
		print('addNextShapeToField: shapeYPos',shapeYPos)
		print('shapeHeight',shapeHeight)
	fieldLen = len(field)
	rowsToAdd = shapeHeight - (fieldLen - shapeYPos)
	if debug_addNextShapeToField:
		print('addNextShapeToField: rowsToAdd',rowsToAdd)
	for i in range(rowsToAdd):
		# print('addNextShapeToField: i',i)
		field.append('|.......|')
	if debug_addNextShapeToField:
		print('After adding rows')
		printField()
		print()
	# assert False

def notAtEdge(dirMove,shapeWidth,shapeXPos):
	debug_notAtEdge = False
	canMove = False
	if debug_notAtEdge:
		print('dirMoves',dirMove)
		print('shapeWidth',shapeWidth)
		print('shapeXPos',shapeXPos)
	if dirMove == '>':
		if shapeXPos+shapeWidth < 8:
			canMove = True
	elif dirMove == '<':
		if shapeXPos > 1:
			canMove = True
	if debug_notAtEdge:
		print('notAtEdge: canMove',canMove)
	return canMove

def findNextInsertRow():
	debug_findNextInsertRow = False
	if debug_findNextInsertRow:
		print('findNextInsertRow: got here')
	rowNum = 1
	if len(field) == 1:
		return 1
	while field[rowNum] != '|.......|':
		rowNum += 1
	if debug_findNextInsertRow:
		print('findNextInsertRow: rowNum (2)',rowNum)
	return rowNum + 3

def printshape(currentShape):
	for y in range(len(currentShape)):
		for x in range(len(currentShape[0])):
			print(currentShape[y][x],end='')
		print()
		
def printShapeInField(currentShape,shapeXPos,shapeYPos,shapeWidth,shapeHeight):
	debug_printShapeInField = False
	global manualIn
	if debug_printShapeInField or manualIn:
		print('printShapeInField:')
		shapeY=0
		for y in range(len(field)-1,-1,-1):
			shapeX = 0
			for x in range(len(field[0])):
				if (shapeYPos <= y < shapeYPos+shapeHeight) and (shapeXPos <= x < shapeXPos+shapeWidth):
					print('o',end='')
					shapeX += 1
					if shapeX == shapeWidth:
						shapeY += 1
				else:
					print(field[y][x],end='')
			print()

def canShapeMoveVert(currentShape,shapeXPos,shapeYPos,shapeWidth,shapeHeight):
	debug_canShapeMoveVert = False
	global manualIn
	if debug_canShapeMoveVert or manualIn:
		print('canShapeMoveVert: currentShape')
		printshape(currentShape)
		print('shapeXPos,shapeYPos',shapeXPos,shapeYPos)
		print('shapeWidth,shapeHeight',shapeWidth,shapeHeight)
	if shapeYPos == 1:
		if manualIn:
			print('canShapeMoveVert: at bottom')
		return False
	for y in range(shapeHeight):
		for x in range(shapeWidth):
			if debug_canShapeMoveVert or manualIn:
					print('canShapeMoveVert: x,33-y',x,3-shapeHeight)
			if currentShape[3-y][x] == '#' and (field[shapeYPos-1+y][shapeXPos+x] == '#'):
				if manualIn:
					print('canShapeMoveVert: False','x,y',x,y)
				return False
	return True

def canShapeMoveHoriz(currentShape,shapeXPos,shapeYPos,dirMove,shapeWidth,shapeHeight):
	debug_canShapeMoveHoriz = False
	# printShapeInField(currentShape,shapeXPos,shapeYPos,shapeWidth,shapeHeight)
#	destArray = []
	canMove = True
	if debug_canShapeMoveHoriz:
		print('canShapeMoveHoriz(1): shapeXPos',shapeXPos,'dirMove',dirMove)
#	print('canShapeMoveHoriz(2)shapeWidth',shapeWidth,'shapeHeight',shapeHeight)
	if dirMove == '>':
		if shapeXPos+shapeWidth>7:
			if debug_canShapeMoveHoriz:
				print('canShapeMoveHoriz(3): right side can not move')
			canMove = False
		else:
			for y in range(shapeHeight):
				# print('canShapeMoveHoriz(4): y',y,'currentShape[y]',currentShape[y])
				if currentShape[shapeHeight-y-1][shapeWidth-1] == '#' and field[shapeYPos+y][shapeXPos+shapeWidth] == '#':
					if debug_canShapeMoveHoriz:
						print('canShapeMoveHoriz(5): right side can not move y',y)
					canMove = False
	elif dirMove == '<':
		if shapeXPos == 1:
			if debug_canShapeMoveHoriz:
				print('canShapeMoveHoriz(6): left side can not move')
			canMove = False
		else:
			for y in range(shapeHeight):
				if debug_canShapeMoveHoriz:
					print('canShapeMoveHoriz(9) currentShape[shapeHeight-y-1][0] ',currentShape[shapeHeight-y-1][0],'field[shapeYPos+y][shapeXPos-1]',field[shapeYPos+y][shapeXPos-1])
					print('canShapeMoveHoriz(11) field[shapeYPos+y]',field[shapeYPos+y])
				if currentShape[shapeHeight-y-1][0] == '#' and field[shapeYPos+y][shapeXPos-1] == '#':
					if debug_canShapeMoveHoriz:
						print('canShapeMoveHoriz(7): left side can not move')
					canMove = False			
	if debug_canShapeMoveHoriz:
		if canMove:
			print('canShapeMoveHoriz(8): can move')
	return canMove

def replaceChar(inStr,offset,newChar):
	outStr=''
	for fromOff in range(0,offset):
		outStr += inStr[fromOff]
	outStr += newChar
	for fromOff in range(offset+1,len(inStr)):
		outStr += inStr[fromOff]
	return outStr

def insertBlock(shapeXPos,shapeYPos,currentShape,shapeWidth,shapeHeight):
	# print('insertBlock: field (before)')
	# printField()
	debug_insertBlock = False
	if debug_insertBlock:
		print('insertBlock: shapeXPos',shapeXPos)
		print('insertBlock: shapeYPos',shapeYPos)
		print('insertBlock: currentShape',currentShape)
		print('insertBlock: shapeWidth',shapeWidth)
		print('insertBlock: shapeHeight',shapeHeight)
	shY = 0
	for y in range(4):
		if debug_insertBlock:
			print('insertBlock: currentShape row',currentShape[y])
		for x in range(4):
			if currentShape[3-y][x] == '#':
				if debug_insertBlock:
					print('insertBlock: # x,y',x,y,'at',shapeXPos+x,shapeYPos+y)
				line=field[shapeYPos+y]
				if debug_insertBlock:
					print('insertBlock: line',line)
				line = replaceChar(line,shapeXPos+x,'#')
				if debug_insertBlock:
					print('insertBlock: line[shapeXPos+x]',line[shapeXPos+x])
				field[shapeYPos+y] = line
				
			else:
				if debug_insertBlock:
					print('insertBlock: . x,y',x,y)
	if debug_insertBlock:
		print('insertBlock: field (after)')
		printField()

shapes = [['....','....','....','####'],['....','.#..','###.','.#..'],['....','..#.','..#.','###.'],['#...','#...','#...','#...'],['....','....','##..','##..']]

shapeHorizSize = [4,3,3,1,2]
shapeVertSize = [1,3,3,4,2]

# fileName = 'input2.txt'
# fileName = 'input.txt'
fileName = 'input1.txt'

inLine = readInFile(fileName)
manualIn = False
debug_main = False  
singleStep = True
if debug_main:
	print('main: inLine',inLine)
	print('main: len(inLine)',len(inLine))
dirOffset = 0
# for i in range(50):
	# dirMove = getNextDir()
	# print('main: dirMove',i, dirMove)

shapeOffset = 0
# for i in range(10):
	# currentShape = getNextShape();
	# print('currentShape',currentShape)

field = []
blankFieldLine = '|.......|'
field.append('+-------+')
insert3BlankRowsIntoField()
moveCount = 1
while moveCount < 2023:
	if debug_main:
		print('moveCount',moveCount)
	shapeYPos = findNextInsertRow()
	currentShape,shapeWidth,shapeHeight = getNextShape()
	if debug_main:
		print('main: shapeWidth,shapeHeight',shapeWidth,shapeHeight)
	addNextShapeToField(shapeHeight,shapeYPos)
	# print('main field (before)')
	# printField()
	if debug_main or manualIn or singleStep:
		print('New shape')
		printshape(currentShape)
	shapeXPos = 3
	if debug_main or manualIn:
		printShapeInField(currentShape,shapeXPos,shapeYPos,shapeWidth,shapeHeight)
	stillMoving = True
	while stillMoving:
		if debug_main:
			print('main: before move corner x,y',shapeXPos,shapeYPos)
		dirMove = getNextDir()
		notEdge = notAtEdge(dirMove,shapeWidth,shapeXPos)
		if notEdge:
			if canShapeMoveHoriz(currentShape,shapeXPos,shapeYPos,dirMove,shapeWidth,shapeHeight):
				#if debug_main:
				# print('main: can move horiz, dirMove',dirMove)
				if dirMove == '>':
					shapeXPos += 1
				elif dirMove == '<':
					shapeXPos -= 1
				else:
					assert False,'main: dir error'
			if debug_main:
				print('main: after X move shape corner x,y',shapeXPos,shapeYPos)
		if canShapeMoveVert(currentShape,shapeXPos,shapeYPos,shapeWidth,shapeHeight):
			if debug_main:
				print('can move vert')
			shapeYPos-=1
		else:
			if debug_main:
				print('can not move vert')
			stillMoving = False
		if debug_main:
			print('main: after Y move shape corner x,y',shapeXPos,shapeYPos)
		if debug_main or manualIn:
			printShapeInField(currentShape,shapeXPos,shapeYPos,shapeWidth,shapeHeight)
	insertBlock(shapeXPos,shapeYPos,currentShape,shapeWidth,shapeHeight)
	moveCount += 1
	if manualIn or singleStep:
		printTopField()
		print('**************************************')
		input('hit any key')

# printField()
print('Height',findNextInsertRow()-4)
print('len(field)-3',len(field)-4)
# At end
print('time',time.time()-startTime)

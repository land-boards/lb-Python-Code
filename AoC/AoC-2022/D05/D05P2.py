""" 
D05P2

"""

def transformRawBoxesList(inList):
	outList = []
	for line in inList:
		lenLine = len(line)
		# print('lenLine',lenLine)
		newLine = []
		for offset in range(1,lenLine,4):
			# print('line[offset]',line[offset])
			newLine.append(line[offset])
		outList.append(newLine)
	# print('outList',outList)
	return(outList)

def flipRawBoxesList(inList):
	print('flipRawBoxesList: inList',inList)
	rowCount = len(inList[0])
	colCount = len(inList)
	print('rows=',rowCount)
	print('columns=',colCount)
	outList = []
	for row in range(rowCount):
		outLine = []
		for col in range(colCount):
			print('current col',col,'row',row)
			if inList[col][row] != ' ':
				outLine.append(inList[col][row])
		outList.append(outLine)
	# print('outList',outList)
	return outList

def doMoves(movesList,flippedList):
	print('movesList',movesList)
	print('flippedList',flippedList)
	for move in movesList:
		# print('move',move)
		moveCount = move[0]
		moveFrom = move[1]
		moveTo = move[2]
		print('move',moveCount,'boxes from',moveFrom,'to',moveTo)
		movePileList=[]
		for box in range(moveCount):
			currentBox = flippedList[moveFrom].pop(0)
			print('currentBox',currentBox)
			movePileList.append(currentBox)
		movePileList.reverse()
		for box in movePileList:
			flippedList[moveTo].insert(0,box)
		print('flippedList',flippedList)
	for col in range(len(flippedList)):
		print(flippedList[col][0],end='')
	print

fileName = 'input.txt'
state = 'readCrates'
rawBoxesList = []
rawNumsList = []
movesList = []
numColumns=0
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		# print(inLine)
		if state == 'readCrates':
			if inLine[1] == '1':
				state = 'boxesList'
				rawNumsList = inLine.split()
				numColumns=len(rawNumsList)
				# print('numColumns',numColumns)
			else:
				rawBoxesList.append(inLine)
		elif state == 'boxesList':
			if inLine == '':
				state = 'empySep'
		elif state == 'empySep':
			state = 'inMoves'
			if inLine != '':
				movesLine=inLine.split()
				movesLine2=[]
				movesLine2.append(int(movesLine[1]))
				movesLine2.append(int(movesLine[3])-1)
				movesLine2.append(int(movesLine[5])-1)
				movesList.append(movesLine2)
		elif state == 'inMoves':
			if inLine != '':
				movesLine=inLine.split()
				movesLine2=[]
				movesLine2.append(int(movesLine[1]))
				movesLine2.append(int(movesLine[3])-1)
				movesLine2.append(int(movesLine[5])-1)
				movesList.append(movesLine2)
		# print(state)
		
# print('rawBoxesList',rawBoxesList)
# print('Number of columns =',numColumns)
# print('movesList',movesList)
transformedList = transformRawBoxesList(rawBoxesList)
# print('transformedList',transformedList)
flippedList = flipRawBoxesList(transformedList)
# print('flippedList',flippedList)
doMoves(movesList,flippedList)

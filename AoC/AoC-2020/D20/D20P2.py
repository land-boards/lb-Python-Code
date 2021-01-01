""" 
D20P1
1987 too low
2347 too high
"""

# DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	global DEBUG_PRINT		# need to put in each function
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileOfStringsToListOfLists(fileName):
	inList = []
	tileCount = 0
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			if line[0] == 'T':
				tileNumStr = inLine[5:-1]
				inList.append(int(tileNumStr))
				tileCount += 1
			elif line != '':
				inList.append(list(inLine))
	# print('tileCount',tileCount)
	return inList

def makeBetterList(inList):
	bigList = []
	lineList = []
	for line in inList:
		if isinstance(line,int):
			lineList = []
			lineList.append(line)
		elif line != []:
			lineList.append(line)
		else:
			bigList.append(lineList)
	bigList.append(lineList)
	return bigList
	
def printImage(theImage):
	print()
	for row in theImage:
		for col in row:
			print(col,end='')
		print()

def edgeValLeftToRight(inListTopRow):
	checkBitVal = 1
	accumVal = 0
	# print('inListTopRow',inListTopRow)
	for cellVal in inListTopRow:
		if cellVal == '#':
			accumVal += checkBitVal
		checkBitVal <<= 1
	return accumVal

def edgeValRightToLeft(inListTopRow):
	checkBitVal = 2**(len(inListTopRow)-1)
	accumVal = 0
	for cellVal in inListTopRow:
		if cellVal == '#':
			accumVal += checkBitVal
		checkBitVal >>= 1
	return accumVal

def evalEdges(image):
	# image [2311, ['.', '.', '#', '#', '.', '#', '.', '.', '#', '.'], ...
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('(evalEdges): image ' + str(image))
	theImage = image[1:]
	debugPrint('(evalEdges): original image')
	if DEBUG_PRINT:
		printImage(theImage)
	lfValsList = []
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	if DEBUG_PRINT:
		printImage(theImage)
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	if DEBUG_PRINT:
		printImage(theImage)
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	if DEBUG_PRINT:
		printImage(theImage)
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	if DEBUG_PRINT:
		printImage(theImage)
	debugPrint('lfValsList' + str(lfValsList) + '\n')
	return lfValsList

def findOtherNode(edgeVal,nodeNumberToSkip,edgesList):
	# print('(findOtherNode) : edgesList',edgesList)
	# print('(findOtherNode) : edgeVal',edgeVal)
	# print('(findOtherNode) : nodeNumberToSkip',nodeNumberToSkip)
	for edge in edgesList:
		testNodeNumber = edge[0]
		for checkEdge in edge[1]:
			if checkEdge == edgeVal:
				if testNodeNumber != nodeNumberToSkip:
					# print('Node',edgeVal,'matches to',testNodeNumber)
					return testNodeNumber
	assert False,'findOtherNode) : wtf'

def makeEdgesList(bigList):
	# print('\nSides values list')
	edgesList = []
	for image in bigList:
		edgesLine = []
		edgesLine.append(image[0])
		edgeVals = evalEdges(image)
		edgesLine.append(edgeVals)
		edgesList.append(edgesLine)
	# print('edgesList',edgesList)
	# for edge in edgesList:
		# print('Id',edge[0],end = ' ')
		# for val in edge[1]:
			# print(val,end=' ')
			# pass
		# print()
	# listOfEdges = []
	# allEdgeVals {300: 1, 210: 1, 616: 0, 89: 0, 231: 0, 924: 0, 498: 1, 318: 1, 397: 1, 710: 1, 564: 0, 177: 0, 841: 0, 587: 0, 399: 1, 966: 1, 18: 1, 288: 1, 24: 0, 96: 0, 902: 0, 391: 0, 183: 1, 948: 1, 348: 1, 234: 1, 576: 1, 9: 1, 43: 0, 848: 0, 565: 1, 689: 1, 481: 0, 542: 0, 184: 0, 116: 0, 532: 0, 161: 0, 85: 1, 680: 1, 456: 0, 78: 0, 271: 0, 962: 0}
	return edgesList

def countEdges(edgesList):
	# Sides one by one
	# Id 2311 300 210 616 89 231 924 498 318
	# Id 1951 397 710 318 498 564 177 841 587
	# Id 1171 399 966 18 288 24 96 902 391
	# Id 1427 183 948 348 234 210 300 576 9
	# Id 1489 43 848 288 18 948 183 565 689
	# Id 2473 481 542 184 116 234 348 966 399
	# Id 2971 532 161 689 565 85 680 456 78
	# Id 2729 680 85 9 576 710 397 271 962
	# print('\nSides one by one')
	allEdgeVals = {}
	for edge in edgesList:
		for edgeVal in edge[1]:
			if edgeVal not in allEdgeVals:
				allEdgeVals[edgeVal] = 0
			else:
				allEdgeVals[edgeVal] += 1
	# print('\nCounts of allEdgeVals')
	# for key in allEdgeVals:
		# if allEdgeVals[key] == 0:
			# del allEdgeVals[key]
	# print('allEdgeVals ',end='')
	# print(allEdgeVals)
	return allEdgeVals

def findCorners(edgesList):
	minVal = 9999
	maxVal = 0
	# print('\nCounting edges')
	for shape in edgesList:
		#print('Key Id',shape[0],end = ' ')
		totalEdges = 0
		for keyVal in shape[1]:
			# print(keyVal,allEdgeVals[keyVal],end=' ')
			totalEdges += allEdgeVals[keyVal]
		if totalEdges < minVal:
			minVal = totalEdges
		if totalEdges > maxVal:
			maxVal = totalEdges
	# print('totalEdges',totalEdges)
	# print('minVal',minVal)
	# print('maxVal',maxVal)

	cornerPieces = []
	# print('\nFind corners')
	for shape in edgesList:
		# print('Key Id',shape[0],end = ' ')
		totalEdges = 0
		for keyVal in shape[1]:
			# print(keyVal,allEdgeVals[keyVal],end=' ')
			totalEdges += allEdgeVals[keyVal]
		if totalEdges == minVal:
			cornerPieces.append(shape[0])
		# print('totalEdges',totalEdges>>1)

	# Calculate Part 1 check result
	# print('(findCorners) : corner pieces',cornerPieces)
	return cornerPieces

def solvePt1(cornerPieces):
	total = 1
	for end in cornerPieces:
		total *= end
	print('(solvePt1) : Pt 1 val =',total)

def makeNewEdgesDict(allEdgeVals,edgesList):
	# allEdgeVals = {666: 1, 357: 1, 547: 1, 785: 1, 813: 1,  759: 0, 
	matchedEdges = []
	for edgeVal in allEdgeVals:
		if allEdgeVals[edgeVal] != 0:
			matchedEdges.append(edgeVal)
	debugPrint('matchedEdges' + str(matchedEdges))

	# edgesList = [[2411, [666, 357, 547, 785, 813, 723, 63, 1008]],
	newEdgesDict = {}
	for edge in edgesList:
		nodeNumber = edge[0]
		matchingNodeNumber = []
		firstSecond = 'First'
		for edgeVal in edge[1]:
			if edgeVal not in matchedEdges:
				if firstSecond == 'First':
					matchingNodeNumber.append(-1)
					firstSecond = 'Second'
				else:
					firstSecond = 'First'
			else:
				otherNode = findOtherNode(edgeVal,nodeNumber,edgesList)
				debugPrint('nodeNumber ' + str(nodeNumber) + ' otherNode ' + str(otherNode))
				if firstSecond == 'First':
					matchingNodeNumber.append(otherNode)
					firstSecond = 'Second'
				else:
					firstSecond = 'First'
		newEdgesDict[nodeNumber] = matchingNodeNumber

	debugPrint('(makeNewEdgesDict) : [top,left,bottom,right]')
	debugPrint('(makeNewEdgesDict) : newEdgesDict')
	for row in newEdgesDict:
		debugPrint('  ' + str(row) + str(newEdgesDict[row]))
	return newEdgesDict

def rotateImage(inImage):
	global DEBUG_PRINT
	rotImage = []
	yLen = len(inImage)
	xLen = len(inImage[0])
	if DEBUG_PRINT:
		print('(xLen,yLen)',xLen,yLen)
	for y in range(yLen):
		newRow = []
		for x in range(xLen):
			val = inImage[x][yLen-y-1]
			newRow.append(val)
		rotImage.append(newRow)
	return rotImage

def flipHoriz(theList):
	debugPrint('(flipHoriz) : flipping horizontally')
	newList = []
	for row in range(len(theList)):
		newRow = []
		for col in range(len(theList[0])):
			newRow.append(theList[row][len(theList[0])-col-1])
		newList.append(newRow)
	return newList

def flipVert(theList):
	debugPrint('(flipVert) : flipping vertically')
	newList = []
	for row in range(len(theList)):
		newRow = []
		for col in range(len(theList[0])):
			newRow.append(theList[len(theList)-row-1][col])
		newList.append(newRow)
	return newList
	
def trimEdges(theList):
	debugPrint('(trimEdges) : trimming ')
	trimmedArray = []
	for row in range(1,len(theList)-1):
		lineRow = []
		for col in range(1,len(theList[0])-1):
			lineRow.append(theList[row][col])
		trimmedArray.append(lineRow)
	return trimmedArray
	
def transformBlock(IDVal,transformedDictVal,preTransformedArray):
	# global bigList
	# IDVal 2917
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('\n(transformBlock) : IDVal ' + str(IDVal) + ', transformedDictVal ' + str(transformedDictVal))
	#  transformedDictVal [[2203, 3457, 1039, 3517], True, False, True]
	# preTransformedArray [['#', '#', '.', '#', '.', '#', '#', '#', '#', '#'], ['#', '.', '.', '#', '.', '.', '#', '.', '#', '#'], ['.', '.', '#', '#', '.', '.', '#', '.', '.', '#'], ['#', '.', '.', '#', '.', '#', '#', '.', '#', '#'], ['#', '.', '#', '.', '.', '#', '.', '.', '.', '.'], ['.', '#', '.', '#', '.', '#', '#', '.', '.', '#'], ['.', '#', '#', '#', '#', '.', '.', '.', '.', '.'], ['#', '.', '.', '#', '.', '.', '.', '#', '.', '#'], ['#', '.', '.', '.', '#', '.', '.', '.', '.', '#'], ['.', '#', '.', '#', '.', '#', '#', '.', '.', '#']]
	debugPrint('(transformBlock) : preTransformedArray ')
	for row in preTransformedArray:
		debugPrint(str(row))
	# assert False,'check here'
	debugPrint('(transformBlock) : IDsArray ' + str(IDsArray))
	rotatedArray = []
	if transformedDictVal[1]:
		rotatedArray = rotateImage(preTransformedArray)
	else:
		rotatedArray = preTransformedArray
	horizFlipped = []
	if not transformedDictVal[2]:
		horizFlipped = flipHoriz(rotatedArray)
	else:
		horizFlipped = rotatedArray
	vertFlipped = []
	if transformedDictVal[3]:
		vertFlipped = flipVert(horizFlipped)
	else:
		vertFlipped = horizFlipped
	trimmedArray = trimEdges(vertFlipped)
	debugPrint('(transformBlock) : trimmedArray (after)')
	for row in trimmedArray:
		debugPrint(str(row))
	return trimmedArray
	
def countif(countifList,criteria):
	count = 0
	for val in countifList:
		if val == criteria:
			count += 1
	return count

def makeIDsTransformDict(cornerPieces,newEdgesDict):
	global DEBUG_PRINT
	debugPrint('(makeIDsTransformDict) : cornerPieces ' + str(cornerPieces))
	debugPrint('(makeIDsTransformDict) : newEdgesDict ')
	for row in newEdgesDict:
		debugPrint('  ' + str(row) + ' ' + str(newEdgesDict[row]))
	IDsArray = []
	IDsRow = []
	# currentID 3079
	for corner in range(4):
		debugPrint('(makeIDsTransformDict) : CornerList val ' + str(newEdgesDict[cornerPieces[corner]]))
		if (newEdgesDict[cornerPieces[corner]][2] != -1) and (newEdgesDict[cornerPieces[corner]][3] != -1):
			currentID = cornerPieces[corner]

	# Fill in first cell
	# transformedDict {3079: [[-1, -1, 2473, 2311], False, False, False]}
	debugPrint('(makeIDsTransformDict) : [top,left,bottom,right]')
	debugPrint('(makeIDsTransformDict) : Upper Left Corner ID ' + str(currentID) + ' vals ' + str(newEdgesDict[currentID]))

	transformedList = []
	transformedLine = []
	transformedDict = {}
	transformedLine.append(newEdgesDict[currentID])
	transformedLine.append(False)
	transformedLine.append(False)
	transformedLine.append(False)
	transformedDict[currentID] = transformedLine

	# Fill in top row
	# transformedDict 
	#	{3079: [[-1, -1, 2473, 2311], False, False, False], 
	#	 2311: [[-1, 1951, 1427, 3079], False, True, True]}
	lastCellInRow = False
	while not lastCellInRow:
		debugPrint('\n(makeIDsTransformDict) : currentID ' + str(currentID))
		debugPrint('(makeIDsTransformDict) : transformedDict[currentID] ' + str(transformedDict[currentID]))
		upVal = transformedDict[currentID][0][0]
		leftVal = transformedDict[currentID][0][1]
		downVal = transformedDict[currentID][0][2]
		rightVal = transformedDict[currentID][0][3]
		nextVal0 = newEdgesDict[rightVal][0]
		nextVal1 = newEdgesDict[rightVal][1]
		nextVal2 = newEdgesDict[rightVal][2]
		nextVal3 = newEdgesDict[rightVal][3]
		debugPrint('(makeIDsTransformDict) : ID ' + str(rightVal) + ' before transform ' + str(newEdgesDict[rightVal]))
		rotated = False
		if nextVal1 != currentID and nextVal3 != currentID:
			# rotate if necessary
			n0 = nextVal1
			n1 = nextVal2
			n2 = nextVal3
			n3 = nextVal0
			nextVal0 = n0
			nextVal1 = n1
			nextVal2 = n2
			nextVal3 = n3
			rotated = True
			debugPrint('  cell '+ str(rightVal) + ' rotated')
		else:
			debugPrint('  cell ' + str(rightVal) + ' not rotated')
		flippedHoriz = False
		if currentID != nextVal1:
			n1 = nextVal1
			nextVal1 = nextVal3
			nextVal3 = n1
			flippedHoriz = True
			debugPrint('  cell ' + str(rightVal) + ' flipped horizontally')
		else:
			debugPrint('  cell ' + str(rightVal) + ' not flipped horizontally')
		flippedVert = False
		if nextVal2 == -1:
			n0 = nextVal0
			nextVal0 = nextVal2
			nextVal2 = n0
			debugPrint('  cell ' + str(rightVal) + ' flipped vertically')
			flippedVert = True
		else:
			debugPrint('  cell ' + str(rightVal) + ' not flipped vertically')
		# debugPrint('(makeIDsTransformDict) : After transform ' + str(rightVal) + ' ' + str(nextVal0) + ' ' + str(nextVal1) + ' ' + str(nextVal2) + ' ' + str(nextVal3))
		IDsRow.append(currentID)
		currentID = rightVal
		transformedLine = []
		tranformedCoordList = []
		tranformedCoordList.append(nextVal0)
		tranformedCoordList.append(nextVal1)
		tranformedCoordList.append(nextVal2)
		tranformedCoordList.append(nextVal3)
		transformedLine.append(tranformedCoordList)
		transformedLine.append(rotated)
		transformedLine.append(flippedHoriz)
		transformedLine.append(flippedVert)
		transformedDict[currentID] = transformedLine
		debugPrint('(makeIDsTransformDict) : transformedDict[currentID] ' + str(transformedDict[currentID]))
		if countif(newEdgesDict[currentID][0:4],-1) == 2:
			debugPrint('End of first row\n')
			lastCellInRow = True
	IDsRow.append(currentID)
	IDsArray.append(IDsRow)
	debugPrint('(makeIDsTransformDict) : transformedDict ' + str(transformedDict))
	# assert False,'stop'

	debugPrint('(makeIDsTransformDict) : transformedDict top row')
	for row in transformedDict:
		debugPrint('  ' + str(row) + ' ' + str(transformedDict[row]))
	widthOfField = len(transformedDict)
	debugPrint('\n(makeIDsTransformDict) : IDsArray ' + str(IDsArray))
	debugPrint('  (makeIDsTransformDict) : widthOfField ' + str(widthOfField))
	for row in range(1,widthOfField):
		IDsRow = []
		for col in range(widthOfField):
			prevRowID = IDsArray[row-1][col]
			currentID = transformedDict[prevRowID][0][2]
			debugPrint('\n(makeIDsTransformDict) : currentID ' + str(currentID))
			debugPrint('(makeIDsTransformDict) : prevRowID ' + str(prevRowID))
			debugPrint('  newEdgesDict[currentID] ' + str(newEdgesDict[currentID]))
			nextVal0 = newEdgesDict[currentID][0]
			nextVal1 = newEdgesDict[currentID][1]
			nextVal2 = newEdgesDict[currentID][2]
			nextVal3 = newEdgesDict[currentID][3]
			rotated = False
			if newEdgesDict[currentID][0] != prevRowID and newEdgesDict[currentID][2] != prevRowID:
				n0 = nextVal1
				n1 = nextVal2
				n2 = nextVal3
				n3 = nextVal0
				nextVal0 = n0
				nextVal1 = n1
				nextVal2 = n2
				nextVal3 = n3
				rotated = True
				debugPrint('  cell ' + str(currentID) + ' rotated')
			else:
				debugPrint('  cell ' + str(currentID) + ' not rotated')
			flippedHoriz = False
			# debugPrint('  row ' + str(row) + ' col ' + str(col) + ' IDsRow ' + str(IDsRow))
			if col == 0:
				if nextVal1 != -1:
					n1 = nextVal1
					nextVal1 = nextVal3
					nextVal3 = n1
					flippedHoriz = True
					debugPrint('  cell ' + str(currentID) + ' flipped horizontally')
				else:
					debugPrint('  cell ' + str(currentID) + ' not flipped horizontally')
			elif IDsRow[col-1] != nextVal1:
				n1 = nextVal1
				nextVal1 = nextVal3
				nextVal3 = n1
				flippedHoriz = True
				debugPrint('  cell ' + str(currentID) + ' flipped horizontally')
			else:
				debugPrint('  cell ' + str(currentID) + ' not flipped horizontally')
			flippedVert = False
			if nextVal0 != IDsArray[row-1][col]:
				n0 = nextVal0
				nextVal0 = nextVal2
				nextVal2 = n0
				debugPrint('  cell ' + str(currentID) + ' flipped vertically')
				flippedVert = True
			else:
				debugPrint('  cell ' + str(currentID) + ' not flipped vertically')
			IDsRow.append(currentID)
			
			transformedLine = []
			tranformedCoordList = []
			tranformedCoordList.append(nextVal0)
			tranformedCoordList.append(nextVal1)
			tranformedCoordList.append(nextVal2)
			tranformedCoordList.append(nextVal3)
			transformedLine.append(tranformedCoordList)
			transformedLine.append(rotated)
			transformedLine.append(flippedHoriz)
			transformedLine.append(flippedVert)
			transformedDict[currentID] = transformedLine
		IDsArray.append(IDsRow)
	debugPrint('\n(makeIDsTransformDict) : IDsArray ' + str(IDsArray))
	debugPrint('\n(newEdgesDict) Before : newEdgesDict')
	for row in newEdgesDict:
		debugPrint('  ' + str(row) + ' ' + str(newEdgesDict[row]))
	debugPrint('')
	debugPrint('(makeIDsTransformDict) After : transformedDict')
	for row in transformedDict:
		debugPrint('  ' + str(row) + ' ' + str(transformedDict[row]))
	debugPrint('')
	DEBUG_PRINT = False
	return IDsArray, transformedDict

def countSeaMonsters(seaMonsterList,newArr):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('seaMonsterList' + str(seaMonsterList))
	debugPrint('newArr' + str(newArr))
	monsterCount = 0
	monsterHeight = len(seaMonsterList)
	monsterWidth = len(seaMonsterList[0])
	debugPrint('monsterHeight ' + str(monsterHeight))
	debugPrint('monsterWidth ' + str(monsterWidth))
	for rowInArray in range(len(newArr)-monsterHeight):
		for colInArray in range(len(newArr[0])-monsterWidth):
			debugPrint('anchor x' + str(colInArray) + 'y' + str(rowInArray) + 'val' + str(newArr[rowInArray][colInArray]))
			foundMonster = True
			for rowInMonster in range(monsterHeight):
				for colInMonster in range(monsterWidth):
					# print('checking monster x',colInMonster,'y',rowInMonster,'val',seaMonsterList[rowInMonster][colInMonster])
					if (seaMonsterList[rowInMonster][colInMonster] == '#'):
						debugPrint('monster #')
						if (newArr[rowInArray+rowInMonster][colInArray+colInMonster] == '.'):
							foundMonster = False
							debugPrint('not here x' + str(colInArray) + 'y' + str(rowInArray))
						elif (newArr[rowInArray+rowInMonster][colInArray+colInMonster] == '#'):
							debugPrint('spot match')
						else:
							debugPrint('wtf-2')
							assert False,'wtf-2'
					elif (seaMonsterList[rowInMonster][colInMonster] == ' '):
						debugPrint('ignore')
					else:
						debugPrint('wtf')
						assert False,'wtf'
			if foundMonster:
				print('found a monster x',colInArray,'y',rowInArray)
				monsterCount += 1
	# print('monsterCount',monsterCount)
	return monsterCount

def rotateSeaMonster(inImage):
	global DEBUG_PRINT
	return list(zip(*inImage[::-1]))
	
######################################################################
# Program follows
inList = readFileOfStringsToListOfLists('input.txt')

# bigList [[2311, ['.', '.', '#', '#', '.', '#', '.', '.', '#', '.'], ...
bigList = makeBetterList(inList)
# print('bigList',bigList)

# edgesList [[2311, [300, 210, 616, 89, 231, 924, 498, 318]], [1951, [397, 710, 318, 498, 564, 177, 841, 587]], [1171, [399, 966, 18, 288, 24, 96, 902, 391]], [1427, [183, 948, 348, 234, 210, 300, 576, 9]], [1489, [43, 848, 288, 18, 948, 183, 565, 689]], [2473, [481, 542, 184, 116, 234, 348, 966, 399]], [2971, [532, 161, 689, 565, 85, 680, 456, 78]], [2729, [680, 85, 9, 576, 710, 397, 271, 962]]]
edgesList = makeEdgesList(bigList)

# allEdgeVals {300: 1, 210: 1, 616: 1, 89: 1, 231: 0, 924: 0, 498: 1, 318: 1, 397: 1, 710: 1, 564: 0, 177: 0, 841: 0, 587: 0, 399: 1, 966: 1, 18: 1, 288: 1, 24: 0, 96: 0, 902: 0, 391: 0, 183: 1, 948: 1, 348: 1, 234: 1, 576: 1, 9: 1, 43: 0, 848: 0, 565: 1, 689: 1, 481: 0, 542: 0, 184: 1, 116: 1, 532: 0, 161: 0, 85: 1, 680: 1, 456: 0, 78: 0, 271: 0, 962: 0, 501: 0, 702: 0, 66: 0, 264: 0}
allEdgeVals = countEdges(edgesList)

# cornerPieces [1951, 1171, 2971, 3079]
cornerPieces = findCorners(edgesList)

# (solvePt1) : Pt 1 val = 20899048083289
solvePt1(cornerPieces)

# newEdgesDict {2311: [1427, 3079, -1, 1951], 1951: [2729, 2311, -1, -1], 1171: [2473, 1489, -1, -1], 1427: [1489, 2473, 2311, 2729], 1489: [-1, 1171, 1427, 2971], 2473: [-1, 3079, 1427, 1171], 2971: [-1, 1489, 2729, -1], 2729: [2971, 1427, 1951, -1], 3079: [-1, -1, 2473, 2311]}
newEdgesDict = makeNewEdgesDict(allEdgeVals,edgesList)

IDsArray, transformedDict = makeIDsTransformDict(cornerPieces,newEdgesDict)

debugPrint('\n(main) : IDsArray' + str(IDsArray))

DEBUG_PRINT = False
newDict = {}
for col in range(len(IDsArray)):
	for row in range(len(IDsArray[0])):
		currentBlock = IDsArray[col][row]
		debugPrint('(main) : currentBlock ' + str(currentBlock))
		debugPrint('(main) : transformedDict[currentBlock] id ' + str(currentBlock) + ' val ' + str(transformedDict[currentBlock]))
		for subArray in bigList:
			if subArray[0] == currentBlock:
				# print('(main) : subArray: ',subArray)
				subBlock = subArray[1:]
		debugPrint('(main) : subBlock ')
		# debugPrint(str(subBlock))
		newBlock = transformBlock(currentBlock,transformedDict[currentBlock],subBlock)
		newDict[IDsArray[col][row]] = newBlock
debugPrint('\n(main) : newDict ')
for row in newDict:
	debugPrint(row)
	for myElem in newDict[row]:
		debugPrint(myElem)

oneCell = bigList[0]
blockSize = len(oneCell[1]) - 2
debugPrint('blockSize ' + str(blockSize))

numBlocksInRow = len(IDsArray[0])
debugPrint('numBlocksInRow ' + str(numBlocksInRow))

pixelsWide = blockSize * numBlocksInRow
debugPrint('pixelsWide ' + str(pixelsWide))

newArr = []
for ct in range(pixelsWide):
	newLine = []
	for ct in range(pixelsWide):
		newLine.append(' ')
	newArr.append(newLine)
# debugPrint('newArr\n' + str(newArr))

DEBUG_PRINT = True
# print('IDsArray',IDsArray)

for row in range(pixelsWide):
	# print('id',end = ' ')
	for col in range(pixelsWide):
		id = IDsArray[int(row/blockSize)][int(col/blockSize)]
		# print(id,end = ' ')
		val = newDict[id][row%blockSize][col%blockSize]
		# print(val,end=' ')
		newArr[row][col] = val
	# print('')

seaMonster =   ['                  # ',\
				'#    ##    ##    ###',\
				' #  #  #  #  #  #   ']
seaMonsterList = []
for row in seaMonster:
	seaMonsterRow = []
	for cRow in row:
		seaMonsterRow.append(cRow)
	seaMonsterList.append(seaMonsterRow)

# print('seaMonsterList',seaMonsterList)
# print('seaMonster height',len(seaMonsterList))
# print('seaMonster width',len(seaMonsterList[0]))

hashCnt = 0
for rowInArray in range(0,len(newArr)):
	for colInArray in range(0,len(newArr[0])):
		if newArr[rowInArray][colInArray] == '#':
			hashCnt += 1
# print('hashCnt',hashCnt)

countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('\ncountOfSeaMonsters',countOfSeaMonsters)
	printImage(seaMonsterList)

seaMonsterList = rotateSeaMonster(seaMonsterList)
countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('countOfSeaMonsters',countOfSeaMonsters)
	seaWaves = hashCnt - (15 * countOfSeaMonsters)
	printImage(seaMonsterList)
	printImage(newArr)
	print('seaWaves',seaWaves)

seaMonsterList = rotateSeaMonster(seaMonsterList)
countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('countOfSeaMonsters',countOfSeaMonsters)
	seaWaves = hashCnt - (15 * countOfSeaMonsters)
	printImage(seaMonsterList)
	printImage(newArr)
	print('seaWaves',seaWaves)

seaMonsterList = rotateSeaMonster(seaMonsterList)
countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('countOfSeaMonsters',countOfSeaMonsters)
	seaWaves = hashCnt - (15 * countOfSeaMonsters)
	printImage(seaMonsterList)
	printImage(newArr)
	print('seaWaves',seaWaves)

seaMonsterList = rotateSeaMonster(seaMonsterList)
seaMonsterList = flipHoriz(seaMonsterList)
countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('countOfSeaMonsters',countOfSeaMonsters)
	seaWaves = hashCnt - (15 * countOfSeaMonsters)
	printImage(seaMonsterList)
	printImage(newArr)
	print('seaWaves',seaWaves)

seaMonsterList = rotateSeaMonster(seaMonsterList)
countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('countOfSeaMonsters',countOfSeaMonsters)
	seaWaves = hashCnt - (15 * countOfSeaMonsters)
	printImage(seaMonsterList)
	printImage(newArr)
	print('seaWaves',seaWaves)

seaMonsterList = rotateSeaMonster(seaMonsterList)
countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('countOfSeaMonsters',countOfSeaMonsters)
	seaWaves = hashCnt - (15 * countOfSeaMonsters)
	printImage(seaMonsterList)
	print('seaWaves',seaWaves)

seaMonsterList = rotateSeaMonster(seaMonsterList)
countOfSeaMonsters = countSeaMonsters(seaMonsterList,newArr)
if countOfSeaMonsters > 0:
	print('countOfSeaMonsters',countOfSeaMonsters)
	seaWaves = hashCnt - (15 * countOfSeaMonsters)
	printImage(seaMonsterList)
	print('seaWaves',seaWaves)


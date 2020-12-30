""" 
D20P1
"""

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

def rotateImage(inImage):
	rotImage = []
	yLen = len(inImage)
	xLen = len(inImage[0])
	for y in range(yLen):
		newRow = []
		for x in range(yLen):
			#print('(x,y)',x,y)
			newRow.append(inImage[x][yLen-y-1])
		rotImage.append(newRow)
	return rotImage

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
	# print('(evalEdges): image number',image[0])
	theImage = image[1:]
	# print('(evalEdges): original image')
	# printImage(theImage)
	lfValsList = []
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	# printImage(theImage)
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	# printImage(theImage)
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	# printImage(theImage)
	lfValsList.append(edgeValLeftToRight(theImage[0]))
	lfValsList.append(edgeValRightToLeft(theImage[0]))
	theImage = rotateImage(theImage)
	#printImage(theImage)
	# print('lfValsList',lfValsList,'\n')
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
	# print('matchedEdges',matchedEdges)

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
				#print('nodeNumber',nodeNumber,'otherNode',otherNode)
				if firstSecond == 'First':
					matchingNodeNumber.append(otherNode)
					firstSecond = 'Second'
				else:
					firstSecond = 'First'
		newEdgesDict[nodeNumber] = matchingNodeNumber

	print('(makeNewEdgesDict) : [top,left,bottom,right]')
	print('(makeNewEdgesDict) : newEdgesDict')
	for row in newEdgesDict:
		print('  ',row,newEdgesDict[row])
	return newEdgesDict

def flipHoriz(theList):
	print('(flipHoriz) : flipping horizontally')
	newList = []
	for row in range(len(theList)):
		newRow = []
		for col in range(len(theList[0])):
			newRow.append(theList[col][len(theList[0])-row-1])
		newList.append(newRow)
	return newList

def flipVert(theList):
	print('(flipVert) : flipping vertically')
	newList = []
	for row in range(len(theList)):
		newRow = []
		for col in range(len(theList[0])):
			newRow.append(theList[len(theList)-col-1][row])
		newList.append(newRow)
	return newList
	
def trimEdges(theList):
	print('(trimEdges) : trimming ')
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
	print('(transformBlock) : IDVal',IDVal)
	#  transformedDictVal [[2203, 3457, 1039, 3517], True, False, True]
	print('(transformBlock) : transformedDictVal',transformedDictVal)
	# preTransformedArray [['#', '#', '.', '#', '.', '#', '#', '#', '#', '#'], ['#', '.', '.', '#', '.', '.', '#', '.', '#', '#'], ['.', '.', '#', '#', '.', '.', '#', '.', '.', '#'], ['#', '.', '.', '#', '.', '#', '#', '.', '#', '#'], ['#', '.', '#', '.', '.', '#', '.', '.', '.', '.'], ['.', '#', '.', '#', '.', '#', '#', '.', '.', '#'], ['.', '#', '#', '#', '#', '.', '.', '.', '.', '.'], ['#', '.', '.', '#', '.', '.', '.', '#', '.', '#'], ['#', '.', '.', '.', '#', '.', '.', '.', '.', '#'], ['.', '#', '.', '#', '.', '#', '#', '.', '.', '#']]
	print('(transformBlock) : preTransformedArray')
	print(preTransformedArray)
	# assert False,'check here'
	# print('IDsArray')
	rotatedArray = []
	if transformedDictVal[1]:
		rotatedArray = rotateImage(preTransformedArray)
	else:
		rotatedArray = preTransformedArray
	horizFlipped = []
	if transformedDictVal[2]:
		horizFlipped = flipHoriz(rotatedArray)
	else:
		horizFlipped = rotatedArray
	vertFlipped = []
	if transformedDictVal[3]:
		vertFlipped = flipVert(horizFlipped)
	else:
		vertFlipped = horizFlipped
	trimmedArray = trimEdges(preTransformedArray)
	return trimmedArray
	
######################################################################
# Program follows
inList = readFileOfStringsToListOfLists('input1.txt')

# bigList [[2311, ['.', '.', '#', '#', '.', '#', '.', '.', '#', '.'], ...
bigList = makeBetterList(inList)
# print('bigList',bigList)

# edgesList [[2311, [300, 210, 616, 89, 231, 924, 498, 318]], [1951, [397, 710, 318, 498, 564, 177, 841, 587]], [1171, [399, 966, 18, 288, 24, 96, 902, 391]], [1427, [183, 948, 348, 234, 210, 300, 576, 9]], [1489, [43, 848, 288, 18, 948, 183, 565, 689]], [2473, [481, 542, 184, 116, 234, 348, 966, 399]], [2971, [532, 161, 689, 565, 85, 680, 456, 78]], [2729, [680, 85, 9, 576, 710, 397, 271, 962]]]
edgesList = makeEdgesList(bigList)

allEdgeVals = countEdges(edgesList)

cornerPieces = findCorners(edgesList)

solvePt1(cornerPieces)

newEdgesDict = makeNewEdgesDict(allEdgeVals,edgesList)

# print(cornerPieces[0],'matches',newEdgesDict[cornerPieces[0]])
# print(cornerPieces[1],'matches',newEdgesDict[cornerPieces[1]])
# print(cornerPieces[2],'matches',newEdgesDict[cornerPieces[2]])
# print(cornerPieces[3],'matches',newEdgesDict[cornerPieces[3]])
IDsArray = []
IDsRow = []
for corner in range(4):
	# print('CornerList',newEdgesDict[cornerPieces[corner]])
	if (newEdgesDict[cornerPieces[corner]][2] != -1) and (newEdgesDict[cornerPieces[corner]][3] != -1):
		currentID = cornerPieces[corner]
# Fill in top row
print('(main) : [top,left,bottom,right]')
print('(main) : Upper Left Corner ID',currentID,end = '')
print(', corner vals',newEdgesDict[currentID])
lastCellInRow = False
transformedList = []
transformedLine = []
transformedDict = {}
transformedLine.append(newEdgesDict[currentID])
transformedLine.append(0)
transformedLine.append(False)
transformedLine.append(False)
transformedDict[currentID] = transformedLine
while not lastCellInRow:
	# print('transformedDict[currentID]',transformedDict[currentID])
	upVal = transformedDict[currentID][0][0]
	leftVal = transformedDict[currentID][0][1]
	downVal = transformedDict[currentID][0][2]
	rightVal = transformedDict[currentID][0][3]
	nextVal0 = newEdgesDict[rightVal][0]
	nextVal1 = newEdgesDict[rightVal][1]
	nextVal2 = newEdgesDict[rightVal][2]
	nextVal3 = newEdgesDict[rightVal][3]
	print('(main) : before rightVal',rightVal,nextVal0,nextVal1,nextVal2,nextVal3)
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
		print('  cell',rightVal,'rotated')
	else:
		print('  cell',rightVal,'not rotated')
	flippedHoriz = False
	if currentID == nextVal3:
		n1 = nextVal1
		nextVal1 = nextVal3
		nextVal3 = n1
		flippedHoriz = True
		print('  cell',rightVal,'flipped horizontally')
	else:
		print('  cell',rightVal,'not flipped horizontally')
	flippedVert = False
	if nextVal2 == -1:
		n0 = nextVal0
		nextVal0 = nextVal2
		nextVal2 = n0
		print('  cell',rightVal,'flipped vertically')
		flippedVert = True
	else:
		print('  cell',rightVal,'not flipped vertically')
	print('(main) : After rightVal',rightVal,nextVal0,nextVal1,nextVal2,nextVal3)
	IDsRow.append(currentID)
	currentID = rightVal
	countNeg1s = 0
	if newEdgesDict[currentID][0] == -1:
		countNeg1s += 1
	if newEdgesDict[currentID][1] == -1:
		countNeg1s += 1
	if newEdgesDict[currentID][2] == -1:
		countNeg1s += 1
	if newEdgesDict[currentID][3] == -1:
		countNeg1s += 1
	if countNeg1s == 2:
		print('  end of first row')
		lastCellInRow = True
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
	# print('transformedDict[currentID]',transformedDict[currentID])
IDsRow.append(currentID)
IDsArray.append(IDsRow)

# print('transformedDict top row',transformedDict)
widthOfField = len(transformedDict)
print('(main) : IDsArray',IDsArray)
print('(main) : widthOfField',widthOfField)
for row in range(1,12):
	IDsRow = []
	for col in range(widthOfField):
		prevRowID = IDsArray[row-1][col]
		print('(main) : prevRowID',prevRowID)
		print('')
		currentID = transformedDict[prevRowID][0][2]
		print('(main) : currentID',currentID,'newEdgesDict[currentID]',newEdgesDict[currentID])
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
			print('  cell',rightVal,'rotated')
		else:
			print('  cell',rightVal,'not rotated')
		flippedHoriz = False
		print('  row',row,'col',col,'IDsRow',IDsRow)
		if col == 0:
			if nextVal1 != -1:
				n1 = nextVal1
				nextVal1 = nextVal3
				nextVal3 = n1
				flippedHoriz = True
				print('  cell',rightVal,'flipped horizontally')
			else:
				print('  cell',rightVal,'not flipped horizontally')
		elif IDsRow[col-1] == nextVal1:
			n1 = nextVal1
			nextVal1 = nextVal3
			nextVal3 = n1
			flippedHoriz = True
			print('  cell',rightVal,'flipped horizontally')
		else:
			print('  cell',rightVal,'not flipped horizontally')
		flippedVert = False
		if nextVal0 != IDsArray[row-1][col]:
			n0 = nextVal0
			nextVal0 = nextVal2
			nextVal2 = n0
			print('  cell','flipped vertically')
			flippedVert = True
		else:
			print('  cell','not flipped vertically')
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

for col in range(len(IDsArray)):
	newDict = {}
	for row in range(len(IDsArray[0])):
		currentBlock = IDsArray[col][row]
		# print('(main) : currentBlock',currentBlock) #,end = ' ')
		# print('(main) : transformedDict[currentBlock]','id',currentBlock,'val',transformedDict[currentBlock])
		for subArray in bigList:
			if subArray[0] == currentBlock:
				# print('(main) : subArray: ',subArray)
				subBlock = subArray[1:]
		# print('(main) : subBlock',subBlock)
		newBlock = transformBlock(currentBlock,transformedDict[currentBlock],subBlock)
		newDict[IDsArray[col][row]] = newBlock
print('newEdgesDict')
print(newEdgesDict)


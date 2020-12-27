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

# Program follows
inList = readFileOfStringsToListOfLists('input1.txt')

# bigList [[2311, ['.', '.', '#', '#', '.', '#', '.', '.', '#', '.'], ...
bigList = makeBetterList(inList)
# print('bigList',bigList)

# print('\nSides values list')
# edgesList [[2311, [300, 210, 616, 89, 231, 924, 498, 318]], [1951, [397, 710, 318, 498, 564, 177, 841, 587]], [1171, [399, 966, 18, 288, 24, 96, 902, 391]], [1427, [183, 948, 348, 234, 210, 300, 576, 9]], [1489, [43, 848, 288, 18, 948, 183, 565, 689]], [2473, [481, 542, 184, 116, 234, 348, 966, 399]], [2971, [532, 161, 689, 565, 85, 680, 456, 78]], [2729, [680, 85, 9, 576, 710, 397, 271, 962]]]
edgesList = []
for image in bigList:
	edgesLine = []
	edgesLine.append(image[0])
	edgeVals = evalEdges(image)
	edgesLine.append(edgeVals)
	edgesList.append(edgesLine)
# print('edgesList',edgesList)

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
# for edge in edgesList:
	# print('Id',edge[0],end = ' ')
	# for val in edge[1]:
		# print(val,end=' ')
		# pass
	# print()
# listOfEdges = []
# allEdgeVals {300: 1, 210: 1, 616: 0, 89: 0, 231: 0, 924: 0, 498: 1, 318: 1, 397: 1, 710: 1, 564: 0, 177: 0, 841: 0, 587: 0, 399: 1, 966: 1, 18: 1, 288: 1, 24: 0, 96: 0, 902: 0, 391: 0, 183: 1, 948: 1, 348: 1, 234: 1, 576: 1, 9: 1, 43: 0, 848: 0, 565: 1, 689: 1, 481: 0, 542: 0, 184: 0, 116: 0, 532: 0, 161: 0, 85: 1, 680: 1, 456: 0, 78: 0, 271: 0, 962: 0}
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
print('corner pieces',cornerPieces)
total = 1
for end in cornerPieces:
	total *= end
print('Pt 1 val =',total)

initialCornerId = cornerPieces[0]
# print('initialCornerId',initialCornerId)

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

print('newEdgesDict')
for row in newEdgesDict:
	print(row,newEdgesDict[row])
print('initialCornerId',initialCornerId)
print(cornerPieces[0],'matches',newEdgesDict[cornerPieces[0]])
print(cornerPieces[1],'matches',newEdgesDict[cornerPieces[1]])
print(cornerPieces[2],'matches',newEdgesDict[cornerPieces[2]])
print(cornerPieces[3],'matches',newEdgesDict[cornerPieces[3]])
for corner in range(4):
	print('CornerList',newEdgesDict[cornerPieces[corner]])
	if (newEdgesDict[cornerPieces[corner]][2] != -1) and (newEdgesDict[cornerPieces[corner]][3] != -1):
		upperLeftCornerID = cornerPieces[corner]
print('Upper Left Corner ID',upperLeftCornerID)

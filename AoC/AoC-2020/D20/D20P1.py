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
	print('tileCount',tileCount)
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
# Program follows
inList = readFileOfStringsToListOfLists('input.txt')
		
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
print('edgesList',edgesList)

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
for edge in edgesList:
	print('Id',edge[0],end = ' ')
	for val in edge[1]:
		print(val,end=' ')
	print()
listOfEdges = []
allEdgeVals = {}
for edge in edgesList:
	for edgeVal in edge[1]:
		if edgeVal not in allEdgeVals:
			allEdgeVals[edgeVal] = 1
		else:
			allEdgeVals[edgeVal] += 1
print('allEdgeVals')
print(allEdgeVals)
minVal = 9999
maxVal = 0
for shape in edgesList:
	# print('Key Id',shape[0],end = ' ')
	totalEdges = 0
	for keyVal in shape[1]:
		# print(keyVal,allEdgeVals[keyVal],end=' ')
		totalEdges += allEdgeVals[keyVal]
	if totalEdges < minVal:
		minVal = totalEdges
	if totalEdges > maxVal:
		maxVal = totalEdges
	# print('totalEdges',totalEdges)
print('minVal',minVal)
print('maxVal',maxVal)

ends = []
for shape in edgesList:
	print('Key Id',shape[0],end = ' ')
	totalEdges = 0
	for keyVal in shape[1]:
		print(keyVal,allEdgeVals[keyVal],end=' ')
		totalEdges += allEdgeVals[keyVal]
	if totalEdges == minVal:
		ends.append(shape[0])
	print('totalEdges',totalEdges>>1)

print('corner pieces',ends)
total = 1
for end in ends:
	total *= end

print('val',total)

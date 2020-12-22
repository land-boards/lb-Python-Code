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
	# print('image number',image[0])
	theImage = image[1:]
	# print('original image')
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

inList = readFileOfStringsToListOfLists('input.txt')
		
bigList = makeBetterList(inList)

edgesList = []
for image in bigList:
	edgesLine = []
	edgesLine.append(image[0])
	edgeVals = evalEdges(image)
	edgesLine.append(edgeVals)
	edgesList.append(edgesLine)

print('edgesList',edgesList)
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

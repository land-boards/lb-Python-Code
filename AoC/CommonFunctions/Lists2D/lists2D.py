# rotate 2D list
newList = list(zip(*oldList[::-1]))

# make 2D list
newArr = []
pixelsTall = 10
pixelsWide = 10
initVal = ''
for ct in range(pixelsTall):
	newLine = []
	for ct in range(pixelsWide):
		newLine.append(initVal)
	newArr.append(newLine)

# print 2D array
def printImage(theImage):
	print()
	for row in theImage:
		for col in row:
			print(col,end='')
		print()

# flip 2D array horizontally	
def flipHoriz(theList):
	debugPrint('(flipHoriz) : flipping horizontally')
	newList = []
	for row in range(len(theList)):
		newRow = []
		for col in range(len(theList[0])):
			newRow.append(theList[row][len(theList[0])-col-1])
		newList.append(newRow)
	return newList

# flip 2D array vertically
def flipVert(theList):
	debugPrint('(flipVert) : flipping vertically')
	newList = []
	for row in range(len(theList)):
		newRow = []
		for col in range(len(theList[0])):
			newRow.append(theList[len(theList)-row-1][col])
		newList.append(newRow)
	return newList


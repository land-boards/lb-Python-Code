# 2871 is too high

def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def makeArray(inList):
	row2d = []
	lenY = len(inList)
	lenX = len(inList[0])
	# print("lenY",lenY)
	# print("lenX",lenX)
	for offY in range(lenY +2):
		newRow = []
		for offX in range(lenX + 2):
			newRow.append('.')
		row2d.append(newRow)
	return row2d

def countLights(lightArray):
	lenY = len(lightArray)
	lenX = len(lightArray[0])
	lightCount = 0
	for offY in range(1,lenY-1):
		for offX in range(1,lenX-1):
			if lightArray[offY][offX] == '#':
				lightCount += 1
	return lightCount

def fillArray(inList):
	row2d = []
	lenY = len(inList)
	lenX = len(inList[0])
	# print("lenY",lenY)
	# print("lenX",lenX)
	newRow = []
	for off in range(lenX + 2):
		newRow.append('.')
	row2d.append(newRow)
	for row in inList:
		newRow = []
		newRow.append('.')
		for charInRow in row:
			newRow.append(charInRow)
		newRow.append('.')
		row2d.append(newRow)
	newRow = []
	for off in range(lenX + 2):
		newRow.append('.')
	row2d.append(newRow)
	return row2d

def neighborCount(yoff,xoff,row2d):
	count = 0
	if row2d[yoff-1][xoff-1] == '#':
		count += 1
	if row2d[yoff-1][xoff] == '#':
		count += 1
	if row2d[yoff-1][xoff+1] == '#':
		count += 1
	if row2d[yoff][xoff-1] == '#':
		count += 1
	if row2d[yoff][xoff+1] == '#':
		count += 1
	if row2d[yoff+1][xoff-1] == '#':
		count += 1
	if row2d[yoff+1][xoff] == '#':
		count += 1
	if row2d[yoff+1][xoff+1] == '#':
		count += 1
	return count

inList = readFileToList()
# print(inList)
row2d = fillArray(inList)
lenY = len(inList)
lenX = len(inList[0])
loopCount = 100
while loopCount > 0:
	newArray = makeArray(inList)
	for yoff in range(1,lenY+1):
		for xoff in range(1,lenX+1):
			count = neighborCount(yoff,xoff,row2d)
			if row2d[yoff][xoff] == '#':
				if (count == 2) or (count == 3):
					newArray[yoff][xoff] = '#'
				else:
					newArray[yoff][xoff] = '.'
			else:
				if count == 3:
					newArray[yoff][xoff] = '#'
				else:
					newArray[yoff][xoff] = '.'
	row2d = newArray
	loopCount -= 1
	print("loopCount",loopCount)
#print(row2d)
print(countLights(row2d))

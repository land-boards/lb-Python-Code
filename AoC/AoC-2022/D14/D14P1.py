'''
D14P1.py

'''

def printArray(newArr):
	global minX
	global maxX
	global minY
	global maxY
	for y in range(minY,maxY+1):
		for x in range(minX,maxX+1):
			print(newArr[y][x],end='')
		print()

def fillArray(segList):
	# draw lines
	for seg in segList:
		for pair in range(len(seg)-1):
			startX = seg[pair][0]
			startY = seg[pair][1]
			endX = seg[pair+1][0]
			endY = seg[pair+1][1]
			newArr[startY][startX] = '#'
			newArr[endY][endX] = '#'
			if startX == endX:
				if startY > endY:
					for y in range(endY,startY):
						newArr[y][startX] = '#'
				else:
					for y in range(startY,endY):
						newArr[y][startX] = '#'
			if startY == endY:
				# print('horiz',startX,endX)
				if startX > endX:
					for x in range(endX,startX):
						newArr[startY][x] = '#'
						# print(x,startY)
				else:
					for x in range(startX,endX):
						newArr[startY][x] = '#'
						# print(x,startY)

def dropSand():
	global minX
	global maxX
	global minY
	global maxY
	sandMoving = True
	sandX = 500
	sandY = 0
	# print('minX',minX,'maxX',maxX)
	# print('minY',minY,'maxY',maxY)
	while sandMoving:
		if newArr[sandY+1][sandX] == '.':
			sandY += 1
		elif newArr[sandY+1][sandX-1] == '.':
			sandY += 1
			sandX -= 1
		elif newArr[sandY+1][sandX+1] == '.':
			sandY += 1
			sandX += 1
		else:
			sandMoving = False
		# print('sandX,sandY',sandX,sandY)
		# minX 494 maxX 503
		# minY 0 maxY 9
		if sandX<minX:
			return False
		if sandX>=maxX:
			return False
		if sandY == maxY:
			return False
	newArr[sandY][sandX] = 'o'
	# input('hit key')
	return True
	
fileName = 'input.txt'
# fileName = 'input1.txt'

inList=[]
theList=[]

segments = []
with open(fileName, 'r') as filehandle:  
	lineSegmentsList = []
	for line in filehandle:
		inLine = line.strip('\n')
		# print('inLine -',inLine)
		lineSegmentsList.append(inLine.split(' -> '))
# print('lineSegmentsList',lineSegmentsList)

segList = []
for points in lineSegmentsList:
	lineList=[]
	for segment in points:
		pointsString = segment.split(',')
		# print('pointsString',pointsString)
		lineList.append([int(pointsString[0]),int(pointsString[1])])
		# print('lineList',lineList)
	segList.append(lineList)
# print('segList',segList)

minX = 500
maxX = 500
minY = 0
maxY = 0
for seg in segList:
	for pair in range(len(seg)-1):
		# print('line from',seg[pair],'to',seg[pair+1])
		if seg[pair][0] < minX:
			minX = seg[pair][0]
		if seg[pair][0] > maxX:
			maxX = seg[pair][0]
		if seg[pair][1] < minY:
			minY = seg[pair][1]
		if seg[pair][1] > maxY:
			maxY = seg[pair][1]
		if seg[pair+1][0] < minX:
			minX = seg[pair+1][0]
		if seg[pair+1][0] > maxX:
			maxX = seg[pair+1][0]
		if seg[pair+1][1] < minY:
			minY = seg[pair+1][1]
		if seg[pair+1][1] > maxY:
			maxY = seg[pair+1][1]
print('minX',minX,'maxX',maxX)
print('minY',minY,'maxY',maxY)

# make 2D list
newArr = []
pixelsTall = maxY
pixelsWide = maxX
initVal = '.'
for ct in range(pixelsTall+1):
	newLine = []
	for ct in range(pixelsWide+1):
		newLine.append(initVal)
	newArr.append(newLine)
# printArray(newArr)
# print()

fillArray(segList)
printArray(newArr)
print()

sandCount = 0
insertedSand = True
while insertedSand:
	insertedSand = dropSand()
#	printArray(newArr)
	sandCount += 1

printArray(newArr)
print()
	
print('sandCount',sandCount-1)


# DougAmpWHH123!
# D04P1.py
# 2021 Advent of Code
# Day 4
# Part 1
# 3852 is too low
# Answer was 5147

# readFileOfStringsToListOfLists
def readFileOfStringsToList(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	return inList

# returns list of x1,y1,x2,y3 line segments
def makeLinesList(inList):
	lineList = []
	for line in inList:
		newList = line.replace(' -> ',',')
		#print("newList",newList)
		newLineList = newList.split(',')
		newRow = []
		newRow.append(int(newLineList[0]))
		newRow.append(int(newLineList[1]))
		newRow.append(int(newLineList[2]))
		newRow.append(int(newLineList[3]))
		lineList.append(newRow)
	# print("List of all lines",lineList)
	return lineList

# Return list of straight lines
def makeStraightLionesList(lineList):
	straightLines = []
	for line in lineList:
		if line[0] == line[2]:
			straightLines.append(line)
		elif line[1] == line[3]:
			straightLines.append(line)
		# if (line[0] == line[2]) and (line[1] == line[3]):
			# print("Single point",line)
		# else:
			# print("Discarding",line)
	# print("List of all straight lines")
	# for line in straightLines:
		# print(line)
	return straightLines

inList = readFileOfStringsToList('input.txt')
lineList = makeLinesList(inList)
straightLines = makeStraightLionesList(lineList)

filledPoints = {}
for line in straightLines:
	if line[0] == line[2]:
		xVal = line[0]
		if line[1] < line[3]:
			yStart = line[1]
			yEnd = line[3]
		else:
			yStart = line[3]
			yEnd = line[1]
		for yVal in range(yStart,yEnd+1):
			currentPoint = (xVal,yVal)
			if currentPoint in filledPoints:
				filledPoints[currentPoint] += 1
			else:
				filledPoints[currentPoint] = 1

	elif line[1] == line[3]:
		yVal = line[1]
		if line[0] < line[2]:
			xStart = line[0]
			xEnd = line[2]
		else:
			xStart = line[2]
			xEnd = line[0]
		for xVal in range(xStart,xEnd+1):
			currentPoint = (xVal,yVal)
			if currentPoint in filledPoints:
				filledPoints[currentPoint] += 1
			else:
				filledPoints[currentPoint] = 1

# print("filledPoints",filledPoints)		

overlapCount = 0
for point in filledPoints:
	# print("point",point,filledPoints[point])
	if filledPoints[point] > 1:
		overlapCount += 1
		# print("Overlap at",point)
print("overlapCount",overlapCount)
	
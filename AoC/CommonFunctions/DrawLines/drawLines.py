filledPoints = {}
for line in linesList:
	# print("line",line)	# horiz
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
	elif line[1] == line[3]:	# vert
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
	else:	# 45 degree diag
		print("line(diag)",line)
		xStart = line[0]
		yStart = line[1]
		xEnd = line[2]
		yEnd = line[3]
		if line[0] < line[2]:
			incXVal = 1
		else:
			incXVal = -1
		if line[1] < line[3]:
			incYVal = 1
		else:
			incYVal = -1
		print("incXVal,incYVal",incXVal,incYVal)
		xPos = xStart
		yPos = yStart
		while xPos != xEnd:
			currentPoint = (xPos,yPos)
			print("Fill point",currentPoint)
			if currentPoint in filledPoints:
				filledPoints[currentPoint] += 1
			else:
				filledPoints[currentPoint] = 1
			xPos += incXVal
			yPos += incYVal
		currentPoint = (xPos,yPos)
		print("Fill point",currentPoint)
		if currentPoint in filledPoints:
			filledPoints[currentPoint] += 1
		else:
			filledPoints[currentPoint] = 1

# print("filledPoints",filledPoints)		

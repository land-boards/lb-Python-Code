# D22P1.py
# 2021 Advent of Code
# Day 22
# Part 1

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def fillSpace(onOffFlag,xStart,xEnd,yStart,yEnd,zStart,zEnd):
	global spaceDict
	# print(onOffFlag,xStart,xEnd,yStart,yEnd,zStart,zEnd)
	# if xEnd < -50:
		# return
	# if xStart > 50:
		# return
	# if yEnd < -50:
		# return
	# if yStart > 50:
		# return
	# if zEnd < -50:
		# return
	# if zStart > 50:
		# return
	for zVal in range(zStart,zEnd+1):
		for yVal in range(yStart,yEnd+1):
			for xVal in range(xStart,xEnd+1):
				if (-50 <= xVal <= 50) and (-50 <= yVal <= 50) and (-50 <= zVal <= 50):
					spaceDict[(xVal,yVal,zVal)] = onOffFlag
				
	return

def countOnInSpace():
	global spaceDict
	onCount = 0
	for item in spaceDict:
		# print("countOnInSpace: item, spaceDict[item]",item,spaceDict[item])
		if spaceDict[item] == 'on':
			onCount += 1
	return onCount

inList = readFileToListOfStrings('input.txt')
# print(inList)
spaceDict = {}
for row in inList:
	row = row.replace("..",",")
	row = row.replace(" ",",")
	row = row.replace("=",",")
	rowList = row.split(",")
	# print(rowList)
	onOffFlag = rowList[0]
	xStart = int(rowList[2])
	xEnd = int(rowList[3])
	yStart = int(rowList[5])
	yEnd = int(rowList[6])
	zStart = int(rowList[8])
	zEnd = int(rowList[9])
	fillSpace(onOffFlag,xStart,xEnd,yStart,yEnd,zStart,zEnd)

# print("spaceDict",spaceDict)
# for item in spaceDict:
	# print("item, spaceDict[item]",item,spaceDict[item])
onCount = countOnInSpace()
print("onCount",onCount)

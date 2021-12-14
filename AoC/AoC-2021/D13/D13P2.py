# D14P1.py
# 2021 Advent of Code
# Day 13
# Part 1

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def makeArray(maxXVal,maxYVal):
	theArray = []
	for y in range(maxYVal+1):
		rowVals = []
		lineVals = []
		for x in range(maxXVal+1):
			lineVals.append('.')
		theArray.append(lineVals)
	return theArray

def printTheArray(theArray):
	for yVal in range(len(theArray)):
		for xVal in range(len(theArray[0])):
			print(theArray[yVal][xVal],end = '')
		print()

def countVals(theArray):
	count = 0
	for yVal in range(len(theArray)):
		for xVal in range(len(theArray[0])):
			if theArray[yVal][xVal] == '#':
				count += 1
	return count

def foldArray(theArray,foldDir,foldVal):
	# print("foldDir",foldDir)
	print("foldVal",foldVal)
	newArray = []
	if foldDir == 'y':
		newArray = makeArray(len(theArray[0])-1,foldVal-1)
		for yVal in range(foldVal):
			for xVal in range(len(newArray[0])):
				newArray[yVal][xVal] = theArray[yVal][xVal]
		# print("newArray")
		# printTheArray(newArray)
		fromYVal = foldVal + 1
		toYVal = foldVal - 1
		while (fromYVal < len(theArray)) and (toYVal >= 0):
			# print("fromYVal",fromYVal,end = ' ')
			# print("toYVal",toYVal)
			for xVal in range(len(theArray[0])):
				if theArray[fromYVal][xVal] == '#':
					newArray[toYVal][xVal] = '#'
			fromYVal += 1
			toYVal -= 1
	elif foldDir == 'x':
		newArray = makeArray(foldVal-1,len(theArray)-1)
		for yVal in range(len(theArray)):
			for xVal in range(foldVal):
				newArray[yVal][xVal] = theArray[yVal][xVal]
		fromXVal = foldVal + 1
		toXVal = foldVal - 1
		while (fromXVal < len(theArray[0])) and (toXVal >= 0):
			# print("fromXVal",fromXVal,end = ' ')
			# print("toXVal",toXVal)
			for yVal in range(len(theArray)):
				if theArray[yVal][fromXVal] == '#':
					newArray[yVal][toXVal] = '#'
			fromXVal += 1
			toXVal -= 1
	return newArray

inList = readFileToListOfStrings('input.txt')
# print(inList)
# for row in inList:
	# print(row)
stateVals = ['numPairs','blank','folds']
state = 'numPairs'
xyPairs = []
folds = []
maxXVal = 0
maxYVal = 0
for row in inList:
	if state == 'numPairs':
		if row == '':
			state = 'folds'
		else:
			# print("row =",row)
			pair = row.split(',')
			# print("pair",pair)
			xVal = int(pair[0])
			if xVal > maxXVal:
				maxXVal = xVal
			yVal = int(pair[1])
			if yVal > maxYVal:
				maxYVal = yVal
			xyPairs.append([xVal,yVal])
	elif state == 'folds':
		# print("row",row)
		line = row.split(' ')
		# print("line",line)
		dirNum = line[2].split('=')
		dirPair = [dirNum[0],int(dirNum[1])]
		folds.append(dirPair)
print("xyPairs",xyPairs)
print("folds",folds)
print("maxXVal",maxXVal)
print("maxYVal",maxYVal)
theArray = makeArray(maxXVal,maxYVal)
print("array size x",len(theArray[0]),"y",len(theArray))
# print("theArray",theArray)
for pair in xyPairs:
	xVal = pair[0]
	yVal = pair[1]
	theArray[yVal][xVal] = '#'
# print("theArray",theArray)
# printTheArray(theArray)
# count = countVals(theArray)
# print("count",count)
# print("First fold",folds[0])
# if folds[0][0] == 'y':
	# print("Folding on y at",folds[0][1],end=' ')
# elif folds[0][0] == 'x':
	# print("Folding on x at",folds[0][1])
# else:
	# assert False,"Illegal fold axis"
for fold in folds:
	theArray = foldArray(theArray,fold[0],fold[1])
	print("array size x",len(theArray[0]),"y",len(theArray))
	# printTheArray(theArray)
	count = countVals(theArray)
	print("count",count)
# theArray = foldArray(theArray,folds[1][0],folds[1][1])
printTheArray(theArray)
# count = countVals(theArray)
# print("count",count)

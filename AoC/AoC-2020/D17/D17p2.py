""" 
2020 D17 P1

Inputs like:
..##.......
#...#...#..
.#....#..#.

Output:
[['.', '.', '#', '#', '.', '.', '.', '.', '.', '.', '.'],
['#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.'],
['.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.']]

112 is too low

"""

import copy

DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileOfStringsToListOfLists(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(list(inLine))
	return inList

def countNeighbors(location,oldDict):
	global DEBUG_PRINT
	global neighborsOffsetList
	neighborCount = 0
	for neighbor in neighborsOffsetList:
		checkLoc = (location[0]+neighbor[0],location[1]+neighbor[1],location[2]+neighbor[2],location[3]+neighbor[3])
		if checkLoc in oldDict:
			debugPrint('found # at (x,y,z,w) = ' + str(checkLoc))
			neighborCount += 1
	return neighborCount

def makeNewDict(oldDict):
	global DEBUG_PRINT
	global neighborsOffsetList
	#DEBUG_PRINT = True
	debugPrint('(makeNewDict) : dict (before) = ' + str(oldDict))
	newDict = {}
	for location in oldDict:
		debugPrint('\nchecking around location ' + str(location))
		neighborCount = 0
		neighborCount = countNeighbors(location,oldDict)
		if (neighborCount == 2) or (neighborCount == 3):
			if location not in newDict:
				newDict[location] = '#'
		neighborCount = 0		
		for neighbor in neighborsOffsetList:
			checkLoc = (location[0]+neighbor[0],location[1]+neighbor[1],location[2]+neighbor[2],location[3]+neighbor[3])
			neighborCount = countNeighbors(checkLoc,oldDict)
			debugPrint('Location at ' + str(location) + ' has ' + str(neighborCount) + ' neighbor(s)')
			if (neighborCount == 3):
				debugPrint('new active location ' + str(location) + ' has ' + str(neighborCount) + ' neighbors active ')
				if checkLoc not in newDict:
					debugPrint('adding neighbor ' + str(neighbor))
					newDict[checkLoc] = '#'
	debugPrint('newDict (after) is '+ str(newDict) + '\n')
	DEBUG_PRINT = False
	return newDict

def printDict(arrayDict):
	xMax, xMin, yMax, yMin, zMax, zMin, wMax, wMin = 0,0,0,0,0,0,0,0
	for point in arrayDict:
		if point[0] > xMax:
			xMax = point[0]
		if point[0] < xMin:
			xMin = point[0]
		if point[1] > yMax:
			yMax = point[1]
		if point[1] < yMin:
			yMin = point[1]
		if point[2] > zMax:
			zMax = point[2]
		if point[2] < zMin:
			zMin = point[2]
		if point[3] > wMax:
			wMax = point[3]
		if point[3] < wMin:
			wMin = point[3]
	#print('max/min x,y,z,w',xMax, xMin, yMax, yMin, zMax, zMin, wMax, wMin)
	for w in range(wMin,wMax+1):
		for z in range(zMin,zMax+1):
			print('z=',z,'w=',w)
			for y in range(yMin,yMax+1):
				for x in range(xMin,xMax+1):
					if (x,y,z,w) in arrayDict:
						print('#',end='')
					else:
						print('.',end='')
				print()
			print()
		print(point)

# program
inList = readFileOfStringsToListOfLists('input.txt')
debugPrint(str(inList))

# list of offsets to all possible neighbors
neighborsOffsetList = []
for w in range(-1,2,1):
	for z in range(-1,2,1):
		debugPrint(z)
		for y in range(-1,2,1):
			for x in range(-1,2,1):
				if (x,y,z,w) != (0,0,0,0):
					neighborsOffsetList.append((x,y,z,w))
debugPrint('neighborsOffsetList' + str(neighborsOffsetList))
debugPrint(str(len(neighborsOffsetList)))

w = 0
z = 0
conroySpaceDict = {}
for y in range(len(inList)):
	for x in range(len(inList[0])):
		debugPrint(str(inList[y][x]))
		if inList[y][x] == '#':
			conroySpaceDict[(x,y,z,w)] = '#'
	debugPrint('')
debugPrint(str(conroySpaceDict))
for dictItem in conroySpaceDict:
	debugPrint(str(dictItem))
printDict(conroySpaceDict)
for loopCount in range(6):
	print(loopCount)
	debugPrint(str(loopCount))
	conroySpaceDict = copy.deepcopy(makeNewDict(conroySpaceDict))
	printDict(conroySpaceDict)
	print('filled count',len(conroySpaceDict))
debugPrint(str(conroySpaceDict))

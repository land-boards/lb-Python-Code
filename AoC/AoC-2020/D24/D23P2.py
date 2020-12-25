""" 

AoC 2020 D24P2

181 too low

Hex shapes encoded as cube coordinates
	https://www.redblobgames.com/grids/hexagons/

"""

import math

DEBUG_PRINT = True
#DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def parseInList():
	global inList
	newList = []
	for row in inList:
		off = 0
		newRow = []
		while off < len(row):
			if row[off] == 'n' or row[off] == 's':
				newRow.append(row[off:off+2])
				off += 2
			elif row[off] == 'e' or row[off] == 'w':
				newRow.append(row[off])
				off += 1
		newList.append(newRow)
	return newList

def initList(dirsLists):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	posList = []
	for row in dirsLists:
		pos = [0,0,0]
		for elem in row:
			if elem == 'e':
				pos[0] += 1
				pos[1] += -1
			elif elem == 'w':
				pos[0] += -1
				pos[1] += 1
			elif elem == 'ne':
				pos[0] += 1
				pos[2] += -1
			elif elem == 'sw':
				pos[0] += -1
				pos[2] += 1
			elif elem == 'nw':
				pos[1] += 1
				pos[2] += -1
			elif elem == 'se':
				pos[1] += -1
				pos[2] += 1
		foundAtPos = False
		for item in posList:
			if item[0] == pos:
				oldColor = item[1]
				if oldColor == 'white':
					color = 'black'
				else:
					color = 'white'
				item[1] = color
				foundAtPos = True
		if not foundAtPos:
			newLineVal = []
			newLineVal.append(pos)
			newLineVal.append('black')
			posList.append(newLineVal)
	debugPrint('(initList): posList' + str(posList))
	return posList

def removeWhites(inList):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('(removeWhites): before number of whole list ' + str(len(inList)))
	outList = []
	for checkLocation in inList:
		if checkLocation[1] == 'black':
			outList.append(checkLocation)
	debugPrint('(removeWhites): after number of blacks only ' + str(len(outList)))
	return outList

def addOffsetToBase(base,offset):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	hexOffsetList = [[0,1,-1],[0,-1,1],[1,0,-1],[-1,0,1],[1,-1,0],[-1,1,0]]
	debugPrint('(addOffsetToBase): base ' + str(base))
	debugPrint('offset ' + str(offset))
	xVal = base[0] + hexOffsetList[offset][0]
	yVal = base[1] + hexOffsetList[offset][1]
	zVal = base[2] + hexOffsetList[offset][2]
	newList = []
	newList.append(xVal)
	newList.append(yVal)
	newList.append(zVal)
	return newList

def padCellList(onlyBlackCellsList,blackCellsXYZsList):
	"""
	padCellList - make cells surrounding all black into white
	"""
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('(padCellList): onlyBlackCellsList' + str(onlyBlackCellsList))
	debugPrint('(padCellList): before len onlyBlackCellsList ' + str(len(onlyBlackCellsList)))
	allLocationsToCheck = []
	for checkLocation in onlyBlackCellsList:
		for hexValOffset in range(6):
			padCellLocation = addOffsetToBase(checkLocation[0],hexValOffset)
			# Make sure the cell isn't black already
			# if padCellLocation not in blackCellsXYZsList:
			if padCellLocation not in blackCellsXYZsList:
				cellWhole = []
				cellWhole.append(padCellLocation)
				cellWhole.append('white')
				allLocationsToCheck.append(cellWhole)
		allLocationsToCheck.append(checkLocation)
	DEBUG_PRINT = False
	debugPrint('(padCellList): After len allLocationsToCheck ' + str(len(allLocationsToCheck)))
	debugPrint('(padCellList):allLocationsToCheck: ' + str(allLocationsToCheck))
	return allLocationsToCheck
	
def countBlackNeighbors(checkLocation,blackCellsXYZsList):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	neighborCount = 0
	debugPrint('(countBlackNeighbors): checking locn ' + str(checkLocation))
	for hexValOffset in range(6):
		neighborLocation = addOffsetToBase(checkLocation,hexValOffset)
		if neighborLocation in blackCellsXYZsList:
			neighborCount += 1
	return neighborCount

def evalNeighbors(blackCellsPaddedWithWhiteCells,blackCellsXYZsList):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	outList = []
	# debugPrint('(evalNeighbors) len of blackCellsXYZsList ' + str(len(blackCellsXYZsList)))
	for cell in blackCellsPaddedWithWhiteCells:
		neighborCount = countBlackNeighbors(cell[0],blackCellsXYZsList)
		DEBUG_PRINT = False
		# debugPrint('(evalNeighbors) ' + str(cell[1]) + ' location ' + str(cell[0]) + ' has ' + str(neighborCount) + ' black neighbors')
		if cell[1] == 'white':
			if neighborCount == 2:
				outLine = []
				outLine.append(cell[0])
				outLine.append('black')
				if outLine not in outList:
					debugPrint('(evalNeighbors) ' + str(cell[1]) + ' locn ' + str(cell[0]) + ' is not in list - adding ' + str(outLine))
					outList.append(outLine)
				elif DEBUG_PRINT:
					debugPrint('(evalNeighbors) locn ' + str(cell[0]) + ' is already black ' + str(outLine))
			else:
				debugPrint('(evalNeighbors) Leaving locn ' + str(cell[1]) + ' '+ str(cell[0]))
				outList.append(cell)
		elif cell[1] == 'black':
			if (neighborCount == 0) or (neighborCount > 2):
				outLine = []
				outLine.append(cell[0])
				outLine.append('white')
				if outLine not in outList:
					debugPrint('(evalNeighbors) locn ' + str(cell[1]) + ' ' + str(cell[0]) + ' is not in list - adding ' + str(outLine))
					outList.append(outLine)
				elif DEBUG_PRINT:
					debugPrint('(evalNeighbors) locn ' + str(cell[0]) + 'is already white' + str(outLine))
			else:
				debugPrint('(evalNeighbors) Leaving locn ' + str(cell[1]) + ' '+ str(cell[0]))
				outList.append(cell)
	return outList

def conwayIt(inList):
	onlyBlackCellsList = removeWhites(inList)
	blackCellsXYZsList = []
	for blackCells in onlyBlackCellsList:
		blackCellsXYZsList.append(blackCells[0])
	blackCellsPaddedWithWhiteCells = padCellList(onlyBlackCellsList,blackCellsXYZsList)
	outList = evalNeighbors(blackCellsPaddedWithWhiteCells,blackCellsXYZsList)
	return outList

# program follows
inList = readFileToListOfStrings('input.txt')
# inList = readFileToListOfStrings('input1.txt')
# inList = ['esenee','esew','nwwswee']
# inList = ['nwwswee']
dirsLists = parseInList()
posList = initList(dirsLists)
for loopCount in range (0,101):
	print('Day',loopCount,end=' ')
	blackCount = 0
	for row in posList:
		if row[1] == 'black':
			blackCount += 1
	print('- black locations count',blackCount)
	posList = conwayIt(posList)
	
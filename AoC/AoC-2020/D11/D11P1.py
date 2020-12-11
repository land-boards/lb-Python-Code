""" 
AoC D11 P1
"""

import copy

DEBUG_PRINT = True
DEBUG_PRINT = False
def debugPrint(thingToPrint):
	global DEBUG_PRINT
	if DEBUG_PRINT:
		print(thingToPrint)
		
def readFileOfStringsToListOfLists(fileName):
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(list(inLine))
	return inList

def padWithFloor(inList):
	newList = []
	rowLen = len(inList[0])
	endRow = []
	for hor in range(rowLen+2):
		endRow.append('.')
	newList.append(endRow)
	for y in range(len(inList)):
		newRow = []
		newRow.append('.')
		for x in range(len(inList[0])):
			newRow.append(inList[y][x])
		newRow.append('.')
		newList.append(newRow)
	endRow = []
	for hor in range(rowLen+2):
		endRow.append('.')
	newList.append(endRow)
	return newList

def printFloorplan(inList):
	for row in inList:
		for seat in row:
			print(seat,end='')
		print('')

def countNeighbors(inList,y,x):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('(hasNoNeighbor) passed: '+str(y)+' '+str(x))
	occupiedCount = 0
	offsetsList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
	for offset in offsetsList:
		debugPrint('offset'+str(offset))
		if inList[y+offset[0]][x+offset[1]] == '#':
			debugPrint('had neighbor at '+str(y+offset[0])+' '+(str(x+offset[1])))
			occupiedCount += 1
	return occupiedCount
	
def runRules(inList):
	"""
	runRules
	If a seat is empty (L) and there are no occupied seats adjacent to it, 
	the seat becomes occupied.
	If a seat is occupied (#) and four or more seats adjacent to it are 
	also occupied, the seat becomes empty.
	Otherwise, the seat's state does not change.
	"""
	newList = []
	for y in range(len(inList)):
		newRow = []
		for x in range(len(inList[0])):
			if inList[y][x] == '.':
				newRow.append('.')
			elif inList[y][x] == 'L':	# seat is empty
				if countNeighbors(inList,y,x) == 0:
					newRow.append('#')
				else:
					newRow.append('L')
			elif inList[y][x] == '#':	# seat is occupied
				if countNeighbors(inList,y,x) >= 4:
					newRow.append('L')
				else:
					newRow.append(inList[y][x])
		newList.append(newRow)
	return newList
	
def countSeats(inList):
	seatCount = 0
	for y in range(len(inList)):
		for x in range(len(inList[0])):
			if inList[y][x] == '#':
				seatCount += 1
	return seatCount

inList = readFileOfStringsToListOfLists('input.txt')
if DEBUG_PRINT:
	printFloorplan(inList)
	print('\nPadded floorplan')
newFloorPlan = padWithFloor(inList)
if DEBUG_PRINT:
	printFloorplan(newFloorPlan)
savedList = []

roundCount = 1
while savedList != newFloorPlan:
	savedList = copy.deepcopy(newFloorPlan)
	newFloorPlan2 = []
	newFloorPlan2 = runRules(newFloorPlan)
	debugPrint('\nAfter round '+str(roundCount))
	roundCount += 1
	if DEBUG_PRINT:
		printFloorplan(newFloorPlan2)
	newFloorPlan = copy.deepcopy(newFloorPlan2)

print('\nAfter all rounds')
if DEBUG_PRINT:
	printFloorplan(newFloorPlan)
print('count',countSeats(newFloorPlan))

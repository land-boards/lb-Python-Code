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
	for row in inList[1:len(inList)-1]:
		for seat in row[1:len(row)-1]:
			print(seat,end='')
		print('')

def countNeighbors(inList,y,x):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('(hasNoNeighbor) passed: '+str(y)+' '+str(x))
	neighborCount = 0
	offsetsList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
	for offset in offsetsList:
		debugPrint('offset'+str(offset))
		if inList[y+offset[0]][x+offset[1]] == '#':
			debugPrint('had neighbor at '+str(y+offset[0])+' '+(str(x+offset[1])))
			neighborCount += 1
	return neighborCount
	
def countNeighborsPt2(inList,y,x):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	debugPrint('\n(countNeighborsPt2): val '+str(inList[y][x])+' at location: ' + str(y) + ' ' + str(x))
	maxY = len(inList)
	maxX = len(inList[0])
	neighborCount = 0
	offsetsList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
	foundNeighborList = ['N','N','N','N','N','N','N','N']
	span = 1
	stillInBox = True
	while stillInBox:
		stillInBox = False
		for offset in range(len(offsetsList)):
			checkX = x+(offsetsList[offset][1]*span)
			checkY = y+(offsetsList[offset][0]*span)
			debugPrint('checking offset at '+str(checkY)+' '+str(checkX))
			if (0 <= checkX < maxX) and (0 <= checkY < maxY) and (foundNeighborList[offset] == 'N'):
				debugPrint(' val at offset'+str(inList[checkY][checkX]))
				if inList[checkY][checkX] == '#':
					debugPrint('had neighbor at '+str(checkY)+' '+str(checkX))
					neighborCount += 1
				if (inList[checkY][checkX] == '#') or (inList[checkY][checkX] == 'L'):
					foundNeighborList[offset] = 'Y'
				stillInBox = True
			else:
				debugPrint(' outside of the area')
		span += 1
	debugPrint('neighborCount '+str(neighborCount))
	return neighborCount
	
def runRulesPt2(inList):
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
			debugPrint('(runRulesPt2): at'+str(y)+str(x)+'val'+str(inList[y][x]))
			if inList[y][x] == '.':
				newRow.append('.')
			elif inList[y][x] == 'L':	# seat is empty
				if countNeighborsPt2(inList,y,x) == 0:
					newRow.append('#')
				else:
					newRow.append('L')
			elif inList[y][x] == '#':	# seat is occupied
				if countNeighborsPt2(inList,y,x) >= 5:
					newRow.append('L')
				else:
					newRow.append(inList[y][x])
		newList.append(newRow)
	return newList
	
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

newFloorPlan = readFileOfStringsToListOfLists('input.txt')
# if DEBUG_PRINT:
	# printFloorplan(inList)
	# print('\nPadded floorplan')
#newFloorPlan = padWithFloor(inList)
#if DEBUG_PRINT:
#printFloorplan(newFloorPlan)
# print()
savedList = []

roundCount = 1
while savedList != newFloorPlan:
	savedList = copy.deepcopy(newFloorPlan)
	newFloorPlan2 = []
	newFloorPlan2 = runRulesPt2(newFloorPlan)
	debugPrint('\nAfter round '+str(roundCount))
	roundCount += 1
	#if DEBUG_PRINT:
	#printFloorplan(newFloorPlan2)
	newFloorPlan = copy.deepcopy(newFloorPlan2)
	# input('hit a key')
	# print()
	#assert False,'yep'

print('\nAfter all rounds')
# if DEBUG_PRINT:
	# printFloorplan(newFloorPlan)
print('Count',countSeats(newFloorPlan))

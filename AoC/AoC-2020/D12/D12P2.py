""" 
AoC D12 P2
13340 is right
"""

def readFileToListOfStrings(fileName):
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def getNewWayPointPosition(direction):
	# translate waypoint offset to be relative to the ship
	#	store the relative offset at the start
	# Rotate the waypoint
	# Translate the waypoint back relative to the original offset at the start
	global shipX
	global shipY
	global waypointAbsoluteX
	global waypointAbsoluteY
	dir = direction[1]
	# print('\n(getNewWayPointPosition): got here')
	waypointRelativeToOriginX = waypointAbsoluteX - shipX
	waypointRelativeToOriginY = waypointAbsoluteY - shipY
	# print('(before)waypoint relative to origin',waypointRelativeToOriginX,waypointRelativeToOriginY)
	if ((direction[0] == 'L') and (dir == 90)) or ((direction[0] == 'R') and (dir == 270)):
		# print('L90 or R270')
		store = waypointRelativeToOriginX
		waypointRelativeToOriginX = -waypointRelativeToOriginY
		waypointRelativeToOriginY = store
	elif ((direction[0] == 'L') and (dir == 270)) or ((direction[0] == 'R') and (dir == 90)):
		# print('L270 or R90')
		store = waypointRelativeToOriginY
		waypointRelativeToOriginY = -waypointRelativeToOriginX
		waypointRelativeToOriginX = store
	elif dir == 180:
		# print('LR180')
		waypointRelativeToOriginX = -waypointRelativeToOriginX
		waypointRelativeToOriginY = -waypointRelativeToOriginY
	else:
		print('parse error')
	# print('(after)waypoint relative to origin',waypointRelativeToOriginX,waypointRelativeToOriginY)
	waypointAbsoluteX = waypointRelativeToOriginX + shipX
	waypointAbsoluteY = waypointRelativeToOriginY + shipY

def doOperation(direction):
	global shipX
	global shipY
	global waypointAbsoluteX
	global waypointAbsoluteY
	# print('\n',direction,end= ' ')
	delta = direction[1]
	if direction[0] == 'N':
		waypointAbsoluteY += delta
	elif direction[0] == 'S':
		waypointAbsoluteY -= delta
	elif direction[0] == 'E':
		waypointAbsoluteX += delta
	elif direction[0] == 'W':
		waypointAbsoluteX -= delta
	elif (direction[0] == 'L') or (direction[0] == 'R'):
		getNewWayPointPosition(direction)
	elif direction[0] == 'F':
		# print('\nbefore move')
		# report()
		deltaX = delta * (shipX - waypointAbsoluteX)
		deltaY = delta * (shipY - waypointAbsoluteY)
		shipX -= deltaX
		shipY -= deltaY
		waypointAbsoluteX -= deltaX
		waypointAbsoluteY -= deltaY
	else:
		assert False,'parse error decode'
	
def report():
	global shipX
	global shipY
	global waypointAbsoluteX
	global waypointAbsoluteY
	print('ship ',shipX,' ',shipY,end=' ')
	print('absolute waypoint ',waypointAbsoluteX,' ',waypointAbsoluteY,end=' ')
	print('distance ',waypointAbsoluteX-shipX,' ',waypointAbsoluteY-shipY)

def setShipLocXyWaypointXY(sX,sY,wX,wY):
	global shipX
	global shipY
	global waypointAbsoluteX
	global waypointAbsoluteY
	shipX = sX
	shipY = sY
	waypointAbsoluteX = wX
	waypointAbsoluteY = wY
	
# setShipLocXyWaypointXY(0,0,1,2)
# print('Before',end = ' ')
# report()
# doOperation(['L',180])
# print('After', end = ' ')
# report()
# print('')
# print('')

# setShipLocXyWaypointXY(0,0,2,1)
# print('Before',end = ' ')
# report()
# doOperation(['L',90])
# print('After', end = ' ')
# report()
# print('')
# print('')

# setShipLocXyWaypointXY(0,0,1,2)
# print('Before',end = ' ')
# report()
# doOperation(['R',90])
# print('After', end = ' ')
# report()
# print('')
# print('')

# assert False,"tested"

shipX = 0
shipY = 0
waypointAbsoluteX = 0
waypointAbsoluteY = 0

inList = readFileToListOfStrings('input.txt')
# print(inList)
directionsList = []
for row in inList:
	listRow = []
	listRow.append(row[0])
	listRow.append(int(row[1:]))
	directionsList.append(listRow)

# print('directionsList',directionsList)
# print('')

setShipLocXyWaypointXY(0,0,10,1)

# report()
for direction in directionsList:
	doOperation(direction)
	# report()

# #print('\n',shipX,shipY)
print(abs(shipX)+abs(shipY))

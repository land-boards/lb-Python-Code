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


def doMove(direction):
	global shipX
	global shipY
	global waypointRelativeToShipX
	global waypointRelativeToShipY
	dir = direction[1]
	print('\n',direction)
	delta = direction[1]
	if direction[0] == 'N':
		waypointRelativeToShipY += delta
	elif direction[0] == 'S':
		waypointRelativeToShipY -= delta
	elif direction[0] == 'E':
		waypointRelativeToShipX += delta
	elif direction[0] == 'W':
		waypointRelativeToShipX -= delta
	elif ((direction[0] == 'L') and (dir == 90)) or ((direction[0] == 'R') and (dir == 270)):
		store = waypointRelativeToShipX
		waypointRelativeToShipX = -waypointRelativeToShipY
		waypointRelativeToShipY = store
	elif ((direction[0] == 'L') and (dir == 270)) or ((direction[0] == 'R') and (dir == 90)):
		store = waypointRelativeToShipX
		waypointRelativeToShipX = waypointRelativeToShipY
		waypointRelativeToShipY = -store
	elif dir == 180:
		waypointRelativeToShipX = -waypointRelativeToShipX
		waypointRelativeToShipY = -waypointRelativeToShipY
	elif direction[0] == 'F':
		shipX += delta * (waypointRelativeToShipX)
		shipY += delta * (waypointRelativeToShipY)
	else:
		assert False,'parse error decode'
	
def report():
	global shipX
	global shipY
	global waypointRelativeToShipX
	global waypointRelativeToShipY
	print('ship ',shipX,' ',shipY,end=' ')
	print('waypoint ',waypointRelativeToShipX,' ',waypointRelativeToShipY,end=' ')
	print('distance ',waypointRelativeToShipX-shipX,' ',waypointRelativeToShipY-shipY,end='')

def setShipLocXyWaypointXY(sX,sY,wX,wY):
	global shipX
	global shipY
	global waypointRelativeToShipX
	global waypointRelativeToShipY
	shipX = sX
	shipY = sY
	waypointRelativeToShipX = wX
	waypointRelativeToShipY = wY
	
setShipLocXyWaypointXY(0,0,1,2)
print('Before',end = ' ')
report()
doMove(['L',180])
print('After', end = ' ')
report()
print('')
print('')

setShipLocXyWaypointXY(4,1,5,3)
print('Before',end = ' ')
report()
doMove(['R',180])
print('After', end = ' ')
report()
print('')
print('')

setShipLocXyWaypointXY(0,0,2,1)
print('Before',end = ' ')
report()
doMove(['L',90])
print('After', end = ' ')
report()
print('')
print('')

setShipLocXyWaypointXY(3,6,5,7)
print('Before',end = ' ')
report()
doMove(['R',270])
print('After', end = ' ')
report()
print('')
print('')

setShipLocXyWaypointXY(0,0,1,2)
print('Before',end = ' ')
report()
doMove(['R',90])
print('After', end = ' ')
report()
print('')
print('')

setShipLocXyWaypointXY(4,5,5,7)
print('Before',end = ' ')
report()
doMove(['L',270])
print('After', end = ' ')
report()
print('')
print('')


#assert False,"tested"

inList = readFileToListOfStrings('input.txt')
print(inList)
directionsList = []
for row in inList:
	listRow = []
	listRow.append(row[0])
	listRow.append(int(row[1:]))
	directionsList.append(listRow)

print('directionsList',directionsList)

setShipLocXyWaypointXY(0,0,10,1)

report()
for direction in directionsList:
	doMove(direction)
	report()

print('\n',shipX,shipY)
print(abs(shipX)+abs(shipY))

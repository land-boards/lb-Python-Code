from __future__ import print_function

def getNewRobotDirection(currentRobotDirection,newTurn):
	debug_getNewRobotDirection = False
	if debug_getNewRobotDirection:
		print("@getNewRobotDirection : currentRobotDirection",currentRobotDirection)
		print("@getNewRobotDirection : newTurn",newTurn)
	if newTurn == '<':
		if currentRobotDirection == '^':
			resultingDirection = '<'
		elif currentRobotDirection == '<':
			resultingDirection = 'v'
		elif currentRobotDirection == '>':
			resultingDirection = '^'
		elif currentRobotDirection == 'v':
			resultingDirection = '>'
		else:
			assert False,"getNewRobotDirection : bad current direction"
	elif newTurn == '>':
		if currentRobotDirection == '^':
			resultingDirection = '>'
		elif currentRobotDirection == '<':
			resultingDirection = '^'
		elif currentRobotDirection == '>':
			resultingDirection = 'v'
		elif currentRobotDirection == 'v':
			resultingDirection = '<'
		else:
			assert False,"getNewRobotDirection : bad current direction"
	else:
		assert False,"getNewRobotDirection: Illegal direction"
	if debug_getNewRobotDirection:
		print("@debug_getNewRobotDirection : resultingDirection",resultingDirection)
	return resultingDirection
	
def getNewRobotLocation(currentLocation,startDirection):
	debug_getNewRobotLocation = False
	if debug_getNewRobotLocation:
		print("@getNewRobotLocation : currentLocation",currentLocation)
		print("@getNewRobotLocation : startDirection",startDirection)
	if startDirection == '^':
		newLocation = [currentLocation[0],currentLocation[1]+1]
	elif startDirection == '<':
		newLocation = [currentLocation[0]-1,currentLocation[1]]
	elif startDirection == '>':
		newLocation = [currentLocation[0]+1,currentLocation[1]]
	elif startDirection == 'v':
		newLocation = [currentLocation[0],currentLocation[1]-1]
	if debug_getNewRobotLocation:
		print("@getNewRobotLocation : newLocation",newLocation)
	return newLocation
	
print("Test Movement")

currentRobotLocation=[0,0]
currentRobotDirection = '^'
print("Location",currentRobotLocation)
print("Direction",currentRobotDirection)

print("\nFirst Move")
turnDirection = '<'
print("Moving",turnDirection)
newDirection = getNewRobotDirection(currentRobotDirection,turnDirection)
newLocation = getNewRobotLocation(currentRobotLocation,newDirection)
currentRobotLocation = newLocation
currentRobotDirection = newDirection
print("Location",currentRobotLocation)
print("Direction",currentRobotDirection)

print("\nSecond Move")
turnDirection = '<'
print("Moving",turnDirection)
newDirection = getNewRobotDirection(currentRobotDirection,turnDirection)
newLocation = getNewRobotLocation(currentRobotLocation,newDirection)
currentRobotLocation = newLocation
currentRobotDirection = newDirection
print("Location",currentRobotLocation)
print("Direction",currentRobotDirection)

print("\n3rd Move")
turnDirection = '<'
print("Moving",turnDirection)
newDirection = getNewRobotDirection(currentRobotDirection,turnDirection)
newLocation = getNewRobotLocation(currentRobotLocation,newDirection)
currentRobotLocation = newLocation
currentRobotDirection = newDirection
print("Location",currentRobotLocation)
print("Direction",currentRobotDirection)

print("\n4th Move")
turnDirection = '<'
print("Moving",turnDirection)
newDirection = getNewRobotDirection(currentRobotDirection,turnDirection)
newLocation = getNewRobotLocation(currentRobotLocation,newDirection)
currentRobotLocation = newLocation
currentRobotDirection = newDirection
print("Location",currentRobotLocation)
print("Direction",currentRobotDirection)

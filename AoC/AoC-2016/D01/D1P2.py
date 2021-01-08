#steps = ['R2','L3']
#steps = ['R2','R2','R2']
#steps = ['R5','L5','R5','R3']
steps = ['R8','R4','R4','R8']
# steps = ['R4','R1','L2','R1','L1','L1','R1','L5','R1','R5','L2','R3','L3','L4','R4','R4','R3','L5','L1','R5','R3','L4','R1','R5','L1','R3','L2','R3','R1','L4','L1','R1','L1','L5','R1','L2','R2','L3','L5','R1','R5','L1','R188','L3','R2','R52','R5','L3','R79','L1','R5','R186','R2','R1','L3','L5','L2','R2','R4','R5','R5','L5','L4','R5','R3','L4','R4','L4','L4','R5','L4','L3','L1','L4','R1','R2','L5','R3','L4','R3','L3','L5','R1','R1','L3','R2','R1','R2','R2','L4','R5','R1','R3','R2','L2','L2','L1','R2','L1','L3','R5','R1','R4','R5','R2','R2','R4','R4','R1','L3','R4','L2','R2','R1','R3','L5','R5','R2','R5','L1','R2','R4','L1','R5','L3','L3','R1','L4','R2','L2','R1','L1','R4','R3','L2','L3','R3','L2','R1','L4','R5','L1','R5','L2','L1','L5','L2','L5','L2','L4','L2','R3']

# 156 is too high

def intersectionPoint(vect,listOfVects):
	intersection = [0,0]
	for traveledPath in listOfVects:
		if linesCross(vect,traveledPath):
			return intersection
	assert False,'(intersectionPoint) : intersection error'

def linesCross(vect,traveledPath):
	print('check line',vect,'against',traveledPath)
	# if 
	return False

def pathCrossesPreviousPaths(vect,listOfVects):
	for traveledPath in listOfVects:
		if linesCross(vect,traveledPath):
			return True
	return False
	
distanceX = 0
distanceY = 0
dirOfTravel='N'
places = []
print("original dirOfTravel",dirOfTravel)
prevLoc = [0,0]
for movement in steps:
	moveDir = movement[0]
	moveDistance = int(movement[1:])
	if moveDir == 'R':
		if dirOfTravel=='N':
			distanceX = distanceX + moveDistance
			dirOfTravel='E'
		elif dirOfTravel=='E':
			distanceY = distanceY - moveDistance
			dirOfTravel='S'
		elif dirOfTravel=='S':
			distanceX = distanceX - moveDistance
			dirOfTravel='W'
		elif dirOfTravel=='W':
			distanceY = distanceY + moveDistance
			dirOfTravel='N'
	elif movement[0] == 'L':
		if dirOfTravel=='N':
			distanceX = distanceX - moveDistance
			dirOfTravel='W'
		elif dirOfTravel=='W':
			distanceY = distanceY - moveDistance
			dirOfTravel='S'
		elif dirOfTravel=='S':
			distanceX = distanceX + moveDistance
			dirOfTravel='E'
		elif dirOfTravel=='E':
			distanceY = distanceY + moveDistance
			dirOfTravel='N'
	# print("Movement",movement,"dirOfTravel",dirOfTravel,"X,Y :",distanceX,distanceY)
	newXYLoc = [distanceX,distanceY]
	if not pathCrossesPreviousPaths([prevLoc,newXYLoc],places):
		places.append([prevLoc,newXYLoc])
		# print('added',prevLoc,newXYLoc)
	else:
		print('newXYLoc',newXYLoc)
		print('result',abs(newXYLoc[0])+abs(newXYLoc[1]))
		break
	prevLoc = newXYLoc
print('paths',places)

#steps = ['R2','L3']
#steps = ['R2','R2','R2']
#steps = ['R5','L5','R5','R3']
steps = ['R4','R1','L2','R1','L1','L1','R1','L5','R1','R5','L2','R3','L3','L4','R4','R4','R3','L5','L1','R5','R3','L4','R1','R5','L1','R3','L2','R3','R1','L4','L1','R1','L1','L5','R1','L2','R2','L3','L5','R1','R5','L1','R188','L3','R2','R52','R5','L3','R79','L1','R5','R186','R2','R1','L3','L5','L2','R2','R4','R5','R5','L5','L4','R5','R3','L4','R4','L4','L4','R5','L4','L3','L1','L4','R1','R2','L5','R3','L4','R3','L3','L5','R1','R1','L3','R2','R1','R2','R2','L4','R5','R1','R3','R2','L2','L2','L1','R2','L1','L3','R5','R1','R4','R5','R2','R2','R4','R4','R1','L3','R4','L2','R2','R1','R3','L5','R5','R2','R5','L1','R2','R4','L1','R5','L3','L3','R1','L4','R2','L2','R1','L1','R4','R3','L2','L3','R3','L2','R1','L4','R5','L1','R5','L2','L1','L5','L2','L5','L2','L4','L2','R3']

# 277 is too hogh
# 535 is too high
#Your puzzle answer was 161.

distanceX = 0
distanceY = 0
dirOfTravel='N'
places = []
print("original dirOfTravel",dirOfTravel)
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
	print("Movement",movement,"dirOfTravel",dirOfTravel,"X :",distanceX,"Y :",distanceY)
	xyLoc = [distanceX,distanceY]
	places.append(xyLoc)
print('places[end]',places[-1])
print('result',abs(places[-1][0])+abs(places[-1][1]))

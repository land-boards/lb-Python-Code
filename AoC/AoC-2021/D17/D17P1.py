# D17P1.py
# 2021 Advent of Code
# Day 17
# Part 1
# 5671 is too low
# 5761 is too low

import time

# At start
startTime = time.time()

def moveProbe(currentPos,velocity):
	xPos = currentPos[0] + velocity[0]
	yPos = currentPos[1] + velocity[1]
	xVelocity = velocity[0]
	yVelocity = velocity[1]
	if xVelocity > 0:
		xVelocity -= 1
	elif xVelocity < 1:
		xVelocity += 1
	yVelocity -= 1
	newPosVelocity = (xPos,yPos),(xVelocity,yVelocity)
	# print("(x,y) =",(xPos,yPos))
	return (xPos,yPos),(xVelocity,yVelocity)

def getArea(inStr):
	global area
	# inStr = 'target area: x=235..259, y=-118..-62'
	inStr = inStr.replace('target area: x=','')
	inStr = inStr.replace('..',',')
	inStr = inStr.replace(' y=','')
	# print(inStr)
	area1=inStr.split(',')
	area2 = []
	for point in area1:
		area2.append(int(point))
	area = []
	area.append(area2[0])
	area.append(area2[2])
	area.append(area2[1])
	area.append(area2[3])

def checkPositionInArea(currentPos):
	global area
	# print("\ncheckPositionInArea: currentPos",currentPos)
	# print("checkPositionInArea: area",area)
	if currentPos[0] > area[2]:
		return 'PastAreaInX'
	if currentPos[1] < area[1]:
		return 'PastAreaInY'
	if currentPos[0] < area[0]:
		return 'BeforeAreaInX'
	if currentPos[1] > area[3]:
		return 'BeforeAreaInY'
	if area[0] <= currentPos[0] <= area[2]:
		if area[1] <= currentPos[1] <= area[3]:
			return 'InArea'
	quit()

def testVelocity(probePosition,velocity):
	stop = False
	pathTaken = []
	initVelocity = velocity
	# print("initVelocity",initVelocity)
	while not stop:
		pathTaken.append(probePosition)
		# print("testVelocity: velocity",velocity)
		probePosition,velocity = moveProbe(probePosition,velocity)
		result = checkPositionInArea(probePosition)
		# print("testVelocity: ",result)
		if result == 'PastAreaInX':
			stop = True
		elif result == 'PastAreaInY':
			stop = True
		elif result == 'Unknown':
			print("testVelocity: Early stop with velocity",velocity)
			quit()
		elif result == 'InArea':
			stop = True
			# print("testVelocity: In Area: init velocity =",initVelocity)
			pathsTaken.append(pathTaken)
			return True
	return False

inStr = 'target area: x=20..30, y=-10..-5'
# inStr = 'target area: x=235..259, y=-118..-62'
getArea(inStr)
print("area goes from (",end='')
print(area[0],end=', ')
print(area[1],end=') to (')
print(area[2],end=', ')
print(area[3],end='')
print(")")
probePosition = (0,0)
hitTargetInitVelocities = []
pathsTaken = []
maxX = area[2] + 1
minY = area[1] - 1
print("(maxX, maxY) = (",end='')
print(maxX,end='')
print(",",minY,end='')
print(")")
for velY in range(-abs(minY),abs(minY)):
	for velX in range(-abs(maxX),abs(maxX)):
		initVel = (velX,velY)
		if testVelocity(probePosition,initVel):
			hitTargetInitVelocities.append(initVel)
print("hitTargetInitVelocities",hitTargetInitVelocities)
print("pathsTaken")
for path in pathsTaken:
	print(' ',path)
maxVal = 0
allUniqInitVels = []
for path in hitTargetInitVelocities:
	if path not in allUniqInitVels:
		allUniqInitVels.append(path)
print(len(allUniqInitVels))
print("allUniqInitVels",allUniqInitVels)
endTime = time.time()
print('Time elapsed',endTime-startTime)

'''
D15P1.py
12876527204400 is too high

'''
import time

# At start
startTime = time.time()

def readInFile(fileName):
	inList=[]
	with open(fileName, 'r') as filehandle:  
		lineSegmentsList = []
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)
	sensorBeaconList = []
	for line in inList:
		line = line.replace('Sensor at x=',',')
		line = line.replace(': closest beacon is at',',')
		line = line.replace('x=',',')
		line = line.replace('y=',',')
		newLine = line.split(', ')
		# print('newLine',newLine)
		intLine = [int(newLine[0][1:]),int(newLine[1][1:]),int(newLine[2][1:]),int(newLine[3][1:])]
		sensorBeaconList.append(intLine)
	return sensorBeaconList

def Y_ValIsInSensorArea(sensorBeacon,manhattanDistance,intersectingY):
	if sensorBeacon[1]-manhattanDistance <= intersectingY <= sensorBeacon[1]+manhattanDistance:
		return True
	return False

def findIntersections(sensorBeacon,manhattanDistance,intersectingY):
		# print('findIntersections: sensorBeacon,manhattanDistance,intersectingY',sensorBeacon,manhattanDistance,intersectingY)
		deltaY = abs(sensorBeacon[1]-intersectingY)
		delyaX = manhattanDistance - deltaY
		xOff1 = sensorBeacon[0] + delyaX
		xOff2 = sensorBeacon[0] - delyaX
		if xOff1 < xOff2:
			return xOff1,xOff2
		return xOff2,xOff1


def ifOverlap(seg1,seg2):
	retVal = False
	# print('ifOverlap: seg1,seg2',seg1,seg2)
	if seg2[0] <= seg1[0] <= seg2[1]:
		# print('ifOverlap: overlaps')
		retVal = True
	if seg2[0] <= seg1[1] <= seg2[1]:
		# print('ifOverlap: seg1,seg2',seg1,seg2,'ifOverlap: overlaps')
		retVal = True
	if seg1[0] <= seg2[0] <= seg1[1]:
		# print('ifOverlap: overlaps')
		retVal = True
	if seg1[0] <= seg2[1] <= seg1[1]:
		# print('ifOverlap: seg1,seg2',seg1,seg2,'ifOverlap: overlaps')
		retVal = True
	# if retVal:
		# print('ifOverlap: overlaps')
	# else:
		# print('ifOverlap: no overlap')
	return retVal

def findOverlapRange(seg1,seg2):
	# print('findOverlapRange: seg1,seg2',seg1,seg2)
	if seg2[0] <= seg1[0] <= seg2[1]:
		startX = seg2[0]
	else:
		startX = seg1[0]
	if seg2[0] <= seg1[1] <= seg2[1]:
		endX = seg2[1]
	else:
		endX = seg1[1]
	# print('findOverlapRange: startX,endX',startX,endX)
	return startX,endX
	
def isContainedInList(segment, newList):
	# print('isContainedInList: newList,segment',newList,segment)
	if newList == []:
		# print('empty list')
		return False, 0, 0, 0
	for listOff in range(len(newList)):
		if ifOverlap(segment,newList[listOff]):
			# print('segment Overlaps, segment, offset', segment, listOff)
			newStartX, newEndX = findOverlapRange(segment,newList[listOff])
			return True, listOff, newStartX, newEndX
	return False, 0, 0, 0

def reduceSegmentsList(lineSegments):
	# feed in list of overlapping segments
	# send out reduced list
	
	newList = []
	for segment in lineSegments:
		# print('reduceSegmentsList: (before) newList',newList)
		isInLost, offset, newStartX, newEndX = isContainedInList(segment, newList)
		if isInLost:
			# print('reduceSegmentsList: is in list, offset, newStartX, newEndX',offset, newStartX, newEndX)
			newList[offset] = newStartX, newEndX
		else:
			# print('reduceSegmentsList: not in list, offset, newStartX, newEndX',offset, newStartX, newEndX)
			newList.append(segment)
		# print('reduceSegmentsList: (after) newList',newList)
		# print('')
	return newList

# fileName = 'input2.txt'
fileName = 'input.txt'
# fileName = 'input1.txt'
# print(inList)
# intersectingY = 2000000

sensorBeaconList = readInFile(fileName)
print('main: sensorBeaconList',sensorBeaconList)
for intersectingY in range(4000000):
	lineSegments = []
	for sensorBeacon in sensorBeaconList:
		manhattanDistance = (abs(sensorBeacon[0]-sensorBeacon[2])) + (abs(sensorBeacon[1]-sensorBeacon[3]))
		# print('sensorBeacon',sensorBeacon,'manhattanDistance',manhattanDistance)
		if Y_ValIsInSensorArea(sensorBeacon,manhattanDistance,intersectingY):
			# print('Y Line intersects area')
			startEnd = findIntersections(sensorBeacon,manhattanDistance,intersectingY)
			# print('main: start, end',startEnd)
			lineSegments.append(startEnd)

	# print('lineSegments',lineSegments)
	reducedSegs = list(lineSegments)
	keepReducing = True
	segmentCount = len(reducedSegs)
	while keepReducing:
		reducedSegs = reduceSegmentsList(reducedSegs)
		newSeqCt = len(reducedSegs)
		if newSeqCt == segmentCount:
			keepReducing = False
		segmentCount = newSeqCt
	# print('reducedSegs',reducedSegs)
	if len(reducedSegs) > 1:
		print('reducedSegs',reducedSegs)
		print('y',intersectingY)
		endTime = time.time()
		print('time',endTime-startTime)
		assert False,""
	segListLen = 0
	for seg in reducedSegs:
		segListLen += (seg[1]-seg[0])
	if intersectingY % 10000 == 0:
		print('intersectingY',intersectingY)

	# print('intersectingY, number of points',intersectingY,segListLen)

# x=3204400
# y=3219131
# At end
endTime = time.time()
print('time',endTime-startTime)

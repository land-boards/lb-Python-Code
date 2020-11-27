def readFileToList():
	with open('input.txt', 'r') as filehandle:  
		inLine = []
		for line in filehandle:
			inLineList = []
			inLineRow = line.split(' ')
			inLineList.append(inLineRow[0])			# 0 - Reindeer name
			inLineList.append(int(inLineRow[3]))	# 1 - flying speed
			inLineList.append(int(inLineRow[6]))	# 2 - flying time
			inLineList.append(int(inLineRow[13]))	# 3 - rest time
			inLineList.append(int(inLineRow[6]))	# 4 - time left flying
			inLineList.append(0)					# 5 - time left resting
			inLineList.append(0)					# 6 - distance traveled
			inLineList.append(0)					# 7 - points			
			inLine.append(inLineList)
		return inLine

def getMaxDist(reindeerArray):
	maxDist = 0
	for reindeer in reindeerArray:
		if reindeer[6] > maxDist:
			maxDist = reindeer[6]
	return maxDist

def getMaxPoints(reindeerArray):
	maxPoints = 0
	for reindeer in reindeerArray:
		if reindeer[7] > maxPoints:
			maxPoints = reindeer[7]
	return maxPoints

reindeerArray = readFileToList()
print(reindeerArray)
loopCount = 2503
while (loopCount > 0):
	for reindeer in reindeerArray:
		if reindeer[4] > 0:
			reindeer[6] += reindeer[1]
			reindeer[4] -= 1
			if reindeer[4] == 0:
				reindeer[5] = reindeer[3]
		else:
			reindeer[5] -= 1
			if reindeer[5] == 0:
				reindeer[4] = reindeer[2]
	loopCount -= 1
	maxDistance = getMaxDist(reindeerArray)
	for reindeer in reindeerArray:
		if reindeer[6] == maxDistance:
			reindeer[7] += 1
	
print(reindeerArray)
maxDistance = getMaxDist(reindeerArray)
print("maxDistance",maxDistance)
maxPoints = getMaxPoints(reindeerArray)
print("maxPoints",maxPoints)

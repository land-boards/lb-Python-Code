import time

# At start
startTime = time.time()

# The program

DEBUG_PRINT = True
#DEBUG_PRINT = False

def debugPrint(thingToPrint):
	global DEBUG_PRINT		# need to put in each function
	if DEBUG_PRINT:
		print(thingToPrint)

def getCups():
	global q
	
#inStr = '284573961'	# My input
inStr = '389125467'		# Example
moves = 10				# Number of moves

# Initalize the queue
q = []
for element in inStr:
	q.append(int(element))
numberOfCups = len(q)
debugPrint('Number of cups ' + str(numberOfCups))
debugPrint('Initial cups list ' + str(q))

# Setup
moveNumber = 1
currentCupPtr = 0

# The loop
while moveNumber <= moves:
	debugPrint('\n-- Move ' + str(moveNumber) + ' --')
	debugPrint('cups (before move) ' + str(q))
	cupsRemovedList = []
	for i in range(3):
		getCupOffset = (currentCupPtr + 1 + i) % numberOfCups
		debugPrint('getCupOffset ' + str(getCupOffset))
		cupsRemovedList.append(q[getCupOffset])
	debugPrint('picked up cups ' + str(cupsRemovedList))
	lookingForValue = q[currentCupPtr] - 1
	debugPrint('Initial destination cup ' + str(lookingForValue))
	for cupToRemove in cupsRemovedList:
		q.remove(cupToRemove)
	debugPrint('q after removal ' + str(q))
	if lookingForValue in cupsRemovedList:
		while lookingForValue in cupsRemovedList:
			debugPrint('new looking for value ' + str(lookingForValue))
			lookingForValue -= 1
			if lookingForValue == 0:
				lookingForValue = numberOfCups
		debugPrint('found val ' + str(lookingForValue))
		debugPrint('destination (looking for value) after adjustment ' + str(lookingForValue))
		for offset in range(len(q)):
			if q[offset] == lookingForValue:
				break
		offset += 1
		debugPrint('insert at offset ' + str(offset))
	else:
		debugPrint('destination (looking for value) after adjustment ' + str(lookingForValue))
		if lookingForValue == 0:
			lookingForValue = numberOfCups
		for offset in range(len(q)):
			if q[offset] == lookingForValue:
				break
		offset += 1
		debugPrint('insert at offset ' + str(offset))
	debugPrint('inserting cups ' + str(cupsRemovedList))
	for val in range(3):
		q.insert(offset,cupsRemovedList[2-val])	# insert backwards
	if offset < currentCupPtr:
		# rotate left 3 positions
		q = q[3:] + q[:3]
	currentCupPtr += 1
	if currentCupPtr >= numberOfCups:
		currentCupPtr = 0
	moveNumber += 1

# At end
endTime = time.time()
print('time',endTime-startTime)

import time

# 94365872 too high

# At start
startTime = time.time()

# The program

# DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	global DEBUG_PRINT		# need to put in each function
	if DEBUG_PRINT:
		print(thingToPrint)

def getCups():
	global q
	
inStr = '284573961'	# My input
# inStr = '389125467'		# Example
moves = 100				# Number of moves

# Initalize the queue
q = []
for element in inStr:
	q.append(int(element))
numberOfCups = len(q)
debugPrint('Number of cups ' + str(numberOfCups))
debugPrint('Number of moves ' + str(moves) + '\n')
# debugPrint('Initial cups list ' + str(q))

# Setup
moveNumber = 1
currentCupPtr = 0

# The loop
while moveNumber <= moves:
	debugPrint('-- Move ' + str(moveNumber) + ' --')
	debugPrint('cups: ' + str(q))
	cupsRemovedList = []
	nextCupNumber = q[(currentCupPtr + 4) % numberOfCups]
	debugPrint('nextCupNumber ' + str(nextCupNumber))
	for i in range(3):
		getCupOffset = (currentCupPtr + 1 + i) % numberOfCups
		debugPrint('getCupOffset ' + str(getCupOffset))
		cupsRemovedList.append(q[getCupOffset])
	debugPrint('pick up: ' + str(cupsRemovedList))
	lookingForValue = q[currentCupPtr] - 1
	if lookingForValue == 0:
		lookingForValue = numberOfCups
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
		debugPrint('destination: ' + str(lookingForValue))
		for offset in range(len(q)):
			if q[offset] == lookingForValue:
				break
		offset += 1
		debugPrint('insert at offset ' + str(offset))
	else:
		# assert False,'wtf'
		debugPrint('destination:  ' + str(lookingForValue))
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
	currentCupPtr = (currentCupPtr + 1) % numberOfCups
	# rotate left until lines up
	while q[currentCupPtr] != nextCupNumber:
		q = q[1:] + q[:1]
	moveNumber += 1
	debugPrint('')

print('q before final rotation',q)
while q[0] != 1:
	q = q[1:] + q[:1]
print('q (after final rotation',q)
for num in q[1:]:
	print(num,end='')
print()
# At end
endTime = time.time()
print('time',endTime-startTime)

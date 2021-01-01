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

q = []
for element in inStr:
	q.append(int(element))
moves = 7
currentCupPtr = 0
while moves > 0:
	debugPrint('\nMove ' + str(11-moves))
	debugPrint('cups ' + str(q))
	cupList = []
	for i in range(3):
		getCupOffset = currentCupPtr + 1 + i
		if getCupOffset > 8:
			getCupOffset = 0
		cupList.append(q[getCupOffset])
	debugPrint('pick up : ' + str(cupList))
	valueAtPoint = q[currentCupPtr]
	debugPrint('value at the point ' + str(currentCupPtr) + ' is ' + str(valueAtPoint))
	lookingForValue = valueAtPoint - 1
	debugPrint('Starting looking for value ' + str(lookingForValue))
	for cupToRemove in cupList:
		q.remove(cupToRemove)
	debugPrint('q after removal ' + str(q))
	if lookingForValue in cupList:
		while lookingForValue in cupList:
			debugPrint('looking for this ' + str(lookingForValue))
			lookingForValue -= 1
			if lookingForValue == 0:
				lookingForValue = 9
		debugPrint('found val ' + str(lookingForValue))
		offset = lookingForValue
		debugPrint('destination (looking for value) after adjustment ' + str(lookingForValue))
		for offset in range(len(q)):
			if q[offset] == lookingForValue:
				break
		offset += 1
		debugPrint('insert at offset ' + str(offset))
	else:
		offset = lookingForValue
		debugPrint('destination (looking for value) after adjustment ' + str(offset))
		for offset in range(len(q)):
			if q[offset] == lookingForValue:
				break
		offset += 1
		debugPrint('insert at offset ' + str(offset))
	for val in range(3):
		q.insert(offset,cupList[2-val])	# insert backwards
	currentCupPtr += 1
	if currentCupPtr > 9:
		currentCupPtr = 0
	moves -= 1

# At end
endTime = time.time()
print('time',endTime-startTime)

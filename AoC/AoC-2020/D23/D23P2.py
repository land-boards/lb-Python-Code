import time

# At start
startTime = time.time()

# The program

# DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	global DEBUG_PRINT		# need to put in each function
	if DEBUG_PRINT:
		print(thingToPrint)
	
def fillInDictFromList():
	# Initalize the input list
	global inDict
	global inStr
	for element in range(len(inStr)-1):
		inDict[int(inStr[element])] = int(inStr[element+1])
	inDict[int(inStr[-1])] = int(inStr[0])
	return int(inStr[0]), int(inStr[-1])

def printTenFromOne(space=False,ct=9):
	global inDict
	global DEBUG_PRINT
	val = 1
	if DEBUG_PRINT:
		print(val,end = ' ')
	for _ in range(ct):
		val = inDict[val]
		if space:
			print(val,end = ' ')
		else:
			print(val,end = ' ')
	print()

def doMove(currentVal):
	global maxVal
	pickupList = []
	pickupList.append(inDict[currentVal])
	pickupList.append(inDict[pickupList[-1]])
	pickupList.append(inDict[pickupList[-1]])
	# debugPrint('pick up: ' + str(pickupList))
	nextVal = inDict[pickupList[-1]]
	afterLoc = inDict[inDict[pickupList[-1]]]
	insertLoc = currentVal - 1
	if insertLoc == 0:
		insertLoc = maxVal
	# debugPrint('insertLoc (before) = ' + str(insertLoc))
	while insertLoc in pickupList:
		insertLoc -= 1
		if insertLoc == 0:
			insertLoc = maxVal
	# debugPrint('destination: ' + str(insertLoc))
	endLoc = inDict[insertLoc]
	# debugPrint('  currentVal = ' + str(currentVal))
	# debugPrint('  next val   = ' + str(nextVal))
	# debugPrint('  afterLoc   = ' + str(afterLoc))
	inDict[insertLoc] = pickupList[0]
	inDict[pickupList[2]] = endLoc
	inDict[currentVal] = nextVal
	return nextVal
	
inStr = '284573961'		# My input
# inStr = '389125467'	# Example
moves = 10_000_000		# Number of moves
maxVal = 1_000_000

inDict = {}
currentVal,lastVal = fillInDictFromList()
print('first val',currentVal,'last val',lastVal)
# printTenFromOne(True,maxVal)
for num in range(10,1_000_001):
	inDict[num] = num + 1
inDict[1_000_000] = currentVal
inDict[lastVal] = 10
# printTenFromOne(True,10)

endTime = time.time()
print('after creating dict time',endTime-startTime)
	
# debugPrint('currentVal ' + str(currentVal))
for move in range(moves):
	# if move % 100_000 == 0:
		# print(move)
	# debugPrint('\n--- move '+ str(move+1) + ' ---')
	# if DEBUG_PRINT:
		# printTenFromOne()
	currentVal = doMove(currentVal)
printTenFromOne()

endTime = time.time()
print('time',endTime-startTime)
# input('enter to exit')

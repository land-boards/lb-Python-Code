""" 

2020 AoC Day 13 Part 1
1000109 too high

"""
import math

DEBUG_PRINT = False
#DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint,end='')

def readFileToListOfStrings(fileName):
	"""
	readFileToListOfStrings(fileName)
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

dVec = []
def isDivisible(timeSlot,testNum):
	if math.remainder(timeSlot,testNum) == 0:
		debugPrint('D')
		dVec.append('D')
		return True
	else:
		debugPrint('.')
		dVec.append('.')
		return False

inList = readFileToListOfStrings('input.txt')

sched = inList[1].split(',')
print(sched)
reduxSched2 = []
for bus in sched:
	if bus != 'x':
		reduxSched2.append(int(bus))
maxNum = max(reduxSched2)
print(reduxSched2)
print('maxNum',maxNum)

reduxSched = []
for bus in sched:
	if bus != 'x':
		reduxSched.append(int(bus))
	else:
		reduxSched.append(1)
print('reduxSched',reduxSched)
numberBuses = len(reduxSched)
print('numberBuses',numberBuses)

# assert False,'stats'

stepSize = maxNum
slotNumMaxNum = 0
slotMaxOffset = 0
for busSlot in range(len(reduxSched)):
	if reduxSched[busSlot] == maxNum:
		slotMaxOffset = busSlot
print('slotMaxOffset',slotMaxOffset)

noMatchAtTime = True
busNumOffset = 0

allMatch = False
timeStart = maxNum-slotMaxOffset
timeStart = 4211100242		# from 1st offset
# step up by the max slot value
#timeStep = maxNum
#timeStep = 5367
timeStep = 5679312743 		# from repeat
timeCurrent = timeStart
dVec = []

dVecCnt = 0
matchVal = 0
while not allMatch:
	debugPrint(str(timeCurrent) + ' ')
	allMatch = True
	dVec = []
	for slot in range(len(reduxSched)):
		if reduxSched[slot] != 1:
			if not isDivisible(timeCurrent+slot,reduxSched[slot]):
				allMatch = False
	#print(dVec)
	testVal = 'DDDDDDDDD'
	marchDs = True
	for dtestOff in range(len(testVal)):
		if dVec[dtestOff] != 'D':
			marchDs = False
	if marchDs:
		#print(testVal,timeCurrent)
		#assert False,'first match'
		print(dVec)
		if dVecCnt == 0:
			matchVal = -timeCurrent
			print('First offset',timeCurrent)
		else:
			matchVal += timeCurrent
			print('delta T',matchVal)
		print('DD',timeCurrent)
		dVecCnt += 1
		if dVecCnt == 2:
			assert False,"Matched D's"
	#leftOver = sumRemainders()
	#print(leftOver)
	debugPrint('\n')
	if allMatch:
		print('Match at time',timeCurrent)
		break
	timeCurrent += timeStep
	#timeCurrent += 1
	# if timeCurrent >= 1000000:
		# assert False,'ended due to time'

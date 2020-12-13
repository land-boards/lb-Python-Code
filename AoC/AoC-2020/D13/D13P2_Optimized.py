""" 

2020 AoC Day 13 Part 2

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

def isDivisible(timeSlot,testNum):
	if math.remainder(timeSlot,testNum) == 0:
		dVec.append('D')
		return True
	else:
		dVec.append('.')
		return False

inList = readFileToListOfStrings('input.txt')

sched = inList[1].split(',')
digitCount = 0
reduxSched = []
for bus in sched:
	if bus != 'x':
		reduxSched.append(int(bus))
		digitCount += 1
	else:
		reduxSched.append(1)
numberBuses = len(reduxSched)

dVec = []
def findStartStopFactors(timeStart,timeStep,numDigits):
	global reduxSched
	global dVec
	timeCurrent = timeStart
	dVecCnt = 0
	matchVal = 0
	allMatch = False
	firstOffset = 0
	while not allMatch:
		debugPrint(str(timeCurrent) + ' ')
		allMatch = True
		dVec = []
		for slot in range(len(reduxSched)):
			if reduxSched[slot] != 1:
				if not isDivisible(timeCurrent+slot,reduxSched[slot]):
					allMatch = False
		testVal = ''
		for x in range(numDigits):
			testVal += 'D'
		marchDs = True
		for dtestOff in range(len(testVal)):
			if dVec[dtestOff] != 'D':
				marchDs = False
		if marchDs:
			if dVecCnt == 0:
				firstOffset = timeCurrent
				print('First offset',firstOffset)
			else:
				matchVal = timeCurrent - firstOffset
				print('delta T',matchVal)
			dVecCnt += 1
			if dVecCnt == 2:
				return [firstOffset,matchVal]
		timeCurrent += timeStep

timeStart = 1		# from 1st offset
timeStep = 1 		# from repeat
for loopLen in range(digitCount):
	print('look for T count',loopLen)
	res = findStartStopFactors(timeStart,timeStep,loopLen)
	timeStart = res[0]		# from 1st offset
	timeStep = res[1]		# from repeat

# Pt2-AoCDay7.py
# 2018 Advent of Code
# Day 7
# Part 2
# https://adventofcode.com/2018/day/7

import time
import re

"""

--- Part Two ---
As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workerCount should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workerCount) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .        
   1        C          .        
   2        C          .        
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE
Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workerCount can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workerCount to complete these steps.

With 5 workerCount and the 60+ second step durations described above, how long will it take to complete all of the steps?

"""

def readTextFileAndSortToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
	:returns: the list sorted list
	"""
	textFile = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textFile.append(line.strip())
		textFile.sort()
	return textFile

def parseInFile(inFileList):
	"""parseInFile - 
	"""
	inLists = []
	for record in inFileList:
		inListListed = record.split()
		inLine = []
		inLine.append(inListListed[1])
		inLine.append(inListListed[7])
		inLists.append(inLine)
	return inLists

def getNextLetter(sL):
	global originalListCopy
	nextLettersList = []
	for pair in originalListCopy:
		if pair[0] == sL:
			nextLetter = pair[1]
			nextLettersList.append(pair[1])
	nextLettersList.sort()
	nextLetter1 = nextLettersList[0]
	return nextLetter1

def addLetterToResultList(firstLetterList,secondLetterList):
	sll = []
	for letter in firstLetterList:
		if letter not in secondLetterList:
			sll.append(letter)
	sll.sort()
	return sll

def fillFirstLetterList():
	global originalListCopy
	firstLetterList = []
	for pair in originalListCopy:
		if pair[0] not in firstLetterList:
			firstLetterList.append(pair[0])
	firstLetterList.sort()
	return firstLetterList
	
def fillSecondLetterList():
	global originalListCopy
	secondLetterList = []
	for pair in originalListCopy:
		if pair[1] not in secondLetterList:
			secondLetterList.append(pair[1])
	secondLetterList.sort()
	return secondLetterList

def getRecordCount(pushpushPair,offset):
	recordCount = 0
	firstCharInRecord = pushPair[offset][0]
	while pushPair[offset+recordCount] == firstCharInRecord:
		recordCount += 1
	return recordCount

def availableLetterCount():
	global originalListCopy
	pushPair2 = []
	firstLetterList = fillFirstLetterList(originalListCopy)
	secondLetterList = fillSecondLetterList(originalListCopy)
	startingLetterList = addLetterToResultList(firstLetterList,secondLetterList)
	startingLetter = startingLetterList[0]
	nextLetter1 = getNextLetter(startingLetter,originalListCopy)
	pushPair2.append(startingLetter)
	return len(pushPair2)

def getAvailableLettersList():
	global originalListCopy
	pushPair2 = []
	firstLetterList = fillFirstLetterList()
	secondLetterList = fillSecondLetterList()
	startingLetterList = addLetterToResultList(firstLetterList,secondLetterList)
	startingLetter = startingLetterList[0]
	nextLetter = getNextLetter(startingLetter)
	pushPair2.append(startingLetter)
	return startingLetterList
	
def removePair(sL,nL):
	"""remove pair with the first letter
	"""
	global originalListCopy
	newList = []
	for line in originalListCopy:
		if sL == line[0] and nL == line[1]:
			originalListCopy.remove([line[0],line[1]])
		
def removeAllMatchingPairs(sL):
	"""remove pairs with the first letter
	"""
	global originalListCopy
	test = True
	while test:
		test = False
		for line in originalListCopy:
			if sL == line[0]:
				originalListCopy.remove([line[0],line[1]])
				test = True
	return

def initWorkerSchedule(numberOfWorkers):
	"""initialize the worker schedule
	"""
	global workerSchedule
	for i in range(workerCount):
		workerSchedule.append(['',0])
	return True

def freedWorker():
	"""predict next worker to be freedWorker
	"""
	global workerSchedule
	for theRecord in workerSchedule:
		if theRecord[1] == 1 and theRecord[0] != '':
			print 'found task that will complete next',theRecord[0]
			return theRecord[0]
	else:
		return ''

def findWorkerToReschedule():
	global workerSchedule
	for theRecord in workerSchedule:
		if theRecord[1] == 0 and theRecord[0] != '':
			return theRecord[0]
		else:
			return ''
	
def isWorkerAvailable():
	"""isWorkerAvailable
	"""
	global workerSchedule
	for theRecord in workerSchedule:
		if theRecord[0] == '':
			return True
	return False

def scheduleAvailableWorkerForTask(taskLetter):
	"""checks workerCount to see if any are available
	If worker is available, then schedule worker for the task
	"""
	global workerSchedule
	recordOffset = 0
	while recordOffset < len(workerSchedule):
		#print 'recordOffset',recordOffset
		if workerSchedule[recordOffset][0] == '':
			workerSchedule[recordOffset][0] = taskLetter
			val = ord(taskLetter)-ord('A')+2
			workerSchedule[recordOffset][1] = val
			return
		recordOffset += 1

def incrScheduleTimes():
	global workerSchedule
	newWS = []
	for theRecord in workerSchedule:
		wsLine = []
		taskLetter = theRecord[0]
		taskTime = theRecord[1]
		taskTime -= 1
		if taskTime > 0 and taskLetter != '':
			wsLine.append(taskLetter)
			wsLine.append(taskTime)
			newWS.append(wsLine)
		else:
			wsLine.append('')
			wsLine.append(0)
			newWS.append(wsLine)
	workerSchedule = newWS

def getListActiveWorkers():
	global workerSchedule
	activeWorkers = []
	for theRecord in workerSchedule:
		if theRecord[0] != '':
			activeWorkers.append(theRecord[0])
	return activeWorkers

def getLetterToPush(availableLetters,activeWorkers):
	if availableLetters == activeWorkers:
#		print 'getLetterToPush blocked',availableLetters,activeWorkers
		return ''
	for testLetter in availableLetters:
		if testLetter not in activeWorkers:
#			print 'getLetterToPush: testLetter',testLetter
			return testLetter
	return ''

def removeExpiredWorkers():
	activeWorkerList = getListActiveWorkers()
	for busyWorker in busyWorkerList:
		if busyWorker not in activeWorkerList:
			busyWorkerList.remove(busyWorker)
			removeAllMatchingPairs(busyWorker)
	return

###########################################
## Code
###########################################

print 'Reading in file',time.strftime('%X %x %Z')
inFileList = readTextFileAndSortToList('input2.txt')
parsedInList = parseInFile(inFileList)
originalListCopy = parsedInList

pushPair = []
choseString = ''

while len(originalListCopy) > 0:
	availableLetters = getAvailableLettersList()
	startingLetter = availableLetters[0]
	nextLetter = getNextLetter(startingLetter)
	pushPair.append([startingLetter,nextLetter])
	removePair(startingLetter,nextLetter)
lastChar = ''
for pair in pushPair:
	if pair[0] not in choseString:
		choseString += pair[0]
	lastChar = pair[1]
choseString += lastChar
print 'Part 1 string',choseString
print 

workerCount = 2
timeStep = 1

timeIncrement = 1
timeCounter = 0

inFileList = readTextFileAndSortToList('input2.txt')
parsedInList = parseInFile(inFileList)
originalListCopy = parsedInList

# get a copy of the original input file
originalListCopy = parsedInList
#print 'main: originalListCopy2',originalListCopy

workerSchedule = []
initWorkerSchedule(workerCount)

busyWorkerList = []

while timeCounter < 25:
	print 't =',timeCounter
	print 'Worker sched',workerSchedule
	loopMax = 10
	loopTest = True
	while loopTest:
		if not isWorkerAvailable():
			break
		availableLetters = getAvailableLettersList()
		availableLetters.sort()
		activeWorkers = getListActiveWorkers()
		activeWorkers.sort()
		singleLetter = getLetterToPush(availableLetters,activeWorkers)
		if singleLetter != '':
			print '***scheduling letter',singleLetter
			scheduleAvailableWorkerForTask(singleLetter)
			busyWorkerList.append(singleLetter)
			print 'busyWorkerList',busyWorkerList
		else:
			loopTest = False
			break;
		loopMax -= 1
		if loopMax < 1:
			exit()
	incrScheduleTimes()
	removeExpiredWorkers()
	timeCounter += 1
	
exit()
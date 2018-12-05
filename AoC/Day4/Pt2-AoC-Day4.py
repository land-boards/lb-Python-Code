# Pt1-AoCDay4.py
# Pt1-AoCDay4.py
# 2018 Advent of Code
# Day 4
# Part 1
# https://adventofcode.com/2018/day/4

import time
import re

"""

Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)

Your puzzle answer was 7887.

"""

def readTextFileToList(fileName):
	"""readTextFileToList - Turn a text file into a list.
	Every line is an element in the list.
	"""
	textFile = []
	# open file and read the content into an accumulated sum
	#print 'Reading in file',time.strftime('%X %x %Z')
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textFile.append(line.strip())
		textFile.sort()
	return textFile

def parseGuardLog(guardLog):
	"""parseGuardLog - Turns three record types into single records remembering the guard number in case it is not changed
	[1518-11-01 23:58] Guard #99 begins shift
	[1518-11-02 00:40] falls asleep
	[1518-11-02 00:50] wakes up
	Turned by filterInputLine to be
	YYYY,MM,DD,HH,MM,Key,Opt1,d/c
	0   ,1 ,2 ,3 ,4 ,5  ,6   ,7
	Key is either Guard, falls or wakes
	Opt1 is Guard number when Key is Guard
	"""
	totalTimeAsleep = 0
	asleepTime = 0
	awakeTime = 0
	sleepLog = []
	for record in guardLog:
		newRecord = re.split('[\W]+',record[1:])		# make this really easy
		if (newRecord[5] == 'Guard'):
			guardNumber = int(newRecord[6])
		elif (newRecord[5] == 'falls'):
			asleepTime = int(newRecord[4])
		elif (newRecord[5] == 'wakes'):
			awakeTime = int(newRecord[4])
			totalTimeAsleep = awakeTime - asleepTime
			sleepLogLine = []
			sleepLogLine.append(guardNumber)
			sleepLogLine.append(asleepTime)
			sleepLogLine.append(awakeTime-1)
			sleepLogLine.append(totalTimeAsleep)
			sleepLog.append(sleepLogLine)
		else:
			print 'parseGuardLog: key error'
			exit()
	guardHoursList = sorted(sleepLog, key = lambda errs: errs[0])		# sort by length column
	return guardHoursList
	
def fillMinsList(previousList,start,end):
	"""
	"""
	#print 'fillMinsList',
	currentOff = start
	while (currentOff <= end):
		previousList[currentOff] = previousList[currentOff] + 1
		currentOff += 1
	#print 'previousList',previousList
	return previousList
	
def getMaxHours(guardSleepWindows):
	"""getMaxHours - 
	Input format [ID,startTime,endTime]
	:returns: list of [ID, timelist...]
	timelist is 0-59 slots with the counts of times that the elf was asleep during that time
	"""
	guardID = -1
	guardRecordsByMinute = []
	minutesList = [0 for i in range(60)]
	for timeRecord in guardSleepWindows:
		#print 'timeRecord',timeRecord
		currentGuardID = timeRecord[0]
		#print 'previous guardID',guardID,
		#print 'this record guardID',currentGuardID
		loopStart = timeRecord[1]
		loopEnd = timeRecord[2]
		loopCount = loopStart
		if guardID == -1:
			#print 'first record'
			minutesList = fillMinsList(minutesList,loopStart,loopEnd)
			guardID = currentGuardID
		elif currentGuardID == guardID:
			#print ' same guard'
			minutesList = fillMinsList(minutesList,loopStart,loopEnd)
		elif currentGuardID != guardID:
			#print '   write out old record'
			shorterList = []
			shorterList.append(guardID)
			shorterList += minutesList
			guardRecordsByMinute.append(shorterList)
			#print '  new record'
			minutesList = [0 for i in range(60)]
			minutesList = fillMinsList(minutesList,loopStart,loopEnd)
			guardID = currentGuardID
	shorterList = []
	shorterList.append(guardID)
	shorterList += minutesList
	guardRecordsByMinute.append(shorterList)
	#print 'guardRecordsByMinute',guardRecordsByMinute
	return guardRecordsByMinute

def getMaxMinByMin(minuteByMinute):
	"""getMaxMinByMin
	"""
	highestSec = 0
	timeOff = 0
	for sec in minuteByMinute:
		if sec > highestSec:
			highestSec = sec
			timeSlot = timeOff
		timeOff += 1
	return [highestSec,timeSlot]
	
def getMaxMinute(guardMaxsByMins):
	"""getMaxMinute
	"""
	#print 'guardMaxsByMins',guardMaxsByMins
	foundGuardID = -1
	foundMaxMins = 0
	for record in guardMaxsByMins:
		currentMaxMins = getMaxMinByMin(record[1:])[0]
		currentMinSlot = getMaxMinByMin(record[1:])[1]
		if currentMaxMins > foundMaxMins:
			foundMaxMins = currentMaxMins
			foundGuardID = record[0]
			foundMinSlot = currentMinSlot
	
	return [foundGuardID,foundMaxMins,foundMinSlot]
	
guardLog = readTextFileToList('input.txt')
guardSleepWindows = parseGuardLog(guardLog)
#print 'guardSleepWindows',guardSleepWindows
guardMaxsByMins = getMaxHours(guardSleepWindows)
guardMinOff = getMaxMinute(guardMaxsByMins)
print 'guard',guardMinOff[0]
print 'time',guardMinOff[2]
print 'PRODUCT',guardMinOff[0]*guardMinOff[2]

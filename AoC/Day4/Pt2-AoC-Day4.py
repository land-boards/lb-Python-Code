# Pt1-AoCDay4.py
# Pt1-AoCDay4.py
# 2018 Advent of Code
# Day 4
# Part 1
# https://adventofcode.com/2018/day/4

import time

"""
--- Day 4: Repose Record ---
You've sneaked into another supply closet - this time, it's across from the prototype suit manufacturing lab. You need to sneak inside and fix the issues with the suit, but there's a guard stationed outside the lab, so this is as close as you can safely get.

As you search the closet for anything that might help, you discover that you're not the first person to want to sneak in. Covering the walls, someone has spent an hour starting every midnight for the past few months secretly observing this guard post! They've been writing down the ID of the one guard on duty that night - the Elves seem to have decided that one guard was enough for the overnight shift - as well as when they fall asleep or wake up while at their post (your puzzle input).

For example, consider the following records, which have already been organized into chronological order:

[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
Timestamps are written using year-month-day hour:minute format. The guard falling asleep or waking up is always the one whose shift most recently started. Because all asleep/awake times are during the midnight hour (00:00 - 00:59), only the minute portion (00 - 59) is relevant for those events.

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-03  #10  ........................#####...............................
11-02  #99  ........................................##########..........
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....


Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?

In the example above, Guard #99 spent minute 45 asleep more than any other guard or minute - three times in total. (In all other cases, any guard spent any minute asleep at most twice.)

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 99 * 45 = 4455.)

"""

def readTextFileToList(fileName):
	"""
	"""
	textFile = []
	# open file and read the content into an accumulated sum
	#print 'Reading in file',time.strftime('%X %x %Z')
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textFile.append(line.strip('\n\r'))
		textFile.sort()
	return textFile

def parseGuardLog(guardLog):
	"""
	012345678901234567890123456789
	[1518-11-01 23:58] Guard #99 begins shift
	[1518-11-02 00:40] falls asleep
	[1518-11-02 00:50] wakes up
	"""
	sleepLog = []
	guardNumber = 0
	totalTimeAsleep = 0
	asleepTime = 0
	awakeTime = 0
	#print 'parseGuardLog: parsing raw log',guardLog
	for record in guardLog:
		timeMins10s = ord(record[15]) - ord('0')
		timeMins1s = ord(record[16]) - ord('0')
		timeMins = 10*timeMins10s + timeMins1s
		#print 'time',timeMins,
		if record[19] == 'G':	# Guard record
			if record[25] != '#':	# verify record type is correct
				print 'error - expected a pound'
				exit()
			lineOff = 26
			if guardNumber != 0:
				totalTimeAsleep = 0	# reset the time
			guardNumber = 0
			while (record[lineOff] != ' '):
				guardNumber = guardNumber * 10
				guardNumber += ord(record[lineOff]) - ord('0')
				lineOff += 1
			hourworthOfZeros = [0] * 60
			#print 'guard',guardNumber
		elif record[19] == 'f':
			#print 'falls asleep at',timeMins,
			asleepTime = timeMins
		elif record[19] == 'w':
			#print 'wakes up at',timeMins,
			awakeTime = timeMins
			totalTimeAsleep += awakeTime - asleepTime
			sleepLogLine = []
			sleepLogLine.append(guardNumber)
			sleepLogLine.append(asleepTime)
			sleepLogLine.append(awakeTime-1)
			#sleepLogLine.append(totalTimeAsleep)
			sleepLog.append(sleepLogLine)
			totalTimeAsleep = 0
			#print 'slept for',totalTimeAsleep
	#print 'sleepLog',sleepLog
	guardHoursList = sorted(sleepLog, key = lambda errs: errs[0])		# sort by length column
	#print guardHoursList
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
	print 'guardMaxsByMins',guardMaxsByMins
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

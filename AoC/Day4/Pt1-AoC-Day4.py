# Pt1-AoCDay4.py
# Pt1-AoCDay4.py
# 2018 Advent of Code
# Day 4
# Part 1
# https://adventofcode.com/2018/day/4

import time
import re

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

Visually, these records show that the guards are asleep at these times:

Date   ID   Minute
            000000000011111111112222222222333333333344444444445555555555
            012345678901234567890123456789012345678901234567890123456789
11-01  #10  .....####################.....#########################.....
11-02  #99  ........................................##########..........
11-03  #10  ........................#####...............................
11-04  #99  ....................................##########..............
11-05  #99  .............................................##########.....
The columns are Date, which shows the month-day portion of the relevant day; ID, which shows the guard on duty that day; and Minute, which shows the minutes during which the guard was asleep within the midnight hour. (The Minute column's header shows the minute's ten's digit in the first row and the one's digit in the second row.) Awake is shown as ., and asleep is shown as #.

Note that guards count as asleep on the minute they fall asleep, and they count as awake on the minute they wake up. For example, because Guard #10 wakes up at 00:25 on 1518-11-01, minute 25 is marked as awake.

If you can figure out the guard most likely to be asleep at a specific time, you might be able to trick that guard into working tonight so you can have the best chance of sneaking in. You have two strategies for choosing the best guard/minute combination.

Strategy 1: Find the guard that has the most minutes asleep. What minute does that guard spend asleep the most?

In the example above, Guard #10 spent the most minutes asleep, a total of 50 minutes (20+25+5), while Guard #99 only slept for a total of 30 minutes (10+10+10). Guard #10 was asleep most during minute 24 (on two days, whereas any other minute the guard was asleep was only seen on one day).

While this example listed the entries in chronological order, your entries are in the order you found them. You'll need to organize them before they can be analyzed.

What is the ID of the guard you chose multiplied by the minute you chose? (In the above example, the answer would be 10 * 24 = 240.)

Your puzzle answer was 95199.

"""

def readTextFileAndSortToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	:returns: the list sorted list
	"""
	textFile = []
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
	Uses regular expressions to parse the input string into separate items in a list
	YYYY,MM,DD,HH,MM,Key,Opt1,d/c
	0   ,1 ,2 ,3 ,4 ,5  ,6   ,7
	Key is either Guard, falls or wakes
	Opt1 is Guard number when Key is Guard
	"""
	minOffset = 4
	commandOffset = 5
	opt1Offset = 6
	totalTimeAsleep = 0
	asleepTime = 0
	awakeTime = 0
	sleepLog = []
	for record in guardLog:
		eachLogRecord = re.split('[\W]+',record[1:])		# regex makes this easy
		if len(eachLogRecord) != 9 and len(eachLogRecord) != 7:
			print 'parseGuardLog: Error - unexpected command length'
			exit()
		if (eachLogRecord[commandOffset] == 'Guard'):
			guardNumber = int(eachLogRecord[opt1Offset])
		elif (eachLogRecord[commandOffset] == 'falls'):
			asleepTime = int(eachLogRecord[minOffset])
		elif (eachLogRecord[commandOffset] == 'wakes'):
			awakeTime = int(eachLogRecord[minOffset])
			totalTimeAsleep = awakeTime - asleepTime
			sleepLogLine = []
			sleepLogLine.append(guardNumber)
			sleepLogLine.append(asleepTime)
			sleepLogLine.append(awakeTime-1)
			sleepLogLine.append(totalTimeAsleep)
			sleepLog.append(sleepLogLine)
		else:	
			print 'parseGuardLog: Error - unsupported command type'
			exit()
	guardHoursList = sorted(sleepLog, key = lambda errs: errs[0])		# sort by length column
	return guardHoursList
	
def mostLikelyAsleepTime(selectedGuardHours):
	"""
	"""
	#print 'selectedGuardHours',selectedGuardHours
	minutesList = [0 for i in range(60)]
	for record in selectedGuardHours:
		startTime = record[0]
		endTime = record[1]
		time = startTime
		while(time <= endTime):
			minutesList[time] += 1
			time += 1
	#print 'minutesList',minutesList
	startTime = 0
	endTime = 59
	currentTime = 0
	maxCountNumber = minutesList[1];
	maxCountTime = 0
	while(currentTime <= endTime):
		#print 'time',currentTime,'count',minutesList[currentTime],'maxCountTime',maxCountTime
		if minutesList[currentTime] > maxCountNumber:
			maxCountNumber = minutesList[currentTime]
			maxCountTime = currentTime
			#print 'max at',currentTime
		currentTime += 1
	return maxCountTime

def maxHours(guardIDvsHours):
	"""
	"""
	maxHours = 0
	selGuard = []
	#print 'guardIDvsHours',guardIDvsHours
	for guardIDTotalHours in guardIDvsHours:
		#print 'guardID',guardIDTotalHours[0]
		#print 'total hrs',guardIDTotalHours[1]
		if guardIDTotalHours[1] > maxHours:
			maxHours = guardIDTotalHours[1]
			selGuard = guardIDTotalHours
	#print 'selGuard',selGuard
	return selGuard

def getHoursByGuardID(guardLog):
	"""
	input list is in format:
	[guardNumber, sleepStartTime, sleepEndTime, sleepTime]
	"""
	guardHours = {}
	
	for guardRecord in guardLog:
		#print 'processing guardRecord',guardRecord
		if guardRecord[0] in guardHours:
			#print '  record exists'
			#print 'hours before',guardHours[guardRecord[0]]
			guardHours[guardRecord[0]] = guardHours[guardRecord[0]] + guardRecord[3]
			#print 'hours after',guardHours[guardRecord[0]]
		else:
			#print '  new record guard number',guardRecord[0],
			#print 'guard hours',guardRecord[3]
			guardHours[guardRecord[0]] = guardRecord[3]
	
	#print 'guardHours',guardHours
	guardHoursList = []
	for key,value in guardHours.iteritems():
		temp = [key,value]
		guardHoursList.append(temp)
	#print 'guardHoursList',guardHoursList
	return guardHoursList

def extractGuardRecords(guardList,selectedGuardID):
	newList = []
	for record in guardList:
		if record[0] == selectedGuardID:
			newList.append(record[1:])
	#print 'newList',newList
	return newList

print 'Reading in file',time.strftime('%X %x %Z')
guardLog = readTextFileAndSortToList('input.txt')
guardList = parseGuardLog(guardLog)
guardIDvsHours = getHoursByGuardID(guardList)
maxHoursForAllGuards = maxHours(guardIDvsHours)
#print 'Total max hours [Guard ID, hours] =',maxHoursForAllGuards
print 'Guard with the most total hours =',maxHoursForAllGuards[0]
print 'Total hours', maxHoursForAllGuards[1]
timeRecords = extractGuardRecords(guardList,maxHoursForAllGuards[0])
criticalTime = mostLikelyAsleepTime(timeRecords)
#print 'Critical Time to do job',criticalTime
print 'PRODUCT=',maxHoursForAllGuards[0]*criticalTime

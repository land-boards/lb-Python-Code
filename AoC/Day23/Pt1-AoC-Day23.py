# Pt1-AoCDay23.py
# 2018 Advent of Code
# Day 23
# Part 1
# https://adventofcode.com/2018/day/23

import time
import re
import os

"""
--- Day 23: Experimental Emergency Teleportation ---
Using your torch to search the darkness of the rocky cavern, you finally locate the man's friend: a small reindeer.

You're not sure how it got so far in this cave. It looks sick - too sick to walk - and too heavy for you to carry all the way back. Sleighs won't be invented for another 1500 years, of course.

The only option is experimental emergency teleportation.

You hit the "experimental emergency teleportation" button on the device and push I accept the risk on no fewer than 18 different warning messages. Immediately, the device deploys hundreds of tiny nanobots which fly around the cavern, apparently assembling themselves into a very specific formation. The device lists the X,Y,Z position (pos) for each nanobot as well as its signal radius (r) on its tiny screen (your puzzle input).

Each nanobot can transmit signals to any integer coordinate which is a distance away from it less than or equal to its signal radius (as measured by Manhattan distance). Coordinates a distance away of less than or equal to a nanobot's signal radius are said to be in range of that nanobot.

Before you start the teleportation process, you should determine which nanobot is the strongest (that is, which has the largest signal radius) and then, for that nanobot, the total number of nanobots that are in range of it, including itself.

For example, given the following nanobots:

pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
The strongest nanobot is the first one (position 0,0,0) because its signal radius, 4 is the largest. Using that nanobot's location and signal radius, the following nanobots are in or out of range:

The nanobot at 0,0,0 is distance 0 away, and so it is in range.
The nanobot at 1,0,0 is distance 1 away, and so it is in range.
The nanobot at 4,0,0 is distance 4 away, and so it is in range.
The nanobot at 0,2,0 is distance 2 away, and so it is in range.
The nanobot at 0,5,0 is distance 5 away, and so it is not in range.
The nanobot at 0,0,3 is distance 3 away, and so it is in range.
The nanobot at 1,1,1 is distance 3 away, and so it is in range.
The nanobot at 1,1,2 is distance 4 away, and so it is in range.
The nanobot at 1,3,1 is distance 5 away, and so it is not in range.
In this example, in total, 7 nanobots are in range of the nanobot with the largest signal radius.

Find the nanobot with the largest signal radius. How many nanobots are in range of its signals?

Your puzzle answer was 588.

That's the right answer! You are one gold star closer to fixing the time stream.

"""

#####################################################################################
## Functions which operate on the input file and node lists

class InputFileHandler():

	def readTextFileLinesToList(self,fileName):
		"""readTextFileAndSrtToList - open file and read the content to a list
		File is sorted to produce a date/time ordered file
		:returns: the list sorted list
		"""
		textFile = ''
		with open(fileName, 'r') as filehandle:  
			textFile = filehandle.readlines()
		inList = []
		for yValueNum in textFile:
			inList.append(yValueNum.strip('\n\r'))
		return inList
	
	def textListToVectorList(self,mapList):
		"""Write out the mapList to a file because it is too big to see on the screen
		
		:param vectorStringsList: List of the file vector strings
		:returns: vector list [x,y,z,radius] as integers
		"""
		debug_mapToList = False
		if debug_mapToList:
			print 'textListToVectorList: newLine',mapList[0]
			print 'textListToVectorList: mapList has line count',len(mapList)
		outList = []
		for line in mapList:
			newLine = line
			newLine = newLine.replace('pos=<','')
			newLine = newLine.replace('>','')
			newLine = newLine.replace(' r=','')
			newList = newLine.split(',')
			newItem = []
			newItemList = []
			for item in newList:
				newItem = int(item)
				newItemList.append(newItem)
			newItemList.append(0)			# distance vector
			outList.append(newItemList)
		return outList

#####################################################################################
## Functions which deal in general with programming tasks

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	exit()

########################################################################
## 

def findStrongestNanoBot(nanoBotVectorsList):
	strongestNanoBot = -1
	strongestNanoBotSignal = -1
	nanoBotNumber = 0
	for nanoBotVec in nanoBotVectorsList:
		if nanoBotVec[3] > strongestNanoBotSignal:
			strongestNanoBotSignal = nanoBotVec[3]
			strongestNanoBot = nanoBotNumber
		nanoBotNumber += 1
	return strongestNanoBot

def getDistance(vector1,vector2):
	distance = abs(vector1[0]-vector2[0]) + abs(vector1[1]-vector2[1]) + abs(vector1[2]-vector2[2])
	return distance
	
def countNanoBotsInDistance(nanoBotNumber, nanoBotsList):
	skipNanoBot = nanoBotNumber
	inRangeCount = 0
	for nanoBot in range (len(nanoBotsList)):
		distance = getDistance(nanoBotsList[skipNanoBot],nanoBotsList[nanoBot])
		if distance <= nanoBotsList[skipNanoBot][3]:
			inRangeCount += 1
	print 'inRangeCount',inRangeCount

########################################################################
## Code

inFileName = 'input.txt'

debug_main = False
print 'Reading in file',time.strftime('%X %x %Z')
InputFileClass = InputFileHandler()
textList = InputFileClass.readTextFileLinesToList(inFileName)
nanoBotsList = InputFileClass.textListToVectorList(textList)

for nanobot in nanoBotsList:
	print nanobot

strongestNanoBot = findStrongestNanoBot(nanoBotsList)
print 'strongest nanobot is',strongestNanoBot

countNanoBotsInDistance(strongestNanoBot, nanoBotsList)

print 'Finished processing',time.strftime('%X %x %Z')

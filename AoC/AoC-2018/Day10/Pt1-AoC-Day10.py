# Pt1-AoCDay9.py
# 2018 Advent of Code
# Day 9
# Part 1
# https://adventofcode.com/2018/day/9

import time
import re
import os

import numpy as np
import matplotlib.pyplot as plt

"""

--- Day 10: The Stars Align ---
It's no use; your navigation system simply isn't capable of providing walking directions in the arctic circle, 
and certainly not in 1018.

The Elves suggest an alternative. In times like these, North Pole rescue operations will arrange points of light 
in the sky to guide missing Elves back to base. Unfortunately, the message is easy to miss: the points move slowly enough that it takes hours to align them, but have so much momentum that they only stay aligned for a second. If you blink at the wrong time, it might be hours before another message appears.

You can see these points of light floating in the distance, and record their position in the sky and their velocity, 
the relative change in position per second (your puzzle input). 
The coordinates are all given from your perspective; given enough time, those positions and velocities 
will move the points into a cohesive message!

Rather than wait, you decide to fast-forward the process and calculate what the points will eventually spell.

For example, suppose you note the following points:

position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
Each line represents one point. 
Positions are given as <X, Y> pairs: X represents how far left (negative) or right (positive) the point appears, 
while Y represents how far up (negative) or down (positive) the point appears.

At 0 seconds, each point has the position given. Each second, each point's velocity is added to its position. 
So, a point with velocity <1, -2> is moving to the right, but is moving upward twice as quickly. 
If this point's initial position were <3, 9>, after 3 seconds, its position would become <6, 3>.

Over time, the points listed above would move like this:

Initially:
........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........

After 1 second:
......................
......................
..........#....#......
........#.....#.......
..#.........#......#..
......................
......#...............
....##.........#......
......#.#.............
.....##.##..#.........
........#.#...........
........#...#.....#...
..#...........#.......
....#.....#.#.........
......................
......................

After 2 seconds:
......................
......................
......................
..............#.......
....#..#...####..#....
......................
........#....#........
......#.#.............
.......#...#..........
.......#..#..#.#......
....#....#.#..........
.....#...#...##.#.....
........#.............
......................
......................
......................

After 3 seconds:
......................
......................
......................
......................
......#...#..###......
......#...#...#.......
......#...#...#.......
......#####...#.......
......#...#...#.......
......#...#...#.......
......#...#...#.......
......#...#..###......
......................
......................
......................
......................

After 4 seconds:
......................
......................
......................
............#.........
........##...#.#......
......#.....#..#......
.....#..##.##.#.......
.......##.#....#......
...........#....#.....
..............#.......
....#......#...#......
.....#.....##.........
...............#......
...............#......
......................
......................
After 3 seconds, the message appeared briefly: HI. Of course, your message will be much longer and will take many more seconds to appear.

What message will eventually appear in the sky?

"""


def readTextFileToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
	:returns: the list sorted list
	"""
	textList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textList.append(line.strip())
	# for line in textList:
		# print line
	return textList
	
def textFileToList(textFile):
	"""Convert the text file into a list
	
	"""
	theList = []
	for row in textFile:
		myRow = []
		myRow = row.replace('position=< ','')
		myRow = myRow.replace('position=<','')
		myRow = myRow.replace('velocity=<',',')
		myRow = myRow.replace('>','')
		myRow = myRow.replace(',,,',',')
		myRow = myRow.replace(',,',',')
		myRow = myRow.replace(' ','')
		myRow = myRow.split(',')
		newRow = []
		newRow.append(int(myRow[0]))
		newRow.append(int(myRow[1]))
		newRow.append(int(myRow[2]))
		newRow.append(int(myRow[3]))
		theList.append(newRow)
	return theList

#####################################################################################
## Functions which operate on the input file and node lists


#####################################################################################
## Functions which operate on the node list


########################################################################
## This is the workhorse of this assignment

def moveStars(starElement):
	xPos = starElement[0]
	yPos = starElement[1]
	xVel = starElement[2]
	yVel = starElement[3]
	newX = xPos + xVel
	newY = yPos + yVel
	return [newX,newY,xVel,yVel]

def make2dList(yVals,xVals):
	"""make2dList - Make a 2D list
	"""
	a=[]
	for row in xrange(yVals): a += [[0]*(xVals)]
	return a
	

#################################################################################
##  plot the map
## Some helpful tutorials out there for this
## https://matplotlib.org/index.html
## https://matplotlib.org/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py
## https://matplotlib.org/gallery/shapes_and_collections/scatter.html

def plotScatterPoints(xyList):
	print 'plotScatterPoints: reached function'
	x = []
	y = []
	for point in xyList:
		x.append(point[0])
		y.append(point[1])
	plt.scatter(x,y)
	plt.show()

def getBoundingBox(xyList):
	xMin = xyList[0][0]
	yMin = xyList[0][1]
	xMax = xyList[0][0]
	yMax = xyList[0][1]
	for point in xyList:
		if point[0] < xMin:
			xMin = point[0]
		if point[1] < yMin:
			yMin = point[1]
		if point[0] > xMax:
			xMax = point[0]
		if point[1] > yMax:
			yMax = point[1]
#	print 'Bounding box size is',xMax-xMin,'by',yMax-yMin
	return [xMax-xMin,yMax-yMin]


########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

textList = readTextFileToList('input.txt')

myList = textFileToList(textList)

timeInSecs = 0
xyList = []
for row in myList:
	xyList.append([row[0],-row[1],row[2],row[3]])
plotScatterPoints(xyList)
saveBoundBoxXY = getBoundingBox(xyList)
print timeInSecs

plotOn = False
while True:
	#print 'length of xyList',len(xyList)
	for pointIndex in xrange(len(xyList)):
		#print pointIndex
		xyList[pointIndex][0] = xyList[pointIndex][0] + xyList[pointIndex][2]
		xyList[pointIndex][1] = xyList[pointIndex][1] - xyList[pointIndex][3]
	boundBoxXY = getBoundingBox(xyList)
	if boundBoxXY == [115,69]:
		plotOn = True
	if plotOn:
		print timeInSecs
		plotScatterPoints(xyList)
	timeInSecs += 1
	#os.system('pause')

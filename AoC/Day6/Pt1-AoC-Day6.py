# Pt1-AoCDay5.py
# 2018 Advent of Code
# Day 6
# Part 1
# https://adventofcode.com/2018/day/6

import time
import re

"""
--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

"""

def readTextFileTo2DList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	list is converted into a 2D array
	:returns: the list sorted list
	"""
	with open(fileName, 'r') as filehandle: 
		lineData = []
		for line in filehandle:
			lineData.append(line)
	return lineData

def turnTextListInto2DList(list):
	array2D = []
	for line in list:
		lineDat = []
		line = line.strip()
		lineDatA = line.split(',')
		lineDat.append(int(lineDatA[0]))
		lineDat.append(int(lineDatA[1]))
		array2D.append(lineDat)
	return array2D

def getMaxVals(list2D):
	maxX = 0
	maxY = 0
	for row in list2D:
		if row[0] > maxX:
			maxX = row[0]
		if row[1] > maxY:
			maxY = row[1]
	return [maxX,maxY]
	
def getMinVals(list2D):
	minX = 9999
	minY = 9999
	for row in list2D:
		if row[0] < minX:
			minX = row[0]
		if row[1] < minY:
			minY = row[1]
	return [minX,minY]
	
inputList = readTextFileTo2DList('input.txt')
list2D = turnTextListInto2DList(inputList)
print 'list2D',list2D
minVals = getMinVals(list2D)
print 'minVals',minVals
maxVals = getMaxVals(list2D)
print 'maxVals',maxVals

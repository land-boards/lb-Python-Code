# Pt1-AoCDay3.py
# 2017 Advent of Code
# Day 3
# Part 1
# Problem
# https://adventofcode.com/2017/day/3
# Dataset
# https://adventofcode.com/2017/day/3/input

import time
import re
import numpy

"""

--- Day 3: Spiral Memory ---
You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...
While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the location of the only access port for this memory system) by programs that can only move up, down, left, or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.
How many steps are required to carry the data from the square identified in your puzzle input all the way to the access port?

Your puzzle input is 289326.

"""

def make2dList(rows, cols):
    a=[]
    for row in xrange(rows): a += [[0]*cols]
    return a

def put(x,y,val):
	print 'put at x,y value',x,y,val,
	myListArray[x+halfArraySize][y+halfArraySize] = val

def get(x,y):
	return(myListArray[x+halfArraySize][y+halfArraySize])
	
def sumAdjacentSquares(x,y):
	"""sum up all of the squares that surround a particular square
	"""
	sum = 0
	sum += get(x-1,y-1)
	sum += get(x-1,y)
	sum += get(x-1,y+1)
	sum += get(x,y-1)
	sum += get(x,y+1)
	sum += get(x+1,y-1)
	sum += get(x+1,y)
	sum += get(x+1,y+1)
	return sum
	
print 'Starting time',time.strftime('%X %x %Z')

seedInput = 1024

arraySize = 600
halfArraySize = arraySize/2
myListArray = make2dList(600,600)

for row in myListArray:
	for column in row:
		column = 0

dirs = ['right','up','left','down']
putLocX = 0
putLocY = 0
putVal = 1
direction = 'right'
while putVal <= seedInput:
	put(putLocX,putLocY,putVal)
	lastX = putLocX
	lastY = putLocY
	if direction == 'right':
		putLocX += 1
		if get(putLocX,putLocY+1) == 0:
			direction = 'up'
	elif direction == 'up':
		putLocY += 1
		if get(putLocX-1,putLocY) == 0:
			direction = 'left'
	elif direction == 'left':
		putLocX -= 1
		if get(putLocX,putLocY-1) == 0:
			direction = 'down'
	elif direction == 'down':
		putLocY -= 1
		if get(putLocX+1,putLocY) == 0:
			direction = 'right'
	print 'new dir',direction
	putVal += 1
print 'finalX,finalY,value',lastX,lastY
print 'manhattan distance',abs(lastX)+abs(lastY)

# This is a CCW spiral
print 'Finished',time.strftime('%X %x %Z')

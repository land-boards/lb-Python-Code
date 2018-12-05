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
--- Part Two ---
As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
What is the first value written that is larger than your puzzle input?

Your puzzle input is still 289326.

"""

def make2dList(rows, cols):
    a=[]
    for row in xrange(rows): a += [[0]*cols]
    return a

def put(x,y,val):
	#print 'put at x,y value',x,y,val,
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

seedInput = 289326

arraySize = 600
halfArraySize = arraySize/2
myListArray = make2dList(600,600)

for row in myListArray:
	for column in row:
		column = 0

dirs = ['right','up','left','down']
put(0,0,1)
putLocX = 1
putLocY = 0
putVal = 1
direction = 'up'
while True:
	putVal = sumAdjacentSquares(putLocX,putLocY)
	put(putLocX,putLocY,putVal)
	if putVal > seedInput:
		break
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
	#print 'new dir',direction
print 'value',lastX,putVal

# This is a CCW spiral
print 'Finished',time.strftime('%X %x %Z')

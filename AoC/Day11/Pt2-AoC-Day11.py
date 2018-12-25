# Pt1-AoCDay11.py
# 2018 Advent of Code
# Day 11
# Part 1
# https://adventofcode.com/2018/day/11

import time
import re
import os

"""

--- Day 11: Chronal Charge ---

--- Part Two ---
You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. 
Sizes from 1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. 
Identify this square by including its size as a third parameter after the top-left coordinate: 
a 9x9 square with a top-left corner of 3,5 is identified as 3,5,9.

For example:

For grid serial number 18, the largest total square (with a total power of 113) is 16x16 
and has a top-left corner of 90,269, so its identifier is 90,269,16.
For grid serial number 42, the largest total square (with a total power of 119) is 12x12 
and has a top-left corner of 232,251, so its identifier is 232,251,12.
What is the X,Y,size identifier of the square with the largest total power?

Your puzzle input is still 2866.

"""

#####################################################################################
## Functions which deal in general with programming tasks

def abbyTerminate(string):
	"""Terminate program due to abnormal condition
	"""
	print 'ERROR Terminating due to',string
	exit()

#####################################################################################
##

def make2dList(ySize,xSize):
	"""make2dList - Make a 2D list
	"""
	a=[]
	for row in xrange(ySize): a += [[0]*(xSize)]
	return a
	
def clearArray(arrayToClear,fillValue=0):
	"""clearArray - Fill 2D square array with -1 values
	"""
	for y in range(len(arrayToClear)):
		for x in range(len(arrayToClear[0])):
			arrayToClear[y][x] = fillValue
	return arrayToClear
	
def setFuelLevels(fuelCellArrayAs2DList):
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])):
			rackID = xOffset + 10
			powerLevel = (rackID * yOffset) + gridSerialNumber
			powerLevel = powerLevel * rackID
			#print 'xy',xOffset,yOffset,'powerLevel',powerLevel
			if powerLevel < 100:
				powerLevel = 0
			else:
				powerString = str(powerLevel)
				#print 'powerString',powerString
				power100sDigitString = str(powerString)
				#print 'power100sDigitString',power100sDigitString
				powerLevel = int(power100sDigitString[-3])
			powerLevel -= 5
			#print 'powerLevel',powerLevel
			fuelCellArrayAs2DList[yOffset][xOffset] = powerLevel
	return fuelCellArrayAs2DList

def dumpFuelCellArray(fuelCellArrayAs2DList):
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])):
			print fuelCellArrayAs2DList[yOffset][xOffset],
		print

def get3x3Power(xOffset,yOffset,fuelCellArrayAs2DList):
	totalPower = fuelCellArrayAs2DList[yOffset][xOffset]
	totalPower += fuelCellArrayAs2DList[yOffset][xOffset+1]
	totalPower += fuelCellArrayAs2DList[yOffset][xOffset+2]
	totalPower += fuelCellArrayAs2DList[yOffset+1][xOffset]
	totalPower += fuelCellArrayAs2DList[yOffset+1][xOffset+1]
	totalPower += fuelCellArrayAs2DList[yOffset+1][xOffset+2]
	totalPower += fuelCellArrayAs2DList[yOffset+2][xOffset]
	totalPower += fuelCellArrayAs2DList[yOffset+2][xOffset+1]
	totalPower += fuelCellArrayAs2DList[yOffset+2][xOffset+2]
	return totalPower

def getNxNPower(xOffset,yOffset,size,fuelCellArrayAs2DList):
	xDim = size
	yDim = size
	totalPower = 0
	for yVal in xrange(yOffset,yOffset+size):
		for xVal in xrange(xOffset,xOffset+size):
			totalPower =+ fuelCellArrayAs2DList[yVal][xVal]
	return totalPower

def findLargest3x3PowerGrid(fuelCellArrayAs2DList):
	maxPower = getNxNPower(1,1,3,fuelCellArrayAs2DList)
	maxXY = [1,1]
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)-2):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])-2):
			cells3x3Power = getNxNPower(xOffset,yOffset,3,fuelCellArrayAs2DList)
			#print 'xy,power',xOffset,yOffset,cells3x3Power
			if cells3x3Power > maxPower:
				maxPower = cells3x3Power
				maxXY = [xOffset,yOffset]
	return maxXY

def findLargestNxNPowerGrid(fuelCellArrayAs2DList):
	maxPower = getNxNPower(1,1,3,fuelCellArrayAs2DList)
	maxXY = [1,1]
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)-2):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])-2):
			cells3x3Power = getNxNPower(xOffset,yOffset,3,fuelCellArrayAs2DList)
			#print 'xy,power',xOffset,yOffset,cells3x3Power
			if cells3x3Power > maxPower:
				maxPower = cells3x3Power
				maxXY = [xOffset,yOffset]
	return maxXY
	
########################################################################
## This is the workhorse of this assignment


########################################################################
## Code

#gridSerialNumber = 18
gridSerialNumber = 2866	# The program input

print 'Starting Processing',time.strftime('%X %x %Z')

fuelCellArrayAs2DList = make2dList(301,301)
clearArray(fuelCellArrayAs2DList,0)
setFuelLevels(fuelCellArrayAs2DList)
#dumpFuelCellArray(fuelCellArrayAs2DList)
#print 'power at 101,153 is',fuelCellArrayAs2DList[153][101]
#exit()
maxXY = findLargest3x3PowerGrid(fuelCellArrayAs2DList)
print '3x3 maxXY is at',maxXY

print 'Finished processing',time.strftime('%X %x %Z')

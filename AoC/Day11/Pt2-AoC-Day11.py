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
	debug_setFuelLevels = False
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])):
			rackID = xOffset + 10
			powerLevel = (rackID * yOffset) + gridSerialNumber
			powerLevel = powerLevel * rackID
			if debug_setFuelLevels:
				print 'xy',xOffset,yOffset,'powerLevel',powerLevel
			if powerLevel < 100:
				powerLevel = 0
			else:
				powerString = str(powerLevel)
				if debug_setFuelLevels:
					print 'powerString',powerString
				power100sDigitString = str(powerString)
				if debug_setFuelLevels:
					print 'power100sDigitString',power100sDigitString
				powerLevel = int(power100sDigitString[-3])
			powerLevel -= 5
			if debug_setFuelLevels:
				print 'powerLevel',powerLevel
			fuelCellArrayAs2DList[yOffset][xOffset] = powerLevel
	return fuelCellArrayAs2DList

def dumpFuelCellArray(fuelCellArrayAs2DList):
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])):
			print fuelCellArrayAs2DList[yOffset][xOffset],
		print

def getNxNPower(xOffset,yOffset,size,fuelCellArrayAs2DList):
	debug_getNxNPower = False
	if debug_getNxNPower:
		print 'reached getNxNPower:'
	xDim = size
	yDim = size
	totalPower = 0
	for yVal in xrange(yOffset,yOffset+size):
		for xVal in xrange(xOffset,xOffset+size):
			if debug_getNxNPower:
				print 'getNxNPower: at xy',xVal,yVal,'power',fuelCellArrayAs2DList[yVal][xVal]
			totalPower = totalPower + fuelCellArrayAs2DList[yVal][xVal]
	if debug_getNxNPower:
		print 'getNxNPower: totalPower',totalPower
	return totalPower

def findLargestNxNPowerGrid(size,fuelCellArrayAs2DList):
	maxPower = getNxNPower(1,1,size,fuelCellArrayAs2DList)
	maxXY_Power = [1,1,maxPower]
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)-(size-1)):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])-(size-1)):
			cellsNxNPower = getNxNPower(xOffset,yOffset,size,fuelCellArrayAs2DList)
			#print 'xy,power',xOffset,yOffset,cellsNxNPower
			if cellsNxNPower > maxPower:
				maxPower = cellsNxNPower
				maxXY_Power = [xOffset,yOffset,size,maxPower]
	print 'maxXY_Power',maxXY_Power
	return maxXY_Power
	
def interateOverFuelArraySizes(fuelCellArrayAs2DList):
	maxXY_Power = findLargestNxNPowerGrid(3,fuelCellArrayAs2DList)
	print 'interateOverFuelArraySizes: (with fixed size = 3)',maxXY_Power
	powerMax = 0
	powerLocation = [0,0]
	for size in xrange(1,len(fuelCellArrayAs2DList)-1):
		maxXY_Power = findLargestNxNPowerGrid(size,fuelCellArrayAs2DList)
		if maxXY_Power[3] > powerMax:
			print 'new highest power'
			powerMax = maxXY_Power[3]
			powerLocation = maxXY_Power
			sizeKeeper = size
		print '.',
	return maxXY_Power

########################################################################
## Main

#gridSerialNumber = 18
#gridSerialNumber = 42
gridSerialNumber = 2866	# The program input

print 'Starting Processing',time.strftime('%X %x %Z')

fuelCellArrayAs2DList = make2dList(301,301)
clearArray(fuelCellArrayAs2DList,0)
setFuelLevels(fuelCellArrayAs2DList)
#dumpFuelCellArray(fuelCellArrayAs2DList)
#print 'Using nxn function power at 33,45 is',getNxNPower(33,45,3,fuelCellArrayAs2DList)
# maxXY = findLargestNxNPowerGrid(3,fuelCellArrayAs2DList)
# print 'Using nxn function 3x3 maxXY is at',maxXY
powerLocation = interateOverFuelArraySizes(fuelCellArrayAs2DList)
print 'max is', powerLocation

print 'Finished processing',time.strftime('%X %x %Z')

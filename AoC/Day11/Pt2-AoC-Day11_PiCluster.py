from mpi4py import MPI
import time
import re
import os

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
				powerLevel = powerLevel / 100
				powerLevel %= 10
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
			totalPower += fuelCellArrayAs2DList[yVal][xVal]
	if debug_getNxNPower:
		print 'getNxNPower: totalPower',totalPower
	return totalPower

def findLargestNxNPowerGrid(size,fuelCellArrayAs2DList):
	maxPower = getNxNPower(1,1,size,fuelCellArrayAs2DList)
	maxXY_Power = [1,1,size,maxPower]
	for yOffset in xrange(1,len(fuelCellArrayAs2DList)-(size-1)):
		for xOffset in xrange(1,len(fuelCellArrayAs2DList[0])-(size-1)):
			cellsNxNPower = getNxNPower(xOffset,yOffset,size,fuelCellArrayAs2DList)
			#print 'xy,power',xOffset,yOffset,cellsNxNPower
			if cellsNxNPower > maxPower:
				maxPower = cellsNxNPower
				maxXY_Power = [xOffset,yOffset,size,maxPower]
	print 'findLargestNxNPowerGrid: node',MPrank,'power',maxXY_Power[3],'size',size
	return maxXY_Power
	
def interateOverFuelArraySizes(fuelCellArrayAs2DList):
	maxXY_Power = [0,0,0,0]
	powerMax = 0
	powerLocation = [0,0]
	powerVector = maxXY_Power
	for size in xrange(MPrank,len(fuelCellArrayAs2DList)-1,MPsize):
		maxXY_Power = findLargestNxNPowerGrid(size,fuelCellArrayAs2DList)
		if maxXY_Power[3] > powerMax:
			print 'new highest power processor rank',MPrank
			powerMax = maxXY_Power[3]
			powerLocation = maxXY_Power
			sizeKeeper = size
			powerVector = maxXY_Power
			print 'interateOverFuelArraySizes: node number',MPrank,'will return',powerVector
	return powerVector

########################################################################
## Main

comm = MPI.COMM_WORLD
MPsize = comm.Get_size()
MPrank = comm.Get_rank()

gridSerialNumber = 18
#gridSerialNumber = 42
#gridSerialNumber = 2866	# The program input

print 'Starting Processing at',time.strftime('%X %x %Z')

fuelCellArrayAs2DList = make2dList(301,301)
clearArray(fuelCellArrayAs2DList,0)
setFuelLevels(fuelCellArrayAs2DList)
#dumpFuelCellArray(fuelCellArrayAs2DList)
print 'Using nxn function power at 33,45 is',getNxNPower(33,45,3,fuelCellArrayAs2DList)
maxXY = findLargestNxNPowerGrid(3,fuelCellArrayAs2DList)
print 'Using nxn function 3x3 maxXY is at',maxXY
powerLocation = interateOverFuelArraySizes(fuelCellArrayAs2DList)
print 'max is', powerLocation

# print 'Finished processing',time.strftime('%X %x %Z')

newData = comm.gather(powerLocation,root=0)
if MPrank == 0:
   print 'master:'
   maxPowerFound = 0
   for processor in newData:
	print processor
	if processor[3] > maxPowerFound:
		maxPowerFound = processor[3]
	print 'Max power is',maxPowerFound
		
print 'Ended Processing at',time.strftime('%X %x %Z')

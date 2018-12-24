# Pt1-AoCDay22.py
# Pt1-AoCDay22.py
# 2018 Advent of Code
# Day 22
# Part 1
# 

import time
import re
import os

"""

--- Day 22: Mode Maze ---

Part 2 using tools go through the maze

"""

#####################################################################################
## Functions which operate on the input file and node lists

class InputFileHandler():

	def readTextFileLinesToList(self,fileName):
		"""readTextFileAndSrtToList - open file and read the content to a list
		:returns: the list
		"""
		textFile = ''
		with open(fileName, 'r') as filehandle:  
			textFile = filehandle.readlines()
		inList = []
		for row in textFile:
			inList.append(row.strip('\n\r'))
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

#####################################################################################
## 2D list code

def make2dList(yVals,xVals):
	"""make2dList - Make a 2D list
	"""
	a=[]
	for row in xrange(yVals): a += [[0]*(xVals)]
	return a

def clearArray(arrayToClear,fillValue=0):
	"""clearArray - Fill 2D square array with -1 values
	"""
	for y in range(len(arrayToClear)):
		for x in range(len(arrayToClear[0])):
			arrayToClear[y][x] = fillValue
	return arrayToClear
			
def get(x,y):
	return(myListArray[x][y])

def printMap(erosionIndex):
	for yVal in xrange(len(erosionIndex)):
		for xVal in xrange(len(erosionIndex[0])):
			if erosionIndex[yVal][xVal] == 'M':
				print 'M',
			elif erosionIndex[yVal][xVal] == 'T':
				print 'T',
			elif erosionIndex[yVal][xVal] %3 == 0:
				print '.',
			elif erosionIndex[yVal][xVal] %3 == 1:
				print '=',
			elif erosionIndex[yVal][xVal] %3 == 2:
				print '|',
		print
	
def determineRiskLevel(erosionIndex):
	risk = 0
	for yVal in xrange(targetXY[1]+1):
		for xVal in xrange(targetXY[0]+1):
			if erosionIndex[yVal][xVal] == 'M':
				risk += 0
			elif erosionIndex[yVal][xVal] == 'T':
				risk += 0
			elif erosionIndex[yVal][xVal] %3 == 0:
				risk += 0
			elif erosionIndex[yVal][xVal] %3 == 1:
				risk += 1
			elif erosionIndex[yVal][xVal] %3 == 2:
				risk += 2
	print 'Risk is',risk

#####################################################################################
## Code

depth = 5355
targetXY = [14,796]

# depth = 510
# targetXY = [10,10]

# cave is pretty narrow but pretty long

debug_main = False
print 'Started processing',time.strftime('%X %x %Z')

geoIndex = make2dList(targetXY[1]+1,targetXY[0]+1)
geoIndex = clearArray(geoIndex)

erosionIndex = make2dList(targetXY[1]+1,targetXY[0]+1)
erosionIndex = clearArray(erosionIndex)

for yVal in xrange(len(geoIndex)):
	for xVal in xrange(len(geoIndex[0])):
		geologicalIndexAtPoint = 0
		if yVal == 0 and xVal == 0:
			geologicalIndexAtPoint = 0
		elif yVal == 0:
			geologicalIndexAtPoint = xVal * 16807
		elif xVal == 0:
			geologicalIndexAtPoint = yVal * 48271
		else:
			geologicalIndexAtPoint = (erosionIndex[yVal-1][xVal]) * (erosionIndex[yVal][xVal-1])
		geoIndex[yVal][xVal] = geologicalIndexAtPoint
		erosionIndex[yVal][xVal] = (geologicalIndexAtPoint + depth) % 20183
		
print 'len(erosionIndex)',len(erosionIndex)
print 'len(erosionIndex[0])',len(erosionIndex[0])

erosionIndex[0][0] = 'M'
erosionIndex[targetXY[1]][targetXY[0]] = 'T'

printMap(erosionIndex)

determineRiskLevel(erosionIndex)

#print geoIndex

print 'Finished processing',time.strftime('%X %x %Z')

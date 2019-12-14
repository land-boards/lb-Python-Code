# Pt1-AoCDayX.py
# 2019 Advent of Code
# Day X
# Part 1

"""

"""
from __future__ import print_function

fileName = 'input.txt'

def listOfCharsToString(charList):
	#print("CharList ",charList)
	charString = ''.join(charList)
	#print("charString",charString)
	return(charString)

def parseSrcEquations(inLine):
	""" Return list of elements in the line
	"""
	#print("inLine =",inLine)
	lineState = 'delims'
	discardList = [' ','=','>',',']
	for x in range(0,10):
		discardList.append(str(x))
	#print("Discard List is",discardList)
	charSymbols = []
	currentSymbol = []
	for lineChar in inLine:
		if lineChar in discardList:
			if currentSymbol != []:
				charSymbols.append(currentSymbol)
			#print("Discarding",lineChar)
			lineState = 'delims'
			currentSymbol = []
		elif lineState == 'delims':
			lineState = 'symbolChar'
			#print("Chemical char(1)",lineChar)
			currentSymbol.append(lineChar)
		else:
			#print("Chemical char(2)",lineChar)
			currentSymbol.append(lineChar)
	charSymbols.append(currentSymbol)
	#print("charSymbols",charSymbols)
	listOfSymbols = []
	for charStr in charSymbols:
		listOfSymbols.append(listOfCharsToString(charStr))
	#print("Final List ",listOfSymbols)
	return(listOfSymbols)

def getElementList(srcEquations):
	elementList = []
	for line in srcEquations:
		#print("line",line)
		lineElements = parseSrcEquations(line)
		#print(lineElements)
		for element in lineElements:
			if element not in elementList:
				elementList.append(element)
	return(sorted(elementList))

def readInputFile(fileName):
	srcEquations = []
	# open file and read the contents
	with open(fileName, 'r') as filehandle:  
		for lineIn in filehandle:
			srcEquations.append(lineIn.strip())
	return(srcEquations)

goal = 'FUEL'
start = 'ORE'

srcEquations = readInputFile(fileName)
sortedElementList = getElementList(srcEquations)
print("elementList",sortedElementList)


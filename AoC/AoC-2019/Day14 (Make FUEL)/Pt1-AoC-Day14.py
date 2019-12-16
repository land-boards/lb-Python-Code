# Pt1-AoCDay14.py
# 2019 Advent of Code
# Day 14
# Part 1
# https://adventofcode.com/2019/day/14

"""
AN SQQ-89/AN SQQ-89/TI20/AAC TDP/
"""
from __future__ import print_function

#fileName = 'input.txt'
fileName = 'example_1_1.txt'
#fileName = 'example_1_2.txt'
#fileName = 'example_1_3.txt'
#fileName = 'example_1_4.txt'
print("fileName",fileName)

def listOfCharsToString(charList):
	#print("CharList ",charList)
	charString = ''.join(charList)
	#print("charString",charString)
	return(charString)

def parseSrcEquations(inLine):
	""" Return list of elements in the line
	"""
	debug_parseSrcEquations = False
	if debug_parseSrcEquations:
		print("parseSrcEquations: inLine =",inLine)
	lineState = 'delims'
	discardList = [' ','=','>',',','\n']
	for x in range(0,10):
		discardList.append(str(x))
	if debug_parseSrcEquations:
		print("parseSrcEquations: Discard List is",discardList)
	charSymbols = []
	currentSymbol = []
	for lineChar in inLine:
		if lineChar in discardList:
			if currentSymbol != []:
				charSymbols.append(currentSymbol)
				if debug_parseSrcEquations:
					print("parseSrcEquations: Discarding",lineChar)
			lineState = 'delims'
			currentSymbol = []
		elif lineState == 'delims':
			lineState = 'symbolChar'
			if debug_parseSrcEquations:
				print("parseSrcEquations: Chemical char(1)",lineChar)
			currentSymbol.append(lineChar)
		else:
			if debug_parseSrcEquations:
				print("parseSrcEquations: Chemical char(2)",lineChar)
			currentSymbol.append(lineChar)
	charSymbols.append(currentSymbol)
	if debug_parseSrcEquations:
		print("parseSrcEquations: charSymbols",charSymbols)
	listOfSymbols = []
	for charStr in charSymbols:
		listOfSymbols.append(listOfCharsToString(charStr))
	if debug_parseSrcEquations:
		print("parseSrcEquations: Final List ",listOfSymbols)
	return(listOfSymbols)

def getElementList(srcEquations):
	elementList = []
	for line in srcEquations:
		lineElements = parseSrcEquations(line)
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

def makeRecipePairs(listOfRecipes):
	""" 
	"""
	recipePairList = []
	for recipe in listOfRecipes:
		print("makeRecipePairs: recipe",recipe)
		for element in recipe[:-1]:
			elementPair = []
			#print("makeRecipePairs: source element",element)
			elementPair.append(element)
			#print("makeRecipePairs: destination element",recipe[-1])
			elementPair.append(recipe[-1])
			print("makeRecipePairs: elementPair",elementPair)
			recipePairList.append(elementPair)
	#print("recipePairList",recipePairList)
	return recipePairList

def makeRecipes(inEquations):
	"""Take the list of recipes and turn it into a list of equations
	Input: 
	"""
	#print("makeRecipes: inEquations",inEquations)
	listOfRecipes = []
	for recipe in inEquations:
		#print("makeRecipes: recipe",recipe)
		parsedResult = parseSrcEquations(recipe)
		listOfRecipes.append(parsedResult)
	#print("listOfRecipes",listOfRecipes)
	return(listOfRecipes)
		
def makeGraphOutput(listOfRecipePairs):
	# Drop into http://webgraphviz.com/
	print("vvvvvvvvvv BEGINNING OF GRAPH OUTPUT")
	for recipePair in listOfRecipePairs:
		print('"',end='')
		print(recipePair[0],end='')
		print('"',end='')
		print(" -> ",end='')
		print('"',end='')
		print(recipePair[1],end='')
		print('"')
	print("END OF GRAPH OUTPUT ^^^^^^^^^^^^^^^^^")

goal = 'FUEL'
start = 'ORE'

srcEquations = readInputFile(fileName)
print("srcEquations",srcEquations)
sortedElementList = getElementList(srcEquations)
print("elementList",sortedElementList)
recipesWithAllIngredientS = makeRecipes(srcEquations)
print("recipesWithAllIngredientS",recipesWithAllIngredientS)
recipesWithPairsOfIngredients = makeRecipePairs(recipesWithAllIngredientS)
print ("recipesWithPairsOfIngredients",recipesWithPairsOfIngredients)
makeGraphOutput(recipesWithPairsOfIngredients)
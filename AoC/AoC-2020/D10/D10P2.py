# D10P1.py
# 2020 Advent of Code
# Day 10
# Part 2

# 5856458868470016 too big

import itertools

# """
# """

DEBUG_PRINT = True
DEBUG_PRINT = False
def debugPrint(thingToPrint):
	global DEBUG_PRINT
	if DEBUG_PRINT:
		print(thingToPrint)
		
# open file and read the content into an accumulated sum
def readListOfInts():
	global DEBUG_PRINT
	newList = []
	with open('input.txt', 'r') as filehandle:  
		for lineIn in filehandle:
			newList.append(int(lineIn.strip()))
	debugPrint('newList')
	debugPrint(newList)
	return newList
#	return [1,2,3,4,5]

def isRowLegal(row,check):
	global DEBUG_PRINT
	debugPrint('isRowLegal: check ends' + str(check))
	if row[0] != check[0]:
		debugPrint('bad first digit')
		return False
	if row[-1] != check[-1]:
		debugPrint('bad last digit')
		return False
	for digitIndex in range(len(check)-1):
		if check[digitIndex] > check[digitIndex+1]:
			return False
	for digitIndex in range(len(check)-1):
		if check[digitIndex]+3 < check[digitIndex+1]:
			return False
	debugPrint('end are OK')
	return True

def reduceRow(inRow):
	global DEBUG_PRINT
	debugPrint('reduceRow in')
	debugPrint(inRow)
	outRow = []
	outRow.append(inRow[0])
	for digitOffset in range(1,len(inRow)-1):
		if inRow[digitOffset-1] < inRow[digitOffset]:
			outRow.append(inRow[digitOffset])
	outRow.append(inRow[-1])
	debugPrint('reduceRow out')
	debugPrint(outRow)
	return outRow
	
def makeListOfAllCombos(inList):
	runListPerms = list(itertools.permutations(inList))
	debugPrint('runListPerms')
	debugPrint(runListPerms)
	newPermList = []
	for permVal in runListPerms:
		newPermList.append(list(permVal))
	debugPrint('newPermList')
	debugPrint(newPermList)
	for listLen in range(len(inList)-1,1,-1):
		debugPrint('listLen'+str(listLen))
		comboList = list(itertools.combinations(inList,listLen))
		debugPrint('comboList')
		debugPrint(comboList)
		for row in comboList:
			newPermList.append(list(row))
		debugPrint('newPermList')
		debugPrint(newPermList)
	return newPermList

def countLegalPerms(inRunList):
	global DEBUG_PRINT
	if len(inRunList) == 1:
		return 1
	runList = list(inRunList)
	debugPrint('runList')
	debugPrint(runList)
	runListPerms = makeListOfAllCombos(runList)
	legalLists = []
	for checkRow in runListPerms:
		row = list(checkRow)
		debugPrint('\nchecking combination')
		debugPrint(list(row))
		passCheck = True
		if isRowLegal(list(runList),row):
			newRow = reduceRow(row)
			if newRow != []:
				if newRow not in legalLists:
					debugPrint('adding newRow')
					debugPrint(newRow)
					legalLists.append(newRow)
		else:
			debugPrint('fails check for legal')
			debugPrint(row)
	DEBUG_PRINT = True
	debugPrint('legalLists')
	debugPrint(legalLists)
	DEBUG_PRINT = False
	debugPrint('count of legalLists' + str(len(legalLists)))
	return(len(legalLists))

adapterJoltages = readListOfInts()
debugPrint('adapterJoltages')
debugPrint(adapterJoltages)
adapterJoltages.sort()
adapterJoltages.insert(0,0)
lastNum = adapterJoltages[-1]
debugPrint('lastNum' + str(lastNum))
adapterJoltages.append(lastNum+3)
debugPrint('adapterJoltages')
debugPrint(adapterJoltages)
countOfOnes = 0
countOfThrees = 0
for adapterOffset in range(0,len(adapterJoltages)-1):
	if (adapterJoltages[adapterOffset+1] - adapterJoltages[adapterOffset]) == 1:
		debugPrint('Diff of 1 from'+str(adapterJoltages[adapterOffset])+'to'+str(adapterJoltages[adapterOffset+1]))
		countOfOnes += 1
	if (adapterJoltages[adapterOffset+1] - adapterJoltages[adapterOffset]) == 3:
		debugPrint('Diff of 3 from'+str(adapterJoltages[adapterOffset])+'to'+str(adapterJoltages[adapterOffset+1]))
		countOfThrees += 1
debugPrint('length of list'+str(len(adapterJoltages)))
debugPrint('countOfOnes'+str(countOfOnes))
debugPrint('countOfThrees'+str(countOfThrees))
debugPrint('product '+str(countOfOnes*countOfThrees))

# pt 2

listOfLists = []
theList = []
theList.append(adapterJoltages[0])
for adapterOffset in range(0,len(adapterJoltages)-1):
	if adapterJoltages[adapterOffset] == adapterJoltages[adapterOffset+1] -1:
		theList.append(adapterJoltages[adapterOffset+1])
	else:
		listOfLists.append(theList)
		theList = []
		theList.append(adapterJoltages[adapterOffset+1])
DEBUG_PRINT = True
listOfLists.append(theList)
debugPrint('theList')
debugPrint(listOfLists)
DEBUG_PRINT = False
debugPrint('number of sets of numbers')
debugPrint(len(listOfLists))
accumProduct = 1
for runList in listOfLists:
	accumProduct *= countLegalPerms(runList)
print('accumProduct: '+str(accumProduct))

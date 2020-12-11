# D10P1.py
# 2020 Advent of Code
# Day 10
# Part 2

import itertools

DEBUG_PRINT = True
#DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)
		
def isRowLegal(row,check):
	print('isRowLegal: check ends',check,end=' ')
	if row[0] != check[0]:
		print('bad first digit')
		return False
	if row[-1] != check[-1]:
		print('bad last digit')
		return False
	print('end are OK')
	return True

def reduceRow(inRow):
	print('reduceRow in',inRow)
	outRow = []
	outRow.append(inRow[0])
	for digitOffset in range(1,len(inRow)-1):
		if inRow[digitOffset-1] < inRow[digitOffset]:
			outRow.append(inRow[digitOffset])
	outRow.append(inRow[-1])
	print('reduceRow out',outRow)
	return outRow
	
def makeListOfAllCombos(inList):
	runListPerms = list(itertools.permutations(inList))
	print('runListPerms',runListPerms)
	newPermList = []
	for permVal in runListPerms:
		newPermList.append(list(permVal))
	print('newPermList',newPermList)
	for listLen in range(len(inList)-1,1,-1):
		print('listLen',listLen)
		comboList = list(itertools.combinations(inList,listLen))
		print('comboList',comboList)
		for row in comboList:
			newPermList.append(list(row))
	print('newPermList',newPermList)
	return newPermList

def countLegalPerms(inRunList):
	runList = list(inRunList)
	print('runList',runList)
	runListPerms = makeListOfAllCombos(runList)
	legalLists = []
	for checkRow in runListPerms:
		row = list(checkRow)
		print('\nchecking combination',list(row))
		passCheck = True
		if isRowLegal(list(runList),row):
			newRow = reduceRow(row)
			if newRow != []:
				if newRow not in legalLists:
					print('adding newRow',newRow)
					legalLists.append(newRow)
			#assert False,'st'
		else:
			print('fails check for legal',row)
	print('legalLists',legalLists)
	print('count of legalLists',len(legalLists))

startList = [0, 1, 2, 3, 4]
countOfPerms = countLegalPerms(startList)

assert False,'test stop'

""" )
2020 D19 P2
268 is too low
404 is too high
Rule 8 produces 5 versions
Rule 11 produces 4 versions

8: 42
11: 42 31
208

8: 42 42
11: 42 31
30

8: 42 42 42
11: 42 31
21

8: 42 42 42 42
11: 42 31
16

8: 42 42 42 42 42
11: 42 31
4

8: 42 42 42 42 42 42
11: 42 31
0

8: 42
11: 42 42 31 31
16

8: 42
11: 42 42 42 31 31 31
3

8: 42
11: 42 42 42 42 31 31 31 31
1

8: 42
11: 42 42 42 42 42 31 31 31 31 31
0

8: 42 42
11: 42 42 42 42 31 31 31 31
1
"""

import re

# DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileOfStringsToList(inFileName):
	global DEBUG_PRINT		# need to put in each function
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	debugPrint('(readFileOfStringsToList): inList - ' + str(inList))
	return inList

def formatInputList(inList):
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	global testStrings
	DEBUG_PRINT = False
	# Input = ['0: 4 1 5', '1: 2 3 | 3 2', '3: 4 5 | 5 4', 
	# Output = 
	state = 'inRules'
	for line in inList:
		if line == '':
			state = 'inTestData'
		elif state == 'inRules':
			line = line.replace(' ', ',')
			line = line.replace(':', '')
			line = line.replace('"', '')
			sp = line.split(',')
			debugPrint('(formatInputList) : rule=' + str(sp[0]) + ' : ' + str(sp[1:]))
			newRule = []
			newLine = []
			if (len(sp) == 2):
				if 'a' <= sp[1] <= 'z':
					solvedDict[int(sp[0])] = [sp[1]]
				else:
					unsolvedDict[int(sp[0])] = [[int(sp[1])]]
			else:
				off = 1
				while off < len(sp):
					if sp[off] == '|':
						newRule.append(newLine)
						newLine = []
					else:
						newLine.append(int(sp[off]))
					off += 1
				newRule.append(newLine)
				unsolvedDict[int(sp[0])] = newRule
				debugPrint('(formatInputList) : newRule ' + sp[0] + ' ' + str(newRule))
		elif state == 'inTestData':
			testStrings.append(line)
		else:
			print('(formatInputList) : wtf-1')
			assert False,'(formatInputList) : wtf-1'
	# assert False,'formatInputList) : stopped'
	return

def checkAllValsForSolved(checkRule):
	# unsolvedDict = {0: [[4, 1]], 1: [[2, 3], [3, 2]], 3: [[4, 5], [5, 4]], 2: [[4, 4], [5, 5]]}
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	debugPrint('(checkAllValsForSolved) : checking rule' + str(checkRule))
	varsInRule = []
	for level in checkRule:
		for item in level:
			if item not in varsInRule:
				varsInRule.append(item)
	debugPrint('(checkAllValsForSolved) : varsInRule' + str(varsInRule))
	for val in varsInRule:
		if val not in solvedDict:
			debugPrint('(checkAllValsForSolved) : val' + str(val) + 'not in solved')
			return False
	return True

def findNextSolvableRule():
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	for rule in unsolvedDict:
		debugPrint('(findNextSolvableRule) : rule' + str(rule))
		if checkAllValsForSolved(unsolvedDict[rule]):
			 return rule
	print('\n(findNextSolvableRule) : unsolvable rule = ' + str(rule))
	print('(findNextSolvableRule) : solvedDict' + str(solvedDict))
	print('(findNextSolvableRule) : unsolvedDict' + str(unsolvedDict))
	return -1
		
def backFitSolved(rule):
	"""
	rule is a rule that can be solved
	Convert into regular expression
	"""
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	debugPrint('\n(backFitSolved) : unsolvedDict[rule=' + str(rule) + '] = ' + str(unsolvedDict[rule]))
	lineList = []
	lineStr = ''
	orLevels = len(unsolvedDict[rule])
	for orLevel in unsolvedDict[rule]:
		debugPrint('(backFitSolved) : current orLevel=' + str(orLevel))
		lineStr += '('
		for andLevel in orLevel:
			debugPrint('(backFitSolved) : solvedDict[andLevel=' + str(andLevel) + '] ' + str(solvedDict[andLevel]))
			for distVal in solvedDict[andLevel]:
				lineStr += '(' + distVal + ')'
		lineStr += ')'
		orLevels -= 1
		if orLevels > 0:
			lineStr += '|'
		
	debugPrint('(backFitSolved) : lineStr=' + lineStr)
	lineList.append(lineStr)
	debugPrint('(backFitSolved) : lineList ' + str(lineList))
	solvedDict[rule] = lineList
	debugPrint('(backFitSolved) : solvedDict[rule=' + str(rule) + '] = ' + str(solvedDict[rule]))
	unsolvedDict.pop(rule)

# Program start
inList = readFileOfStringsToList('inputPt2b.txt')
# inList = readFileOfStringsToList('inputPt2.txt')
# inList = readFileOfStringsToList('input.txt')
# print(inList)
solvedDict = {}
unsolvedDict = {}
testStrings = []

formatInputList(inList)

solvedGoal = False
while not solvedGoal:
	solvableRule = findNextSolvableRule()
	if solvableRule == 0:
		solvedGoal = True
		backFitSolved(solvableRule)
	elif solvableRule == -1:
		solvedGoal = True
	elif solvableRule != -1:
		backFitSolved(solvableRule)
# assert False,'stopped here'

debugPrint('solvedDict' + str(solvedDict))
debugPrint('unsolvedDict' + str(unsolvedDict))

# unsolvedDict{
	# 0: [[8, 11]], 
	# 8: [[42], [42, 8]], 
	# 11: [[42, 31], [42, 11, 31]]
	# }
if len(unsolvedDict) > 0:
	savedRules = {}
	for rule in unsolvedDict:
		savedRules[rule] = unsolvedDict[rule]
	print('savedRules',savedRules)
	print('')
	assert False,'stop'
else:
	regexVal = solvedDict[0][0]
	DEBUG_PRINT = True
	debugPrint('regexVal( rule 0) ' + str(regexVal))

	count = 0
	for line in testStrings:
		matchVal = bool(re.fullmatch(regexVal,line))
		if matchVal:
			count += 1
		# debugPrint('line ' + str(line) + ' ' + str(matchVal))
		
	print('count',count)

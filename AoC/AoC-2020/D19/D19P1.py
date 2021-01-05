""" )
2020 D19 P1
"""

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
			debugPrint('(formatInputList) : rule' + str(sp[0]) + ' : ' + str(sp[1:]))
			newRule = []
			newLine = []
			if len(sp) == 2:
				solvedDict[int(sp[0])] = [sp[1]]
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
		elif state == 'inTestData':
			testStrings.append(line)
		else:
			print('wtf-1')
	return

def checkAllValsForSolved(checkRule):
	# unsolvedDict = {0: [[4, 1]], 1: [[2, 3], [3, 2]], 3: [[4, 5], [5, 4]], 2: [[4, 4], [5, 5]]}
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	# print('checking rule',checkRule)
	varsInRule = []
	for level in checkRule:
		for item in level:
			if item not in varsInRule:
				varsInRule.append(item)
	# print('varsInRule',varsInRule)
	for val in varsInRule:
		if val not in solvedDict:
			# print('val',val,'not in solved')
			return False
	return True

def findNextSolvableRule():
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	for rule in unsolvedDict:
		# print('rule',rule)
		if checkAllValsForSolved(unsolvedDict[rule]):
			 return rule
	assert False,'wtf'
		
def backFitSolved(rule):
	global DEBUG_PRINT		# need to put in each function
	global unsolvedDict
	global solvedDict
	debugPrint('\n(backFitSolved) : unsolvedDict[rule=' + str(rule) + '] = ' + str(unsolvedDict[rule]))
	lineList = []
	for orLevel in unsolvedDict[rule]:
		debugPrint('(backFitSolved) : current orLevel=' + str(orLevel))
		lineStr = ''
		for andLevel in orLevel:
			debugPrint('(backFitSolved) : solvedDict[andLevel=' + str(andLevel) + '] ' + str(solvedDict[andLevel]))
			for distVal in solvedDict[andLevel]:
				lineStr += distVal
		lineList.append(lineStr)
		debugPrint('(backFitSolved) : lineStr=' + lineStr)
	debugPrint('(backFitSolved) : lineList ' + str(lineList))
	solvedDict[rule] = lineList
	debugPrint('(backFitSolved) : solvedDict[rule=' + str(rule) + '] = ' + str(solvedDict[rule]))
	unsolvedDict.pop(rule)
	

# Program start
inList = readFileOfStringsToList('input1.txt')
# print(inList)
solvedDict = {}
unsolvedDict = {}
testStrings = []

formatInputList(inList)
DEBUG_PRINT = True
print('solvedDict',solvedDict)
print('unsolvedDict',unsolvedDict)

solvedGoal = False
while not solvedGoal:
	solvableRule = findNextSolvableRule()
	if solvableRule == 0:
		solvedGoal = True
	backFitSolved(solvableRule)
	# break

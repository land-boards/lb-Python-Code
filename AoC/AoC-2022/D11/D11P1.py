""" 
D11P1
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

"""

# fileName = 'input2.txt'
fileName = 'input.txt'
# fileName = 'input1.txt'

def calcWorryLevel(worryLevel,op,opVal):
	# print('calcWorryLevel: worryLevel,op,opVal',worryLevel,op,opVal)
	if op == '*':
		if opVal == 'old':
			worry = worryLevel * worryLevel
		else:
			worry = worryLevel * int(opVal)
	elif op == '+':
		worry = worryLevel + int(opVal)
	else:
		assert False,'calcWorryLevel: stop'
	return worry

def addToMonkey(throwToMonkey,divByVal):
	line = monkeyDict[throwToMonkey][0].append(divByVal)
	
parseState = 'getMonkeyNum'
inList=[]
monkeyDict = {}
debugParse = False
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		if debugParse:
			print('inLine',inLine)
		
		if parseState == 'getMonkeyNum':
			monkeyNumStr = inLine[7:-1]
			monkeyNum = int(monkeyNumStr)
			if debugParse:
				print('main: monkeyNum',monkeyNum)
			parseState = 'getStartingItems'
		elif parseState == 'getStartingItems':
			startItems=inLine[18:].split(', ')
			startItemsList = []
			for item in startItems:
				startItemsList.append(int(item))
			if debugParse:
				print('main:startItemsList',startItemsList)
			parseState = 'getOperation'
		elif parseState == 'getOperation':
			opLine = startItems=inLine.split(' ')
			op = opLine[6]
			opVal = opLine[7]
			if debugParse:
				print('main: op,opVal',op,opVal)
			parseState = 'getTestLine'
		elif parseState == 'getTestLine':
			testLine = inLine.split(' ')
			divisivableBy = int(testLine[5])
			if debugParse:
				print('main: divisivableBy',divisivableBy)
			parseState = 'getTrueLine'
		elif parseState == 'getTrueLine':
			ifTrueNextMonkeyLine = inLine.split(' ')
			ifTrueNextMonkey = int(ifTrueNextMonkeyLine[9])
			if debugParse:
				print('main: ifTrueNextMonkey',ifTrueNextMonkey)
			parseState = 'getFalseLine'
		elif parseState == 'getFalseLine':
			ifFalseNextMonkeyLine = inLine.split(' ')
			ifFalseNextMonkey = int(ifFalseNextMonkeyLine[9])
			if debugParse:
				print('main: ifFalseNextMonkey',ifFalseNextMonkey)
				print('main: Monkey=',monkeyNum,', starts with=',startItemsList,', op=',op,', opVal=',opVal,', div by=',divisivableBy,', ifTrueNextMonkey=',ifTrueNextMonkey,', ifFalseNextMonkey=',ifFalseNextMonkey)
			monkeyDecisionTreeList=[]
			monkeyDecisionTreeList.append(startItemsList)
			monkeyDecisionTreeList.append(op)
			monkeyDecisionTreeList.append(opVal)
			monkeyDecisionTreeList.append(divisivableBy)
			monkeyDecisionTreeList.append(ifTrueNextMonkey)
			monkeyDecisionTreeList.append(ifFalseNextMonkey)
			monkeyDict[monkeyNum]=monkeyDecisionTreeList
			parseState = 'getBlankLine'
		elif parseState == 'getBlankLine':
			if debugParse:
				print('main: getBlankLine\n')
			parseState = 'getMonkeyNum'
debugMoves = False
numberOfMonkeys = len(monkeyDict)
print('main: monkeyDict length=',numberOfMonkeys,'monkeys')
print('')
monkeyMoves = []
for monkey in range(numberOfMonkeys):
	monkeyMoves.append(0)
print('monkeyMoves',monkeyMoves)
print('')
print('Before moves')
for monkey in range(numberOfMonkeys):
	print(monkey,monkeyDict[monkey][0])
print('')
for roundNum in range(20):
	for monkey in range(numberOfMonkeys):
	# for monkey in range(1):
		monkeyMoves[monkey] += len(monkeyDict[monkey][0])
		if debugMoves:
			print(monkey,monkeyDict[monkey])
		worryLevelList = monkeyDict[monkey][0]
		op = monkeyDict[monkey][1]
		opVal = monkeyDict[monkey][2]
		if debugMoves:
			print('worryLevelList',worryLevelList)
		while worryLevelList != []:
	#	for worryLevel in worryLevelList:
			worryLevel = worryLevelList.pop(0)
			if debugMoves:
				print('handle worryLevel',worryLevel)
			newWorryLevel = calcWorryLevel(worryLevel,op,opVal)
			if debugMoves:
				print('newWorryLevel',newWorryLevel)
			div3Val = int(newWorryLevel/3)
			if debugMoves:
				print('div3Val',div3Val)
			divByVal = monkeyDict[monkey][3]
			if div3Val%divByVal == 0:
				mathResult = True
				throwToMonkey = monkeyDict[monkey][4]
				if debugMoves:
					print('True, throw to monkey',throwToMonkey)
			else:
				mathResult = False
				throwToMonkey = monkeyDict[monkey][5]
				if debugMoves:
					print('False, throw to monkey',throwToMonkey)
			monkeyDict[throwToMonkey][0].append(div3Val)
			if debugMoves:
				print('throwToMonkey,monkeyDict[throwToMonkey]',throwToMonkey,monkeyDict[throwToMonkey][0])
	print('After round',roundNum+1)
	for monkey in range(numberOfMonkeys):
		print(monkey,monkeyDict[monkey][0])
	print('')

print('Final list')
for monkey in range(numberOfMonkeys):
# for monkey in range(1):
	print(monkey,monkeyDict[monkey][0])
sortedMonkeyMoves = sorted(monkeyMoves)
print('sortedMonkeyMoves',sortedMonkeyMoves)
print('result',sortedMonkeyMoves[-1]*sortedMonkeyMoves[-2])


""" 
D11P1
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
* 2567194800 too low
* 2268469980 too low
"""
import time
import math

# At start
startTime = time.time()

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
print('monkeyDict',monkeyDict)
modulus = 1
for num in range(len(monkeyDict)):
	print('monkeyDict[num][2]',monkeyDict[num][3])
	modulus *= int(monkeyDict[num][3])
print('modulus2',modulus)
# assert False

for roundNum in range(10000):
# for roundNum in range(20):
	# if roundNum%100 == 0:
		# endTime = time.time()
		# print('time',endTime-startTime,end=', Round=')
		# print(roundNum)
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
			worryLevel = worryLevelList.pop(0)
			if debugMoves:
				print('handle worryLevel',worryLevel)
			newWorryLevel = calcWorryLevel(worryLevel,op,opVal)
			if debugMoves:
				print('newWorryLevel',newWorryLevel)
			div3Val = int(newWorryLevel%modulus)
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
	if debugMoves:
		print('After round',roundNum+1)
		for monkey in range(numberOfMonkeys):
			print(monkey,monkeyDict[monkey][0])
	# print('monkeyDict',monkeyDict)
	if debugMoves:
		endTime = time.time()
		print(roundNum+1,end=',')
		print(int(endTime-startTime),end=',')
		for move in range(len(monkeyMoves)):
			print(monkeyMoves[move],',',end='')
		print()

print('Final list',monkeyMoves)

sortedMonkeyMoves = sorted(monkeyMoves)
print('sortedMonkeyMoves',sortedMonkeyMoves)
print('result',sortedMonkeyMoves[-1]*sortedMonkeyMoves[-2])
endTime = time.time()
print(endTime-startTime,'secs')

#65535 is too hogh
def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)
	return inList

operands = ['OR','NOT','AND','LSHIFT','RSHIFT','->']

def makeSymbolTable(functionsList):
	symbols = []
	for line in functionsList:
		#print(line)
		for val in line:
			if (val not in operands) and (val not in symbols) and (not val.isnumeric()):
				symbols.append(val)
	symbols.sort()
	return symbols
	
def loadInitialVals(variableTable,functionsList):
	"""
	"""
	for row in functionsList:
		if (row[0].isnumeric()) and (row[1] == '->'):
			print("(loadInitialVals): row",row)
			for val in variableTable:
				if row[2] == val[0]:
					val[1] = 'solved'
					val[2] = int(row[0])
	return functionsList

def fillFunctionsList(inList):
	functionsList = []
	for row in inList:
		line = row.split(' ')
		functionsList.append(line)
	print("fillFunctionsList: Functions list:",functionsList)
	return functionsList

def solveWhatCanBeSolved():
	for function in functionsList:
		# print("(solveWhatCanBeSolved): function",function)
		opType = classifyOp(function)
		if opType == 'shiftOp':
			# ['x', 'LSHIFT', '2', '->', 'f']
			# ['hz', 'RSHIFT', '1', '->', 'is']
			if checkVar(function[0]) == 'solved':
				varVal = int(getVarVal(function[0]))
				if function[1] == 'LSHIFT':
					resultVal = varVal << int(function[2])
				elif function[1] == 'RSHIFT':
					resultVal = varVal >> int(function[2])
				else:
					assert False,"Unexpected ShiftOp"
				if resultVal < 0:
					resultVal = 65536 - resultVal
				resultVal &= 0xffff
				outVarVal(function[4],str(resultVal))
		elif opType == 'logicalOp':
			# ['x', 'AND', 'y', '->', 'd']
			# ['he', 'OR', 'hp', '->', 'hq']
			# ['1', 'AND', 'cx', '->', 'cy']
			bothResolved = True
			if function[0].isnumeric():
				varVal1 = int(function[0])
			elif checkVar(function[0]) == 'solved':
				varVal1 = int(getVarVal(function[0]))
			else:
				bothResolved = False
			if function[2].isnumeric():
				varVal2 = int(function[2])
			elif checkVar(function[2]) == 'solved':
				varVal2 = int(getVarVal(function[2]))
			else:
				bothResolved = False
			if bothResolved:
				if function[1] == 'AND':
					resultVal = varVal1 & varVal2
				elif function[1] == 'OR':
					resultVal = varVal1 | varVal2
				else:
					assert False,"Unexpected logicalOp"
				if resultVal < 0:
					resultVal = 65536 - resultVal
				resultVal &= 0xffff
				outVarVal(function[4],str(resultVal))
		elif opType == 'unaryOp':
			# ['NOT', 'y', '->', 'i']
			if checkVar(function[1]) == 'solved':
				varVal = int(getVarVal(function[1]))
				if function[0] == 'NOT':
					resultVal = ~varVal
				else:
					assert False,"Unexpected unaryOp"
				if resultVal < 0:
					resultVal = 65536 - resultVal
				resultVal &= 0xffff
				outVarVal(function[3],str(resultVal))
		elif opType == 'moveOp':
			# ['lx', '->', 'a']
			if checkVar(function[0]) == 'solved':
				resultVal = int(getVarVal(function[0]))
				resultVal &= 0xffff
				outVarVal(function[2],str(resultVal))
		elif opType == 'immediateOp':
			pass
		else:
			print("Function",function)
			assert False,"Unclassified op"
			
def outVarVal(varStr,val):
	for varTableLine in variableTable:
		if varTableLine[0] == varStr:
			varTableLine[1] = 'solved'
			varTableLine[2] = val
			return
	assert False,"Failed set"

def getVarVal(varStr):
	for var in variableTable:
		if var[0] == varStr:
			return var[2]
	assert False,"Failed get"

def checkVar(varStr):
	for var in variableTable:
		if var[0] == varStr:
			return var[1]
	print("Failed check",varStr)
	assert False,"Failed check"

def checkAllSolved():
	for variableSet in variableTable:
		if variableSet[1] == 'unsolved':
			return False
	return True
	
def countSolved():
	solvedCount = 0
	for variableSet in variableTable:
		if variableSet[1] == 'solved':
			solvedCount += 1
	return solvedCount

def classifyOp(line):
	""" 
	"""
	if (line[1] == 'LSHIFT') or (line[1] == 'RSHIFT'):
		return 'shiftOp'
	elif (line[1] == 'AND') or (line[1] == 'OR'): 
		return 'logicalOp'
	elif line[0] == 'NOT':
		return 'unaryOp'
	elif (len(line) == 3) and (line[1] == '->') and (not line[0].isnumeric()):
		return 'moveOp'
	elif (len(line) == 3) and (line[1] == '->') and (line[0].isnumeric()):
		return 'immediateOp'
	else:
		print("line",line)
		assert False,"classifyOp - Unclassified Op"
	return

# The main code

inList = readFileToList()
# inList = ['123 -> x','456 -> y','x AND y -> d','x OR y -> e','x LSHIFT 2 -> f','y RSHIFT 2 -> g','NOT x -> h','NOT y -> i']
functionsList = fillFunctionsList(inList)
symbolTable = makeSymbolTable(functionsList)
#print("Symbol Table",symbolTable)
variableTable = []
for row in symbolTable:
	variableLine = []
	variableLine.append(row)
	variableLine.append('unsolved')
	variableLine.append('-123456789')
	variableTable.append(variableLine)
	
#print("variableTable",variableTable)

functionsList = loadInitialVals(variableTable,functionsList)

# print('variableTable after initialization: ',variableTable)
# print('functionsList')
# for row in functionsList:
	# print(row)
# print('variableTable after first pass: ',variableTable)

allSolved = False
lastSolvedCount = 0
while not allSolved:
	solveWhatCanBeSolved()
	#print('variableTable after middle pass: ',variableTable)
	allSolved = checkAllSolved()
	solveCount = countSolved()
	# print("solved Count",solveCount)
	if lastSolvedCount != solveCount:
		lastSolvedCount = solveCount
	else:
		if not allSolved:
			print("ended with unsolveds")
			assert False,"Unsolved"
		allSolved = True
		
print('variableTable after last pass: ')
for var in variableTable:
	varStr = var[0]
	varVal = int(var[2])
	if varVal == '-123456789':
		varVal = 'Uninit'
	elif varVal < 0:
		varVal = 65536 - varVal
	print(varStr,varVal)
	
print("\na val is",getVarVal('a'))

def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)
	return inList

operands = ['OR','NOT','AND','LSHIFT','RSHIFT','->']

def makeSymbolTable(functionList):
	symbols = []
	for line in functionList:
		#print(line)
		for val in line:
			if (val not in operands) and (val not in symbols) and (not val.isnumeric()):
				symbols.append(val)
	symbols.sort()
	return symbols
	
def classifyOp(line):
	""" 
	"""
	if (line[1] == 'LSHIFT') or (line[1] == 'RSHIFT'):
		return 'shiftOp'
	elif (line[1] == 'AND') or (line[1] == 'OR'): 
		return 'logicalOp'
	elif line[0] == 'NOT':
		return 'unaryOp'
	return

def loadInitialVals(variableTable,functionsList):
	"""
	"""
	for row in functionsList:
		if row[0].isnumeric():
			print("row",row)
			for val in variableTable:
				if row[2] == val[0]:
					val[1] = 'solved'
					val[2] = int(row[0])
	return functionsList

def fillFunctionsList(inList):
	functionList = []
	for row in inList:
		line = row.split(' ')
		functionList.append(line)
	print(functionList)
	return functionList

inList = readFileToList()
functionsList = fillFunctionsList(inList)
symbolTable = makeSymbolTable(functionsList)
#print("Symbol Table",symbolTable)
variableTable = []
for row in symbolTable:
	variableLine = []
	variableLine.append(row)
	variableLine.append('unsolved')
	variableLine.append(-123456789)
	variableTable.append(variableLine)
	
#print("variableTable",variableTable)

functionsList = loadInitialVals(variableTable,functionsList)

print('variableTable',variableTable)
print('functionsList')
for row in functionsList:
	print(row)

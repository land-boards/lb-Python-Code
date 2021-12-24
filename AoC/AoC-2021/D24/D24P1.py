# D24P1.py
# 2021 Advent of Code
# Day 24
# Part 1

def readFileOfStringsToListOfLists(fileName):
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inLine= inLine.split(' ')
			inList.append(inLine)
	return inList

def inpOp(opLine):
	global wVarStr
	global inNum
	global inOffset
	# print("Input to reg",opLine[0])
	valToAppend = inNum[inOffset]
	wVarStr += valToAppend
	inOffset += 1
	print("inpOp: Model num accum",wVarStr)

def isReg(val):
	if val == 'w':
		return True
	elif val == 'x':
		return True
	elif val == 'y':
		return True
	elif val == 'z':
		return True
	return False

def complementDigit(digitVal):
	complementDigitVal = ''
	if digitVal == '0':
		return '9'
	elif digitVal == '1':
		return '8'
	elif digitVal == '2':
		return '7'
	elif digitVal == '3':
		return '6'
	elif digitVal == '4':
		return '5'
	elif digitVal == '5':
		return '4'
	elif digitVal == '6':
		return '3'
	elif digitVal == '7':
		return '2'
	elif digitVal == '8':
		return '1'
	elif digitVal == '9':
		return '0'
	assert False,"complementDigit: bad digit"

def complementNumber(val):
	# Complement a negative BCD number
	# -1 = 99999999999998
	gotSign = False
	retVal = ''
	for digitToCheckOffset in range(len(val)-1,-1,-1):
		print("complementNumber: val[digitToCheckOffset]",val[digitToCheckOffset])
		if val[digitToCheckOffset] == '-':
			gotSign = True
		elif gotSign:
			retVal = '9' + retVal
		else:
			retVal = complementDigit(val[digitToCheckOffset]) + retVal
	while len(retVal) < 14:
		retVal = '9' + retVal
	print("complementNumber: retVal",retVal)
	# assert False,'comp'
	return retVal
	
def extendBits(valIn):
	print("extendBits: valIn",valIn)
	newStr = valIn
	if valIn[0] == '-':
		# assert False,"extendBits: TBD Handle neg number"
		newStr = complementNumber(valIn)
	else:
		while len(newStr) < 14:
			newStr = '0' + newStr
	print("extendBits: newStr",newStr)
	return newStr

def addDigits(digA,digB,carry):
	intDigA = int(digA)
	intDigB = int(digB)
	sum = intDigA + intDigB
	# print("addDigits: sum,carry",str(sum),str(carry))
	return str(sum),str(carry)

def addAsStringVals(valA,valB):
	print("addAsStringVals: adding as strings",valA,valB)
	result = ''
	carry = '0'
	if len(valB) < 14:
		valB = extendBits(valB)
	print("addAsStringVals: valB",valB)
	for digit in range(len(valB)-1,-1,-1):
		sum,carry = addDigits(valA[digit],valB[digit],carry)
		result = sum + result 
	print("addAsStringVals: result",result)
	return result

def valReg(reg):
	if reg == 'w':
		return wVarStr
	elif reg == 'x':
		return xVarStr
	elif reg == 'y':
		return yVarStr
	elif reg == 'z':
		return zVarStr
	assert False,"valReg error"

def parseMathOps(opLine):
	global xVar
	global yVar
	global zVar
	global wVarStr
	regA = opLine[0]
	aVal = valReg(regA)
	regB = opLine[1]
	print("parseMathOps: add",regA,regB)
	if isReg(regB):		# B is a register
		retStr = (valReg(regA),valReg(regB))
	else:				# B is a literal
		retStr = (valReg(regA),regB)
	return retStr

def addOp(opLine):
	global xVar
	global yVar
	global zVar
	global wVarStr
	regA,regB = parseMathOps(opLine)
	print("\naddOp: opLine",opLine)
	val = addAsStringVals(regA,regB)
	print("addOp: val",val)
	return 0

def mulOp(opLine):
	return 0

def divOp(opLine):
	return 0

def modOp(opLine):
	return 0

def eqlOp(opLine):
	return 0

def executeLine(line):
	# print("line",line)
	if line[0] == 'inp':
		inpOp(line[1])
	elif line[0] == 'add':
		addOp(line[1:])
	elif line[0] == 'mul':
		mulOp(line[1:])
	elif line[0] == 'div':
		divOp(line[1:])
	elif line[0] == 'mod':
		modOp(line[1:])
	elif line[0] == 'eql':
		eqlOp(line[1:])
	else:
		assert False,"bad opcode"

inList = readFileOfStringsToListOfLists('input.txt')
# print(inList)
wVarStr = ''
xVarStr = '00000000000000'
yVarStr = '00000000000000'
zVarStr = '00000000000000'
inNum = '13579246899999'
inOffset = 0
for line in inList:
	executeLine(line)
print("wVarStr",wVarStr,end=' ')
print("xVarStr",xVarStr,end=' ')
print("yVarStr",yVarStr,end=' ')
print("zVarStr",zVarStr,end=' ')

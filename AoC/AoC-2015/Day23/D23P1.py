# D23P1

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList
	
DEBUG_PRINT = True
#DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def doInstr(instruction):
	global regA
	global regB
	global pc
	#print(instruction)
	if instruction[0] == 'hlf':
		if instruction[1] == 'a':
			regA = int(regA/2)
		else:
			regB = int(regB/2)
		pc += 1
	elif instruction[0] == 'tpl':
		if instruction[1] == 'a':
			regA *= 3
		else:
			regB *= 3
		pc += 1
	elif instruction[0] == 'inc':
		if instruction[1] == 'a':
			regA += 1
		else:
			regB += 1
		pc += 1
	elif instruction[0] == 'jmp':
		pc += int(instruction[1])
	elif instruction[0] == 'jie':
		if instruction[1] == 'a':
			if ((regA & 1) == 0):
				pc += int(instruction[2])
			else:
				pc += 1
		else:
			if ((regB & 1) == 0):
				pc += int(instruction[2])
			else:
				pc += 1
	elif instruction[0] == 'jio':
		if instruction[1] == 'a':
			if regA == 1:
				pc += int(instruction[2])
			else:
				pc += 1
		else:
			if regB == 1:
				pc += int(instruction[2])
			else:
				pc += 1
	else:
		assert False,'weird stuff'

inList = readFileToListOfStrings()
print(inList)
program = []
for row in inList:
	newRow = []
	newLine = row.replace(',','')
	newLine2 = newLine.split(' ')
	print('newLine2',newLine2)
	program.append(newLine2)
print(program)

pc = 0
regA = 0
regB = 0
endPC = len(program)
debugPrint('length='+str(endPC))

while pc < endPC:
	print(pc,' ',program[pc],'a',regA,'b',regB,end='')
	doInstr(program[pc])
	print(', new pc',pc)
print('regB',regB)

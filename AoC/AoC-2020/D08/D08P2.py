# 2020 D08P1

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList
	
DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def doInstr(instruction):
	global regA
	global pc
	#debugPrint(instruction)
	if instruction[0] == 'acc':
		regA += instruction[1]
		pc += 1
	elif instruction[0] == 'jmp':
		pc += int(instruction[1])
	elif instruction[0] == 'nop':
		pc += 1
	else:
		assert False,'bsd instruction'

DEBUG_PRINT = True
DEBUG_PRINT = False
inList = readFileToListOfStrings()
debugPrint(inList)
program = []
for row in inList:
	newRow = []
	newLine = row.replace(',','')
	newLine2 = newLine.split(' ')
	if DEBUG_PRINT:
		print('newLine2' + newLine2)
	opcode = newLine2[0]
	val = int(newLine2[1])
	program.append([opcode,val])
debugPrint(program)

pc = 0
regA = 0
endPC = len(program)
debugPrint('length='+str(endPC))
#assert False,'huh'

loopTerminalCount = 100000
fixLine = 0

loopCount = 0
for line in program:
	newProgram.append(line)
while loopCount < loopTerminalCount:
	while pc < endPC:
		instrCounterList[pc] += 1
		#print(pc,' ',program[pc],'a',regA,end='')
		doInstr(newProgram[pc])
		#print(', new pc',pc)
		#print('regA',regA)
	#	assert False,'huh'
		loopCount += 1
	break
print('regA',regA)

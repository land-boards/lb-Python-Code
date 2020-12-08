# 2020 D08P1

DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings():
	inList = []
	with open('input2.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList
	
def doInstr(instruction):
	global regA
	global pc
	debugPrint(instruction)
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
		print('newLine2' + newLine2[0] + newLine2[1])
	opcode = newLine2[0]
	val = int(newLine2[1])
	program.append([opcode,val])
debugPrint(program)

pc = 0
regA = 0
endPC = len(program)
debugPrint('length='+str(endPC))
#assert False,'huh'

lineNumToFix = 0

# Make a fresh copy of the program
newProgram = []
for line in program:
	newProgram.append(line)
	#print(line)
loopCount = 0
loopTerminalCount = 100000
reachedEndOfCode = 'notYet'
while reachedEndOfCode == 'notYet':
	while pc < endPC:
		#print(pc,' ',program[pc],'a',regA,end='')
		doInstr(newProgram[pc])
		#print(', new pc',pc,end='')
		#print('regA',regA)
		#assert False,'huh'
		loopCount += 1
		#debugPrint('loopCount '+ str(loopCount) + ' out of ' + str(loopTerminalCount))
		if loopCount >= loopTerminalCount:
			reachedEndOfCode = 'reachedLoopTC'
			break
	reachedEndOfCode = 'reachedEndOfCode'
print('reason for ending',reachedEndOfCode)
print('regA',regA)

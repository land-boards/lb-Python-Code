# 2020 D08P1

import copy

#DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
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
		assert False,'bad instruction'

#DEBUG_PRINT = True
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
#print('initial code',program)

#DEBUG_PRINT = True
endPC = len(program)
debugPrint('length='+str(endPC))
#assert False,'huh'

lineNumToFix = 0

reachedEndOfCode = 'notYet'
while reachedEndOfCode != 'reachedEndOfCode':
	# Make a deep copy of the program
	newProgram = copy.deepcopy(program)
	#print('loaded new program',newProgram)
	for lineNum in range(lineNumToFix,endPC):
		if newProgram[lineNumToFix][0] == 'nop':
			newProgram[lineNumToFix][0] = 'jmp'
			#print('patched',lineNumToFix,'nop>jmp')
			lineNumToFix += 1
			break
		elif newProgram[lineNumToFix][0] == 'jmp':
			newProgram[lineNumToFix][0] = 'nop'
			#print('patched',lineNumToFix,'jmp>nop')
			lineNumToFix += 1
			break
		lineNumToFix += 1
		if lineNumToFix >= endPC:
			assert False,'got past end'
	#print(newProgram)
	pc = 0
	regA = 0
	loopCount = 0
	loopTerminalCount = 10000
	while reachedEndOfCode != 'reachedEndOfCode':
		while pc < endPC:
			#print(pc,' ',program[pc],'a',regA,end='')
			doInstr(newProgram[pc])
			#print('pc ',pc,' regA ',regA)
			#assert False,'huh'
			loopCount += 1
			#debugPrint('loopCount '+ str(loopCount) + ' out of ' + str(loopTerminalCount))
			if loopCount >= loopTerminalCount:
				reachedEndOfCode = 'reachedLoopTC'
				break
		if pc >= endPC:
			reachedEndOfCode = 'reachedEndOfCode'
			print('eoc')
		if reachedEndOfCode == 'reachedLoopTC':
			break
	#print('reason for ending ',reachedEndOfCode)
print('regA',regA)

# Pt2-AoCDay19.py
# 2018 Advent of Code
# Day 16
# Part 1
# https://adventofcode.com/2018/day/19

import time
import re
import os

"""
--- Day 19: Go With The Flow ---
With the Elves well on their way constructing the North Pole base, 
you turn your attention back to understanding the inner workings of programming the device.

You can't help but notice that the device's opcodes don't contain any flow control like jump instructions. 
The device's manual goes on to explain:

"In programs where flow control is required, the instruction pointer can be bound to a register 
so that it can be manipulated directly. 
This way, setr/seti can function as absolute jumps, addr/addi can function as relative jumps, 
and other opcodes can cause truly fascinating effects."

This mechanism is achieved through a declaration like #ip 1, 
which would modify register 1 so that accesses to it let the program indirectly access the 
instruction pointer itself. 
To compensate for this kind of binding, there are now six registers (numbered 0 through 5); 
the five not bound to the instruction pointer behave as normal. 
Otherwise, the same rules apply as the last time you worked with this device.

When the instruction pointer is bound to a register, its value is written to that register 
just before each instruction is executed, and the value of that register is written back 
to the instruction pointer immediately after each instruction finishes execution. 
Afterward, move to the next instruction by adding one to the instruction pointer, 
even if the value in the instruction pointer was just updated by an instruction. 
(Because of this, instructions must effectively set the instruction pointer to the 
instruction before the one they want executed next.)

The instruction pointer is 0 during the first instruction, 1 during the second, and so on. 
If the instruction pointer ever causes the device to attempt to load an instruction outside 
the instructions defined in the program, the program instead immediately halts. 
The instruction pointer starts at 0.

It turns out that this new information is already proving useful: 
the CPU in the device is not very powerful, and a background process is occupying most of its time. 
You dump the background process' declarations and instructions to a file (your puzzle input), 
making sure to use the names of the opcodes rather than the numbers.

For example, suppose you have the following program:

#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5

When executed, the following instructions are executed. Each line contains the value of the instruction pointer at the time the instruction started, the values of the six registers before executing the instructions (in square brackets), the instruction itself, and the values of the six registers after executing the instruction (also in square brackets).

ip=0 [0, 0, 0, 0, 0, 0] seti 5 0 1 [0, 5, 0, 0, 0, 0]
ip=1 [1, 5, 0, 0, 0, 0] seti 6 0 2 [1, 5, 6, 0, 0, 0]
ip=2 [2, 5, 6, 0, 0, 0] addi 0 1 0 [3, 5, 6, 0, 0, 0]
ip=4 [4, 5, 6, 0, 0, 0] setr 1 0 0 [5, 5, 6, 0, 0, 0]
ip=6 [6, 5, 6, 0, 0, 0] seti 9 0 5 [6, 5, 6, 0, 0, 9]
In detail, when running this program, the following events occur:

The first line (#ip 0) indicates that the instruction pointer should be bound to register 0 in this program. 
This is not an instruction, and so the value of the instruction pointer does not change during 
the processing of this line.
The instruction pointer contains 0, and so the first instruction is executed (seti 5 0 1). 
It updates register 0 to the current instruction pointer value (0), sets register 1 to 5, 
sets the instruction pointer to the value of register 0 (which has no effect, as the instruction 
did not modify register 0), and then adds one to the instruction pointer.
The instruction pointer contains 1, and so the second instruction, seti 6 0 2, is executed. 
This is very similar to the instruction before it: 6 is stored in register 2, and the instruction pointer 
is left with the value 2.
The instruction pointer is 2, which points at the instruction addi 0 1 0. 
This is like a relative jump: the value of the instruction pointer, 2, is loaded into register 0. 
Then, addi finds the result of adding the value in register 0 and the value 1, storing the result, 3, 
back in register 0. Register 0 is then copied back to the instruction pointer, 
which will cause it to end up 1 larger than it would have otherwise and skip the next instruction 
(addr 1 2 3) entirely. Finally, 1 is added to the instruction pointer.
The instruction pointer is 4, so the instruction setr 1 0 0 is run. 
This is like an absolute jump: it copies the value contained in register 1, 5, into register 0, 
which causes it to end up in the instruction pointer. The instruction pointer is then incremented, 
leaving it at 6.
The instruction pointer is 6, so the instruction seti 9 0 5 stores 9 into register 5. 
The instruction pointer is incremented, causing it to point outside the program, and so the program ends.
What value is left in register 0 when the background process halts?

===================================================================================
Notes about this problem.

The opcodes have already been translated into their mnemonic. 
Could either use the opcode directly and add a "parser" or could translate the opcode into the previous opcode numbers.
Probably easier to use the opcode directly and parse it.

"""

def printList(listToPrint):
	for row in listToPrint:
		print row

def readTextFileToList(fileName):
	"""readTextFileAndSrtToList - open file and read the content to a list
	File is sorted to produce a date/time ordered file
	:returns: the list sorted list
	"""
	textList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			textList.append(line.strip())
	#printList(textList)
	return textList
	
def parseTextFileIntoListOfNumbers(textFile):
	"""Convert the text file into a list
	
	"""
	theList = []
	listOfBefore = []
	listOfAfter = []
	opcodeList = []
	for line in textFile:
		if len(line) == 0:
			continue
		elif line[0:4] == '#ip ':
			instructionPointer = line[4]
			print 'instruction pointer',instructionPointer
			exit()
		elif line[0] == 'B':
			newLine = line[9:-1]
			newLine = newLine.replace(' ','')
			listOfBefore = newLine.split(',')
			#print 'before',
			#printList(listOfBefore)
		elif line[0] == 'A':
			newLine = line[9:-1]
			newLine = newLine.replace(' ','')
			listOfAfter = newLine.split(',')
			#print 'after',listOfAfter
			theThing = []
			theThing.extend(opcodeList)
			theThing.extend(listOfBefore)
			theThing.extend(listOfAfter)
			theNewThing = []
			for item in theThing:
				theNewThing.append(int(item))
			theList.append(theNewThing)
		else:	# opcode case
			opcodeList = line.split()
			#print 'opcode',opcodeList
	#printList(theList)
	return theList

def abbyTerminate(strToPrint):
	print 'abbyTerminate: terminating due to',
	print strToPrint
	exit()
	
#########################################################################
## The 16 instructions
## Do the operation indicated and return what the value would be for the operation
## Higher level code can determine if that matches the expected value

#######################################################################################
## Implement the instruction set in the emulator
##
## Instruction format
## Vector values
## OPCODE[0:3]...BEFORE[4:7]...After[8:11]
## OPCODE[0] = Opcodes with values from 0-15
## OPCODE[1] = Register Select/Immediate A
## OPCODE[2] = Register Select/Immediate B
## OPCODE[3] = Register Select C which register gets the result
## BEFORE[4:7] = The register values before the operation
## AFTER[8:11] = The register values after the operation

class CPU:
	"""The register set is globals to the class
	"""
	CPU_Reg0 = 0
	CPU_Reg1 = 0
	CPU_Reg2 = 0
	CPU_Reg3 = 0
	CPU_Reg4 = 0
	CPU_Reg5 = 0
	CPU_IP = 0

	def emulator(self,vector):
		"""emulator - The function that calls the ALU and returns the return value
		TBD - extend to increment the CPU Instruction Pointer.
		
		:param vector: The instruction vector fields 0-3
		:returns: the contents of the registers.
		"""
		debug_emulator = False
		if debug_emulator:
			print 'emulator:',vector
		self.doALU(vector[0:4])
		return self.getRegisterAfterValues()
	
	def initializeCPU(self):
		"""Sets the registers in the CPU to zeros.
		Used at the start of the program to ensure known values in registers.
		
		:returns: no return value
		"""
		self.CPU_Reg0 = 0
		self.CPU_Reg1 = 0
		self.CPU_Reg2 = 0
		self.CPU_Reg3 = 0
		self.CPU_Reg4 = 0
		self.CPU_Reg5 = 0
		self.CPU_IP = 0

	def setBeforeOperationRegisterValues(self,beforeRegs):
		"""setBeforeOperationRegisterValues
		
		:param beforeRegs: The registers before the operation.
		:returns: nothing
		"""
		#print 'setBeforeOperationRegisterValues: beforeRegs',beforeRegs
		self.CPU_Reg0 = beforeRegs[0]
		self.CPU_Reg1 = beforeRegs[1]
		self.CPU_Reg2 = beforeRegs[2]
		self.CPU_Reg3 = beforeRegs[3]
		self.CPU_Reg4 = beforeRegs[4]
		self.CPU_Reg5 = beforeRegs[5]
		return
	
	def getRegisterAfterValues(self):
		"""getRegisterAfterValues - get the contents of the register after the operation completes
		
		:returns: CPU registers as a vector (6 elements long)
		"""
		return [self.CPU_Reg0, self.CPU_Reg1, self.CPU_Reg2, self.CPU_Reg3, self.CPU_Reg4, self.CPU_Reg5]
		
	def getRegA(self,regSelA):
		"""getRegA - Simulates a 1:6 de-multiplexer
		
		:param regSelA: the select for the the A input to the ALU
		:returns: content of the selected register
		"""
		if regSelA == 0:
			return self.CPU_Reg0
		elif regSelA == 1:
			return self.CPU_Reg1
		elif regSelA == 2:
			return self.CPU_Reg2
		elif regSelA == 3:
			return self.CPU_Reg3
		elif regSelA == 4:
			return self.CPU_Reg4
		elif regSelA == 5:
			return self.CPU_Reg5
		abbyTerminate('getRegA: passed unexpected value for select')

	def getInputA(self,regSelA,immedVsRegFlag):
		"""getInputA - Implement a 2:1 multiplexer.
		
		:param regSelA: The regSelA value itself (immediate value)
		:param immedVsRegFlag: Flags whether the immediate value or the register value is returned
		:returns: The output of the 2:1 multiplexer
		"""
		if immedVsRegFlag == 'Immediate':
			return regSelA
		elif immedVsRegFlag == 'Register':
			return self.getRegA(regSelA)
		abbyTerminate('getInputA: needs flag of Immediate or Register')

	def getRegB(self,regSelB):
		"""getRegB - Simulates a 1:6 de-multiplexer
		
		:param regSelB: the select for the the A input to the ALU
		:returns: content of the selected register
		"""
		if regSelB == 0:
			return self.CPU_Reg0
		elif regSelB == 1:
			return self.CPU_Reg1
		elif regSelB == 2:
			return self.CPU_Reg2
		elif regSelB == 3:
			return self.CPU_Reg3
		elif regSelB == 4:
			return self.CPU_Reg4
		elif regSelB == 5:
			return self.CPU_Reg5
		abbyTerminate('getRegA: passed unexpected value')

	def getInputB(self,regSelB,immedVsRegFlag):
		"""getInputA - Implement a 2:1 multiplexer.
		
		:param regSelA: The regSelA value itself (immediate value)
		:param immedVsRegFlag: Flags whether the immediate value or the register value is returned
		:returns: The output of the 2:1 multiplexer
		"""
		if immedVsRegFlag == 'Immediate':
			return regSelB
		elif immedVsRegFlag == 'Register':
			return self.getRegB(regSelB)
		abbyTerminate('getInputB: needs flag of Immediate or Register')

	def storeCVal(self,regSel,cVal):
		"""storeCVal - Takes the output of the ALU (called C) and routes it to the correct register.
		Implements a 1:6 demultiplexer into the six registers to load the correct register
		In hardware this would be one common bus to all register inputs and a LOAD line to clock the correct register
		
		:param regSel: Register Select value (0-5) which selects which register gets written.
		:param: cVal: Output from the ALU (aka "C")
		"""
		debug_storeCVal = False
		if debug_storeCVal:
			print 'storeCVal: regSel,cVal',regSel,cVal
		if regSel == 0:
			self.CPU_Reg0 = cVal
		elif regSel == 1:
			self.CPU_Reg1 = cVal
		elif regSel == 2:
			self.CPU_Reg2 = cVal
		elif regSel == 3:
			self.CPU_Reg3 = cVal
		elif regSel == 4:
			self.CPU_Reg4 = cVal
		elif regSel == 5:
			self.CPU_Reg5 = cVal
		else:
			abbyTerminate('storeCVal: passed unexpected value')
	
	def doALU(self,opcodeVector):
		"""doALU - Do the Arithmetic Logic Unit worked
		Calls the individual routines for each of the opcodes
		
		:param opcodeVector: The vector for the instruction.
		Vector is [opcodeNumber][regs_before][regs_after]
		"""
		debug_doALU = False
		if debug_doALU:
			print 'doALU: vector',opcodeVector
			print 'doALU: opcode =',opcodesList[opcodeVector[0]]
		if opcodeVector[0] == 'addr':
			self.INSTR_addr(opcodeVector)
		elif opcodeVector[0] == 'addi':
			self.INSTR_addi(opcodeVector)
		elif opcodeVector[0] == 'mulr':
			self.INSTR_mulr(opcodeVector)
		elif opcodeVector[0] == 'muli':
			self.INSTR_muli(opcodeVector)
		elif opcodeVector[0] == 'banr':
			self.INSTR_banr(opcodeVector)
		elif opcodeVector[0] == 'bani':
			self.INSTR_bani(opcodeVector)
		elif opcodeVector[0] == 'borr':
			self.INSTR_borr(opcodeVector)
		elif opcodeVector[0] == 'bori':
			self.INSTR_bori(opcodeVector)
		elif opcodeVector[0] == 'setr':
			self.INSTR_setr(opcodeVector)
		elif opcodeVector[0] == 'seti':
			self.INSTR_seti(opcodeVector)
		elif opcodeVector[0] == 'gtir':
			self.INSTR_gtir(opcodeVector)
		elif opcodeVector[0] == 'gtri':
			self.INSTR_gtri(opcodeVector)
		elif opcodeVector[0] == 'gtrr':
			self.INSTR_gtrr(opcodeVector)
		elif opcodeVector[0] == 'eqir':
			self.INSTR_eqir(opcodeVector)
		elif opcodeVector[0] == 'eqri':
			self.INSTR_eqri(opcodeVector)
		elif opcodeVector[0] == 'eqrr':
			self.INSTR_eqrr(opcodeVector)
		else:
			print 'doALU: opcode =',opcodeVector[0]
			abbyTerminate('doALU: passed bad opcode, exiting...')
		return

	def INSTR_addr(self,vector):	# (add register) stores into register C the result of adding register A and register B.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Register')
		cVal = aVal + bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_addi(self,vector):
		"""# (add immediate) stores into register C the result of adding register A and value B.
		"""
		#print 'INSTR_addi: vector',vector
		aVal = self.getInputA(vector[1],'Register')
		#print 'INSTR_addi: aVal',aVal
		bVal = self.getInputB(vector[2],'Immediate')
		#print 'INSTR_addi: bVal',bVal
		cVal = aVal + bVal
		#print 'INSTR_addi: cVal',cVal
		self.storeCVal(vector[3],cVal)

	def INSTR_mulr(self,vector):
		"""(multiply register) stores into register C the result of multiplying register A and register B.
		"""
		#print 'INSTR_mulr: vector',vector
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Register')
		cVal = aVal * bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_muli(self,vector):	# (multiply immediate) stores into register C the result of multiplying register A and value B.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Immediate')
		cVal = aVal * bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_banr(self,vector):	# (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Register')
		cVal = aVal & bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_bani(self,vector):	# (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Immediate')
		cVal = aVal & bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_borr(self,vector):	# (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Register')
		cVal = aVal | bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_bori(self,vector):	# (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Immediate')
		cVal = aVal | bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_setr(self,vector):	# (set register) copies the contents of register A into register C. (Input B is ignored.) 
		aVal = self.getInputA(vector[1],'Register')
		cVal = aVal
		self.storeCVal(vector[3],cVal)

	def INSTR_seti(self,vector):
		"""(set immediate) stores value A into register C. (Input B is ignored.)
		"""
		#print 'seti instruction decode'
		aVal = self.getInputA(vector[1],'Immediate')
		cVal = aVal
		self.storeCVal(vector[3],cVal)

	def INSTR_gtir(self,vector):	# (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
		aVal = self.getInputA(vector[1],'Immediate')
		bVal = self.getInputB(vector[2],'Register')
		if aVal > bVal:
			cVal = 1
		else:
			cVal = 0
		self.storeCVal(vector[3],cVal)

	def INSTR_gtri(self,vector):	# gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Immediate')
		if aVal > bVal:
			cVal = 1
		else:
			cVal = 0
		self.storeCVal(vector[3],cVal)

	def INSTR_gtrr(self,vector):	# gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Register')
		if aVal > bVal:
			cVal = 1
		else:
			cVal = 0
		self.storeCVal(vector[3],cVal)
		
	def INSTR_eqir(self,vector):	# (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
		aVal = self.getInputA(vector[1],'Immediate')
		bVal = self.getInputB(vector[2],'Register')
		if aVal == bVal:
			cVal = 1
		else:
			cVal = 0
		self.storeCVal(vector[3],cVal)

	def INSTR_eqri(self,vector):	# (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Immediate')
		if aVal == bVal:
			cVal = 1
		else:
			cVal = 0
		self.storeCVal(vector[3],cVal)

	def INSTR_eqrr(self,vector):	# (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Register')
		if aVal == bVal:
			cVal = 1
		else:
			cVal = 0
		self.storeCVal(vector[3],cVal)
	
	#opcodes that failed
	eqri = 0	# 15
	bori = 1	# could be 2,4,7,10,11,13,15
	mulr = 2	# could be 2, not 14
	seti = 3	# could be 3,9
	banr = 4	# could be 2,4,5,7,9,10,11,13,15
	bani = 5	# could be 2,4,5,7,10,11,13,15
	borr = 6	# could be 0,1,2,4,4,5,6,7,8,9,10,12,14
	gtrr = 7	# could be 7,15
	gtir = 8	# could be 10
	addi = 9	# could be 2,4,5,9,10,11,14,15
	setr = 10	# could be 8,10,
	eqrr = 11	# could be 11
	addr = 12	# could be 12
	eqir = 13	# could be 13
	gtri = 14	# could be 1,2,3,4,6,8,9,11,13,14
	muli = 15	# 15
	
#########################################################################
## This is the workhorse of this assignment
## Test opcodes one at a time against all of the instructions
## Can the instructions be sorted/grouped or are they dependent on previous values in the registers?
## Registers start at value 0
## Should registers be global variable or accessed via functions?
"""	addr = 0
	addi = 1
	mulr = 2
	muli = 3
	banr = 4
	bani = 5
	borr = 6
	bori = 7
	setr = 8
	seti = 9
	gtir = 10
	gtri = 11
	gtrr = 12
	eqir = 13
	eqri = 14
	eqrr = 15
"""

opcodesList = ['eqri','bori','mulr','seti','banr','bani','borr','gtrr','gtir','addi','setr','eqrr','addr','eqir','gtri','muli',]
	
def processList(theList,myCPU):
	"""
	[[0, 0], 
	[1, 0, 4, 7, 8, 11, 13, 14], 
	[2, 1, 2, 3, 4, 6, 9, 10, 11, 13, 14], 
	[3, 0, 2, 3, 4, 5, 8, 11, 14], 
	[4, 0, 3, 4, 5, 7, 8, 11, 13, 14], 
	[5, 0, 4, 5, 7, 8, 11, 13, 14], 
	[6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15], 
	[7, 0, 7], 
	[8, 8, 10], 
	[9, 3, 9], 
	[10, 0, 7, 8, 11, 13, 14], 
	[11, 2, 3, 4, 5, 6, 10, 11, 13], 
	[12, 3, 9, 12], [13, 0, 11, 13, 14], 
	[14, 7, 14], 
	[15, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
	"""
	listByOpcode = sorted(theList, key = lambda errs: errs[0])
	listVals = []
	for opCodeVal in xrange(16):
		listLine = []
		listLine.append(opCodeVal)
		passingCases = 0
		failedCases = 0
		passBins = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
		failBins = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
		for testVec in listByOpcode:
			if testVec[0] == opCodeVal:
				for myOpCodes in range(16):
					myCPU.initializeCPU()
					testVec[0] = myOpCodes
					if testOpcode(myCPU,testVec[4:8],testVec[0:4],testVec[8:12]):
						passBins[testVec[0]] = passBins[testVec[0]] + 1
						passingCases += 1
					else:
						failBins[testVec[0]] = failBins[testVec[0]] + 1
						failedCases += 1
		print opCodeVal,',',
		print opcodesList[opCodeVal],',',
		for x,y in passBins.items():
			if y > 0:
				print x,',',
				listLine.append(x)
		print
		listVals.append(listLine)
		
	print listVals
	print 'passBins',passBins
	print 'failedCases',failedCases
	print 'failBins',failBins
	
def testRegisters(myCPU):
	"""tests the register write path via the store of the ALU output - storeCVal
	tests the readback of the register values via getRegisterAfterValues
	"""
	debug_testRegisters = False
	afterRegs = myCPU.getRegisterAfterValues()
	if afterRegs == [0,0,0,0]:
		if debug_testRegisters:
			print 'testRegisters: CPU registers were intialized to zeros'
	else:
		abbyTerminate('testRegisters: CPU registers did not initialize')
	if debug_testRegisters:
		print 'testRegisters: storing 12 to register 0'
	myCPU.storeCVal(0,12)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisters:
		print 'testRegisters: afterRegs',afterRegs
	if afterRegs == [12,0,0,0]:	
		if debug_testRegisters:
			print 'testRegisters: Register 0 was set to 12'
	else:
		abbyTerminate('testRegisters: CPU registers did not initialize')
	myCPU.storeCVal(1,15)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisters:
		print 'testRegisters: afterRegs',afterRegs
	if afterRegs == [12,15,0,0]:	
		if debug_testRegisters:
			print 'testRegisters: Register 1 was set to 15'
	else:
		abbyTerminate('testRegisters: CPU registers did not initialize')
	myCPU.storeCVal(2,18)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisters:
		print 'testRegisters: afterRegs',afterRegs
	if afterRegs == [12,15,18,0]:	
		if debug_testRegisters:
			print 'testRegisters: Register 2 was set to 18'
	else:
		abbyTerminate('testRegisters: CPU registers did not initialize')
	myCPU.storeCVal(3,21)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisters:
		print 'testRegisters: afterRegs',afterRegs
	if afterRegs == [12,15,18,21]:
		if debug_testRegisters:
			print 'testRegisters: Register 3 was set to 21'
	else:
		abbyTerminate('testRegisters: CPU registers did not initialize')
	if debug_testRegisters:
		print 'testRegisters: register tests passed'
	myCPU.initializeCPU()	# reset registers
	afterRegs = myCPU.getRegisterAfterValues()
	if afterRegs == [0,0,0,0]:
		if debug_testRegisters:
			print 'testRegisters: initializeCPU function passed'
	else:
		abbyTerminate('testRegisters: initializeCPU function failed to clear CPU registers')
	return True
	
def testOpcode(myCPU,regsBefore,instructionVector,expectedVector):
	"""Used to test the ALU executes correctly. 
	Called from testALU. 
	
	:param myCPU: the CPU class
	:param regsBefore: The registers before the opcode is executed
	:param instructionVector: The Instruction vector
	:param expectedVector: The expected contents of the vector after the instruction is executed
	:returns: True if the ALU operation succeeded (returned the expected value)
	False if the ALU operation failed
	"""
	debug_testOpcode = False
	if debug_testOpcode:
		print 'testOpcode: Setting the before operation register values'
	myCPU.setBeforeOperationRegisterValues(regsBefore)	# Using problem example
	if debug_testOpcode:
		print 'testOpcode: Setting the instruction vector'
		print 'testOpcode: calling the emulator code'
	myCPU.emulator(instructionVector)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testOpcode:
		print 'testOpcode:afterRegs',afterRegs
	if afterRegs == expectedVector:
		if debug_testOpcode:
			print 'testOpcode: opcode',instructionVector[0],' passed'
		return True
	if debug_testOpcode:
		print 'testOpcode: opcode',instructionVector[0],' failed'
	return False

def testALU(myCPU):
	"""testALU - Run test vectors on the ALU to make sure it operates correctly
	
	:param myCPU: The CPU class
	"""
	debug_testALU = False
	if debug_testALU:
		print 'testALU: Initializing the CPU registers'
	myCPU.initializeCPU()	# reset registers at the end of the testALU
	if not testOpcode(myCPU,[3,2,1,1],[0,2,1,2],[3,2,3,1]):		# addr
		abbyTerminate('opcode 0 failed')
	if not testOpcode(myCPU,[3,2,1,1],[1,2,1,2],[3,2,2,1]):		# addi
		abbyTerminate('opcode 1 failed')
	if not testOpcode(myCPU,[3,2,1,1],[2,2,1,2],[3,2,2,1]):		# mulr
		abbyTerminate('opcode 2 failed')
	if not testOpcode(myCPU,[3,4,5,6],[3,2,1,3],[3,4,5,5]):		# muli
		abbyTerminate('opcode 3 failed')
	if not testOpcode(myCPU,[3,2,1,1],[9,2,1,2],[3,2,2,1]):		# seti
		abbyTerminate('opcode 9 failed')
	if testOpcode(myCPU,[3,2,1,1],[4,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 4 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[5,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 5 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[6,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 6 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[7,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 7 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[8,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 8 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[10,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 10 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[11,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 11 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[12,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 12 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[13,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 13 should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[14,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 14  should not have passed')
	if testOpcode(myCPU,[3,2,1,1],[15,2,1,2],[3,2,2,1]):			# 
		abbyTerminate('opcode 15 should not have passed')
	return True
	
def testCPU(myCPU):
	debug_testCPU = False
	if debug_testCPU:
		print 'testCPU: Initialized CPU Class'
	myCPU.initializeCPU()
	
	if testRegisters(myCPU):
		if debug_testCPU:
			print 'testCPU: testRegisters passed'
	
	if testALU(myCPU):
		if debug_testCPU:
			print 'testCPU: ALU tests passed'	
	return True
	
def processListPart1(theList,myCPU):
	listByOpcode = sorted(theList, key = lambda errs: errs[0])
	totalThatHaveThreeOrMoreOpcodes = 0
	for testVec in listByOpcode:
		testCaseMatches = 0
		for x in range(16):
			testVecReplacement = testVec[0:4]
			testVecReplacement[0] = x
			if testOpcode(myCPU,testVec[4:8],testVecReplacement,testVec[8:12]):
				testCaseMatches += 1
		if testCaseMatches >= 3:
			totalThatHaveThreeOrMoreOpcodes += 1
	print 'totalThatHaveThreeOrMoreOpcodes',totalThatHaveThreeOrMoreOpcodes


########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

textList = readTextFileToList('input.txt')

myList = parseTextFileIntoListOfNumbers(textList)

myCPU = CPU()

processListPart1(myList,myCPU)

print 'Completed processing',time.strftime('%X %x %Z')

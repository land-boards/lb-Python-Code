# Pt2-AoCDay16.py
# 2018 Advent of Code
# Day 16
# Part 2
# https://adventofcode.com/2018/day/16

import time
import re
import os

"""
The challenge in part 2 is to map the test file opcodes to my opcodes.
The test file  does not have enough test cases to eliminate multiple possibilities.
Approach #1 - Run dataset for individual values to determine which are possible solutions.
Approach #2 - Brute force attack it by moving through the possible codes and running them
until there are no mismatches.
Bits across are:
	4 bits OPCODE x 16
		Seems like the order of magnitude is 64 bits. 
		2^64 is too big to solve brute force.
Approach #3 - Hybrid approach. Find the lists of possibilites for each opcode.
Use the list of possibles to increment through all the possibilities.

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
	
def integerize(str):
	return int(str)

def loadProgram(fileName='input2.txt'):
	textList = readTextFileToList(fileName)
	programVectors = []
	for line in textList:
		programLine = line.split(" ")
		newList = map(integerize,programLine)
		programVectors.append(newList)

#	print 'programVectors',programVectors
	return programVectors
		
def parseTextFileIntoListOfNumbers(textFile):
	"""Convert the text file into a list
	
	list is [opcode][before][after]
	Where [opcode] is [opcode,A,B,C]
	[before] = [R0,R1,R2,R3]
	[after] = [R0,R1,R2,R3]
	
	"""
	theList = []
	listOfBefore = []
	listOfAfter = []
	opcodeList = []
	for line in textFile:
		if len(line) == 0:
			continue
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
	CPU_Reg0 = 0
	CPU_Reg1 = 0
	CPU_Reg2 = 0
	CPU_Reg3 = 0

	def emulator(self,vector):
		debug_emulator = False
		if debug_emulator:
			print 'emulator:',vector
		self.doALU(vector[0:4])
		return self.getRegisterAfterValues()
	
	def initializeCPU(self):
		self.CPU_Reg0 = 0
		self.CPU_Reg1 = 0
		self.CPU_Reg2 = 0
		self.CPU_Reg3 = 0

	def setBeforeOperationRegisterValues(self,beforeRegs):
		#print 'setBeforeOperationRegisterValues: beforeRegs',beforeRegs
		self.CPU_Reg0 = beforeRegs[0]
		self.CPU_Reg1 = beforeRegs[1]
		self.CPU_Reg2 = beforeRegs[2]
		self.CPU_Reg3 = beforeRegs[3]
		return
	
	def getRegisterAfterValues(self):
		return [self.CPU_Reg0, self.CPU_Reg1, self.CPU_Reg2, self.CPU_Reg3]
		
	def getRegA(self,regSelA):
		if regSelA == 0:
			return self.CPU_Reg0
		elif regSelA == 1:
			return self.CPU_Reg1
		elif regSelA == 2:
			return self.CPU_Reg2
		elif regSelA == 3:
			return self.CPU_Reg3
		abbyTerminate('getRegA: passed unexpected value')

	def getInputA(self,regSelA,immedVsRegFlag):
		if immedVsRegFlag == 'Immediate':
			return regSelA
		elif immedVsRegFlag == 'Register':
			return self.getRegA(regSelA)
		abbyTerminate('getInputA: needs flag of Immediate or Register')

	def getRegB(self,regSelB):
		if regSelB == 0:
			return self.CPU_Reg0
		elif regSelB == 1:
			return self.CPU_Reg1
		elif regSelB == 2:
			return self.CPU_Reg2
		elif regSelB == 3:
			return self.CPU_Reg3
		abbyTerminate('getRegA: passed unexpected value')

	def getInputB(self,regSelB,immedVsRegFlag):
		if immedVsRegFlag == 'Immediate':
			return regSelB
		elif immedVsRegFlag == 'Register':
			return self.getRegB(regSelB)
		abbyTerminate('getInputB: needs flag of Immediate or Register')

	def storeCVal(self,regSel,cVal):
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
		else:
			abbyTerminate('storeCVal: passed unexpected value')
	
	def doALU(self,opcodeVector):
		debug_doALU = False
		if debug_doALU:
			print 'doALU: vector',opcodeVector
			print 'doALU: opcode =',opcodesList[opcodeVector[0]]
		if opcodeVector[0] == self.addr:
			self.INSTR_addr(opcodeVector)
		elif opcodeVector[0] == self.addi:
			self.INSTR_addi(opcodeVector)
		elif opcodeVector[0] == self.mulr:
			self.INSTR_mulr(opcodeVector)
		elif opcodeVector[0] == self.muli:
			self.INSTR_muli(opcodeVector)
		elif opcodeVector[0] == self.banr:
			self.INSTR_banr(opcodeVector)
		elif opcodeVector[0] == self.bani:
			self.INSTR_bani(opcodeVector)
		elif opcodeVector[0] == self.borr:
			self.INSTR_borr(opcodeVector)
		elif opcodeVector[0] == self.bori:
			self.INSTR_bori(opcodeVector)
		elif opcodeVector[0] == self.setr:
			self.INSTR_setr(opcodeVector)
		elif opcodeVector[0] == self.seti:
			self.INSTR_seti(opcodeVector)
		elif opcodeVector[0] == self.gtir:
			self.INSTR_gtir(opcodeVector)
		elif opcodeVector[0] == self.gtri:
			self.INSTR_gtri(opcodeVector)
		elif opcodeVector[0] == self.gtrr:
			self.INSTR_gtrr(opcodeVector)
		elif opcodeVector[0] == self.eqir:
			self.INSTR_eqir(opcodeVector)
		elif opcodeVector[0] == self.eqri:
			self.INSTR_eqri(opcodeVector)
		elif opcodeVector[0] == self.eqrr:
			self.INSTR_eqrr(opcodeVector)
		else:
			print 'doALU: opcode =',opcodeVector[0]
			abbyTerminate('doALU: passed bad opcode')
		return

	def INSTR_addr(self,vector):	# (add register) stores into register C the result of adding register A and register B.
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Register')
		cVal = aVal + bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_addi(self,vector):
		"""# (add immediate) stores into register C the result of adding register A and value B.
		"""
		aVal = self.getInputA(vector[1],'Register')
		bVal = self.getInputB(vector[2],'Immediate')
		cVal = aVal + bVal
		self.storeCVal(vector[3],cVal)

	def INSTR_mulr(self,vector):
		"""(multiply register) stores into register C the result of multiplying register A and register B.
		"""
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
	eqri = 0
	banr = 1
	bori = 2
	mulr = 3
	seti = 4
	bani = 5
	muli = 6
	gtrr = 7
	setr = 8
	addi = 9
	gtir = 10
	borr = 11
	addr = 12
	eqrr = 13
	gtri = 14
	eqir = 15
	
#########################################################################
## Test opcodes one at a time against all of the instructions
## Instructions for this portion are not dependent on previous values in the registers.
## Registers start at value 0
## Should registers be global variable or accessed via functions?

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
	sortedListByOpcode = sorted(theList, key = lambda errs: errs[0])
	listVals = []
	for opcVal in xrange(16):	# cycling through the opcode values one at a time
		listLine = []
		listLine.append(opcVal)
		passingCases = 0
		failedCases = 0
		passBins = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
		failBins = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0}
		for testVec in sortedListByOpcode:		# Only do one opcode value from the input file at a time
			myTestVec = list(testVec)	# had to force a copy of it
			if myTestVec[0] == opcVal:
				for testingOpCodeValue in xrange(16):
					myCPU.initializeCPU()
					myTestVec[0] = testingOpCodeValue
					if testOpcode(myCPU,myTestVec[4:8],myTestVec[0:4],myTestVec[8:12]):
						passBins[myTestVec[0]] = passBins[myTestVec[0]] + 1
						passingCases += 1
					else:
						failBins[myTestVec[0]] = failBins[myTestVec[0]] + 1
						failedCases += 1
		for x in xrange(16):
			if failBins[x] == 0 and passBins[x] > 0:
				listLine.append(x)
		listVals.append(listLine)
		
	for val in listVals:
		print val[0],
		print '===>',val[1:]
	return listVals
	
def testRegisterCPath(myCPU):
	"""Tests the register write path via the store of the ALU output - storeCVal
	Also tests the readback of the register values via getRegisterAfterValues
	The storeCVal path is the 1:4 demultiplexer on the ALU output into the four registers.
	"""
	debug_testRegisterCPath = False
	afterRegs = myCPU.getRegisterAfterValues()
	if afterRegs == [0,0,0,0]:
		if debug_testRegisterCPath:
			print 'testRegisterCPath: CPU registers were intialized to zeros'
	else:
		abbyTerminate('testRegisterCPath: CPU registers did not initialize')
	if debug_testRegisterCPath:
		print 'testRegisterCPath: storing 12 to register 0'
	myCPU.storeCVal(0,12)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisterCPath:
		print 'testRegisterCPath: afterRegs',afterRegs
	if afterRegs == [12,0,0,0]:	
		if debug_testRegisterCPath:
			print 'testRegisterCPath: Register 0 was set to 12'
	else:
		abbyTerminate('testRegisterCPath: CPU registers did not initialize')
	myCPU.storeCVal(1,15)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisterCPath:
		print 'testRegisterCPath: afterRegs',afterRegs
	if afterRegs == [12,15,0,0]:	
		if debug_testRegisterCPath:
			print 'testRegisterCPath: Register 1 was set to 15'
	else:
		abbyTerminate('testRegisterCPath: CPU registers did not initialize')
	myCPU.storeCVal(2,18)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisterCPath:
		print 'testRegisterCPath: afterRegs',afterRegs
	if afterRegs == [12,15,18,0]:	
		if debug_testRegisterCPath:
			print 'testRegisterCPath: Register 2 was set to 18'
	else:
		abbyTerminate('testRegisterCPath: CPU registers did not initialize')
	myCPU.storeCVal(3,21)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testRegisterCPath:
		print 'testRegisterCPath: afterRegs',afterRegs
	if afterRegs == [12,15,18,21]:
		if debug_testRegisterCPath:
			print 'testRegisterCPath: Register 3 was set to 21'
	else:
		abbyTerminate('testRegisterCPath: CPU registers did not initialize')
	if debug_testRegisterCPath:
		print 'testRegisterCPath: register tests passed'
	myCPU.initializeCPU()	# reset registers
	afterRegs = myCPU.getRegisterAfterValues()
	if afterRegs == [0,0,0,0]:
		if debug_testRegisterCPath:
			print 'testRegisterCPath: initializeCPU function passed'
	else:
		abbyTerminate('testRegisterCPath: initializeCPU function failed to clear CPU registers')
	return True
	
def testOpcode(myCPU,regsBefore,instructionVector,expectedVector):
	debug_testOpcode = False
	if debug_testOpcode:
		print 'testOpcode: Setting the before operation register values'
	myCPU.setBeforeOperationRegisterValues(regsBefore)	# Using problem example
	if debug_testOpcode:
		print 'testOpcode: Setting the instruction vector, calling the emulator code'
	myCPU.emulator(instructionVector)
	afterRegs = myCPU.getRegisterAfterValues()
	if debug_testOpcode:
		print 'testOpcode:afterRegs',afterRegs
	if afterRegs == expectedVector:
		if debug_testOpcode:
			print 'testOpcode: opcode',opcodesList[instructionVector[0]],'passed'
		return True
	if debug_testOpcode:
		print 'testOpcode: opcode',opcodesList[instructionVector[0]],'failed'
	return False

eqri = 0
banr = 1
bori = 2
mulr = 3
seti = 4
bani = 5
muli = 6
gtrr = 7
setr = 8
addi = 9
gtir = 10
borr = 11
addr = 12
eqrr = 13
gtri = 14
eqir = 15

opcodesList = ['eqri','banr','bori','mulr','seti','bani','muli','gtrr','setr','addi','gtir','borr','addr','eqrr','gtri','eqir']
	
def testALU(myCPU):
	debug_testALU = False
	if debug_testALU:
		print 'testALU: Initializing the CPU registers'
	myCPU.initializeCPU()	# reset registers at the end of the testALU
	if not testOpcode(myCPU,[3,2,1,1],[addr,2,1,2],[3,2,3,1]):		# addr
		abbyTerminate('addr opcode failed to return value')
	if testOpcode(myCPU,[3,2,1,1],[addr,2,1,2],[3,2,1,1]):			# addr
		abbyTerminate('addr opcode should have failed')
	if not testOpcode(myCPU,[3,2,1,1],[addi,2,1,2],[3,2,2,1]):		# addi
		abbyTerminate('addi failed to return value')
	if testOpcode(myCPU,[3,2,1,1],[addi,2,1,2],[3,2,1,1]):			# addi
		abbyTerminate('addi should have failed')
	if not testOpcode(myCPU,[3,2,1,1],[mulr,2,1,2],[3,2,2,1]):		# mulr
		abbyTerminate('mulr failed to return value')
	if testOpcode(myCPU,[3,2,1,1],[mulr,2,1,2],[3,2,1,1]):			# mulr
		abbyTerminate('mulr should have failed')
	if not testOpcode(myCPU,[3,4,5,6],[muli,2,2,3],[3,4,5,10]):		# muli
		abbyTerminate('muli should have failed')
	if testOpcode(myCPU,[3,4,5,6],[muli,2,2,3],[3,4,5,6]):			# muli
		abbyTerminate('muli failed to return value')
	if not testOpcode(myCPU,[3,2,1,1],[seti,2,1,2],[3,2,2,1]):		# seti
		abbyTerminate('seti opcode failed to return value')
	if testOpcode(myCPU,[3,2,1,1],[seti,2,1,2],[3,2,1,1]):			# seti
		abbyTerminate('seti should have failed')
	if not testOpcode(myCPU,[15,9,1,1],[banr,0,1,2],[15,9,9,1]):	# banr
		abbyTerminate('banr opcode failed to return value')
	if testOpcode(myCPU,[15,9,1,1],[banr,0,1,2],[15,9,8,1]):		# banr
		abbyTerminate('banr should have failed')		
	if not testOpcode(myCPU,[15,1,1,1],[bani,0,9,2],[15,1,9,1]):	# bani 
		abbyTerminate('bani opcode failed to return value')
	if testOpcode(myCPU,[15,1,1,1],[bani,0,9,2],[15,1,1,1]):		# bani
		abbyTerminate('bani should have failed')
	if not testOpcode(myCPU,[1,2,4,8],[borr,0,1,2],[1,2,3,8]):		# borr
		abbyTerminate('borr failed to return value')
	if testOpcode(myCPU,[1,2,4,8],[borr,0,1,2],[1,2,4,8]):			# borr
		abbyTerminate('borr should have failed')
	if not testOpcode(myCPU,[1,2,4,8],[setr,0,1,2],[1,2,1,8]):		# setr
		abbyTerminate('setr failed to return value')
	if testOpcode(myCPU,[1,2,4,8],[setr,0,1,2],[1,2,4,8]):			# setr
		abbyTerminate('setr should have failed')
	if not testOpcode(myCPU,[1,2,4,8],[bori,0,2,2],[1,2,3,8]):		# bori
		abbyTerminate('bori failed to return value')
	if testOpcode(myCPU,[1,2,4,8],[bori,0,1,2],[1,2,4,8]):			# bori
		abbyTerminate('bori should have failed')
	if not testOpcode(myCPU,[1,2,4,8],[gtir,0,1,2],[1,2,0,8]):			# 
		abbyTerminate('gtir failed to return value 0')
	if not testOpcode(myCPU,[1,2,4,8],[gtir,2,0,2],[1,2,1,8]):			# 
		abbyTerminate('gtir failed to return value 1')
	if testOpcode(myCPU,[1,2,4,8],[gtir,0,1,2],[1,2,1,8]):			# 
		abbyTerminate('gtir should have failed')
	if not testOpcode(myCPU,[1,2,4,8],[gtri,0,1,2],[1,2,0,8]):			# 
		abbyTerminate('gtri should not have passed 0')
	if not testOpcode(myCPU,[1,2,4,8],[gtri,0,0,2],[1,2,1,8]):			# 
		abbyTerminate('gtri should not have passed 1')
	if testOpcode(myCPU,[1,2,4,8],[gtri,0,1,2],[2,1,4,8]):			# 
		abbyTerminate('gtri should not have passed 4')
	if not testOpcode(myCPU,[1,2,4,8],[gtrr,0,1,2],[1,2,0,8]):			# 
		abbyTerminate('gtrr should not have passed 0')
	if not testOpcode(myCPU,[2,1,4,8],[gtrr,0,1,2],[2,1,1,8]):			# 
		abbyTerminate('gtrr should not have passed 1')
	if testOpcode(myCPU,[2,1,4,8],[gtrr,0,1,2],[2,1,4,8]):			# 
		abbyTerminate('gtrr should have failed')
	if not testOpcode(myCPU,[1,2,4,8],[gtrr,0,1,2],[1,2,0,8]):			# 
		abbyTerminate('gtrr should not have passed')
	if not testOpcode(myCPU,[2,1,4,8],[gtrr,0,1,2],[2,1,1,8]):			# 
		abbyTerminate('gtrr should not have passed')
	if testOpcode(myCPU,[2,1,4,8],[gtrr,0,1,2],[2,1,0,8]):			# 
		abbyTerminate('gtrr should have failed')
	if not testOpcode(myCPU,[1,2,4,8],[eqir,2,1,2],[1,2,1,8]):			# 
		abbyTerminate('eqir should not have passed 1')
	if not testOpcode(myCPU,[1,2,4,8],[eqir,0,1,2],[1,2,0,8]):			# 
		abbyTerminate('eqir should not have passed 0')
	if testOpcode(myCPU,[1,2,4,8],[eqir,0,1,2],[1,2,1,8]):			# 
		abbyTerminate('eqir should not have passed 0')
	if not testOpcode(myCPU,[1,2,4,8],[eqri,0,1,2],[1,2,1,8]):			# 
		abbyTerminate('eqri should not have passed')
	if not testOpcode(myCPU,[1,2,4,8],[eqri,0,99,2],[1,2,0,8]):			# 
		abbyTerminate('eqri should not have passed')
	if testOpcode(myCPU,[1,2,4,8],[eqri,0,99,2],[1,2,1,8]):			# 
		abbyTerminate('eqri should not have passed')		
	if not testOpcode(myCPU,[1,1,4,8],[eqrr,0,1,2],[1,1,1,8]):			# 
		abbyTerminate('eqrr should not have passed 1')
	if not testOpcode(myCPU,[1,2,4,8],[eqrr,0,1,2],[1,2,0,8]):			# 
		abbyTerminate('eqrr should not have passed 0')
	if testOpcode(myCPU,[1,2,4,8],[eqrr,0,1,2],[1,2,1,8]):			# 
		abbyTerminate('eqrr should not have passed 0')	
	return True
	
def testRegisterBankAnd4To1Muxes(myCPU):
	"""Purpose is to test the four registers in the register bank.
	Use setr instuction to test path A - set each of them one at a time.
	This path also tests the multiplexer selection for the ALU
	Use borr to test path B
	"""
	debug_testRegisterBankAnd4To1Muxes = False
	if debug_testRegisterBankAnd4To1Muxes:
		print 'testRegisterBankAnd4To1Muxes: Checking that all of the registers can be read and set via setr command'
	if not testOpcode(myCPU,[1,2,3,4],[setr,0,1,1],[1,1,3,4]):	# Quick test setr instruction 
		abbyTerminate('testRegisterBankAnd4To1Muxes: setr register bank test failed')
	if not testOpcode(myCPU,[1,2,3,4],[setr,1,1,1],[1,2,3,4]):	# Quick test setr instruction 
		abbyTerminate('testRegisterBankAnd4To1Muxes: setr register bank test failed')
	if not testOpcode(myCPU,[1,2,3,4],[setr,2,1,1],[1,3,3,4]):	# Quick test setr instruction 
		abbyTerminate('testRegisterBankAnd4To1Muxes: setr register bank test failed')
	if not testOpcode(myCPU,[1,2,3,4],[setr,3,1,1],[1,4,3,4]):	# Quick test setr instruction 
		abbyTerminate('testRegisterBankAnd4To1Muxes: setr register bank test failed')
	if debug_testRegisterBankAnd4To1Muxes:
		print 'testRegisterBankAnd4To1Muxes: register bank path A passed, testing path B'
	if not testOpcode(myCPU,[1,2,4,8],[borr,0,1,2],[1,2,3,8]):	# 
		abbyTerminate('testRegisterBankAnd4To1Muxes: borr test failed')
	if not testOpcode(myCPU,[1,2,4,8],[borr,1,2,2],[1,2,6,8]):	# 
		abbyTerminate('testRegisterBankAnd4To1Muxes: borr test failed')
	if not testOpcode(myCPU,[1,2,4,8],[borr,2,3,2],[1,2,12,8]):	# 
		abbyTerminate('testRegisterBankAnd4To1Muxes: borr test failed')
	if not testOpcode(myCPU,[1,2,4,8],[borr,3,0,2],[1,2,9,8]):	# 
		abbyTerminate('testRegisterBankAnd4To1Muxes: borr test failed')
	if debug_testRegisterBankAnd4To1Muxes:
		print 'testRegisterBankAnd4To1Muxes: register bank path B passed'
	return True
	
def testCPU(myCPU):
	debug_testCPU = False
	if debug_testCPU:
		print 'testCPU: Initialized CPU Class'
	myCPU.initializeCPU()
	
	if testRegisterCPath(myCPU):
		if debug_testCPU:
			print 'testCPU: testRegisterCPath passed'
			
	if testOpcode(myCPU,[3,2,1,1],[setr,2,1,2],[3,2,2,1]):	# Quick test setr instruction 
		abbyTerminate('setr quick test failed')
	if not testRegisterBankAnd4To1Muxes(myCPU):
		abbyTerminate('register bank test failed')
	
	if testALU(myCPU):
		if debug_testCPU:
			print 'testCPU: ALU tests passed'	
	return True
	
########################################################################
## Code

print 'Reading in file',time.strftime('%X %x %Z')

textList = readTextFileToList('input-mjg.txt')

myList = parseTextFileIntoListOfNumbers(textList)

myCPU = CPU()

if testCPU(myCPU):
	print 'main: testCPU code passed'
else:
	print 'main: testCPU code failed'
	abbyTerminate('WTF')

possibleOpCodesList = processList(myList,myCPU)

theProgram = loadProgram()

myCPU.initializeCPU()

for instruction in theProgram:
	retVal = myCPU.emulator(instruction)
print 'reg0-reg3 values after running',myCPU.getRegisterAfterValues()
print 'Register 0 contents :',myCPU.getRegisterAfterValues()[0]

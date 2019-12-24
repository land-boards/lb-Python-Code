# Pt2-AoCDay19.py
# 2019 Advent of Code
# Day 19
# Part 
# https://adventofcode.com/2019/day/19

import os
import sys
import time

debugAll = False

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	
	def __init__(self):
		debug_initCPU = True
		self.programMemory = []
		self.setProgState('initCPU')
		self.programCounter = 0
		self.relativeBaseRegister = 0
		self.inputQueue = []
		self.outputQueue = []
		self.loadIntCodeProgram()
		if debug_initCPU:
			print("Memory Dump :",self.programMemory)
		
	def loadIntCodeProgram(self):
		""" 
		"""
		debug_loadIntCodeProgram = False
		progName = "D19input.txt"
		if debug_loadIntCodeProgram:
			print("Input File Name :",progName)
		with open(progName, 'r') as filehandle:  
			inLine = filehandle.readline()
#			self.programMemory = map(int, inLine.split(','))
			lineListChars = inLine.split(',')
			for charz in lineListChars:
				self.programMemory.append(int(charz))
		for i in range(1000):
			self.programMemory.append(0)
		if debug_loadIntCodeProgram:
			print(self.programMemory)
			
	def getProgState(self):
		""" Returns the value of the program state variable
		"""
		return self.progState
	
	def setProgState(self,state):
		""" Sets the value of the program state variable
		"""
		debug_setProgState = False
		self.progState = state
		if debug_setProgState:
			print("setProgState: self.progState =",self.progState)
			
	def intTo5DigitString(self, instruction):
		"""Takes a variable length string and packs the front with zeros 
		to make it 5 digits long.
		"""
		instrString=str(instruction)
		if len(instrString) == 1:
			return("0000" + str(instruction))
		elif len(instrString) == 2:
			return("000" + str(instruction))
		elif len(instrString) == 3:
			return("00" + str(instruction))
		elif len(instrString) == 4:
			return("0" + str(instruction))
		elif len(instrString) == 5:
			return(str(instruction))

	def extractFieldsFromInstruction(self, instruction):
		""" Take the Instruction and turn into opcode fields
		ABCD
		A = mode of 3rd parm
		B = mode of 2nd parm
		C = mode of 1st parm
		D = opcode
		
		:returns: [opcode,parm1,parm2,parm3]
		"""
		instructionAsFiveDigits = self.intTo5DigitString(instruction)
		parm3=int(instructionAsFiveDigits[0])
		parm2=int(instructionAsFiveDigits[1])
		parm1=int(instructionAsFiveDigits[2])
		opcode=int(instructionAsFiveDigits[3:5])
		retVal=[opcode,parm1,parm2,parm3]
		return retVal

	def evalOpPair(self, currentOp):
		""" Evaluages the two values for instruction like ADD, MUL
		Returns the two values as a list pair
		"""
		debug_BranchEval = False
		if debug_BranchEval:
			print("         evalOpPair: currentOp =",currentOp)
		val1 = self.dealWithOp(currentOp,1)
		val2 = self.dealWithOp(currentOp,2)
		return[val1,val2]
	
	def dealWithOp(self,currentOp,offset):
		""" Single place to interpret opcodes which read program memory
		Input the opcode field and the offset to the correct opcode field
		"""
		debug_dealWithOp = False
		if currentOp[offset] == 0:	# position mode
			val = self.programMemory[self.programMemory[self.programCounter+offset]]
			if debug_dealWithOp:
				print("         dealWithOp: Position Mode Parm",offset,"pos :",self.programCounter+offset,"value =",val)
		elif currentOp[offset] == 1:	# immediate mode
			val = self.programMemory[self.programCounter+offset]
			if debug_dealWithOp:
				print("         dealWithOp: Immediate Mode parm",offset,": value =",val)
		elif currentOp[offset] == 2:	# relative mode
			val = self.programMemory[self.programMemory[self.programCounter+offset] + self.relativeBaseRegister]
			if debug_dealWithOp:
				print("         dealWithOp: Relative Mode parm",offset,": value =",val)
		else:
			assert False,"dealWithOp: WTF-dealWithOp"
		return val
	
	def writeOpResult(self,opcode,opOffset,val):
		debug_writeEqLtResult = False
		if opcode[opOffset] == 0:
			self.programMemory[self.programMemory[self.programCounter+opOffset]] = val
			if debug_writeEqLtResult:
				print("         output position mode comparison val =",val)
		elif opcode[opOffset] == 1:
			self.programMemory[self.programCounter+opOffset] = val
			if debug_writeEqLtResult:
				print("         output immediate mode comparison val =",val,)
		elif opcode[opOffset] == 2:
			self.programMemory[self.programMemory[self.programCounter+opOffset] + self.relativeBaseRegister] = val
			if debug_writeEqLtResult:
				print("         output relative mode comparison val =",val,)
	
	def runCPU(self):
#		debug_runCPU = True
		debug_runCPU = False
		while(1):
			currentOp = self.extractFieldsFromInstruction(self.programMemory[self.programCounter])
			if currentOp[0] == 1:		# Addition Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"ADD Opcode = ",currentOp," ")
				result = self.dealWithOp(currentOp,1) + self.dealWithOp(currentOp,2)
				if debug_runCPU:
					print(self.dealWithOp(currentOp,1),"+",self.dealWithOp(currentOp,2),"=",result)
				self.writeOpResult(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"MUL Opcode = ",currentOp," ")
				result = self.dealWithOp(currentOp,1) * self.dealWithOp(currentOp,2)
				if debug_runCPU:
					print(self.dealWithOp(currentOp,1),"*",self.dealWithOp(currentOp,2),"=",result)
				self.writeOpResult(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				debug_CPUInput = False
#				debug_CPUInput = True
				if debug_runCPU or debug_CPUInput:
					print("PC =",self.programCounter,"INP Opcode = ",currentOp)
				if len(self.inputQueue) == 0:
					if debug_runCPU or debug_CPUInput:
						print(" - Returning to main for input value")
					self.setProgState('waitForInput')
					return
				if debug_runCPU or debug_CPUInput:
					print(" value =",self.inputQueue[0])
				result = self.inputQueue[0]
				self.writeOpResult(currentOp,1,result)
				del self.inputQueue[0]	 # Empty the input queue
				self.setProgState('inputWasRead')
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				debug_CPUOutput = False
#				debug_CPUOutput = True
				val1 = self.dealWithOp(currentOp,1)
				if debug_runCPU or debug_CPUOutput:
					print("PC =",self.programCounter,"OUT Opcode = ",currentOp)
					print(" value =",val1)
				self.outputQueue.append(val1)
				self.programCounter = self.programCounter + 2
				self.setProgState('outputReady')
				return
			elif currentOp[0] == 5:		# Jump if true
				if self.dealWithOp(currentOp,1) != 0:
					self.programCounter = self.dealWithOp(currentOp,2)
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT Opcode = ",currentOp,"Branch taken")
				else:
					self.programCounter = self.programCounter + 3		
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT Opcode = ",currentOp,"Branch not taken")
			elif currentOp[0] == 6:		# Jump if false
				if self.dealWithOp(currentOp,1) == 0:
					self.programCounter = self.dealWithOp(currentOp,2)
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT Opcode = ",currentOp,"Branch taken")
				else:
					self.programCounter = self.programCounter + 3		
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT currentOp",currentOp,"Branch not taken")
			elif currentOp[0] == 7:		# Evaluate if less-than
				valPair = self.evalOpPair(currentOp)
				pos = self.programMemory[self.programCounter+3]
				if valPair[0] < valPair[1]:
					result = 1
					if debug_runCPU:
						print("PC =",self.programCounter,"ELT Opcode = ",currentOp,valPair[0],"less than =",valPair[1],"True")
				else:
					result = 0
					if debug_runCPU:
						print("PC =",self.programCounter,"ELT Opcode = ",currentOp,valPair[0],"less than =",valPair[1],"False")
				self.writeOpResult(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 8:		# Evaluate if equal
				valPair = self.evalOpPair(currentOp)
				pos = self.programMemory[self.programCounter+3]
				if valPair[0] == valPair[1]:
					result = 1
					if debug_runCPU:
						print("PC =",self.programCounter,"EEQ does",valPair[0],"equal =",valPair[1],"True")
				else:
					result = 0
					if debug_runCPU:
						print("PC =",self.programCounter,"EEQ does",valPair[0],"equal =",valPair[1],"False")
				self.writeOpResult(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 9:		# Sets relative base register value
				if debug_runCPU:
					print("PC =",self.programCounter,"SBR Opcode = ",currentOp," ")
				self.relativeBaseRegister += self.dealWithOp(currentOp,1)
				if debug_runCPU:
					print("self.relativeBaseRegister =",self.relativeBaseRegister)
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 99:
				if debug_runCPU:
					print("PC =",self.programCounter,"END Opcode = ",currentOp)
				self.progState = 'progDone'
				return 'Done'
			else:
				print("PC =",self.programCounter,"END Opcode = ",currentOp)
				print("error - unexpected opcode", currentOp[0])
				exit()
		assert False,"Unexpected exit of the CPU"


def runToEnd(xVal,yVal):
	""" runToEnd(xVal,yVal)
	Returns the output from the CPU
	"""
	debug_runToEnd = False
#	debug_runToEnd = False
	myCPU = CPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	myCPU.inputQueue.append(xVal)
	if debug_runToEnd:
		print("inputQueue",myCPU.inputQueue)
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	myCPU.inputQueue.append(yVal)
	if debug_runToEnd:
		print("inputQueue",myCPU.inputQueue)
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	if debug_runToEnd:
		print("outputQueue",myCPU.outputQueue)
	retVal = myCPU.outputQueue[0]
	del myCPU.outputQueue[0]
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	return retVal

debug_main = True
#debug_main = False

inTractorBeamCount = 0

yVal = 812
leftX1 = 9999
rightX1 = 0
leftCount = (1017 * yVal) / 1000
rightCount = (1270 * yVal) / 1000
for xVal in range(leftCount,leftCount+5):
	val = runToEnd(xVal,yVal)
	if val == 1:
		if xVal < leftX1:
			leftX1 = xVal

for xVal in range(rightCount-5,rightCount+2):
	val = runToEnd(xVal,yVal)
	if val == 1:
		if xVal > rightX1:
			rightX1 = xVal
			
yVal2 = yVal + 99
leftX2 = 9999
rightX2 = 0
leftCount = (1017 * yVal2) / 1000
rightCount = (1270 * yVal2) / 1000
for xVal in range(leftCount,leftCount+5):
	val = runToEnd(xVal,yVal2)
	if val == 1:
		if xVal < leftX2:
			leftX2 = xVal

for xVal in range(rightCount-5,rightCount):
	val = runToEnd(xVal,yVal2)
	if val == 1:
		if xVal > rightX2:
			rightX2 = xVal

print("result",int(10000*leftX2+yVal))

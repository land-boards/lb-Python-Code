# PtX-AoCDayYY.py
# 2019 Advent of Code
# Day YY
# Part X
# https://adventofcode.com/2019/day/YY

from __future__ import print_function

import os
import sys
import time

"""
	IntCode skeleton

"""

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	
	def __init__(self):
		debug_initCPU = False
		# Class variables
		self.programMemory = []
		self.setProgState('initCPU')
		self.programCounter = 0
		self.relativeBaseRegister = 0
		self.inputQueue = []
		self.outputQueue = []
		# Initialization functions
		self.loadIntCodeProgramToMemory()
		if debug_initCPU:
			print("Memory Dump :",self.programMemory)
		
	def loadIntCodeProgramToMemory(self):
		""" 
		"""
		debug_loadIntCodeProgramToMemory = False
		progName = "input.txt"
		if debug_loadIntCodeProgramToMemory:
			print("Input File Name :",progName)
		with open(progName, 'r') as filehandle:  
			inLine = filehandle.readline()
			self.programMemory = [int(charz) for charz in filehandle.readline().split(',') if True]
		for i in range(10000):	# Some IntCode programs need extra memory past the loaded program
			self.programMemory.append(0)
		if debug_loadIntCodeProgramToMemory:
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
			
	def padInstructionTo5Chars(self, instruction):
		"""Takes a variable length string and packs the front with zeros 
		to make it 5 digits long.
		"""
		if len(instruction) > 5:
			assert False,"padInstructionTo5Chars: Something went wrong with an opcode (more than 5 chars"
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
		Instruction is encoded as 1-5 ASCII characters representing numbers
		ABCDE
		A = mode of 3rd parm
		B = mode of 2nd parm
		C = mode of 1st parm
		DE = opcode
		
		:returns: [opcode,parm1,parm2,parm3]
		"""
		instructionAsFiveDigits = self.padInstructionTo5Chars(instruction)
		parm3=int(instructionAsFiveDigits[0])
		parm2=int(instructionAsFiveDigits[1])
		parm1=int(instructionAsFiveDigits[2])
		opcode=int(instructionAsFiveDigits[3:5])
		retVal=[opcode,parm1,parm2,parm3]
		return retVal

	def evaluatePairOfOpcodes(self, currentOp):
		""" Evaluates the two opcode fields for instruction like ADD, MUL
		Returns the two values as a list pair
		
		:returns: list of the values of the two opcodes
		"""
		debug_BranchEval = False
		if debug_BranchEval:
			print("         evaluatePairOfOpcodes: currentOp =",currentOp)
		val1 = self.handleReadOpcodeAddressingMode(currentOp,1)
		val2 = self.handleReadOpcodeAddressingMode(currentOp,2)
		return[val1,val2]
	
	def handleReadOpcodeAddressingMode(self,currentOp,offsetToOpcodeField):
		""" Interpret opcodes which read program memory
		Input the opcode field and the offsetToOpcodeField to the correct opcode field
		
		:param currentOp: [opcode,parm1,parm2,parm3]
		:param offsetToOpcodeField: Which field of currentOp is being evaluated
		
		"""
		debug_handleReadOpcodeAddressingMode = False
		if currentOp[offsetToOpcodeField] == 0:	# position mode
			val = self.programMemory[self.programMemory[self.programCounter+offsetToOpcodeField]]
			if debug_handleReadOpcodeAddressingMode:
				print("         handleReadOpcodeAddressingMode: Position Mode Parm",offsetToOpcodeField,"pos :",self.programCounter+offsetToOpcodeField,"value =",val)
		elif currentOp[offsetToOpcodeField] == 1:	# immediate mode
			val = self.programMemory[self.programCounter+offsetToOpcodeField]
			if debug_handleReadOpcodeAddressingMode:
				print("         handleReadOpcodeAddressingMode: Immediate Mode parm",offsetToOpcodeField,": value =",val)
		elif currentOp[offsetToOpcodeField] == 2:	# relative mode
			val = self.programMemory[self.programMemory[self.programCounter+offsetToOpcodeField] + self.relativeBaseRegister]
			if debug_handleReadOpcodeAddressingMode:
				print("         handleReadOpcodeAddressingMode: Relative Mode parm",offsetToOpcodeField,": value =",val)
		else:
			assert False,"handleReadOpcodeAddressingMode: WTF-handleReadOpcodeAddressingMode"
		return val
	
	def handleWriteOpcodeAddressingModes(self,opcode,opOffset,val):
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
		ADD_Opcode = 1
		MUL_Opcode = 2
		INP_Opcode = 3
		OUT_Opcode = 4
		JIT_Opcode = 5
		JIF_Opcode = 6
		ELT_Opcode = 7
		EEQ_Opcode = 8
		SBR_Opcode = 9
		END_Opcode = 99
		
		# CPU returns with INPut and OUTput instructions
		while True:
			currentOp = self.extractFieldsFromInstruction(self.programMemory[self.programCounter])
			if currentOp[0] == ADD_Opcode:		# Addition Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"ADD Opcode = ",currentOp," ",end='')
				result = self.handleReadOpcodeAddressingMode(currentOp,1) + self.handleReadOpcodeAddressingMode(currentOp,2)
				if debug_runCPU:
					print(self.handleReadOpcodeAddressingMode(currentOp,1),"+",self.handleReadOpcodeAddressingMode(currentOp,2),"=",result)
				self.handleWriteOpcodeAddressingModes(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == MUL_Opcode:	# Multiplication Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"MUL Opcode = ",currentOp," ",end='')
				result = self.handleReadOpcodeAddressingMode(currentOp,1) * self.handleReadOpcodeAddressingMode(currentOp,2)
				if debug_runCPU:
					print(self.handleReadOpcodeAddressingMode(currentOp,1),"*",self.handleReadOpcodeAddressingMode(currentOp,2),"=",result)
				self.handleWriteOpcodeAddressingModes(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == INP_Opcode:	# Input Operator
				debug_CPUInput = False
#				debug_CPUInput = True
				if debug_runCPU or debug_CPUInput:
					print("PC =",self.programCounter,"INP Opcode = ",currentOp,end='')
				if len(self.inputQueue) == 0:
					if debug_runCPU or debug_CPUInput:
						print(" - Returning to main for input value")
					self.setProgState('waitForInput')
					return
				if debug_runCPU or debug_CPUInput:
					print(" value =",self.inputQueue[0])
				result = self.inputQueue[0]
				self.handleWriteOpcodeAddressingModes(currentOp,1,result)
				del self.inputQueue[0]	 # Empty the input queue
				self.setProgState('inputWasRead')
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == OUT_Opcode:	# Output Operator
				debug_CPUOutput = False
#				debug_CPUOutput = True
				val1 = self.handleReadOpcodeAddressingMode(currentOp,1)
				if debug_runCPU or debug_CPUOutput:
					print("PC =",self.programCounter,"OUT Opcode = ",currentOp,end='')
					print(" value =",val1)
				self.outputQueue.append(val1)
				self.programCounter = self.programCounter + 2
				self.setProgState('outputReady')
				return
			elif currentOp[0] == JIT_Opcode:	# Jump if true
				if self.handleReadOpcodeAddressingMode(currentOp,1) != 0:
					self.programCounter = self.handleReadOpcodeAddressingMode(currentOp,2)
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT Opcode = ",currentOp,"Branch taken")
				else:
					self.programCounter = self.programCounter + 3		
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT Opcode = ",currentOp,"Branch not taken")
			elif currentOp[0] == JIF_Opcode:	# Jump if false
				if self.handleReadOpcodeAddressingMode(currentOp,1) == 0:
					self.programCounter = self.handleReadOpcodeAddressingMode(currentOp,2)
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT Opcode = ",currentOp,"Branch taken")
				else:
					self.programCounter = self.programCounter + 3		
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT currentOp",currentOp,"Branch not taken")
			elif currentOp[0] == ELT_Opcode:	# Evaluate if less-than
				valPair = self.evaluatePairOfOpcodes(currentOp)
				pos = self.programMemory[self.programCounter+3]
				if valPair[0] < valPair[1]:
					result = 1
					if debug_runCPU:
						print("PC =",self.programCounter,"ELT Opcode = ",currentOp,valPair[0],"less than =",valPair[1],"True")
				else:
					result = 0
					if debug_runCPU:
						print("PC =",self.programCounter,"ELT Opcode = ",currentOp,valPair[0],"less than =",valPair[1],"False")
				self.handleWriteOpcodeAddressingModes(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == EEQ_Opcode:	# Evaluate if equal
				valPair = self.evaluatePairOfOpcodes(currentOp)
				pos = self.programMemory[self.programCounter+3]
				if valPair[0] == valPair[1]:
					result = 1
					if debug_runCPU:
						print("PC =",self.programCounter,"EEQ does",valPair[0],"equal =",valPair[1],"True")
				else:
					result = 0
					if debug_runCPU:
						print("PC =",self.programCounter,"EEQ does",valPair[0],"equal =",valPair[1],"False")
				self.handleWriteOpcodeAddressingModes(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == SBR_Opcode:	# Sets relative base register value
				if debug_runCPU:
					print("PC =",self.programCounter,"SBR Opcode = ",currentOp," ",end='')
				self.relativeBaseRegister += self.handleReadOpcodeAddressingMode(currentOp,1)
				if debug_runCPU:
					print("self.relativeBaseRegister =",self.relativeBaseRegister)
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == END_Opcode:	# Program is done
				if debug_runCPU:
					print("PC =",self.programCounter,"END Opcode = ",currentOp)
				self.progState = 'progDone'
				return 'Done'
			else:								# Something went wrong with the opcode
				print("PC =",self.programCounter,"END Opcode = ",currentOp)
				print("error - unexpected opcode", currentOp[0])
				exit()
		assert False,"Unexpected exit of the CPU"

debugAll = False

myCPU = CPU()

debug_main = True
#debug_main = False

# Pt2-AoCDay19.py
# 2019 Advent of Code
# Day 19
# Part 1
# https://adventofcode.com/2019/day/19

from __future__ import print_function

import os
import sys
import time

"""
--- Day 19: Tractor Beam ---
Unsure of the state of Santa's ship, you borrowed the tractor beam technology from Triton. Time to test it out.

When you're safely away from anything else, you activate the tractor beam, but nothing happens. It's hard to tell whether it's working if there's nothing to use it on. Fortunately, your ship's drone system can be configured to deploy a drone to specific coordinates and then check whether it's being pulled. There's even an Intcode program (your puzzle input) that gives you access to the drone system.

The program uses two input instructions to request the X and Y position to which the drone should be deployed. Negative numbers are invalid and will confuse the drone; all numbers should be zero or positive.

Then, the program will output whether the drone is stationary (0) or being pulled by something (1). For example, the coordinate X=0, Y=0 is directly in front of the tractor beam emitter, so the drone control program will always report 1 at that location.

To better understand the tractor beam, it is important to get a good picture of the beam itself. For example, suppose you scan the 10x10 grid of points closest to the emitter:

       X
  0->      9
 0#.........
 |.#........
 v..##......
  ...###....
  ....###...
Y .....####.
  ......####
  ......####
  .......###
 9........##
In this example, the number of points affected by the tractor beam in the 10x10 area closest to the emitter is 27.

However, you'll need to scan a larger area to understand the shape of the beam. How many points are affected by the tractor beam in the 50x50 area closest to the emitter? (For each of X and Y, this will be 0 through 49.)

1250 is too high

"""

debugAll = False

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	progState = ''
	programCounter = 0
	relativeBaseRegister = 0
	
	def getProgState(self):
		#print("getProgState: progState =",self.progState)
		return self.progState
	
	def setProgState(self,state):
		debug_setProgState = False
		self.progState = state
		if debug_setProgState:
			print("setProgState: progState =",self.progState)
			
	def intTo5DigitString(self, instruction):
		"""Takes a variable length string and packs the front with zeros to make it
		5 digits long.
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
		ABCDE
		A = mode of 3rd parm
		B = mode of 2nd parm
		C = mode of 1st parm
		DE = opcode
		
		:returns: [opcode,parm1,parm2,parm3]
		"""
		instructionAsFiveDigits = self.intTo5DigitString(instruction)
		parm3=int(instructionAsFiveDigits[0])
		parm2=int(instructionAsFiveDigits[1])
		parm1=int(instructionAsFiveDigits[2])
		opcode=int(instructionAsFiveDigits[3:5])
		retVal=[opcode,parm1,parm2,parm3]
		return retVal

	def initCPU(self):
		global inputQueue
		global outputQueue
		debug_initCPU = False
		# state transitions are 
		# 'inputReady' => 'waitingOnInput' => 
		# 'inputReady' => 'waitingOnInput' => 
		# 'progDone'
		self.setProgState('initCPU')
		self.programCounter = 0
		self.relativeBaseRegister = 0
		inputQueue = []
		outputQueue = []
		if debug_initCPU:
			print("Memory Dump :",programMemory)
		
	def evalOpPair(self, currentOp):
		debug_BranchEval = False
		if debug_BranchEval:
			print("         evalOpPair: currentOp =",currentOp)
		val1 = self.dealWithOp(currentOp,1)
		val2 = self.dealWithOp(currentOp,2)
		return[val1,val2]
	
	def dealWithOp(self,currentOp,offset):
		global programMemory
		global programCounter
		debug_dealWithOp = False
		if currentOp[offset] == 0:	# position mode
			val = programMemory[programMemory[self.programCounter+offset]]
			if debug_dealWithOp:
				print("         dealWithOp: Position Mode Parm",offset,"pos :",self.programCounter+offset,"value =",val)
		elif currentOp[offset] == 1:	# immediate mode
			val = programMemory[self.programCounter+offset]
			if debug_dealWithOp:
				print("         dealWithOp: Immediate Mode parm",offset,": value =",val)
		elif currentOp[offset] == 2:	# relative mode
			val = programMemory[programMemory[self.programCounter+offset] + self.relativeBaseRegister]
			if debug_dealWithOp:
				print("         dealWithOp: Relative Mode parm",offset,": value =",val)
		else:
			assert False,"dealWithOp: WTF-dealWithOp"
		return val
	
	def writeOpResult(self,opcode,opOffset,val):
		global programMemory
		global programCounter
		debug_writeEqLtResult = False
		if opcode[opOffset] == 0:
			programMemory[programMemory[self.programCounter+opOffset]] = val
			if debug_writeEqLtResult:
				print("         output position mode comparison val =",val)
		elif opcode[opOffset] == 1:
			programMemory[self.programCounter+opOffset] = val
			if debug_writeEqLtResult:
				print("         output immediate mode comparison val =",val,)
		elif opcode[opOffset] == 2:
			programMemory[programMemory[self.programCounter+opOffset] + self.relativeBaseRegister] = val
			if debug_writeEqLtResult:
				print("         output relative mode comparison val =",val,)
	
	def runCPU(self):
#		debug_runCPU = True
		debug_runCPU = False
		global programMemory
		global inputQueue
		global outputQueue
		while(1):
			currentOp = self.extractFieldsFromInstruction(programMemory[self.programCounter])
			#self.getProgState()
			if currentOp[0] == 1:		# Addition Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"ADD Opcode = ",currentOp," ",end='')
				result = self.dealWithOp(currentOp,1) + self.dealWithOp(currentOp,2)
				if debug_runCPU:
					print(self.dealWithOp(currentOp,1),"+",self.dealWithOp(currentOp,2),"=",result)
				self.writeOpResult(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"MUL Opcode = ",currentOp," ",end='')
				result = self.dealWithOp(currentOp,1) * self.dealWithOp(currentOp,2)
				if debug_runCPU:
					print(self.dealWithOp(currentOp,1),"*",self.dealWithOp(currentOp,2),"=",result)
				self.writeOpResult(currentOp,3,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				debug_CPUInput = False
#				debug_CPUInput = True
				if debug_runCPU or debug_CPUInput:
					print("PC =",self.programCounter,"INP Opcode = ",currentOp,end='')
				if len(inputQueue) == 0:
					if debug_runCPU or debug_CPUInput:
						print(" - Returning to main for input value")
					self.setProgState('waitForInput')
					return
				if debug_runCPU or debug_CPUInput:
					print(" value =",inputQueue[0])
				result = inputQueue[0]
				self.writeOpResult(currentOp,1,result)
				del inputQueue[0]	 # Empty the input queue
				if len(inputQueue) != 0:
					assert False,"Still stuff in output queue"
				self.setProgState('inputWasRead')
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				debug_CPUOutput = False
#				debug_CPUOutput = True
				val1 = self.dealWithOp(currentOp,1)
				if debug_runCPU or debug_CPUOutput:
					print("PC =",self.programCounter,"OUT Opcode = ",currentOp,end='')
					print(" value =",val1)
				outputQueue.append(val1)
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
				pos = programMemory[self.programCounter+3]
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
				pos = programMemory[self.programCounter+3]
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
					print("PC =",self.programCounter,"SBR Opcode = ",currentOp," ",end='')
				self.relativeBaseRegister += self.dealWithOp(currentOp,1)
				if debug_runCPU:
					print("relativeBaseRegister =",self.relativeBaseRegister)
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

programMemory = []

def runToEnd(xVal,yVal):
	""" runToEnd(xVal,yVal)
	Returns the output from the CPU
	"""
	global programMemory
	global inputQueue
	global outputQueue
	debug_runToEnd = False
#	debug_runToEnd = False
	# Load program memory from file
	progName = "input.txt"
	if debug_runToEnd:
		print("Input File Name :",progName)
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		programMemory = map(int, inLine.split(','))
	# pad out past end
	for i in range(100):
		programMemory.append(0)
	if debug_runToEnd:
		print(programMemory)
	myCPU = CPU()
	myCPU.initCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	inputQueue.append(xVal)
	if debug_runToEnd:
		print("inputQueue",inputQueue)
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	inputQueue.append(yVal)
	if debug_runToEnd:
		print("inputQueue",inputQueue)
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	if debug_runToEnd:
		print("outputQueue",outputQueue)
	retVal = outputQueue[0]
	del outputQueue[0]
	myCPU.runCPU()
	if debug_runToEnd:
		print("progState :",myCPU.getProgState())
	return retVal

debug_main = True
#debug_main = False

inTractorBeamCount = 0

for yVal in range(0,50):
	rowVal = []
	for xVal in range(0,50):
		# if debug_main:
			# print("main: Providing input val",xVal,yVal)
		inTractorBeamCount += runToEnd(xVal,yVal)
		
print("inTractorBeamCount",inTractorBeamCount)

# Pt1-AoCDay21.py
# 2019 Advent of Code
# Day 21
# Part 1
# https://adventofcode.com/2019/day/21

from __future__ import print_function

import os
import sys
import time

"""
--- Day 21: Springdroid Adventure ---

	You lift off from Pluto and start flying in the direction of Santa.

	While experimenting further with the tractor beam, you accidentally pull an asteroid directly into your ship! It deals significant damage to your hull and causes your ship to begin tumbling violently.

	You can send a droid out to investigate, but the tumbling is causing enough artificial gravity that one wrong step could send the droid through a hole in the hull and flying out into space.

	The clear choice for this mission is a droid that can jump over the holes in the hull - a springdroid.

	You can use an Intcode program (your puzzle input) running on an ASCII-capable computer to program the springdroid. However, springdroids don't run Intcode; instead, they run a simplified assembly language called springscript.

	While a springdroid is certainly capable of navigating the artificial gravity and giant holes, it has one downside: it can only remember at most 15 springscript instructions.

	The springdroid will move forward automatically, constantly thinking about whether to jump. The springscript program defines the logic for this decision.

	Springscript programs only use Boolean values, not numbers or strings. Two registers are available: T, the temporary value register, and J, the jump register. If the jump register is true at the end of the springscript program, the springdroid will try to jump. Both of these registers start with the value false.

	Springdroids have a sensor that can detect whether there is ground at various distances in the direction it is facing; these values are provided in read-only registers. Your springdroid can detect ground at four distances: one tile away (A), two tiles away (B), three tiles away (C), and four tiles away (D). If there is ground at the given distance, the register will be true; if there is a hole, the register will be false.

	There are only three instructions available in springscript:

		AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
		OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
		NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.

	In all three instructions, the second argument (Y) needs to be a writable register (either T or J). The first argument (X) can be any register (including A, B, C, or D).

	For example, the one-instruction program NOT A J means "if the tile immediately in front of me is not ground, jump".

	Or, here is a program that jumps if a three-tile-wide hole (with ground on the other side of the hole) is detected:

	NOT A J
	NOT B T
	AND T J
	NOT C T
	AND T J
	AND D J

	The Intcode program expects ASCII inputs and outputs. It will begin by displaying a prompt; then, input the desired instructions one per line. End each line with a newline (ASCII code 10). When you have finished entering your program, provide the command WALK followed by a newline to instruct the springdroid to begin surveying the hull.

	If the springdroid falls into space, an ASCII rendering of the last moments of its life will be produced. In these, @ is the springdroid, # is hull, and . is empty space. For example, suppose you program the springdroid like this:

	NOT D J
	WALK

	This one-instruction program sets J to true if and only if there is no ground four tiles away. In other words, it attempts to jump into any hole it finds:

	.................
	.................
	@................
	#####.###########

	.................
	.................
	.@...............
	#####.###########

	.................
	..@..............
	.................
	#####.###########

	...@.............
	.................
	.................
	#####.###########

	.................
	....@............
	.................
	#####.###########

	.................
	.................
	.....@...........
	#####.###########

	.................
	.................
	.................
	#####@###########

	However, if the springdroid successfully makes it across, it will use an output instruction to indicate the amount of damage to the hull as a single giant integer outside the normal ASCII range.

	Program the springdroid with logic that allows it to survey the hull without falling into space. What amount of hull damage does it report?
	Your puzzle answer was 19359316.

"""

debugAll = False

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	
	def __init__(self):
		self.programMemory = []
		debug_initCPU = False
		self.setProgState('initCPU')
		self.programCounter = 0
		self.relativeBaseRegister = 0
		self.inputQueue = []
		self.outputQueue = []
		self.loadIntCodeProgram()
		if debug_initCPU:
			print("Memory Dump :",self.programMemory)
		
	def getProgState(self):
		""" Returns the value of the program state variable
		"""
		#print("getProgState: self.progState =",self.progState)
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
		#global self.programMemory
		#global self.programCounter
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
		#global self.programMemory
		#global self.programCounter
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
				# if len(self.inputQueue) != 0:
					# assert False,"Still stuff in input queue"
				self.setProgState('inputWasRead')
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				debug_CPUOutput = False
#				debug_CPUOutput = True
				val1 = self.dealWithOp(currentOp,1)
				if debug_runCPU or debug_CPUOutput:
					print("PC =",self.programCounter,"OUT Opcode = ",currentOp,end='')
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
					print("PC =",self.programCounter,"SBR Opcode = ",currentOp," ",end='')
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

	def loadIntCodeProgram(self):
		""" 
		"""
		#global self.programMemory
		#global self.inputQueue
		#global self.outputQueue
	#	debug_loadIntCodeProgram = True
		debug_loadIntCodeProgram = False
		# Load program memory from file
		progName = "AOC2019D21input.txt"
		if debug_loadIntCodeProgram:
			print("Input File Name :",progName)
		with open(progName, 'r') as filehandle:  
			inLine = filehandle.readline()
			self.programMemory = map(int, inLine.split(','))
		# pad out past end
		for i in range(10000):
			self.programMemory.append(0)
		if debug_loadIntCodeProgram:
			print(self.programMemory)

T_Register = False
J_Register = False

TileA_Value = False
TileB_Value = False
TileC_Value = False
TileD_Value = False

myCPU = CPU()

debug_main = True
#debug_main = False

def uploadSpringScriptProgram(myCPU,springScriptProgram):
	for line in springScriptProgram:
		for charOut in line:
			myCPU.inputQueue.append(ord(charOut))
		myCPU.inputQueue.append(10)
	#print("uploadSpringScriptProgram: myCPU.inputQueue",myCPU.inputQueue)

springScriptProgram = []
springScriptProgram.append('OR A T')	# T = A
springScriptProgram.append('NOT C J')	# J = NOT C
springScriptProgram.append('AND C T')	# T = A AND NOT C
springScriptProgram.append('NOT T J')	# 
springScriptProgram.append('AND D J')	# 
springScriptProgram.append('WALK')		# 

programLoaded = False
progRunning = True
print("Running Springscript Program")
while progRunning:
	myCPU.runCPU()
	state = myCPU.getProgState()
	#print(state)
	if state == 'outputReady':
		try:
			print(str(unichr(myCPU.outputQueue[0])),end='')
		except:
			print(myCPU.outputQueue[0])
		del myCPU.outputQueue[0]
	elif state == 'waitForInput' and not programLoaded:
		uploadSpringScriptProgram(myCPU,springScriptProgram)
		programLoaded = True
	elif state == 'progDone':
		print("Program done")
		progRunning = False

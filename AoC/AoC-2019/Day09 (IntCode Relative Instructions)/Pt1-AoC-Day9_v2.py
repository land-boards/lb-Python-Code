# Pt1-AoCDay9.py
# 2019 Advent of Code
# Day 9
# Part 1
# https://adventofcode.com/2019/day/9

from __future__ import print_function

"""
--- Day 9: Sensor Boost ---
You've just said goodbye to the rebooted rover and left Mars when you receive a faint distress signal coming from the asteroid belt. It must be the Ceres monitoring station!

In order to lock on to the signal, you'll need to boost your sensors. The Elves send up the latest BOOST program - Basic Operation Of System Test.

While BOOST (your puzzle input) is capable of boosting your sensors, for tenuous safety reasons, it refuses to do so until the computer it runs on passes some checks to demonstrate it is a complete Intcode computer.

Your existing Intcode computer is missing one key feature: it needs support for parameters in relative mode.

Parameters in mode 2, relative mode, behave very similarly to parameters in position mode: the parameter is interpreted as a position. Like position mode, parameters in relative mode can be read from or written to.

The important difference is that relative mode parameters don't count from address 0. Instead, they count from a value called the relative base. The relative base starts at 0.

The address a relative mode parameter refers to is itself plus the current relative base. When the relative base is 0, relative mode parameters and position mode parameters with the same value refer to the same address.

For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address 50 + -7 = 43.

The relative base is modified with the relative base offset instruction:

Opcode 9 adjusts the relative base by the value of its only parameter. The relative base increases (or decreases, if the value is negative) by the value of the parameter.
For example, if the relative base is 2000, then after the instruction 109,19, the relative base would be 2019. If the next instruction were 204,-34, then the value at address 1985 would be output.

Your Intcode computer will also need a few other capabilities:

The computer's available memory should be much larger than the initial program. Memory beyond the initial program starts with the value 0 and can be read or written like any other memory. (It is invalid to try to access memory at a negative address, though.)
The computer should have support for large numbers. Some instructions near the beginning of the BOOST program will verify this capability.
Here are some example programs that use these features:

109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a copy of itself as output.
1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
104,1125899906842624,99 should output the large number in the middle.
The BOOST program will ask for a single input; run it in test mode by providing it the value 1. It will perform a series of checks on each opcode, output any opcodes (and the associated parameter modes) that seem to be functioning incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report no malfunctioning opcodes when run in test mode; it should only output a single value, the BOOST keycode. What BOOST keycode does it produce?

203 is too low


"""

debugMessage = False
disassemble = False

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	progState = ''
	programCounter = 0
	relativeBaseRegister = 0
	
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
		# state transitions are 
		# 'inputReady' => 'waitingOnInput' => 
		# 'inputReady' => 'waitingOnInput' => 
		# 'progDone'
		self.progState = 'initInput' 
		self.programCounter = 0
		self.relativeBaseRegister = 0
		
	def evalOpPair(self, currentOp):
		debug_BranchEval = False
		global programMemory
		if debug_BranchEval:
			print("         evalOpPair: currentOp =",currentOp)
		val1 = self.dealWithOp(currentOp,1)
		val2 = self.dealWithOp(currentOp,2)
		return[val1,val2]
	
	def dealWithOp(self,currentOp,offset):
		debug_dealWithOp = False
		if currentOp[offset] == 0:	# position mode
			val1 = programMemory[programMemory[self.programCounter+offset]]
			if debug_dealWithOp:
				print("         dealWithOp: Position Mode Parm",offset,"pos :",self.programCounter+offset,"value =",val1)
		elif currentOp[offset] == 1:	# immediate mode
			val1 = programMemory[self.programCounter+offset]
			if debug_dealWithOp:
				print("         dealWithOp: Immediate Mode parm",offset,": value =",val1)
		elif currentOp[offset] == 2:	# relative mode
			val1 = programMemory[programMemory[self.programCounter+offset] + self.relativeBaseRegister]
			if debug_dealWithOp:
				print("         dealWithOp: Relative Mode parm",offset,": value =",val1)
		else:
			assert False,"dealWithOp: WTF-dealWithOp"
		return val1
	
	def writeOpResult(self,opcode,result):
		global programMemory
		global programCounter
		debug_writeEqLtResult = False
		if opcode == 0:
			programMemory[programMemory[self.programCounter+3]] = result
			if debug_writeEqLtResult:
				print("         output position mode comparison result =",result)
		elif opcode == 1:
			programMemory[self.programCounter+3] = result
			if debug_writeEqLtResult:
				print("         output immediate mode comparison result =",result,)
		elif opcode == 2:
			programMemory[programMemory[self.programCounter+3] + self.relativeBaseRegister] = result
			if debug_writeEqLtResult:
				print("         output relative mode comparison result =",result,)
	
	def runCPU(self):
		debug_runCPU = False
		global inputQueuePtr
		global inputQueue
		global outputQueue
		while(1):
			currentOp = self.extractFieldsFromInstruction(programMemory[self.programCounter])
			#self.getProgState()
			if currentOp[0] == 1:		# Addition Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"ADD")
				result = self.dealWithOp(currentOp,1) + self.dealWithOp(currentOp,2)
				self.writeOpResult(currentOp[3],result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"MUL")
				result = self.dealWithOp(currentOp,1) * self.dealWithOp(currentOp,2)
				self.writeOpResult(currentOp[3],result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				debug_CPUInput = False
				if debug_runCPU or debug_CPUInput:
					print("PC =",self.programCounter,"INP ",end='')
				if inputQueuePtr >= len(inputQueue):
					if debug_runCPU or debug_CPUInput:
						print("inputQueuePtr",inputQueuePtr,"len(inputQueue)",len(inputQueue),end='')
						print("Returning to main for input")
					return
				programMemory[programMemory[self.programCounter+3]] = inputQueue[inputQueuePtr]
				inputQueuePtr = inputQueuePtr + 1
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				debug_CPUOutput = False
				if debug_runCPU or debug_CPUOutput:
					print("PC =",self.programCounter,"OUT")
				val1 = self.dealWithOp(currentOp,1)
				outputQueue.append(val1)
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 5:		# Jump if true
				if self.dealWithOp(currentOp,1) != 0:
					self.programCounter = self.dealWithOp(currentOp,2)
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT currentOp",currentOp,"Branch taken")
				else:
					self.programCounter = self.programCounter + 3		
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT currentOp",currentOp,"Branch not taken")
			elif currentOp[0] == 6:		# Jump if false
				if self.dealWithOp(currentOp,1) == 0:
					self.programCounter = self.dealWithOp(currentOp,2)
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT currentOp",currentOp,"Branch taken")
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
						print("PC =",self.programCounter,"ELT is",valPair[0],"less than =",valPair[1],"True")
				else:
					result = 0
					if debug_runCPU:
						print("PC =",self.programCounter,"ELT is",valPair[0],"less than =",valPair[1],"False")
				self.writeOpResult(currentOp[3],result)
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
				self.writeOpResult(currentOp[3],result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 9:		# Sets relative base register value
				if debug_runCPU:
					print("PC =",self.programCounter,"SBR ",end='')
				self.relativeBaseRegister += self.dealWithOp(currentOp,1)
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 99:
				self.progState = 'progDone'
				return 'Done'
			else:
				print("error - unexpected opcode", currentOp[0])
				exit()
		assert False,"Unexpected exit of the CPU"

inputQueuePtr = 0
inputQueue = []
outputQueuePtr = 0
outputQueue = []

myCPU = CPU()
myCPU.initCPU()

progName = "input.txt"
print("Input File Name :",progName)

programMemory = []

with open(progName, 'r') as filehandle:  
	inLine = filehandle.readline()
	programMemory = map(int, inLine.split(','))
lenOfProgram=len(programMemory)
for i in range(10000):
	programMemory.append(0)
inputQueue.append(2)
myCPU.runCPU()
print("Output Queue :", outputQueue)

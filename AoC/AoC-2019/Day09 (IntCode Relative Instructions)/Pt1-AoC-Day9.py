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
"""

"""
Instead of getting input fed into the function it has to wait on input from the previous stage

"""

debugMessage = False
disassemble = True

programMemory = []

inputQueuePtr = 0
inputQueue = []
outputQueuePtr = 0
outputQueue = []

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	progState = ''
	programCounter = 0
	relativeBaseRegister = 0
	outVal = 0
	
	def evaluateSingleOperation(self,currentOp):
		debugMessage = True
		if debugMessage:
			print("\nevaluateSingleOperation: ",end='')
		if currentOp[1] == 0:	# position mode
			pos = programMemory[self.programCounter+1]
			val1 = programMemory[pos]
			if debugMessage:
				print("Read parm 1 from pos :",pos,"value :",val1,end='')
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[self.programCounter+1]
			if debugMessage:
				print("Immed parm :",val1,end='')
		elif currentOp[1] == 2:	# relative mode
			val1 = programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister]
			print("Rel Mode - Base Reg =",self.relativeBaseRegister,end='')
			print(" op1 val =",val1,end='')
			if debugMessage:
				print(" Rel parm :",val1,end='')
		else:
			print("Unexpected currentOp",currentOp[1])
			exit()
		if debugMessage:
			print(" ")
		debugMessage = False
		return (val1)
	
	def mathOperation(self, currentOp):
		if currentOp[1] == 0:	# position mode
			pos = programMemory[self.programCounter+1]
			val1 = programMemory[pos]
			if debugMessage:
				print("mathOperation: Read parm 1 from pos :",pos,"value :",val1)
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[self.programCounter+1]
			if debugMessage:
				print("mathOperation: Immed parm 1 :",val1)
		elif currentOp[1] == 2:	# relative mode
			val1 = programMemory[self.programCounter+1] + self.relativeBaseRegister
			if debugMessage:
				print("mathOperation: Relative parm 1 :",val1)
		else:
			print("\nmathOperation: Unexpected currentOp[1]",currentOp[1])
			exit()
		if currentOp[2] == 0:	# position mode
			pos = programMemory[self.programCounter+2]
			val2 = programMemory[pos]
			if debugMessage:
				print("mathOperation: Read parm 2 from pos :",pos,"value :",val2)
		elif currentOp[2] == 1:	# immediate mode
			val2 = programMemory[self.programCounter+2]
			if debugMessage:
				print("mathOperation: Immed parm 2 :",val2)
		elif currentOp[2] == 2:	# relative mode
			val1 = programMemory[self.programCounter+2] + self.relativeBaseRegister
			if debugMessage:
				print("mathOperation: Relative parm 2 :",val1)
		else:
			if debugMessage:
				print("mathOperation: Unexpected currentOp[2]",currentOp[2])
			exit()
		if currentOp[3] != 0:	
			print("mathOperation: Error - Should have been position mode not immediate mode")
			exit()
		return[val1,val2]
		
	def branchEval(self, currentOp):
		if debugMessage:
			print("branchEval: Reached function")
		if currentOp[1] == 0:	# position mode
			pos = programMemory[self.programCounter+1]
			val1 = programMemory[pos]
			if debugMessage:
				print("branchEval: Read (parm 1) from pos :",pos,"value :",val1)
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[self.programCounter+1]
			if debugMessage:
				print("branchEval: Immed parm 1 :",val1)
		elif currentOp[1] == 2:	# relative mode
			#TBD
			val1 = programMemory[self.programCounter+1] + self.relativeBaseRegister
			if debugMessage:
				print("branchEval: Relative parm 1 :",val1)
		else:
			pass
			if debugMessage:
				print("branchEval: Unexpected currentOp[1]",currentOp[1])
		if currentOp[2] == 0:	# position mode
			pos = programMemory[self.programCounter+2]
			val2 = programMemory[pos]
			if debugMessage:
				print("branchEval: Read (parm 2) from pos :",pos,"value :",val2)
		elif currentOp[2] == 1:	# immediate mode
			val2 = programMemory[self.programCounter+2]
			if debugMessage:
				print("branchEval: Immed parm 2 :",val2)
		elif currentOp[2] == 2:	# relative mode
			#TBD
			val2 = programMemory[self.programCounter+2]  + self.relativeBaseRegister
			if debugMessage:
				print("branchEval: Relative parm 2 :",val2)
		else:
			pass
			if debugMessage:
				print("branchEval: Unexpected currentOp[2]",currentOp[2])
		return[val1,val2]
	
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
		self.outVal = 0
		
	def runCPU(self):
		if debugMessage:
			print("Reached runCPU")
			print("Length of list is :",len(programMemory))
			print("Memory Dump :",programMemory)
		while(1):
			currentOp = self.extractFieldsFromInstruction(programMemory[self.programCounter])
			if debugMessage:
				print("PC =",self.programCounter,", Opcode",programMemory[self.programCounter],", currentOp",currentOp)
			if currentOp[0] == 1:		# Addition Operator
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"ADD, ",end='')
				valPair = self.mathOperation(currentOp)
				if debugMessage or disassemble:
					print("Values",valPair[0],"+",valPair[1],"= ",end='')
				result = valPair[0] + valPair[1]
				if debugMessage or disassemble:
					print(result," stored at loc :",programMemory[self.programCounter+3])
				programMemory[programMemory[self.programCounter+3]] = result
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"MUL, ",end='')
				valPair = self.mathOperation(currentOp)
				if debugMessage or disassemble:
					print("Values",valPair[0],"*",valPair[1],"= ",end='')
				result = valPair[0] * valPair[1]
				programMemory[programMemory[self.programCounter+3]] = result
				if debugMessage or disassemble:
					print(result," stored at loc :",self.programCounter+3)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"INP, Value :",inputQueue[inputQueuePtr]," from input queue",end='')
				opVal = self.evaluateSingleOperation(currentOp)
				if debugMessage or disassemble:
					print("Value",opVal,end='')
				programMemory[programMemory[opVal]] = inputQueue[inputQueuePtr]
				if debugMessage or disassemble:
					print("Storing at pos :",opVal)
				inputQueuePtr = inputQueuePtr + 1
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"OUT, Location =",self.programCounter+1,", Value = ",end='')
				opVal = self.evaluateSingleOperation(currentOp)
				if debugMessage or disassemble:
					print("Returned opVal =",opVal,"Storing at ",self.programCounter+1)
				programMemory[programMemory[self.programCounter+1]] = opVal
				if debugMessage or disassemble:
					print(programMemory[programMemory[self.programCounter+1]])
				outputQueue.append(programMemory[programMemory[self.programCounter+1]])
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 5:		# Jump if true
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"Jump-if-true opcode")
				valPair = self.branchEval(currentOp)
				if debugMessage:
					print("Jump-if-true parm 1 :",valPair[0])
					print("Jump-if-true parm 2 :",valPair[1])
				if valPair[0] != 0:
					self.programCounter = valPair[1]
				else:
					self.programCounter = self.programCounter + 3
			elif currentOp[0] == 6:		# Jump if false
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"JIF, ")
				valPair = self.branchEval(currentOp)
				if debugMessage:
					print("runCPU: Jump-if-false parm 1 :",valPair[0])
					print("runCPU: Jump-if-false parm 2 :",valPair[1])
				if valPair[0] == 0:
					if debugMessage:
						print("Taking branch")
					self.programCounter = valPair[1]
				else:
					if debugMessage:
						print("Not taking branch")
					self.programCounter = self.programCounter + 3	
			elif currentOp[0] == 7:		# Evaluate if less-than
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"ELT, ")
				valPair = self.branchEval(currentOp)
				if debugMessage:
					print("Evaluate-if-less-than parm 1 :",valPair[0])
					print("Evaluate-if-less-than parm 2 :",valPair[1])
				pos = programMemory[self.programCounter+3]
				if valPair[0] < valPair[1]:
					programMemory[pos] = 1
				else:
					programMemory[pos] = 0
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 8:		# Evaluate if equal
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"EEQ, ")
				valPair = self.branchEval(currentOp)
				if debugMessage:
					print("Evaluate-if-equal parm 1 :",valPair[0])
					print("Evaluate-if-equal parm 2 :",valPair[1])
				pos = programMemory[self.programCounter+3]
				if valPair[0] == valPair[1]:
					programMemory[pos] = 1
				else:
					programMemory[pos] = 0
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 9:		# Sets relative base register value
				self.relativeBaseRegister = self.relativeBaseRegister + programMemory[self.programCounter+1]
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"SBR, Val =",self.relativeBaseRegister)
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 99:
				self.progState = 'progDone'
				if debugMessage:
					pass
					print("CPU program ended normally")
				print("")
				return(-2)
			else:
				print("error - unexpected opcode", currentOp[0])
				exit()
		print("Unexpected exit of the CPU")
		print("self.progState",self.progState)
		return(-9999)

def testCPUOps(object):
	""" Code to test the opcodes and make sure they work as expected
	"""
	# Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
	print("Test case 01A - ",end='')
	inputVal = [7]
	numbers=[3,9,8,9,10,9,4,9,99,-1,8]
	if object.runCPU(numbers,inputVal) == 0:
		print("Passed")
	else:
		print("Failed")
	print("Test case 01B - ",end='')
	inputVal = [8]
	numbers=[3,9,8,9,10,9,4,9,99,-1,8]
	if object.runCPU(numbers,inputVal) == 1:
		print("Passed")
	else:
		print("Failed")

	# Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
	print("Test case 02A - ",end='')
	inputVal = [7]
	numbers=[3,9,7,9,10,9,4,9,99,-1,8]
	if object.runCPU(numbers,inputVal) == 1:
		print("Passed")
	else:
		print("Failed")
	print("Test case 02B - ",end='')
	inputVal = [8]
	numbers=[3,9,7,9,10,9,4,9,99,-1,8]
	if object.runCPU(numbers,inputVal) == 0:
		print("Passed")
	else:
		print("Failed")

	# Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
	print("Test case 03A - ",end='')
	inputVal = [7]
	numbers=[3,3,1108,-1,8,3,4,3,99]
	if object.runCPU(numbers,inputVal) == 0:
		print("Passed")
	else:
		print("Failed")
	print("Test case 03B - ",end='')
	inputVal = [8]
	numbers=[3,3,1108,-1,8,3,4,3,99]
	if object.runCPU(numbers,inputVal) == 1:
		print("Passed")
	else:
		print("Failed")
		
	# Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
	print("Test case 04A - ",end='')
	inputVal = [7]
	numbers=[3,3,1107,-1,8,3,4,3,99]
	if object.runCPU(numbers,inputVal) == 1:
		print("Passed")
	else:
		print("Failed")
	print("Test case 04B - ",end='')
	inputVal = [8]
	numbers=[3,3,1107,-1,8,3,4,3,99]
	if object.runCPU(numbers,inputVal) == 0:
		print("Passed")
	else:
		print("Failed")
		
	#debugMessage = True
	print("Test case 05A - ",end='')
	inputVal = [1]
	numbers=[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
	if debugMessage:
		print("numbers",numbers)
		print("inputVal",inputVal)
	if object.runCPU(numbers,inputVal) == 1:
		print("Passed")
	else:
		print("Failed")
		exit()
		
	print("Test case 05B - ",end='')
	inputVal = [0]
	numbers=[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
	if debugMessage:
		print("05B - numbers :",numbers)
		print("05B - inputVal :",inputVal)
	if object.runCPU(numbers,inputVal) == 0:
		print("Passed")
	else:
		print("Failed")
		exit()

myCPU = CPU()
myCPU.initCPU()

progName = "testCasePt1_2.txt"

with open(progName, 'r') as filehandle:  
	inLine = filehandle.readline()
	programMemory = map(int, inLine.split(','))
#print("Program loaded")
print(" ")
lenOfProgram=len(programMemory)
# Reserve an extra 512B of memory for program
for i in range(512):
	programMemory.append(0)
inputQueue.append(0)
myCPU.runCPU()
print("Output : ",end='')
print("Output Queue :", outputQueue)
print("programMemory :",programMemory)
exit()

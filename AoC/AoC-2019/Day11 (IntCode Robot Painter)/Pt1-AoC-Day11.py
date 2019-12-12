# Pt1-AoCDay11.py
# 2019 Advent of Code
# Day 11
# Part 1
# https://adventofcode.com/2019/day/11

from __future__ import print_function

"""
--- Day 11: Space Police ---
On the way to Jupiter, you're pulled over by the Space Police.

"Attention, unmarked spacecraft! You are in violation of Space Law! All spacecraft must have a clearly visible registration identifier! You have 24 hours to comply or be sent to Space Jail!"

Not wanting to be sent to Space Jail, you radio back to the Elves on Earth for help. Although it takes almost three hours for their reply signal to reach you, they send instructions for how to power up the emergency hull painting robot and even provide a small Intcode program (your puzzle input) that will cause it to paint your ship appropriately.

There's just one problem: you don't have an emergency hull painting robot.

You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid of square panels on the side of your ship, detect the color of its current panel, and paint its current panel black or white. (All of the panels are currently black.)

The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then, the program will output two values:

First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
After the robot turns, it should always move forward exactly one panel. The robot starts facing up.

The robot will continue running for a while like this and halt when it is finished drawing. Do not restart the Intcode computer inside the robot during this process.

For example, suppose the robot is about to start running. Drawing black panels as ., white panels as #, and the robot pointing the direction it is facing (< ^ > v), the initial state and region near the robot looks like this:

.....
.....
..^..
.....
.....
The panel under the robot (not visible here because a ^ is shown instead) is also black, and so any input instructions at this point should be provided 0. Suppose the robot eventually outputs 1 (paint white) and then 0 (turn left). After taking these actions and moving forward one panel, the region now looks like this:

.....
.....
.<#..
.....
.....
Input instructions should still be provided 0. Next, the robot might output 0 (paint black) and then 0 (turn left):

.....
.....
..#..
.v...
.....
After more outputs (1,0, 1,0):

.....
.....
..^..
.##..
.....
The robot is now back where it started, but because it is now on a white panel, input instructions should be provided 1. After several more outputs (0,1, 1,0, 1,0), the area looks like this:

.....
..<#.
...#.
.##..
.....
Before you deploy the robot, you should probably have an estimate of the area it will cover: specifically, you need to know the number of panels it paints at least once, regardless of color. In the example above, the robot painted 6 panels at least once. (It painted its starting panel twice, but that panel is still only counted once; it also never painted the panel it ended on.)

Build a new emergency hull painting robot and run the Intcode program on it. How many panels does it paint at least once?

498 is too low
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
	outVal = 0
	
	def getProgState(self):
		return self.progState
	
	def mathOperation(self, currentOp):
		global debugMessage
		if debugMessage or disassemble:
			print("mathOperation: ")
		if currentOp[1] == 0:	# position mode
			val1 = programMemory[programMemory[self.programCounter+1]]
			if debugMessage or disassemble:
				print("mathOperation: Read parm 1 from pos :",self.programCounter+1,"value :",val1)
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[self.programCounter+1]
			if debugMessage or disassemble:
				print("mathOperation: Immed parm 1 :",val1)
		elif currentOp[1] == 2:	# relative mode
			val1 = programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister]
			if debugMessage or disassemble:
				print("mathOperation: Relative parm 1 :",val1)
		else:
			print("\nmathOperation: Unexpected currentOp[1]",currentOp[1])
			exit()
		if currentOp[2] == 0:	# position mode
			val2 = programMemory[programMemory[self.programCounter+2]]
			if debugMessage:
				print("mathOperation: Read parm 2 from pos :",self.programCounter+1,"value :",val2)
		elif currentOp[2] == 1:	# immediate mode
			val2 = programMemory[self.programCounter+2]
			if debugMessage:
				print("mathOperation: Immed parm 2 :",val2)
		elif currentOp[2] == 2:	# relative mode
			val2 = programMemory[programMemory[self.programCounter+2] + self.relativeBaseRegister]
			if debugMessage:
				print("mathOperation: Relative parm 2 :",val1)
		else:
			if debugMessage:
				print("mathOperation: Unexpected currentOp[2]",currentOp[2])
			exit()
		# if currentOp[3] != 0:
			# print("currentOp[3]",currentOp[3])
			# assert False,"mathOperation: Error - Should have been position"
		return[val1,val2]
		
	def branchEval(self, currentOp):
		if debugMessage or disassemble:
			print("branchEval: Reached function currentOp =",currentOp)
		if currentOp[1] == 0:	# position mode
			val1 = programMemory[programMemory[self.programCounter+1]]
			if debugMessage or disassemble:
				print("branchEval: Read (parm 1) from pos :",self.programCounter+1,"value :",val1)
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[self.programCounter+1]
			if debugMessage or disassemble:
				print("branchEval: Immed parm 1 :",val1)
		elif currentOp[1] == 2:	# relative mode
			val1 = programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister]
			if debugMessage or disassemble:
				print("branchEval: Relative parm 1 :",val1)
		else:
			assert False,"branchEval: WTF-1"
			
		if currentOp[2] == 0:	# position mode
			val2 = programMemory[programMemory[self.programCounter+2]]
			if debugMessage:
				print("branchEval: Read (parm 2) from pos :",self.programCounter+2,"value :",val2)
		elif currentOp[2] == 1:	# immediate mode
			val2 = programMemory[self.programCounter+2]
			if debugMessage:
				print("branchEval: Immed parm 2 :",val2)
		elif currentOp[2] == 2:	# relative mode
			#TBD
			val2 = programMemory[programMemory[self.programCounter+2]  + self.relativeBaseRegister]
			if debugMessage:
				print("branchEval: Relative parm 2 :",val2)
		else:
			assert False,"branchEval: WTF-2"
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
		
	def mathOut(self,outType,outVal):
		if outType == 0:		# position mode
			programMemory[programMemory[self.programCounter+3]] = outVal					
		elif outType == 1:	# immediate mode
			programMemory[self.programCounter+3] = outVal
			assert False,"multiply in immediate mode"
		elif outType == 2:	# relative mode
			programMemory[programMemory[self.programCounter+3] + self.relativeBaseRegister] = outVal
	
	def runCPU(self):
		global inputQueuePtr
		global inputQueue
		global disassemble
		if debugMessage:
			print("Reached runCPU")
			print("Length of list is :",len(programMemory))
			print("Memory Dump :",programMemory)
		while(1):
			currentOp = self.extractFieldsFromInstruction(programMemory[self.programCounter])
			if debugMessage:
				print("PC =",self.programCounter,", Opcode",programMemory[self.programCounter],", currentOp",currentOp)
			if currentOp[0] == 1:		# Addition Operator
				valPair = self.mathOperation(currentOp)
				result = valPair[0] + valPair[1]
				self.mathOut(currentOp[3],result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				valPair = self.mathOperation(currentOp)
				result = valPair[0] * valPair[1]
				self.mathOut(currentOp[3],result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				if debugMessage or disassemble:
					if inputQueuePtr >= len(inputQueue):
						print("Waiting on input")
						return 'waitForInput'
					print("PC =",self.programCounter,"INP, Value :",inputQueue[inputQueuePtr]," from input queue ",end='')
					inputQueuePtr += 1
				if currentOp[1] == 0:	# position mode
					programMemory[self.programCounter+3] = inputQueue[0]
					#assert False," INPut position value"
				elif currentOp[1] == 1:	# immediate mode
					assert False," INPut immediate value"
				elif currentOp[1] == 2:	# relative mode
					programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister] = inputQueue[inputQueuePtr]
					inputQueuePtr = inputQueuePtr + 1
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"OUT, Location =",self.programCounter+1,", Value = ",end='')
				if currentOp[1] == 0:	# position mode
					val1 = programMemory[programMemory[self.programCounter+1]]
					if debugMessage or disassemble:
						print("Read parm 1 from pos :",programMemory[self.programCounter+1],"value :",val1,end='')
					programMemory[programMemory[self.programCounter+1]] = val1
					outputQueue.append(val1)
				elif currentOp[1] == 1:	# immediate mode
					val1 = programMemory[self.programCounter+1]
#					programMemory[self.programCounter+1] = val1
					if debugMessage or disassemble:
						print("Immed parm :",val1,end='')
					outputQueue.append(val1)
				elif currentOp[1] == 2:	# relative mode
					val1 = programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister]
					programMemory[programMemory[self.programCounter+1]] = val1
					if debugMessage or disassemble:
						print("Rel Mode - Base Reg =",self.relativeBaseRegister,end='')
						print(" op1 val =",val1,end='')
					if debugMessage or disassemble:
						print(" Rel parm :",val1,end='')
					outputQueue.append(val1)
				else:
					print("Unexpected currentOp",currentOp[1])
					exit()
				if debugMessage or disassemble:
						print(" end of OUT")
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 5:		# Jump if true
				valPair = self.branchEval(currentOp)
				if valPair[0] != 0:
					self.programCounter = valPair[1]
				else:
					self.programCounter = self.programCounter + 3		
			elif currentOp[0] == 6:		# Jump if false
				valPair = self.branchEval(currentOp)
				if valPair[0] == 0:
					self.programCounter = valPair[1]
				else:
					self.programCounter = self.programCounter + 3	
			elif currentOp[0] == 7:		# Evaluate if less-than
				valPair = self.branchEval(currentOp)
				pos = programMemory[self.programCounter+3]
				result = 0
				if valPair[0] < valPair[1]:
					result = 1
				else:
					result = 0
				if currentOp[3] == 0:
					programMemory[programMemory[self.programCounter+3]] = result
				elif currentOp[3] == 1:
					programMemory[self.programCounter+3] = result
				elif currentOp[3] == 2:
					programMemory[programMemory[self.programCounter+3] + self.relativeBaseRegister] = result
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 8:		# Evaluate if equal
				if debugMessage or disassemble:
					print("PC =",self.programCounter,"EEQ, ")
				valPair = self.branchEval(currentOp)
				if debugMessage:
					print("Evaluate-if-equal parm 1 :",valPair[0])
					print("Evaluate-if-equal parm 2 :",valPair[1])
				pos = programMemory[self.programCounter+3]
				result = 0
				if valPair[0] == valPair[1]:
					result = 1
				else:
					result = 0
				if currentOp[3] == 0:
					programMemory[programMemory[self.programCounter+3]] = result
				elif currentOp[3] == 1:
					programMemory[self.programCounter+3] = result
				elif currentOp[3] == 2:
					programMemory[programMemory[self.programCounter+3] + self.relativeBaseRegister] = result
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 9:		# Sets relative base register value
				if currentOp[1] == 0:
					self.relativeBaseRegister = self.relativeBaseRegister + programMemory[programMemory[self.programCounter+1]]
				elif currentOp[1] == 1:
					self.relativeBaseRegister = self.relativeBaseRegister + programMemory[self.programCounter+1]
				elif currentOp[1] == 2:
					self.relativeBaseRegister = self.relativeBaseRegister + programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister]
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 99:
				self.progState = 'progDone'
				return 'Done'
			else:
				print("error - unexpected opcode", currentOp[0])
				exit()
		assert False,"Unexpected exit of the CPU"

myCPU = CPU()
myCPU.initCPU()

progName = "input.txt"
print("Input File Name :",progName)

directionArrows = ['<','^','>','v']
currentRobotLocation = [0,0,0]
currentDirection = '^'
colors = ['Black','White']
currentColor = 'Black'

programMemory = []

inputQueuePtr = 0
inputQueue = []
outputQueuePtr = 0
outputQueue = []

with open(progName, 'r') as filehandle:  
	inLine = filehandle.readline()
	programMemory = map(int, inLine.split(','))
lenOfProgram=len(programMemory)
for i in range(1000):
	programMemory.append(0)
inputQueue.append(0)
while True:
	myCPU.runCPU()
	progStateVal = myCPU.getProgState()
	if progStateVal == 'progDone':
		print("Reached end of program")
		break
	elif progStateVal == 'waitForInput':
		print("outputQueue",outputQueue)
		inputQueue.append(outputQueue[outputQueuePtr])
		outputQueuePtr += 1
	else:
		print("progStateVal =",progStateVal)
		assert False,"weirdo"
print("Output Queue :", outputQueue)
paintedCount = 0
for item in outputQueue:
	if item >= 1:
		paintedCount += 1
print("paintedCount=",paintedCount)

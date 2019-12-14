# Pt2-AoCDay13.py
# 2019 Advent of Code
# Day 13
# Part 2
# https://adventofcode.com/2019/day/13

from __future__ import print_function

"""
1092 is too high
380 is the right answer
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
		debug_initCPU = False
		# state transitions are 
		# 'inputReady' => 'waitingOnInput' => 
		# 'inputReady' => 'waitingOnInput' => 
		# 'progDone'
		self.setProgState('initCPU')
		self.programCounter = 0
		self.relativeBaseRegister = 0
		if debug_initCPU:
			print("Memory Dump :",programMemory)
		
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
	
	def writeOp3Result(self,opcode,result):
		global programMemory
		global programCounter
		debug_writeEqLtResult = False
		if opcode[3] == 0:
			programMemory[programMemory[self.programCounter+3]] = result
			if debug_writeEqLtResult:
				print("         output position mode comparison result =",result)
		elif opcode[3] == 1:
			programMemory[self.programCounter+3] = result
			if debug_writeEqLtResult:
				print("         output immediate mode comparison result =",result,)
		elif opcode[3] == 2:
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
				valPair = self.evalOpPair(currentOp)
				result = valPair[0] + valPair[1]
				self.writeOp3Result(currentOp,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"MUL")
				valPair = self.evalOpPair(currentOp)
				result = valPair[0] * valPair[1]
				self.writeOp3Result(currentOp,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				debug_CPUInput = False
				if debug_runCPU or debug_CPUInput:
					print("PC =",self.programCounter,"INP ",end='')
				if inputQueuePtr >= len(inputQueue):
					if debug_runCPU or debug_CPUInput:
						print("inputQueuePtr",inputQueuePtr,"len(inputQueue)",len(inputQueue),"Returning to main loop for input")
					return
				if currentOp[1] == 0:	# position mode
					if debug_runCPU or debug_CPUInput:
						print("Position mode inputQueuePtr =",inputQueuePtr,"Value :",inputQueue[inputQueuePtr])
					programMemory[self.programCounter+3] = inputQueue[inputQueuePtr]
					inputQueuePtr += 1
				elif currentOp[1] == 1:	# immediate mode
					if debug_runCPU or debug_CPUInput:
						print("Value Immediate mode from input queue,",inputQueue[inputQueuePtr],"Taking Value :",inputQueue[inputQueuePtr]," from input queue, ")
					assert False," INPut immediate value"
				elif currentOp[1] == 2:	# relative mode
					if debug_runCPU or debug_CPUInput:
						print("Value :",inputQueue[inputQueuePtr],"Relative  mode from input queue, ",end='')
					programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister] = inputQueue[inputQueuePtr]
					inputQueuePtr = inputQueuePtr + 1
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				debug_CPUOutput = False
				if debug_runCPU or debug_CPUOutput:
					print("PC =",self.programCounter,"OUT ",end='')
				if currentOp[1] == 0:	# position mode
					val1 = programMemory[programMemory[self.programCounter+1]]
					if debug_runCPU or debug_CPUOutput:
						print("Position Mode, Location =",self.programCounter+1," Read parm from pos :",programMemory[self.programCounter+1],"value :",val1)
					outputQueue.append(val1)
				elif currentOp[1] == 1:	# immediate mode
					val1 = programMemory[self.programCounter+1]
					if debug_runCPU or debug_CPUOutput:
						print("Immediate value from location =",self.programCounter+1,", Value = ",val1)
					outputQueue.append(val1)
				elif currentOp[1] == 2:	# relative mode
					val1 = programMemory[programMemory[self.programCounter+1] + self.relativeBaseRegister]
					if debug_runCPU or debug_CPUOutput:
						print("Relative Mode Location =",self.programCounter+1," Base Reg =",self.relativeBaseRegister,"value :",val1)
					outputQueue.append(val1)
				else:
					assert False,"OUT: Unexpected currentOp"
					exit()
				self.programCounter = self.programCounter + 2
			elif currentOp[0] == 5:		# Jump if true
				valPair = self.evalOpPair(currentOp)
				if valPair[0] != 0:
					self.programCounter = valPair[1]
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT currentOp",currentOp,"Branch taken")
				else:
					self.programCounter = self.programCounter + 3		
					if debug_runCPU:
						print("PC =",self.programCounter,"JIT currentOp",currentOp,"Branch not taken")
			elif currentOp[0] == 6:		# Jump if false
				valPair = self.evalOpPair(currentOp)
				if valPair[0] == 0:
					self.programCounter = valPair[1]
					if debug_runCPU:
						print("PC =",self.programCounter,"JIF currentOp",currentOp,"Branch taken")
				else:
					self.programCounter = self.programCounter + 3	
					if debug_runCPU:
						print("PC =",self.programCounter,"JIF currentOp",currentOp,"Branch not taken")
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
				self.writeOp3Result(currentOp,result)
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
				self.writeOp3Result(currentOp,result)
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

# Initialize queues
inputQueuePtr = 0
inputQueue = []
outputQueuePtr = 0
outputQueue = []

# Load program memory from file
progName = "input.txt"
print("Input File Name :",progName)
programMemory = []
with open(progName, 'r') as filehandle:  
	inLine = filehandle.readline()
	programMemory = map(int, inLine.split(','))
lenOfProgram=len(programMemory)
for i in range(100):
	programMemory.append(0)

# start up the CPU
myCPU = CPU()
myCPU.initCPU()

step = 0
finalStep = 10

# Run the CPU until program terminates
while step < finalStep:
	debug_main = True
	myCPU.runCPU()
	progStateVal = myCPU.getProgState()
	print("progStateVal",progStateVal)
	if progStateVal == 'progDone':
		print("Reached end of program")
		break
	step += 1
print("Output Queue :", outputQueue)
print("Length divided by 3 is",len(outputQueue)/3)
blockCount = 0
for step in range(2,len(outputQueue),3):
	print("step",step)
	if outputQueue[step]==2:
		blockCount += 1
print(blockCount)

	
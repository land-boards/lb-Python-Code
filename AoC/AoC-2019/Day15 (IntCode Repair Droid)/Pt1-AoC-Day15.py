# Pt1-AoCDay15.py
# 2019 Advent of Code
# Day 15
# Part 1
# https://adventofcode.com/2019/day/15

from __future__ import print_function

import os
import sys
import time

"""
--- Day 15: Oxygen System ---
Out here in deep space, many things can go wrong. Fortunately, many of those things have indicator lights. Unfortunately, one of those lights is lit: the oxygen system for part of the ship has failed!

According to the readouts, the oxygen system must have failed days ago after a rupture in oxygen tank two; that section of the ship was automatically sealed once oxygen levels went dangerously low. A single remotely-operated repair droid is your only option for fixing the oxygen system.

The Elves' care package included an Intcode program (your puzzle input) that you can use to remotely control the repair droid. By running that program, you can direct the repair droid to the oxygen system and fix the problem.

The remote control program executes the following steps in a loop forever:

Accept a movement command via an input instruction.
Send the movement command to the repair droid.
Wait for the repair droid to finish the movement operation.
Report on the status of the repair droid via an output instruction.
Only four movement commands are understood: north (1), south (2), west (3), and east (4). Any other command is invalid. The movements differ in direction, but not in distance: in a long enough east-west hallway, a series of commands like 4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

The repair droid can reply with any of the following status codes:

0: The repair droid hit a wall. Its position has not changed.
1: The repair droid has moved one step in the requested direction.
2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
You don't know anything about the area around the repair droid, but you can figure it out by watching the status codes.

For example, we can draw the area using D for the droid, # for walls, . for locations the droid can traverse, and empty space for unexplored locations. Then, the initial state looks like this:

      
      
   D  
      
      
To make the droid go north, send it 1. If it replies with 0, you know that location is a wall and that the droid didn't move:

      
   #  
   D  
      
      
To move east, send 4; a reply of 1 means the movement was successful:

      
   #  
   .D 
      
      
Then, perhaps attempts to move north (1), south (2), and east (4) are all met with replies of 0:

      
   ## 
   .D#
    # 
      
Now, you know the repair droid is in a dead end. Backtrack with 3 (which you already know will get a reply of 1 because you already know that location is open):

      
   ## 
   D.#
    # 
      
Then, perhaps west (3) gets a reply of 0, south (2) gets a reply of 1, south again (2) gets a reply of 0, and then west (3) gets a reply of 2:

      
   ## 
  #..#
  D.# 
   #  
Now, because of the reply of 2, you know you've found the oxygen system! In this example, it was only 2 moves away from the repair droid's starting position.

What is the fewest number of movement commands required to move the repair droid from its starting position to the location of the oxygen system?

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
		global inputQueue
		global outputQueue
		while(1):
			currentOp = self.extractFieldsFromInstruction(programMemory[self.programCounter])
			#self.getProgState()
			if currentOp[0] == 1:		# Addition Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"ADD")
				result = self.dealWithOp(currentOp,1) + self.dealWithOp(currentOp,2)
				self.writeOp3Result(currentOp,result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				if debug_runCPU:
					print("PC =",self.programCounter,"MUL")
				result = self.dealWithOp(currentOp,1) * self.dealWithOp(currentOp,2)
				self.writeOp3Result(currentOp,result)
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
				programMemory[programMemory[self.programCounter+1]] = inputQueue[0]
				if debug_runCPU or debug_CPUInput:
					print(" value =",inputQueue[0])
				del inputQueue[0]
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
inputQueue = []
outputQueue = []

# Load program memory from file
progName = "input.txt"
print("Input File Name :",progName)
programMemory = []
with open(progName, 'r') as filehandle:  
	inLine = filehandle.readline()
	programMemory = map(int, inLine.split(','))
lenOfProgram=len(programMemory)
for i in range(5000):
	programMemory.append(0)

# start up the CPU
myCPU = CPU()
myCPU.initCPU()

anchorLoc = [0,0]
walls = []
openLocs = []
openLocs.append(anchorLoc)
scannedLocs = []
moveState = 'arrivedInBlock'
testingState = 'arrivedInBlock'
destLoc = []

step = 0
while step < 10:
	debug_main = True
	step += 1
	myCPU.runCPU()
	progStateVal = myCPU.getProgState()
	if progStateVal == 'outputReady':
		robotStatus = outputQueue[0]
		if debug_main:
			print("\noutput: outputQueue        :",outputQueue)
		if robotStatus == 0:	# Robot hit wall
			if debug_main:
				print("output: Move hit wall")
				print("output: testingState =",testingState)
				print("output: currentLoc = ",currentLoc)
			if testingState == 'testingNorth':
				walls.append([currentLoc[0],currentLoc[1]+1])
			elif testingState == 'testingSouth':
				walls.append([currentLoc[0],currentLoc[1]-1])
			elif testingState == 'testingEast':
				walls.append([currentLoc[0]+1,currentLoc[1]])
			elif testingState == 'testingWest':
				walls.append([currentLoc[0]-1,currentLoc[1]])
			else:
				print("outputQueue - bad testingState",testingState)
				assert False,"outputQueue - bad testingState"
			moveState = 'hitWall'
			if debug_main:
				print("output: Robot hit wall at",walls[:len(walls)])
		elif robotStatus == 1:	# Robot moved
			if debug_main:
				print("Robot moved ")
			if testingState == 'testingNorth':
				if debug_main:
					print("Checked North")
				openLocs.append(currentLoc)
				currentLoc[1] -= 1
				testingState = 'testingSouth'
			elif testingState == 'testingSouth':
				if debug_main:
					print("Checked South")
				openLocs.append([currentLoc[0],currentLoc[1]-1])
				currentLoc[1] += 1
				testingState = 'testingEast'
			elif testingState == 'testingEast':
				if debug_main:
					print("Checked East")
				openLocs.append([currentLoc[0]+1,currentLoc[1]])
				currentLoc[0] += 1
				testingState = 'testingEast'
			elif testingState == 'testingWest':
				if debug_main:
					print("Checked West")
				openLocs.append([currentLoc[0]-1,currentLoc[1]])
				currentLoc[0] -= 1
				testingState = 'testingEast'
			if debug_main:
				print("Added to openLocs",openLocs)
			print("Robot moved OK added to openLocs",openLocs)
		elif robotStatus == 2:	# Robot is at destination
			if debug_main:
				print("Robot has arrived at destination",destLoc)
			destLoc.append(currentLoc)
			assert False,"Robot has arrived at destination"
		else:
			assert False,"Got bogus output"
		del outputQueue[0]
	elif progStateVal == 'waitForInput':
		if debug_main:
			print("\ninput: progStateVal        :",progStateVal)
			print("input: testingState        :",testingState)
			print("input: inputQueue (before) :",inputQueue)
		currentLoc = anchorLoc
		if debug_main:
			print("input: currentLoc          :",currentLoc)
		if testingState == 'arrivedInBlock':
			inputQueue.append(1)
			testingState='testingNorth'
		elif testingState == 'testingNorth':
			inputQueue.append(2)
			testingState='testingSouth'
		elif testingState == 'testingSouth':
			inputQueue.append(3)
			testingState='testingWest'
		elif testingState == 'testingWest':
			inputQueue.append(4)
			testingState='testingEast'
		elif testingState == 'testingWest':
			testingState = 'doneInBlock'
			assert False,"wait on input"
		if debug_main:
			print("input: inputQueue (after)  :",inputQueue)
	elif progStateVal == 'progDone':
		print("Reached end of IntCode program")
		break
	else:
		assert False,"bad progStateVal"

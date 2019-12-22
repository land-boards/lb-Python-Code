# Pt2-AoCDay19.py
# 2019 Advent of Code
# Day 19
# Part 
# https://adventofcode.com/2019/day/19

from __future__ import print_function

import os
import sys
import time

"""
--- Part Two ---
You aren't sure how large Santa's ship is. You aren't even sure if you'll need to use this thing on Santa's ship, but it doesn't hurt to be prepared. You figure Santa's ship might fit in a 100x100 square.

The beam gets wider as it travels away from the emitter; you'll need to be a minimum distance away to fit a square of that size into the beam fully. (Don't rotate the square; it should be aligned to the same axes as the drone grid.)

For example, suppose you have the following tractor beam readings:

#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########
In this example, the 10x10 square closest to the emitter that fits entirely within the tractor beam has been marked O. Within it, the point closest to the emitter (the only highlighted O) is at X=25, Y=20.

Find the 100x100 square closest to the emitter that fits entirely within the tractor beam; within that square, find the point closest to the emitter. What value do you get if you take that point's X coordinate, multiply it by 10000, then add the point's Y coordinate? (In the example above, this would be 250020.)

Your puzzle answer was 9290812.

Both parts of this puzzle are complete! They provide two gold stars: **

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

# print("012345678901234567890123456789012345678901234567890123456789012345678901234")
# for yVal in range(45,50):
	# rowVal = []
	# for xVal in range(0,50):
		# if debug_main:
			# print("main: Providing input val",xVal,yVal)
		# val = runToEnd(xVal,yVal)
		# inTractorBeamCount += val
		# if val == 1:
			# print("o",end='')
		# else:
			# print(".",end='')
	# print(" < ",yVal)
		
# print("inTractorBeamCount",inTractorBeamCount)

yVal = 812
leftX1 = 9999
rightX1 = 0
leftCount = (1017 * yVal) / 1000
rightCount = (1270 * yVal) / 1000
print("012345678901234567890123456789012345678901234567890123456789012345678901234")
for xVal in range(leftCount,leftCount+5):
	# if debug_main:
		# print("main: Providing input val",xVal,yVal)
	val = runToEnd(xVal,yVal)
	if val == 1:
		print("o",end='')
		if xVal < leftX1:
			leftX1 = xVal
	else:
		print(".",end='')
print(" < ",yVal)

for xVal in range(rightCount-5,rightCount+2):
	# if debug_main:
		# print("main: Providing input val",xVal,yVal)
	val = runToEnd(xVal,yVal)
	if val == 1:
		print("o",end='')
		if xVal > rightX1:
			rightX1 = xVal
	else:
		print(".",end='')
print(" < ",yVal)

print("leftX1",leftX1,"yVal",yVal)
print("rightX1",rightX1,"yVal",yVal)
print("delta",rightX1-leftX1)

yVal2 = yVal + 99
leftX2 = 9999
rightX2 = 0
leftCount = (1017 * yVal2) / 1000
rightCount = (1270 * yVal2) / 1000
print("012345678901234567890123456789012345678901234567890123456789012345678901234")
for xVal in range(leftCount,leftCount+5):
	# if debug_main:
		# print("main: Providing input val",xVal,yVal2)
	val = runToEnd(xVal,yVal2)
	if val == 1:
		print("o",end='')
		if xVal < leftX2:
			leftX2 = xVal
	else:
		print(".",end='')
print(" < ",yVal2)

for xVal in range(rightCount-5,rightCount):
	# if debug_main:
		# print("main: Providing input val",xVal,yVal2)
	val = runToEnd(xVal,yVal2)
	if val == 1:
		print("o",end='')
		if xVal > rightX2:
			rightX2 = xVal
	else:
		print(".",end='')
print(" < ",yVal2)

print("leftX2",leftX2,"yVal2",yVal2)
print("rightX2",rightX2,"yVal2",yVal2)
print("delta",rightX1-leftX2+1)
print("result",10000*leftX2+yVal)

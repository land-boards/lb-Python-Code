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
	outVal = 0
	
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
		self.setProgState('initCPU' )
		self.programCounter = 0
		self.relativeBaseRegister = 0
		self.outVal = 0
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
		global outputQueuePtr
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
						print("Returning to main loop for input")
					self.setProgState('waitForInput')
					return
				if currentOp[1] == 0:	# position mode
					if debug_runCPU or debug_CPUInput:
						print("Position mode, Value :",inputQueue[inputQueuePtr],"inputQueuePtr = ",inputQueuePtr)
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

def moveRobot(currentLocation,currentDirection,newTurn):
	debugMoveRobot = False
	if debugMoveRobot:
		print("\n@moveRobot : currentLocation",currentLocation)
		print("@moveRobot : currentDirection",currentDirection)
		print("@moveRobot : newTurn",newTurn)
	xVal = currentLocation[0]
	yVal = currentLocation[1]
	if newTurn == '<':
		if currentDirection == '^':
			resultingDirection = '<'
			newLocation = [xVal-1,yVal]
		elif currentDirection == '<':
			resultingDirection = 'v'
			newLocation = [xVal,yVal-1]
		elif currentDirection == '>':
			resultingDirection = '^'
			newLocation = [xVal,yVal+1]
		elif currentDirection == 'v':
			resultingDirection = '>'
			newLocation = [xVal-1,yVal]
		else:
			assert False,"moveRobot : bad current direction"
	elif newTurn == '>':
		if currentDirection == '^':
			resultingDirection = '>'
			newLocation = [xVal+1,yVal]
		elif currentDirection == '<':
			resultingDirection = '^'
			newLocation = [xVal,yVal+1]
		elif currentDirection == '>':
			resultingDirection = 'v'
			newLocation = [xVal,yVal-1]
		elif currentDirection == 'v':
			resultingDirection = '<'
			newLocation = [xVal-1,yVal]
		else:
			assert False,"moveRobot : bad current direction"
	else:
		assert False,"moveRobot: Illegal direction"
	retVec = [newLocation[0],newLocation[1],resultingDirection]
	if debugMoveRobot:
		print("@moveRobot : returning",retVec)
	return retVec

def getColor(pointList,currentPointLocation,colorsList):
	debug_getColor = False
	if currentPointLocation not in pointList:
		if debug_getColor:
			print("@getColor current point is not in the list so current color is black")
		return 0
	else:
		pass
		if debug_getColor:
			print("@getColor current point is in the list")
	for count in range(len(pointList)):
		if pointList[count] == currentPointLocation:
			if debug_getColor:
				print("@getColor color at point is",colorsList[count])
			return colorsList[count]

def bAndWText(colorCode):
	if colorCode == 0:
		return("black")
	elif colorCode == 1:
		return("white")
	else:
		assert False,"illegal color"
	
def turnsText(turnCode):
	if turnCode == '^':
		return("up")
	elif turnCode == '>':
		return("right")
	elif turnCode == 'v':
		return("down")
	elif turnCode == '<':
		return("left")
	else:
		assert False,"illegal color"
		
# Initialize queues
inputQueuePtr = 0
inputQueue = []
outputQueuePtr = 0
outputQueue = []
#inputQueue.append(0)

# Initialize robot states
currentRobotLocation = []
currentDirection = ''
pointsOnPath = []
colorsOnPath = []

# Load program memory from file
progName = "input.txt"
print("Input File Name :",progName)
programMemory = []
with open(progName, 'r') as filehandle:  
	inLine = filehandle.readline()
	programMemory = map(int, inLine.split(','))
lenOfProgram=len(programMemory)
for i in range(10000):
	programMemory.append(0)

# start up the CPU
myCPU = CPU()
myCPU.initCPU()

# Run the CPU until program terminates
while True:
	debug_main = False
	myCPU.runCPU()
	progStateVal = myCPU.getProgState()
	if progStateVal == 'progDone':
		print("Reached end of program")
		break
	elif progStateVal == 'waitForInput':
		if len(inputQueue) != 0:
			# first value is color (0=black, 1=white)
			# second value is direction (0 = left, 1 = right)
			if debug_main:
				print("\n@main currentRobotLocation     =",currentRobotLocation)
				print("@main Before move pointsOnPath =",pointsOnPath)
				print("@main Before move colorsOnPath =",colorsOnPath)
				print("@main CPU outputQueue          =",outputQueue)
				print("      Paint the block          = ",end='')
				print(bAndWText(outputQueue[len(outputQueue)-2]))
			pointsOnPath.append(currentRobotLocation)
			colorsOnPath.append(currentColor)
			newColor = outputQueue[len(outputQueue)-2]
			if newColor != 0 and newColor != 1:
				print("Error\n@main bad color",newColor)
				assert False,"Bad color received from output routine"
			if (outputQueue[len(outputQueue)-1] == 0):
				turnLeftRight = '<'
			elif (outputQueue[len(outputQueue)-1] == 1):
				turnLeftRight = '>'
			else:
				print("\n@main Error outputQueue",outputQueue)
				print("@main New robot location",currentRobotLocation,"painting color",currentColor)
				print("@main pointsOnPath (after)",pointsOnPath)
				print("@main colorsOnPath (after)",colorsOnPath)
				assert False,"Bad direction"
			if debug_main:
				print("      Turn (relative) is       =",turnsText(turnLeftRight))
				print("@main Before move direction    =",turnsText(currentDirection))
			currentColor = getColor(pointsOnPath,currentDirection,colorsOnPath)
			if currentColor != 0 and currentColor != 0:
				print("@main got back a bad color from getColor",currentColor)
				assert False,"@main back color from getColor"
			else:
				myCPU.setProgState('gotInput')
			newVals = moveRobot(currentRobotLocation,currentDirection,turnLeftRight)
			if debug_main:
				print("@main Before move location     =",currentRobotLocation)
			currentRobotLocation = newVals[0:2]
			currentDirection = newVals[2]
			if debug_main:
				print("      New direction will be    =",turnsText(currentDirection))
				print("@main inputQueue               =",inputQueue)
			if debug_main:
				print("@main New robot location       =",currentRobotLocation)
				print("@main painting color           =",bAndWText(currentColor))
				print("@main pointsOnPath (after)     =",pointsOnPath)
				print("@main colorsOnPath (after)     =",colorsOnPath)
			outputQueuePtr += 2
		elif len(inputQueue) == 0:
			print("@main Loaded initial position and instruction")
			currentRobotLocation.append(0)
			currentRobotLocation.append(0)
			colorsOnPath.append(0)
			currentDirection = '^'
			myCPU.setProgState('gotInput')
			inputQueue.append(0)
			currentColor = 0
	else:
		print("progStateVal =",progStateVal)
		assert False,"@main : Something happened bad to the program state"
print("Output Queue :", outputQueue)
paintedCount = 0
print("pointsOnPath",pointsOnPath)
for item in outputQueue:
	if item >= 1:
		paintedCount += 1
print("paintedCount=",paintedCount)

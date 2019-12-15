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
Not 248
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
		self.setProgState('startState')
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
				if len(outputQueue) == 2:
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

def getNewRobotDirection(currentRobotDirection,newTurn):
	debug_getNewRobotDirection = False
	if debug_getNewRobotDirection:
		print("\n@getNewRobotDirection : currentRobotDirection",currentRobotDirection)
		print("@getNewRobotDirection : newTurn",newTurn)
	if newTurn == '<':
		if currentRobotDirection == '^':
			resultingDirection = '<'
		elif currentRobotDirection == '<':
			resultingDirection = 'v'
		elif currentRobotDirection == '>':
			resultingDirection = '^'
		elif currentRobotDirection == 'v':
			resultingDirection = '>'
		else:
			assert False,"getNewRobotDirection : bad current direction"
	elif newTurn == '>':
		if currentRobotDirection == '^':
			resultingDirection = '>'
		elif currentRobotDirection == '<':
			resultingDirection = '^'
		elif currentRobotDirection == '>':
			resultingDirection = 'v'
		elif currentRobotDirection == 'v':
			resultingDirection = '<'
		else:
			assert False,"getNewRobotDirection : bad current direction"
	else:
		assert False,"getNewRobotDirection: Illegal direction"
	if debug_getNewRobotDirection:
		print("@debug_getNewRobotDirection : resultingDirection",resultingDirection)
	return resultingDirection
	
def getNewRobotLocation(currentRobotLocation,nextDirection):
	debug_getNewRobotLocation = False
	if debug_getNewRobotLocation:
		print("\n@getNewRobotLocation : currentRobotLocation",currentRobotLocation)
		print("@getNewRobotLocation : nextDirection",nextDirection)
	if nextDirection == '^':
		newLocation = [currentRobotLocation[0],currentRobotLocation[1]+1]
	elif nextDirection == '<':
		newLocation = [currentRobotLocation[0]-1,currentRobotLocation[1]]
	elif nextDirection == '>':
		newLocation = [currentRobotLocation[0]+1,currentRobotLocation[1]]
	elif nextDirection == 'v':
		newLocation = [currentRobotLocation[0],currentRobotLocation[1]-1]
	if debug_getNewRobotLocation:
		print("@getNewRobotLocation : newLocation",newLocation)
	return newLocation
	
def colorsText(colorCode):
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

def getColor(pointList,currentPointLocation,colorsList):
	debug_getColor = False
	if debug_getColor:
		print("\n@getColor pointList            :",pointList)
		print("@getColor currentPointLocation :",currentPointLocation)
		print("@getColor colorsList           :",colorsList)
	for count in range(len(pointList)):
		if pointList[count] == currentPointLocation:
			if debug_getColor:
				print("@getColor color at point is",colorsText(colorsList[count]))
			return colorsList[count]
	if debug_getColor:
		print("@getColor current point has not been visited so return black")
	if debug_getColor:
		print(" ")
	return 0
		
def getPointOffsetOnList(currentRobotLocation,pointsOnPath):
	debugAll_getPointOffsetOnList = False
	if currentRobotLocation not in pointsOnPath:
		if debugAll_getPointOffsetOnList:
			print("getPointOffsetOnList: point was not on list")
		return -1
	for checkPoint in range(len(pointsOnPath)):
		if currentRobotLocation == pointsOnPath[checkPoint]:
			if debugAll_getPointOffsetOnList:
					print("getPointOffsetOnList: point was in list at offset",checkPoint)
			return checkPoint
	else:
		assert False,"getPointOffsetOnList : Error"
	
# Initialize queues
inputQueue = []
outputQueue = []

# Initialize robot states
currentRobotLocation = [0,0]
currentRobotDirection = '^'
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
print("lenOfProgram",lenOfProgram)
for i in range(5000):
	programMemory.append(0)

# start up the CPU
myCPU = CPU()
myCPU.initCPU()

stepCount = 0

while True:
	debug_main = False
	myCPU.runCPU()
	progStateVal = myCPU.getProgState()
	if progStateVal == 'progDone':
		print("Reached end of program")
		break
	elif progStateVal == 'waitForInput':
		stepCount += 1
		if debug_main:
			print("\n@main Getting input")
			print("@main Current location          =",currentRobotLocation)
		colorAtCurrentPoint = getColor(pointsOnPath,currentRobotLocation,colorsOnPath)
		if colorAtCurrentPoint > 1:
			print("@main got a bad color at the current point",colorAtCurrentPoint)
			assert False,"@main bad color at the current point"		
		if debug_main:
			print("@main color at current location =",colorsText(colorAtCurrentPoint))
		inputQueue.append(colorAtCurrentPoint)
		if debug_main:
			print("@main inputQueue to CPU         =",inputQueue)
		myCPU.setProgState('inputReady')
	elif progStateVal == 'outputReady':
		if debug_main:
			print("\n@main Painting and moving")
			print("@main OUTputQueue (from CPU)    =",outputQueue)
		colorFromCPU = outputQueue[0]
		if debug_main:
			print("      Color (from CPU)          =",colorFromCPU,"=",colorsText(colorFromCPU))
		if colorFromCPU > 1:
			print("@main Error - bad color",colorFromCPU)
			print("outputQueue",outputQueue)
			assert False,"Bad color received from output routine"
		if outputQueue[1] == 0:
			turnDirection = '<'
		elif outputQueue[1] == 1:
			turnDirection = '>'
		else:
			assert False,"Bad Turn Direction"
		if debug_main:
			print("      Turn direction (from CPU) =",outputQueue[1],"=",turnDirection)
		pointOffset = getPointOffsetOnList(currentRobotLocation,pointsOnPath)
		if pointOffset == -1:
			pointsOnPath.append(currentRobotLocation)
			colorsOnPath.append(colorFromCPU)
		else:
			colorsOnPath[pointOffset] = colorFromCPU
		
		del outputQueue[1]
		del outputQueue[0]
		if debug_main:
			print("@main Before move location      =",currentRobotLocation)
			print("@main Before move direction     =",currentRobotDirection)
		newDirection = getNewRobotDirection(currentRobotDirection,turnDirection)
		if debug_main:
			print("@main New direction             =",newDirection)
		newLocation = getNewRobotLocation(currentRobotLocation,newDirection)
		if debug_main:
			print("@main After move location       =",newLocation)
		newDirection = getNewRobotDirection(currentRobotDirection,turnDirection)
		newLocation = getNewRobotLocation(currentRobotLocation,newDirection)
		if debug_main:
			print("@main After move pointsOnPath   =",pointsOnPath)
			print("@main After move colorsOnPath   =",colorsOnPath)
		currentRobotDirection = newDirection
		currentRobotLocation = newLocation
	else:
		print("progStateVal =",myCPU.getProgState())
		assert False,"@main : Something happened bad to the program state"

paintedCount = 0
print("paintedCount=",paintedCount)
print("Length of points on path",len(pointsOnPath))
listOfPoints = []
for point in pointsOnPath:
	if point not in listOfPoints:
		listOfPoints.append(point)
print("unique points",len(listOfPoints))

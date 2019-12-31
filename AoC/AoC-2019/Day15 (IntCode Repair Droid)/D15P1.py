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

def nextMove(dir,currentPos):
	""" returning next point given  thne current point and direction
	"""
	debug_nextMove = False
	if debug_nextMove:
		print("nextMove: currentPos",currentPos)
		print("nextMove: dir",dir)
	nextPos = [0,0]
	if dir == north:	# north
		nextPos = [currentPos[0],currentPos[1]+1]
	elif dir == south:	# south
		nextPos = [currentPos[0],currentPos[1]-1]
	elif dir == west:	# west
		nextPos = [currentPos[0]-1,currentPos[1]]
	elif dir == east:	# east
		nextPos = [currentPos[0]+1,currentPos[1]]
	else:
		assert False,"nextMove: bad direction"
	return nextPos

north = 1
south = 2
west = 3
east = 4

def directionAtBlock(dir):
	if dir == north:
		return west
	elif dir == west:
		return south
	elif dir == south:
		return east
	elif dir == east:
		return north
		
def dirIfForward(dir):
	if dir == north:
		return east
	elif dir == west:
		return north
	elif dir == south:
		return west
	elif dir == east:
		return south


def nextMoveForward(moveDir,currentLoc):
	debug_nextMoveForward = False
	if debug_nextMoveForward:
		print("\nnextMoveForward: moveDir",end='')
		dirToText(moveDir)
	if debug_nextMoveForward:
		print("nextMoveForward: currentLoc",currentLoc)
	xVal = currentLoc[0]
	yVal = currentLoc[1]
	if moveDir == north:
		yVal += 1
	elif moveDir == west:
		xVal -= 1
	elif moveDir == south:
		yVal -= 1
	elif moveDir == east:
		xVal += 1
	newLoc = [xVal,yVal]
	if debug_nextMoveForward:
		print("nextMoveForward: newLoc",newLoc)
	return newLoc
		
def dirToText(dir):
	if dir == north:	# north
		print(" north")
	elif dir == south:	# south
		print(" south")
	elif dir == west:	# west
		print(" west")
	elif dir == east:	# east
		print(" east")
	else:
		assert False,"dirToText: bad direction"
	
def makeMaze(openBlockLocs,walls):
	""" Convert lists of open blocks and walls into an array
	"""
	xMin = 0
	xMax = 0
	yMin = 0
	yMax = 0
	for point in openBlockLocs:
		if point[0] > xMax:
			xMax = point[0]
		if point[0] < xMin:
			xMin = point[0]
		if point[1] > yMax:
			yMax = point[1]
		if point[1] < yMin:
			yMin = point[1]
	for point in walls:
		if point[0] > xMax:
			xMax = point[0]
		if point[0] < xMin:
			xMin = point[0]
		if point[1] > yMax:
			yMax = point[1]
		if point[1] < yMin:
			yMin = point[1]
	mazeArray = []
	for yVal in range(yMax,yMin-1,-1):
		row = []
		for xVal in range(xMin,xMax+1):
			if [xVal,yVal] == [0,0]:
				row.append("S")
			elif [xVal,yVal] == dest:
				row.append("D")
			elif [xVal,yVal] in openBlockLocs:
				row.append(" ")
			else:
				row.append("X")
		mazeArray.append(row)
	return mazeArray
	
def dumpMaze(maze):
	""" Dump the maze
	"""
	rowNum = 0
	for row in maze:
		for cell in row:
			print(cell,end='')
		print("<",rowNum)
		rowNum += 1

def countWallsAroundCell(pos,maze):
	"""
	"""
	count = 0
	yPos = pos[0]
	xPos = pos[1]
	if maze[yPos-1][xPos-1] == 'X':
		count += 1
	if maze[yPos-1][xPos] == 'X':
		count += 1
	if maze[yPos-1][xPos+1] == 'X':
		count += 1
	if maze[yPos][xPos-1] == 'X':
		count += 1
	if maze[yPos][xPos+1] == 'X':
		count += 1
	if maze[yPos+1][xPos-1] == 'X':
		count += 1
	if maze[yPos+1][xPos] == 'X':
		count += 1
	if maze[yPos+1][xPos+1] == 'X':
		count += 1
	return count

def findInMaze(findChar,maze):
	"""
	"""
	yCount = 0
	for row in maze:
		xCount = 0
		for col in row:
			if col == findChar:
				return [yCount,xCount]
			xCount += 1
		yCount += 1
	return [-1,-1]

def checkDeadEnd(loc,maze):
	""" Examples of dead ends 
	
	XXX
	X X 
	
	XX
	X
	XX
	
	X X
	XXX 
	
	XX 
	 X
	XX
	
	"""
	if countWallsAroundCell(loc,maze) == 7:
		return True
	locX = loc[1]
	locY = loc[0]
	
#	XXX
#	X X 
	if maze[locY-1][locX-1] == 'X' and maze[locY-1][locX] == 'X' and maze[locY-1][locX+1] == 'X' and maze[locY][locX-1] == 'X' and maze[locY][locX+1] == 'X':
		return True

#	XX
#	X
#	XX
	if maze[locY-1][locX-1] == 'X' and maze[locY-1][locX] == 'X' and maze[locY][locX-1] == 'X' and maze[locY+1][locX-1] == 'X' and maze[locY+1][locX] == 'X':
		return True

#	X X
#	XXX 
	if maze[locY][locX-1] == 'X' and maze[locY][locX+1] == 'X' and maze[locY+1][locX-1] == 'X' and maze[locY+1][locX] == 'X' and maze[locY+1][locX+1] == 'X':
		return True

#	XX 
#	 X
#	XX
	if maze[locY-1][locX] == 'X' and maze[locY-1][locX+1] == 'X' and maze[locY][locX+1] == 'X' and maze[locY+1][locX] == 'X' and maze[locY+1][locX+1] == 'X':
		return True

	return False

def fillDeadEnds(maze):
	"""
	"""
	yCount = 1
	for row in maze[1:-1]:
		xCount = 1
		for col in row[1:-1]:
			if maze[yCount][xCount] == " ":
				if checkDeadEnd([yCount,xCount],maze):
					maze[yCount][xCount] = 'X'
			xCount += 1
		yCount += 1
	return maze

def deadEndsLeft(maze):
	"""
	"""
	yCount = 1
	for row in maze[1:-1]:
		xCount = 1
		for col in row[1:-1]:
			if maze[yCount][xCount] == " ":
				if checkDeadEnd([yCount,xCount],maze):
					return True
			xCount += 1
		yCount += 1
	return False
	
def runMaze(currentLoc,currentDir,maze):
	distanceStartToDest = 0
	distanceDestToStart = 0
	reachedDest = False
	reachedStart = False
	while reachedStart == False:
		currentLocAndDir = getNextLocAndDir(currentLoc,currentDir,maze)
		currentLoc = currentLocAndDir[0]
		currentDir = currentLocAndDir[1]
		if not reachedDest:
			distanceStartToDest += 1
		else:
			distanceDestToStart += 1
		if currentLoc == destLoc:
			reachedDest = True
			#assert False,"at dest"
		if currentLoc == startLoc:
			reachedStart = True
	print("distanceStartToDest",distanceStartToDest)
	print("distanceDestToStart",distanceDestToStart)
		
def getNextLocAndDir(currentLoc,currentDir,maze):
	print("\ngetNextLocAndDir: currentLoc",currentLoc)
	currentY = currentLoc[0]
	currentX = currentLoc[1]
	# print("getNextLocAndDir: currentY",currentY)
	# print("getNextLocAndDir: currentX",currentX)
	print("getNextLocAndDir: currentDir = ",end='')
	dirToText(currentDir)
	if maze[currentY][currentX] == 'X':
		assert False,"Ran into a wall"
	if currentDir == north:
		if checkAbleToMove(currentLoc,east,maze):
			newDir = east
		elif checkAbleToMove(currentLoc,north,maze):
			newDir = north
		elif checkAbleToMove(currentLoc,west,maze):
			newDir = west
		else:
			newDir = south
	elif currentDir == west:
		if checkAbleToMove(currentLoc,north,maze):
			newDir = north
		elif checkAbleToMove(currentLoc,west,maze):
			newDir = west
		elif checkAbleToMove(currentLoc,south,maze):
			newDir = south
		else:
			newDir = east
	elif currentDir == south:
		if checkAbleToMove(currentLoc,west,maze):
			newDir = west
		elif checkAbleToMove(currentLoc,south,maze):
			newDir = south
		elif checkAbleToMove(currentLoc,east,maze):
			newDir = east
		else:
			newDir = north
	elif currentDir == east:
		if checkAbleToMove(currentLoc,south,maze):
			newDir = south
		elif checkAbleToMove(currentLoc,east,maze):
			newDir = east
		elif checkAbleToMove(currentLoc,north,maze):
			newDir = north
		else:
			newDir = west
	if newDir == north:
		currentY -= 1
	elif newDir == south:
		currentY += 1
	elif newDir == west:
		currentX -= 1
	elif newDir == east:
		currentX += 1
	newLocation = [currentY,currentX]
	print("getNextLocAndDir: newLocation",newLocation)
	return [newLocation,newDir]

def checkAbleToMove(currentLoc,testDir,maze):
	print("checkAbleToMove: @",currentLoc,"trying",end='')
	dirToText(testDir)
	currentY = currentLoc[0]
	currentX = currentLoc[1]
	if testDir == north:
		if maze[currentY-1][currentX] == 'X':
			print("                 Not able to move north",maze[currentY+1][currentX])
			return False
	elif testDir == south:
		if maze[currentY+1][currentX] == 'X':
			print("                 Not able to move south",maze[currentY-1][currentX])
			return False
	elif testDir == east:
		if maze[currentY][currentX+1] == 'X':
			print("                 Not able to move east",maze[currentY][currentX+1])
			return False
	elif testDir == west:
		if maze[currentY][currentX-1] == 'X':
			print("                 Not able to move west",maze[currentY][currentX-1])
			return False
	print("                Able to move ")
	return True
	
# Initialize queues
inputQueue = []
outputQueue = []

# Load program memory from file
progName = "AOC2019D15input.txt"
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

currentLoc = [0,0]
walls = []
openBlockLocs = []
moveDir = north		# start out moving west
start = [0,0]
dest = [0,0]
reachedStart = False

debug_main = False
lastStep = 100000

myCPU.runCPU()
progStateVal = myCPU.getProgState()
while progStateVal != 'progDone':
	if debug_main:
		print("\nmain: Getting input")
		print("main: currentLoc",currentLoc)
		print("main: Moving",end='')
		dirToText(moveDir)
	inputQueue.append(moveDir)	
	if debug_main:
		print("main: inputQueue",inputQueue)
	myCPU.runCPU()
	if outputQueue[0] == 0:		# Hit a wall - did not move
		if debug_main:
			print("\nmain: (wall) Hit a wall")
		# Save wall
		walls.append(nextMove(moveDir,currentLoc))
		# Change girection
		moveDir = directionAtBlock(moveDir)
		if debug_main:
			print("\nmain: (wall) moveDir (after direction change)",end='')
			dirToText(moveDir)
			print("main: (wall) done with wall")
	elif outputQueue[0] == 1:	# Move was Ok
		openBlockLocs.append(currentLoc)
		if debug_main:
			print("main: (OK) Move was OK")
			print("main: (OK) walls",walls)
			print("main: (OK) currentLoc",currentLoc)
		currentLoc = nextMoveForward(moveDir,currentLoc)
		if currentLoc == [0,0]:
			reachedStart = True
			break
		if debug_main:
			print("main: (OK) currentLoc",currentLoc)
		moveDir = dirIfForward(moveDir)
		if debug_main:
			print("main: (OK) new currentLoc",currentLoc)
			print("main: (OK) added new block")
			print("main: (OK) openBlockLocs",openBlockLocs)
			print("main: (OK) new moveDir",end='')
			dirToText(moveDir)
	elif outputQueue[0] == 2:	# Reached dest
		openBlockLocs.append(currentLoc)
		if debug_main:
			print("main: (OK) Move was OK")
			print("main: (OK) walls",walls)
			print("main: (OK) currentLoc",currentLoc)
		currentLoc = nextMoveForward(moveDir,currentLoc)
		if debug_main:
			print("main: (OK) currentLoc",currentLoc)
		moveDir = dirIfForward(moveDir)
		if debug_main:
			print("main: (OK) new currentLoc",currentLoc)
			print("main: (OK) added new block")
			print("main: (OK) openBlockLocs",openBlockLocs)
			print("main: (OK) new moveDir",end='')
			dirToText(moveDir)
		dest = currentLoc
		#assert False,"main: Reached dest"
	del outputQueue[0]
	if debug_main:
		print("main: (loop) currentLoc",currentLoc)
		print("main: (loop) openBlockLocs",openBlockLocs)
		print("main: (loop) walls",walls)
	#displayMaze(openBlockLocs,walls)
	progStateVal = myCPU.getProgState()
	#raw_input("main: Press Enter to continue...")
maze = makeMaze(openBlockLocs,walls)
os.system('cls')
dumpMaze(maze)
while deadEndsLeft(maze):
	#raw_input("main: Press Enter to continue...")
	maze = fillDeadEnds(maze)
os.system('cls')
dumpMaze(maze)
destLoc = findInMaze("D",maze)
startLoc = findInMaze("S",maze)
print("destLoc",destLoc)
print("startLoc",startLoc)

currentDir = west
currentLoc = startLoc
runMaze(currentLoc,currentDir,maze)
# print("distanceStartToDest",distanceStartToDest)
# print("distanceDestToStart",distanceDestToStart)


# Pt2-AoCDay15.py
# 2019 Advent of Code
# Day 15
# Part 2
# https://adventofcode.com/2019/day/15

from __future__ import print_function

import os
import sys
import time

"""
--- Part Two ---
You quickly repair the oxygen system; oxygen gradually fills the area.

Oxygen starts in the location containing the repaired oxygen system. It takes one minute for oxygen to spread to all open locations that are adjacent to a location that already contains oxygen. Diagonal locations are not adjacent.

In the example above, suppose you've used the droid to explore the area fully and have the following map (where locations that currently contain oxygen are marked O):

 ##   
#..## 
#.#..#
#.O.# 
 ###  
Initially, the only location which contains oxygen is the location of the repaired oxygen system. However, after one minute, the oxygen spreads to all open (.) locations that are adjacent to a location containing oxygen:

 ##   
#..## 
#.#..#
#OOO# 
 ###  
After a total of two minutes, the map looks like this:

 ##   
#..## 
#O#O.#
#OOO# 
 ###  
After a total of three minutes:

 ##   
#O.## 
#O#OO#
#OOO# 
 ###  
And finally, the whole region is full of oxygen after a total of four minutes:

 ##   
#OO## 
#O#OO#
#OOO# 
 ###  
So, in this example, all locations contain oxygen after 4 minutes.

Use the repair droid to get a complete map of the area. How many minutes will it take to fill with oxygen?
"""

debugAll = False

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	
	def __init__(self):
		# self.inputQueue = []
		# self.outputQueue = []
		# self.progState = ''
		# self.programCounter = 0
		# self.relativeBaseRegister = 0
		self.programMemory = []

		debug_initCPU = False
		# state transitions are 
		# 'inputReady' => 'waitingOnInput' => 
		# 'inputReady' => 'waitingOnInput' => 
		# 'progDone'
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
		#global self.programMemory
		#global self.inputQueue
		#global self.outputQueue
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
		progName = "input.txt"
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

north = 1
south = 2
west = 3
east = 4

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
	#print("\ngetNextLocAndDir: currentLoc",currentLoc)
	currentY = currentLoc[0]
	currentX = currentLoc[1]
	# print("getNextLocAndDir: currentY",currentY)
	# print("getNextLocAndDir: currentX",currentX)
	# print("getNextLocAndDir: currentDir = ",end='')
	# dirToText(currentDir)
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
	#print("getNextLocAndDir: newLocation",newLocation)
	return [newLocation,newDir]

def checkAbleToMove(currentLoc,testDir,maze):
	#print("checkAbleToMove: @",currentLoc,"trying",end='')
	#dirToText(testDir)
	currentY = currentLoc[0]
	currentX = currentLoc[1]
	if testDir == north:
		if maze[currentY-1][currentX] == 'X':
			#print("                 Not able to move north",maze[currentY+1][currentX])
			return False
	elif testDir == south:
		if maze[currentY+1][currentX] == 'X':
			#print("                 Not able to move south",maze[currentY-1][currentX])
			return False
	elif testDir == east:
		if maze[currentY][currentX+1] == 'X':
			#print("                 Not able to move east",maze[currentY][currentX+1])
			return False
	elif testDir == west:
		if maze[currentY][currentX-1] == 'X':
			#print("                 Not able to move west",maze[currentY][currentX-1])
			return False
	#print("                Able to move ")
	return True
	
def findFillNeighbors(currentScanPoints,originalMaze):
	newScanPoints = []
	for point in currentScanPoints:
		locY = point[0]
		locX = point[1]
		if originalMaze[locY-1][locX] == ' ':
			newScanPoints.append([locY-1,locX])
		if originalMaze[locY+1][locX] == ' ':
			newScanPoints.append([locY+1,locX])
		if originalMaze[locY][locX-1] == ' ':
			newScanPoints.append([locY,locX-1])
		if originalMaze[locY][locX+1] == ' ':
			newScanPoints.append([locY,locX+1])
	#print("newScanPoints",newScanPoints)
	return newScanPoints

# start up the CPU
myCPU = CPU()

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
	myCPU.inputQueue.append(moveDir)	
	if debug_main:
		print("main: inputQueue",myCPU.inputQueue)
	myCPU.runCPU()
	if myCPU.outputQueue[0] == 0:		# Hit a wall - did not move
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
	elif myCPU.outputQueue[0] == 1:	# Move was Ok
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
	elif myCPU.outputQueue[0] == 2:	# Reached dest
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
	del myCPU.outputQueue[0]
	if debug_main:
		print("main: (loop) currentLoc",currentLoc)
		print("main: (loop) openBlockLocs",openBlockLocs)
		print("main: (loop) walls",walls)
	#displayMaze(openBlockLocs,walls)
	progStateVal = myCPU.getProgState()
	#raw_input("main: Press Enter to continue...")
maze = makeMaze(openBlockLocs,walls)
originalMaze = makeMaze(openBlockLocs,walls)
#os.system('cls')
#dumpMaze(maze)
print("Filled dead ends")
while deadEndsLeft(maze):
	#raw_input("main: Press Enter to continue...")
	maze = fillDeadEnds(maze)
#os.system('cls')
#dumpMaze(maze)
destLoc = findInMaze("D",maze)
startLoc = findInMaze("S",maze)
print("destLoc",destLoc)
print("startLoc",startLoc)

currentDir = west
currentLoc = startLoc
runMaze(currentLoc,currentDir,maze)

#dumpMaze(originalMaze)

count = 0
currentScanPoints = []
currentScanPoints.append(destLoc)
while currentScanPoints != []:
	for point in currentScanPoints:
		originalMaze[point[0]][point[1]] = 'o'
	currentScanPoints = findFillNeighbors(currentScanPoints,originalMaze)
	if currentScanPoints != []:
		count += 1

print("count",count)


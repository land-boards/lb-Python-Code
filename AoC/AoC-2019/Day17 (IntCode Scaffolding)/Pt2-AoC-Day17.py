# Pt1-AoCDay17.py
# 2019 Advent of Code
# Day 17
# Part 1
# https://adventofcode.com/2019/day/17

from __future__ import print_function

import os
import sys
import time

"""
	--- Day 17: Set and Forget ---
	An early warning system detects an incoming solar flare and automatically activates the ship's electromagnetic shield. Unfortunately, this has cut off the Wi-Fi for many small robots that, unaware of the impending danger, are now trapped on exterior scaffolding on the unsafe side of the shield. To rescue them, you'll have to act quickly!

	The only tools at your disposal are some wired cameras and a small vacuum robot currently asleep at its charging station. The video quality is poor, but the vacuum robot has a needlessly bright LED that makes it easy to spot no matter where it is.

	An Intcode program, the Aft Scaffolding Control and Information Interface (ASCII, your puzzle input), provides access to the cameras and the vacuum robot. Currently, because the vacuum robot is asleep, you can only access the cameras.

	Running the ASCII program on your Intcode computer will provide the current view of the scaffolds. This is output, purely coincidentally, as ASCII code: 35 means #, 46 means ., 10 starts a new line of output below the current one, and so on. (Within a line, characters are drawn left-to-right.)

	In the camera output, # represents a scaffold and . represents open space. The vacuum robot is visible as ^, v, <, or > depending on whether it is facing up, down, left, or right respectively. When drawn like this, the vacuum robot is always on a scaffold; if the vacuum robot ever walks off of a scaffold and begins tumbling through space uncontrollably, it will instead be visible as X.

	In general, the scaffold forms a path, but it sometimes loops back onto itself. For example, suppose you can see the following view from the cameras:

	..#..........
	..#..........
	#######...###
	#.#...#...#.#
	#############
	..#...#...#..
	..#####...^..
	Here, the vacuum robot, ^ is facing up and sitting at one end of the scaffold near the bottom-right of the image. The scaffold continues up, loops across itself several times, and ends at the top-left of the image.

	The first step is to calibrate the cameras by getting the alignment parameters of some well-defined points. Locate all scaffold intersections; for each, its alignment parameter is the distance between its left edge and the left edge of the view multiplied by the distance between its top edge and the top edge of the view. Here, the intersections from the above image are marked O:

	..#..........
	..#..........
	##O####...###
	#.#...#...#.#
	##O###O###O##
	..#...#...#..
	..#####...^..
	For these intersections:

	The top-left intersection is 2 units from the left of the image and 2 units from the top of the image, so its alignment parameter is 2 * 2 = 4.
	The bottom-left intersection is 2 units from the left and 4 units from the top, so its alignment parameter is 2 * 4 = 8.
	The bottom-middle intersection is 6 from the left and 4 from the top, so its alignment parameter is 24.
	The bottom-right intersection's alignment parameter is 40.
	To calibrate the cameras, you need the sum of the alignment parameters. In the above example, this is 76.

	Run your ASCII program. What is the sum of the alignment parameters for the scaffold intersections?

Your puzzle answer was 929045.

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
				# if len(inputQueue) != 0:
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

def loadIntCodeProgram():
	""" 
	"""
	global programMemory
	global inputQueue
	global outputQueue
#	debug_loadIntCodeProgram = True
	debug_loadIntCodeProgram = False
	# Load program memory from file
	progName = "input.txt"
	if debug_loadIntCodeProgram:
		print("Input File Name :",progName)
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		programMemory = map(int, inLine.split(','))
	# pad out past end
	for i in range(10000):
		programMemory.append(0)
	if debug_loadIntCodeProgram:
		print(programMemory)

def scanLine(horizLine):
	""" Return a list of points at the end of lines
	Ex:
	[46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 46, 46, 46, 46, 46, 46, 46, 46, 46, 35, 35, 35, 35, 35, 35, 35, 46, 46, 46, 46, 46, 46]
	012345678901234567890123456789012345678901234
	..........#############.........#######...... <  24
	returns [10,22,32,38]
	"""
	scanState = 'startScan'
	lineOffset = 0
	leftHashMark = -1
	linePoints = []
	while lineOffset < len(horizLine):
		if scanState == 'startScan':
			if horizLine[0] == 35:			# Hash
				leftHashMark = 0
				scanState = 'edgeHashString'
			elif horizLine[0] == 46:		# Dot
				scanState = 'inDots'
		elif scanState == 'edgeHashString':
			if horizLine[lineOffset] == 35:	# Hash
				scanState = 'inHashString'
				linePoints.append(lineOffset-1)
			elif horizLine[lineOffset] == 46:		# Dot
				scanState = 'inDots'
		elif scanState == 'inHashString':
			if horizLine[lineOffset] == 46:
				scanState = 'inDots'
				linePoints.append(lineOffset-1)
		elif scanState == 'inDots':
			if horizLine[lineOffset] == 35:
				scanState = 'edgeHashString'
				leftHashMark = lineOffset
		lineOffset += 1
	if scanState == 'inHashString':
		linePoints.append(lineOffset-1)
	return linePoints

def getOtherEndOfHorizLine(currentPoint,pairsList):
	#print("getOtherEndOfHorizLine: currentPoint",currentPoint)
	for pair in pairsList:
		#print("getOtherEndOfHorizLine: checking pair",pair)
		if pair[0] == currentPoint[0] and pair[1] == currentPoint[1]:
			return [pair[2],pair[3]]
		if pair[2] == currentPoint[0] and pair[3] == currentPoint[1]:
			return [pair[0],pair[1]]
	return[]
		
def getOtherEndOfVertLine(currentPoint,pairsList):
	#print("getOtherEndOfVertLine: currentPoint",currentPoint)
	for pair in pairsList:
		#print("getOtherEndOfVertLine: checking pair",pair)
		if pair[0] == currentPoint[0] and pair[1] == currentPoint[1]:
			return [pair[2],pair[3]]
		if pair[2] == currentPoint[0] and pair[3] == currentPoint[1]:
			return [pair[0],pair[1]]
	return[]

def getNextDir(dir,point1,point2):
	#print("getNextDir: dir",str(unichr(dir)),"point1",point1,"to point2",point2,end='')
	if dir == down:
		if point1[0] > point2[0]:	# OK
			turnDir = left
			absDir = left
		else:
			turnDir = right
			absDir = right
	elif dir == up:
		if point1[0] < point2[0]:
			turnDir = left
			absDir = right
		else:
			turnDir = right
			absDir = left
	elif dir == left:
		if point1[1] < point2[1]:
			turnDir = left
			absDir = up
		else:						# OK
			turnDir = right
			absDir = down
	elif dir == right:
		if point1[1] < point2[1]:
			turnDir = right
			absDir = up
		else:
			turnDir = left
			absDir = down
	#print(" turnDir",str(unichr(turnDir)),"absDir",str(unichr(absDir)),end='')
	return [absDir,turnDir]
	
loadIntCodeProgram()
myCPU = CPU()
myCPU.initCPU()

debug_main = True
#debug_main = False

down = ord('^')
left = ord('<')
right = ord('>')
up = ord('v')

startPoint = []
inList = []
inRow = []
rowNum = 0
colNum = 0
print("000000000011111111112222222222333333333344444")
print("012345678901234567890123456789012345678901234")
while myCPU.getProgState() != 'progDone':
	#print("progState",myCPU.getProgState())
	myCPU.runCPU()
	#print("progState",myCPU.getProgState())
	if myCPU.getProgState() == 'outputReady':
		intOut = outputQueue[0]
		retVal = (str(unichr(intOut)))
		if intOut == 10:	# enter
			if inRow != []:
				inList.append(inRow)
			inRow = []
			print(" < ",rowNum)
			rowNum += 1
			colNum = 0
		elif intOut == 35 or intOut == 46:	# crosshatch or dot
			inRow.append(intOut)
			print(retVal,end='')
			colNum += 1
		else:	# start point has to be here
			inRow.append(35)
			print(retVal,end='')
			startSymbol = intOut
			startPoint = [colNum,rowNum]
			colNum += 1
		del outputQueue[0]

print("startSymbol",startSymbol)
print("startPoint",startPoint)
#print(inList[24])
# scan = scanLine(inList[1])
# print(scan)

# Find endpoints by scanning each line horizontally
pointsList = []
for row in range(0,len(inList)):
	lineStarts = scanLine(inList[row])
	for point in lineStarts:
		thePoint = [point,row]
		pointsList.append(thePoint)
#print("pointsList",pointsList)

# create horizontal line segments list by sorting the x values
# pointsList [[36, 0], [44, 0], [24, 4], [30, 4], [32, 6], [44, 6], [36, 8], [42, 8], [24, 12], [32, 12], [30, 16], [36, 16], [34, 20], [42, 20], [12, 22], [20, 22], [10, 24], [22, 24], [32, 24], [38, 24], [4, 26], [8, 26], [0, 28], [12, 28], [26, 28], [30, 28], [34, 28], [38, 28], [4, 30], [10, 30], [20, 30], [32, 30], [22, 32], [30, 32], [0, 34], [8, 34], [26, 34], [32, 34], [30, 38], [38, 38], [32, 46], [38, 46]]
horizPairsList = []
for yVal in range(0,len(inList)):
	horizLinePointsList = []
	for point in pointsList:
		if point[1] == yVal:
			horizLinePointsList.append(point[0])
	if horizLinePointsList != []:
		horizLinePointsList.sort()
		#print("horizLinePointsList, y",yVal,"xList",horizLinePointsList)
		for pointIndex in range(0,len(horizLinePointsList),2):
			singlePair = []
			singlePair.append(horizLinePointsList[pointIndex])
			singlePair.append(yVal)
			singlePair.append(horizLinePointsList[pointIndex+1])
			singlePair.append(yVal)
			horizPairsList.append(singlePair)
#print("horizPairsList",horizPairsList)
# print("Horizontal Line Segments List (x1,y1,x2,y2)")
# for line in horizPairsList:
	# print(line,abs(line[0]-line[2]))

# create a list of vertical lines
#print("Vertical calculations")
vertPairsList = []
for xVal in range(0,len(inList[0])):
	vertLinePointsList = []
	for point in pointsList:
		if point[0] == xVal:
			vertLinePointsList.append(point[1])
	if vertLinePointsList != []:
		vertLinePointsList.sort()
		#print("xVal",xVal,"vertLinePointsList",vertLinePointsList)
		for pointIndex in range(0,2*(len(vertLinePointsList)/2),2):
			singlePair = []
			singlePair.append(xVal)
			singlePair.append(vertLinePointsList[pointIndex])
			singlePair.append(xVal)
			singlePair.append(vertLinePointsList[pointIndex+1])
			#print("singlePair",singlePair)
			vertPairsList.append(singlePair)
#print("vertPairsList",vertPairsList)
# print("Vertical Line Segments List (x1,y1,x2,y2)")
# for line in vertPairsList:
	# print(line,abs(line[1]-line[3]))

# create chained list of lines
chainList = []
currentPoint = startPoint
chainList.append(currentPoint)
#print("currentPoint (before)",currentPoint)
dir = 'horiz'
while currentPoint != []:
	currentPoint = getOtherEndOfHorizLine(currentPoint,horizPairsList)
	if currentPoint != []:
		chainList.append(currentPoint)
		#print("currentPoint (after horiz)",currentPoint)
		currentPoint = getOtherEndOfVertLine(currentPoint,vertPairsList)
		if currentPoint != []:
			chainList.append(currentPoint)
		#print("currentPoint (after Vert)",currentPoint)
print("chainList",chainList)

# make directions list
currentLoc = chainList[0]
print("currentLoc",currentLoc)
currentDir = startSymbol
print("startSymbol",str(unichr(startSymbol)))

dirPair = []
dirList = []
for point in range(0,len(chainList)-1):
	dist = abs(chainList[point][0] - chainList[point+1][0]) + abs(chainList[point][1] - chainList[point+1][1])
	# currentDir returns [absDir,turnDir]
	dirVect = getNextDir(currentDir,chainList[point],chainList[point+1])
	currentDir = dirVect[0]
	turnDir = dirVect[1]
	# print("point pairs",chainList[point],chainList[point+1],str(unichr(turnDir)),"dist",dist,end='')
	dirPair = []
	if turnDir == left:
		#print(" - L",end='')
		dirPair.append('L')
		dirPair.append(dist)
	else:
		#print(" - R",end='')
		dirPair.append('R')
		dirPair.append(dist)
	#print(dist)
	dirList.append(dirPair)
#print("")
#print(dirList)

for row in dirList:
	print(row[0],end='')
	print(row[1],end='')
	print(",",end='')
print("")

# (['A', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'C', 'A'], ('L', '6', 'R', '12', 'L', '6', 'L', '8', 'L', '8'), ('L', '6', 'R', '12', 'R', '8', 'L', '8'), ('L', '4', 'L', '4', 'L', '6'))

# A = L6,R12,L6,L8,L8,
# A = L6,R12,L6,L8,L8,
# B = L6,R12,R8,L8,
# C = L4,L4,L6,
# B = L6,R12,R8,L8,
# A = L6,R12,L6,L8,L8,
# C = L4,L4,L6,
# B = L6,R12,R8,L8,
# C = L4,L4,L6,
# A = L6,R12,L6,L8,L8


movements = ['A',',','A',',','B',',','C',',','B',',','A',',','C',',','B',',','C',',','A',10,'L',',','6',',','R',',','1','2',',','L',',','6',',','L',',','8',',','L',',','8',10,'L',',','6',',','R',',','1','2',',','R',',','8',',','L',',','8',10,'L',',','4',',','L',',','4',',','L',',','6',10,'N',10]

loadIntCodeProgram()
programMemory[0] = 2
myCPU = CPU()
myCPU.initCPU()
outOffset = 0
printQueue = ''

print("Running Droid")
while True:
	myCPU.runCPU()
	state = myCPU.getProgState()
	#print(state)
	if state == 'outputReady':
		if outputQueue[0] == 10:
			print(printQueue)
			printQueue = ''
		else:
			try:
				printQueue += str(unichr(outputQueue[0]))
			except:
				print(outputQueue[0])
		del outputQueue[0]
		myCPU.setProgState('outputDone')
	elif state == 'waitForInput':
		if outOffset < len(movements):
			#print("sending out",movements[outOffset])
			if movements[outOffset] == 10:
				inputQueue.append(movements[outOffset])
				print(" ")
			elif movements[outOffset] == ',':
				inputQueue.append(ord(movements[outOffset]))
				print(',',end='')
			else:
				inputQueue.append(ord(movements[outOffset]))
				print(movements[outOffset],end='')
			outOffset += 1
		else:
			print("Out of input buffer")
			inputQueue.append('Y')
	elif state == 'progDone':
		break
	else:
		print(state)
		assert False,"ended"

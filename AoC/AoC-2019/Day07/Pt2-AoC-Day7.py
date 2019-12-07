# Pt2-AoCDay7.py
# 2019 Advent of Code
# Day 7
# Part 2

from __future__ import print_function

"""
--- Part Two ---
It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)
Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input, and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback loop: the signal will be sent through the amplifiers many times.

In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce output many times before halting. Provide each amplifier its phase setting at its first input instruction; all further input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens, the last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal that can be sent to the thrusters using the new phase settings and feedback loop arrangement.

Here are some example programs:

Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be sent to the thrusters?

57045 was the last answer

518910 is too low
20211922 is too low

Output Result 39016654

"""

"""
Instead of getting input fed into the function it has to wait on input from the previous stage

"""

debugMessage = False

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	phaseVal = 0
	progState = ''
	programCounter = 0
	outVal = 0
	def setPhase(self, phaseVal):
		self.phaseVal = phaseVal
		self.progState = 'phaseState' 
		# state transitions are 
		# 'phaseState' => 
		# 'inputReady' => 'waitingOnInput' => 
		# 'inputReady' => 'waitingOnInput' => 
		# 'progDone'
		self.programCounter = 0
		self.outVal = 0
		

	def mathOperation(self, currentOp, programMemory):
		if currentOp[1] == 0:	# position mode
			pos = programMemory[self.programCounter+1]
			val1 = programMemory[pos]
			if debugMessage:
				print("mathOperation: Read parm 1 from pos :",pos,"value :",val1)
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[self.programCounter+1]
			if debugMessage:
				print("mathOperation: Immed parm 1 :",val1)
		else:
			if debugMessage:
				print("mathOperation: Unexpected currentOp[1]",currentOp[1])
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
		else:
			if debugMessage:
				print("mathOperation: Unexpected currentOp[2]",currentOp[2])
			exit()
		if currentOp[3] != 0:	
			if debugMessage:
				print("mathOperation: Error - Should have been position mode not immediate mode")
			exit()
		return[val1,val2]
		
	def branchEval(self, currentOp, programMemory):
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
	#	print("instruction",instruction)
		instructionAsFiveDigits = self.intTo5DigitString(instruction)
	#	print("instruction as five digits",instructionAsFiveDigits)
		parm3=int(instructionAsFiveDigits[0])
		parm2=int(instructionAsFiveDigits[1])
		parm1=int(instructionAsFiveDigits[2])
		opcode=int(instructionAsFiveDigits[3:5])
		retVal=[opcode,parm1,parm2,parm3]
	#	print(retVal)
		return retVal

	def getProgState(self):
		return(self.progState)
	
	def runCPU(self, programMemory, inputVal):
		#print("Length of list is :",len(programMemory))
		if debugMessage:
			print("Reached runCPU")
		if self.progState == 'waitingOnInput':
			self.progState = 'inputReady'
		while self.progState != 'waitingOnInput':
			#print("Memory Dump :",programMemory)
			currentOp = self.extractFieldsFromInstruction(programMemory[self.programCounter])
			if debugMessage:
				print("PC =",self.programCounter,", Opcode",programMemory[self.programCounter],", currentOp",currentOp)
			if currentOp[0] == 1:		# Addition Operator
				valPair = self.mathOperation(currentOp,programMemory)
				result = valPair[0] + valPair[1]
				posOut = programMemory[self.programCounter+3]
				programMemory[posOut] = result
				if debugMessage:
						print("Add: Store sum at pos :",posOut,"value :",result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				valPair = self.mathOperation(currentOp,programMemory)
				result = valPair[0] * valPair[1]
				posOut = programMemory[self.programCounter+3]
				programMemory[posOut] = result
				if debugMessage:
					print("Mult: Stored product at pos : ",posOut,"value :",result)
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				if debugMessage:
					print("Reached input operator state =",self.progState)
				pos = programMemory[self.programCounter+1]
				if self.progState == 'phaseState':
					programMemory[pos] = self.phaseVal
					self.progState = 'inputReady'
					self.programCounter = self.programCounter + 2
				elif self.progState == 'inputReady':
					pos = programMemory[self.programCounter+1]
					programMemory[pos] = inputVal
					self.progState = 'waitingOnOutput'
					self.programCounter = self.programCounter + 2
				elif self.progState == 'waitingOnInput':					
					print("Waiting on input")
					return(-1)
				if debugMessage:
					print("Received input value :",inputVal,"Storing at pos :",pos)
			elif currentOp[0] == 4:		# Output Operator
				if debugMessage:
					print("Reached output")
				pos = programMemory[self.programCounter+1]
				if debugMessage:
					print("*** Output value :",programMemory[pos])
				outVal = programMemory[pos]
				self.progState = 'waitingOnInput'
				self.programCounter = self.programCounter + 2
				return(outVal)
			elif currentOp[0] == 5:		# Jump if true
				valPair = self.branchEval(currentOp,programMemory)
				if debugMessage:
					print("Jump-if-true parm 1 :",valPair[0])
					print("Jump-if-true parm 2 :",valPair[1])
				if valPair[0] != 0:
					self.programCounter = valPair[1]
				else:
					self.programCounter = self.programCounter + 3
			elif currentOp[0] == 6:		# Jump if false
				valPair = self.branchEval(currentOp,programMemory)
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
				valPair = self.branchEval(currentOp,programMemory)
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
				valPair = self.branchEval(currentOp,programMemory)
				if debugMessage:
					print("Evaluate-if-equal parm 1 :",valPair[0])
					print("Evaluate-if-equal parm 2 :",valPair[1])
				pos = programMemory[self.programCounter+3]
				if valPair[0] == valPair[1]:
					programMemory[pos] = 1
				else:
					programMemory[pos] = 0
				self.programCounter = self.programCounter + 4
			elif currentOp[0] == 99:
				self.progState = 'progDone'
				if debugMessage:
					pass
					print("CPU program ended normally")
				return(-2)
			else:
				print("error - unexpected opcode", currentOp[0])
				exit()

def testCPUOps(object):
	""" Code to test the new opcodes and make sure they work as expected
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

def genTestVecs(startPh, endPh):
	vecsList = []
	for dig0 in range(startPh,endPh+1):
		for dig1 in range(startPh,endPh+1):
			if dig1!= dig0:
				for dig2 in range(startPh,endPh+1):
					if ((dig2 != dig1) and (dig2 != dig0)):
						for dig3 in range(startPh,endPh+1):
							if ((dig3 != dig2) and (dig3 != dig1) and (dig3 != dig0)):
								for dig4 in range(startPh,endPh+1):
									if ((dig4 != dig3) and (dig4 != dig2) and (dig4 != dig1) and (dig4 != dig0)):
										vecsList.append([dig0,dig1,dig2,dig3,dig4])	
	return(vecsList)

debugMessage = False

#myTestCPU = CPU()
#testCPUOps(myTestCPU)

debugMessage = False

progName = "input.txt"

startPhase = 5
endPhase = 9
testVectors = genTestVecs(startPhase,endPhase)
#print(testVectors)

#testVectors=[[9,7,8,5,6]]
onePass = False

maxVal = 0
AmpCPUA = CPU()
AmpCPUB = CPU()
AmpCPUC = CPU()
AmpCPUD = CPU()
AmpCPUE = CPU()

program1 = []
program2 = []
program3 = []
program4 = []
program5 = []

for phaseSettings in testVectors:
	AmpCPUA.setPhase(phaseSettings[0])
	AmpCPUB.setPhase(phaseSettings[1])
	AmpCPUC.setPhase(phaseSettings[2])
	AmpCPUD.setPhase(phaseSettings[3])
	AmpCPUE.setPhase(phaseSettings[4])

	#print("Phase settings :",phaseSettings,"= ",end='')
	progRunning = True
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program1 = map(int, inLine.split(','))
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program2 = map(int, inLine.split(','))
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program3 = map(int, inLine.split(','))
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program4 = map(int, inLine.split(','))
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program5 = map(int, inLine.split(','))
	if debugMessage:
		print("Program code:",program1)

	resultE = 0
	biggest = 0
	while progRunning:
		if debugMessage:
			print("AmpA")
		inputValsA = resultE
		resultA = AmpCPUA.runCPU(program1,resultE)
		if debugMessage:
			print("resultA :",resultA)

		if debugMessage:
			print("AmpB")
		inputValsB = resultA
		resultB = AmpCPUB.runCPU(program2,inputValsB)
		if debugMessage:
			print("resultB :",resultB)

		if debugMessage:
			print("AmpC")
		inputValsC = resultB
		resultC = AmpCPUC.runCPU(program3,inputValsC)
		if debugMessage:
			print("resultC :",resultC)

		if debugMessage:
			print("AmpD")
		inputValsD = resultC
		resultD = AmpCPUD.runCPU(program4,inputValsD)
		if debugMessage:
			print("resultC :",resultD)

		if debugMessage:
			print("AmpE")
		inputValsE = resultD
		resultE = AmpCPUE.runCPU(program5,inputValsE)
		if debugMessage:
			print("resultE :",resultE)

		if ((AmpCPUA.getProgState() == 'progDone') and (AmpCPUB.getProgState() == 'progDone') and (AmpCPUC.getProgState() == 'progDone') and (AmpCPUD.getProgState() == 'progDone') and (AmpCPUE.getProgState() == 'progDone')):
			progRunning = False
		if resultE > maxVal:
			maxVal = resultE
	if maxVal > biggest:
		biggest = maxVal
	
print("Result",biggest)
exit()

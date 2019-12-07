# Pt1-AoCDay7.py
# 2019 Advent of Code
# Day 7
# Part 1

"""
--- Day 7: Amplification Circuit ---
Based on the navigational maps, you're going to need to send more power to your ship's thrusters to reach Santa in time. To do this, you'll need to configure a series of amplifiers already installed on the ship.

There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They are connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last amplifier's output leads to your ship's thrusters.

    O-------O  O-------O  O-------O  O-------O  O-------O
0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
    O-------O  O-------O  O-------O  O-------O  O-------O
The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that should run on your existing Intcode computer. Each amplifier will need to run a copy of the program.

When a copy of the program starts running on an amplifier, it will first use an input instruction to ask the amplifier for its current phase setting (an integer from 0 to 4). Each phase setting is used exactly once, but the Elves can't remember which amplifier needs which phase setting.

The program will then call another input instruction to get the amplifier's input signal, compute the correct output signal, and supply it back to the amplifier with an output instruction. (If the amplifier has not yet received an input signal, it waits until one arrives.)

Your job is to find the largest output signal that can be sent to the thrusters by trying every possible combination of phase settings on the amplifiers. Make sure that memory is not shared or reused between copies of the program.

For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean setting amplifier A to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that gets sent from amplifier E to the thrusters with the following steps:

Start the copy of the amplifier controller software that will run on amplifier A. At its first input instruction, provide it the amplifier's phase setting, 3. At its second input instruction, provide it the input signal, 0. After some calculations, it will use an output instruction to indicate the amplifier's output signal.
Start the software for amplifier B. Provide it the phase setting (1) and then whatever output signal was produced from amplifier A. It will then produce a new output signal destined for amplifier C.
Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B, then collect its output signal.
Run amplifier D's software, provide the phase setting (4) and input value, and collect its output signal.
Run amplifier E's software, provide the phase setting (0) and input value, and collect its output signal.
The final output signal from amplifier E would be sent to the thrusters. However, this phase setting sequence may not have been the best one; another sequence might have sent a higher signal to the thrusters.

Here are some example programs:

Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0
Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
Try every combination of phase settings on the amplifiers. What is the highest signal that can be sent to the thrusters?
"""
from __future__ import print_function

class CPU:
	""" CPU class
	Runs the program on the CPU 
	Takes input value
	Returns the output value
	"""
	def runCPU(self, programMemory, inputVals):
		#print("Length of list is :",len(programMemory))
		programCounter = 0
		outVal = 0
		inputValCounter = 0
		while 1:
			#print("Memory Dump :",programMemory)
			currentOp = self.extractFieldsFromInstruction(programMemory[programCounter])
			if debugMessage:
				print("PC =",programCounter,", Opcode",programMemory[programCounter],", currentOp",currentOp)
			if currentOp[0] == 1:		# Addition Operator
				valPair = self.mathOperation(programCounter,currentOp,programMemory)
				result = valPair[0] + valPair[1]
				posOut = programMemory[programCounter+3]
				programMemory[posOut] = result
				if debugMessage:
						print("Add: Store sum at pos :",posOut,"value :",result)
				programCounter = programCounter + 4
			elif currentOp[0] == 2:		# Multiplication Operator
				valPair = self.mathOperation(programCounter,currentOp,programMemory)
				result = valPair[0] * valPair[1]
				posOut = programMemory[programCounter+3]
				programMemory[posOut] = result
				if debugMessage:
					print("Mult: Stored product at pos : ",posOut,"value :",result)
				programCounter = programCounter + 4
			elif currentOp[0] == 3:		# Input Operator
				pos = programMemory[programCounter+1]
				programMemory[pos] = inputVals[inputValCounter]
				inputValCounter = inputValCounter + 1
				if debugMessage:
					print("Read input value :",inputVal,"Storing at pos :",pos)
				programCounter = programCounter + 2
			elif currentOp[0] == 4:		# Output Operator
				pos = programMemory[programCounter+1]
				if debugMessage:
					print("*** Output value :",programMemory[pos])
				outVal = programMemory[pos]
				programCounter = programCounter + 2
			elif currentOp[0] == 5:		# Jump if true
				valPair = self.branchEval(programCounter,currentOp,programMemory)
				if debugMessage:
					print("Jump-if-true parm 1 :",valPair[0])
					print("Jump-if-true parm 2 :",valPair[1])
				if valPair[0] != 0:
					programCounter = valPair[1]
				else:
					programCounter = programCounter + 3
			elif currentOp[0] == 6:		# Jump if false
				valPair = self.branchEval(programCounter,currentOp,programMemory)
				if debugMessage:
					print("runCPU: Jump-if-false parm 1 :",valPair[0])
					print("runCPU: Jump-if-false parm 2 :",valPair[1])
				if valPair[0] == 0:
					if debugMessage:
						print("Taking branch")
					programCounter = valPair[1]
				else:
					if debugMessage:
						print("Not taking branch")
					programCounter = programCounter + 3	
			elif currentOp[0] == 7:	# Evaluate if less-than
				valPair = self.branchEval(programCounter,currentOp,programMemory)
				if debugMessage:
					print("Evaluate-if-less-than parm 1 :",valPair[0])
					print("Evaluate-if-less-than parm 2 :",valPair[1])
				pos = programMemory[programCounter+3]
				if valPair[0] < valPair[1]:
					programMemory[pos] = 1
				else:
					programMemory[pos] = 0
				programCounter = programCounter + 4
			elif currentOp[0] == 8:	# Evaluate if equal
				valPair = self.branchEval(programCounter,currentOp,programMemory)
				if debugMessage:
					print("Evaluate-if-equal parm 1 :",valPair[0])
					print("Evaluate-if-equal parm 2 :",valPair[1])
				pos = programMemory[programCounter+3]
				if valPair[0] == valPair[1]:
					programMemory[pos] = 1
				else:
					programMemory[pos] = 0
				programCounter = programCounter + 4
			elif currentOp[0] == 99:
				if debugMessage:
					print("Program ended normally")
				return(outVal)
			else:
				print("error - unexpected opcode", currentOp[0])
				exit()

	def mathOperation(self, programCounter, currentOp, programMemory):
		if currentOp[1] == 0:	# position mode
			pos = programMemory[programCounter+1]
			val1 = programMemory[pos]
			if debugMessage:
				print("mathOperation: Read parm 1 from pos :",pos,"value :",val1)
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[programCounter+1]
			if debugMessage:
				print("mathOperation: Immed parm 1 :",val1)
		else:
			if debugMessage:
				print("mathOperation: Unexpected currentOp[1]",currentOp[1])
			exit()
		if currentOp[2] == 0:	# position mode
			pos = programMemory[programCounter+2]
			val2 = programMemory[pos]
			if debugMessage:
				print("mathOperation: Read parm 2 from pos :",pos,"value :",val2)
		elif currentOp[2] == 1:	# immediate mode
			val2 = programMemory[programCounter+2]
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
		
	def branchEval(self, programCounter, currentOp, programMemory):
		if debugMessage:
			print("branchEval: Reached function")
		if currentOp[1] == 0:	# position mode
			pos = programMemory[programCounter+1]
			val1 = programMemory[pos]
			if debugMessage:
				print("branchEval: Read (parm 1) from pos :",pos,"value :",val1)
		elif currentOp[1] == 1:	# immediate mode
			val1 = programMemory[programCounter+1]
			if debugMessage:
				print("branchEval: Immed parm 1 :",val1)
		else:
			pass
			if debugMessage:
				print("branchEval: Unexpected currentOp[1]",currentOp[1])
		if currentOp[2] == 0:	# position mode
			pos = programMemory[programCounter+2]
			val2 = programMemory[pos]
			if debugMessage:
				print("branchEval: Read (parm 2) from pos :",pos,"value :",val2)
		elif currentOp[2] == 1:	# immediate mode
			val2 = programMemory[programCounter+2]
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

def genTestVecs():
	vecsList = []
	for dig0 in range(0,5):
		print("dig0",dig0)
		for dig1 in range(0,5):
			if dig1!= dig0:
				for dig2 in range(0,5):
					if ((dig2 != dig1) and (dig2 != dig0)):
						for dig3 in range(0,5):
							if ((dig3 != dig2) and (dig3 != dig1) and (dig3 != dig0)):
								for dig4 in range(0,5):
									if ((dig4 != dig3) and (dig4 != dig2) and (dig4 != dig1) and (dig4 != dig0)):
										vecsList.append([dig0,dig1,dig2,dig3,dig4])	
	return(vecsList)

debugMessage = False

#myTestCPU = CPU()
#testCPUOps(myTestCPU)

#debugMessage = True

progName = "input.txt"
testVectors = genTestVecs()
phaseSettings = [1,0,4,3,2]

maxVal = 0
for phaseSettings in testVectors:
#	print("phaseSettings",phaseSettings)
	AmpCPUA = CPU()
#	print("Amplifier A = ",end='')
	inputValsA = [phaseSettings[0],0]
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program = map(int, inLine.split(','))
	resultA = AmpCPUA.runCPU(program,inputValsA)
	print("AmpA",resultA)

	AmpCPUB = CPU()
#	print("Amplifier B = ",end='')
	inputValsB = [phaseSettings[1],resultA]
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program = map(int, inLine.split(','))
	resultB = AmpCPUB.runCPU(program,inputValsB)
	print("AmpB",resultB)

	AmpCPUC = CPU()
#	print("Amplifier C = ",end='')
	inputValsC = [phaseSettings[2],resultB]
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program = map(int, inLine.split(','))
	resultC = AmpCPUC.runCPU(program,inputValsC)
	print("AmpC",resultC)

	AmpCPUD = CPU()
#	print("Amplifier D = ",end='')
	inputValsD = [phaseSettings[3],resultC]
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program = map(int, inLine.split(','))
	resultD = AmpCPUD.runCPU(program,inputValsD)
	print("AmpD",resultD)

	AmpCPUE = CPU()
#	print("Amplifier E = ",end='')
	inputValsE = [phaseSettings[4],resultD]
	with open(progName, 'r') as filehandle:  
		inLine = filehandle.readline()
		program = map(int, inLine.split(','))
	resultE = AmpCPUE.runCPU(program,inputValsE)
	print("AmpE",resultE)
	if resultE > maxVal:
		maxVal = resultE

print("Output Result",maxVal)
exit()

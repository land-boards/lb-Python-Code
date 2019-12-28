# Pt2-AoCDay5.py
# 2019 Advent of Code
# Day 5
# Part 2
# https://adventofcode.com/2019/day/5

"""
--- Day 5: Sunny with a Chance of Asteroids ---

--- Part Two ---

The air conditioner comes online! Its cold air feels good for a while, but then the TEST alarms start to go off. Since the air conditioner can't vent its heat anywhere but back into the spacecraft, it's actually making the air inside the ship warmer.

Instead, you'll need to use the TEST to extend the thermal radiators. Fortunately, the diagnostic program (your puzzle input) is already equipped for this. Unfortunately, your Intcode computer is not.

Your computer is only missing a few opcodes:

    Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
    Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
    Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.

Like all instructions, these instructions need to support parameter modes as described above.

Normally, after an instruction is finished, the instruction pointer increases by the number of values in that instruction. However, if the instruction modifies the instruction pointer, that value is used and the instruction pointer is not automatically increased.

For example, here are several programs that take one input, compare it to the value 8, and then produce one output:

    3,9,8,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
    3,9,7,9,10,9,4,9,99,-1,8 - Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
    3,3,1108,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
    3,3,1107,-1,8,3,4,3,99 - Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).

Here are some jump tests that take an input, then output 0 if the input was zero or 1 if the input was non-zero:

    3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9 (using position mode)
    3,3,1105,-1,9,1101,0,0,12,4,12,99,1 (using immediate mode)

Here's a larger example:

3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99

The above example program uses an input instruction to ask for a single number. The program will then output 999 if the input value is below 8, output 1000 if the input value is equal to 8, or output 1001 if the input value is greater than 8.

This time, when the TEST diagnostic program runs its input instruction to get the ID of the system to test, provide it 5, the ID for the ship's thermal radiator controller. This diagnostic test suite only outputs one number, the diagnostic code.

What is the diagnostic code for system ID 5?

"""

from __future__ import print_function

def mathOperation(programCounter,currentOp,listOfNumbers):
	if currentOp[1] == 0:	# position mode
		pos = listOfNumbers[programCounter+1]
		val1 = listOfNumbers[pos]
		if debugMessage:
			print("mathOperation: Read parm 1 from pos :",pos,"value :",val1)
	elif currentOp[1] == 1:	# immediate mode
		val1 = listOfNumbers[programCounter+1]
		if debugMessage:
			print("mathOperation: Immed parm 1 :",val1)
	else:
		if debugMessage:
			print("mathOperation: Unexpected currentOp[1]",currentOp[1])
		exit()
	if currentOp[2] == 0:	# position mode
		pos = listOfNumbers[programCounter+2]
		val2 = listOfNumbers[pos]
		if debugMessage:
			print("mathOperation: Read parm 2 from pos :",pos,"value :",val2)
	elif currentOp[2] == 1:	# immediate mode
		val2 = listOfNumbers[programCounter+2]
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
	
def branchEval(programCounter,currentOp,listOfNumbers):
	if debugMessage:
		print("branchEval: Reached function")
	if currentOp[1] == 0:	# position mode
		pos = listOfNumbers[programCounter+1]
		val1 = listOfNumbers[pos]
		if debugMessage:
			print("branchEval: Read (parm 1) from pos :",pos,"value :",val1)
	elif currentOp[1] == 1:	# immediate mode
		val1 = listOfNumbers[programCounter+1]
		if debugMessage:
			print("branchEval: Immed parm 1 :",val1)
	else:
		pass
		if debugMessage:
			print("branchEval: Unexpected currentOp[1]",currentOp[1])
	if currentOp[2] == 0:	# position mode
		pos = listOfNumbers[programCounter+2]
		val2 = listOfNumbers[pos]
		if debugMessage:
			print("branchEval: Read (parm 2) from pos :",pos,"value :",val2)
	elif currentOp[2] == 1:	# immediate mode
		val2 = listOfNumbers[programCounter+2]
		if debugMessage:
			print("branchEval: Immed parm 2 :",val2)
	else:
		pass
		if debugMessage:
			print("branchEval: Unexpected currentOp[2]",currentOp[2])
	return[val1,val2]
	
def processList(listOfNumbers):
	#print("Length of list is :",len(listOfNumbers))
	programCounter = 0
	outVal = 0
	while 1:
		#print("Memory Dump :",listOfNumbers)
		currentOp = extractFieldsFromInstruction(listOfNumbers[programCounter])
		if debugMessage:
			print("PC =",programCounter,", Opcode",listOfNumbers[programCounter],", currentOp",currentOp)
		if currentOp[0] == 1:		# Addition Operator
			valPair = mathOperation(programCounter,currentOp,listOfNumbers)
			result = valPair[0] + valPair[1]
			posOut = listOfNumbers[programCounter+3]
			listOfNumbers[posOut] = result
			if debugMessage:
					print("Add: Store sum at pos :",posOut,"value :",result)
			programCounter = programCounter + 4
		elif currentOp[0] == 2:		# Multiplication Operator
			valPair = mathOperation(programCounter,currentOp,listOfNumbers)
			result = valPair[0] * valPair[1]
			posOut = listOfNumbers[programCounter+3]
			listOfNumbers[posOut] = result
			if debugMessage:
				print("Mult: Stored product at pos : ",posOut,"value :",result)
			programCounter = programCounter + 4
		elif currentOp[0] == 3:		# Input Operator
			pos = listOfNumbers[programCounter+1]
			listOfNumbers[pos] = inputVal
			if debugMessage:
				print("Read input value :",inputVal,"Storing at pos :",pos)
			programCounter = programCounter + 2
		elif currentOp[0] == 4:		# Output Operator
			pos = listOfNumbers[programCounter+1]
			if debugMessage:
				print("*** Output value :",listOfNumbers[pos])
			outVal = listOfNumbers[pos]
			programCounter = programCounter + 2
		elif currentOp[0] == 5:		# Jump if true
			valPair = branchEval(programCounter,currentOp,listOfNumbers)
			if debugMessage:
				print("Jump-if-true parm 1 :",valPair[0])
				print("Jump-if-true parm 2 :",valPair[1])
			if valPair[0] != 0:
				programCounter = valPair[1]
			else:
				programCounter = programCounter + 3
		elif currentOp[0] == 6:		# Jump if false
			valPair = branchEval(programCounter,currentOp,listOfNumbers)
			if debugMessage:
				print("processList: Jump-if-false parm 1 :",valPair[0])
				print("processList: Jump-if-false parm 2 :",valPair[1])
			if valPair[0] == 0:
				print("Taking branch")
				programCounter = valPair[1]
			else:
				print("Not taking branch")
				programCounter = programCounter + 3	
		elif currentOp[0] == 7:	# Evaluate if less-than
			valPair = branchEval(programCounter,currentOp,listOfNumbers)
			if debugMessage:
				print("Evaluate-if-less-than parm 1 :",valPair[0])
				print("Evaluate-if-less-than parm 2 :",valPair[1])
			pos = listOfNumbers[programCounter+3]
			if valPair[0] < valPair[1]:
				listOfNumbers[pos] = 1
			else:
				listOfNumbers[pos] = 0
			programCounter = programCounter + 4
		elif currentOp[0] == 8:	# Evaluate if equal
			valPair = branchEval(programCounter,currentOp,listOfNumbers)
			if debugMessage:
				print("Evaluate-if-equal parm 1 :",valPair[0])
				print("Evaluate-if-equal parm 2 :",valPair[1])
			pos = listOfNumbers[programCounter+3]
			if valPair[0] == valPair[1]:
				listOfNumbers[pos] = 1
			else:
				listOfNumbers[pos] = 0
			programCounter = programCounter + 4
		elif currentOp[0] == 99:
			if debugMessage:
				print("Program ended normally")
			return(outVal)
		else:
			print("error - unexpected opcode", currentOp[0])
			exit()

def intTo5DigitString(instruction):
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

def extractFieldsFromInstruction(instruction):
	""" Take the Instruction and turn into opcode fields
	ABCDE
	A = mode of 3rd parm
	B = mode of 2nd parm
	C = mode of 1st parm
	DE = opcode
	
	:returns: [opcode,parm1,parm2,parm3]
	"""
#	print("instruction",instruction)
	instructionAsFiveDigits = intTo5DigitString(instruction)
#	print("instruction as five digits",instructionAsFiveDigits)
	parm3=int(instructionAsFiveDigits[0])
	parm2=int(instructionAsFiveDigits[1])
	parm1=int(instructionAsFiveDigits[2])
	opcode=int(instructionAsFiveDigits[3:5])
	retVal=[opcode,parm1,parm2,parm3]
#	print(retVal)
	return retVal

debugMessage = False
# Using position mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
print("Test case 01A - ",end='')
inputVal = 7
numbers=[3,9,8,9,10,9,4,9,99,-1,8]
if processList(numbers) == 0:
	print("Passed")
else:
	print("Failed")
print("Test case 01B - ",end='')
inputVal = 8
numbers=[3,9,8,9,10,9,4,9,99,-1,8]
if processList(numbers) == 1:
	print("Passed")
else:
	print("Failed")

# Using position mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
print("Test case 02A - ",end='')
inputVal = 7
numbers=[3,9,7,9,10,9,4,9,99,-1,8]
if processList(numbers) == 1:
	print("Passed")
else:
	print("Failed")
print("Test case 02B - ",end='')
inputVal = 8
numbers=[3,9,7,9,10,9,4,9,99,-1,8]
if processList(numbers) == 0:
	print("Passed")
else:
	print("Failed")

# Using immediate mode, consider whether the input is equal to 8; output 1 (if it is) or 0 (if it is not).
print("Test case 03A - ",end='')
inputVal = 7
numbers=[3,3,1108,-1,8,3,4,3,99]
if processList(numbers) == 0:
	print("Passed")
else:
	print("Failed")
print("Test case 03B - ",end='')
inputVal = 8
numbers=[3,3,1108,-1,8,3,4,3,99]
if processList(numbers) == 1:
	print("Passed")
else:
	print("Failed")
	
# Using immediate mode, consider whether the input is less than 8; output 1 (if it is) or 0 (if it is not).
print("Test case 04A - ",end='')
inputVal = 7
numbers=[3,3,1107,-1,8,3,4,3,99]
if processList(numbers) == 1:
	print("Passed")
else:
	print("Failed")
print("Test case 04B - ",end='')
inputVal = 8
numbers=[3,3,1107,-1,8,3,4,3,99]
if processList(numbers) == 0:
	print("Passed")
else:
	print("Failed")
	
debugMessage = True
print("Test case 05A - ",end='')
inputVal = 1
numbers=[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
if debugMessage:
	print("numbers",numbers)
	print("inputVal",inputVal)
if processList(numbers) == 1:
	print("Passed")
else:
	print("Failed")
	exit()
	
print("Test case 05B - ",end='')
inputVal = 0
numbers=[3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
if debugMessage:
	print("05B - numbers :",numbers)
	print("05B - inputVal :",inputVal)
if processList(numbers) == 0:
	print("Passed")
else:
	print("Failed")
	exit()

debugMessage = True

print("\n*** Real data")
inputVal = 5
# open file and read the program memory
with open('AOC2019D05input.txt', 'r') as filehandle:  
	numbers = [int(charX) for charX in filehandle.readline().split(',')]
print(processList(numbers))

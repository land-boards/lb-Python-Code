# Pt1-AoCDay5.py
# 2019 Advent of Code
# Day 5
# Part 1

"""
--- Day 5: Sunny with a Chance of Asteroids ---
You're starting to sweat as the ship makes its way toward Mercury. The Elves suggest that you get the air conditioner working by upgrading your ship computer to support the Thermal Environment Supervision Terminal.

The Thermal Environment Supervision Terminal (TEST) starts by running a diagnostic program (your puzzle input). The TEST diagnostic program will run on your existing Intcode computer after a few modifications:

First, you'll need to add two new instructions:

Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the instruction 3,50 would take an input value and store it at address 50.
Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
Programs that use these instructions will come with documentation that explains what should be connected to the input and output. The program 3,0,4,0,99 outputs whatever it gets as input, then halts.

Second, you'll need to add support for parameter modes:

Each parameter of an instruction is handled based on its parameter mode. Right now, your ship computer already understands parameter mode 0, position mode, which causes the parameter to be interpreted as a position - if the parameter is 50, its value is the value stored at address 50 in memory. Until now, all parameters have been in position mode.

Now, your ship computer will also need to handle parameters in mode 1, immediate mode. In immediate mode, a parameter is interpreted as a value - if the parameter is 50, its value is simply 50.

Parameter modes are stored in the same value as the instruction's opcode. The opcode is a two-digit number based only on the ones and tens digit of the value, that is, the opcode is the rightmost two digits of the first value in an instruction. Parameter modes are single digits, one per parameter, read right-to-left from the opcode: the first parameter's mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third parameter's mode is in the ten-thousands digit, and so on. Any missing modes are 0.

For example, consider the program 1002,4,3,4,33.

The first instruction, 1002,4,3,4, is a multiply instruction - the rightmost two digits of the first value, 02, indicate opcode 2, multiplication. Then, going right to left, the parameter modes are 0 (hundreds digit), 1 (thousands digit), and 0 (ten-thousands digit, not present and therefore zero):

ABCDE
 1002

DE - two-digit opcode,      02 == opcode 2
 C - mode of 1st parameter,  0 == position mode
 B - mode of 2nd parameter,  1 == immediate mode
 A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero
This instruction multiplies its first two parameters. The first parameter, 4 in position mode, works like it did before - its value is the value stored at address 4 (33). The second parameter, 3 in immediate mode, simply has value 3. The result of this operation, 33 * 3 = 99, is written according to the third parameter, 4 in position mode, which also works like it did before - 99 is written to address 4.

Parameters that an instruction writes to will never be in immediate mode.

Finally, some notes:

It is important to remember that the instruction pointer should increase by the number of values in the instruction after the instruction finishes. Because of the new instructions, this amount is no longer always 4.
Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1, store the result in position 4).
The TEST diagnostic program will start by requesting from the user the ID of the system to test by running an input instruction - provide it 1, the ID for the ship's air conditioner unit.

It will then perform a series of diagnostic tests confirming that various parts of the Intcode computer, like parameter modes, function correctly. For each test, it will run an output instruction indicating how far the result of the test was from the expected value, where 0 means the test was successful. Non-zero outputs mean that a function is not working correctly; check the instructions that were run before the output instruction to see which one failed.

Finally, the program will output a diagnostic code and immediately halt. This final output isn't an error; an output followed immediately by a halt means the program finished. If all outputs were zero except the diagnostic code, the diagnostic program ran successfully.

After providing 1 to the only input instruction and passing all the tests, what diagnostic code does the program produce?

223 is too low

"""
from __future__ import print_function

def processList(listOfNumbers):
	print("Length of list is :",len(listOfNumbers))
	programCounter = 0
	while 1:
		currentOp = extractFieldsFromInstruction(listOfNumbers[programCounter])
		print("PC",programCounter,"Opcode",listOfNumbers[programCounter],"currentOp",currentOp)
		if currentOp[0] == 1:		# Addition Operator
			if currentOp[1] == 0:	# position mode
				pos = listOfNumbers[programCounter+1]
				val1 = listOfNumbers[pos]
				print("Add: Read parm 1 from pos :",pos,"value :",val1)
			elif currentOp[1] == 1:	# immediate mode
				val1 = listOfNumbers[programCounter+1]
				print("Add: Immed parm 1 :",val1)
			if currentOp[2] == 0:	# position mode
				pos = listOfNumbers[programCounter+2]
				val2 = listOfNumbers[pos]
				print("Add: Read parm 2 from pos :",pos,"value :",val2)
			elif currentOp[2] == 1:	# immediate mode
				val2 = listOfNumbers[programCounter+2]
				print("Add: Immed parm 2 :",val2)
			if currentOp[3] != 0:	
				print("Should have been position mode not immediate mode")
				exit()
			result = val1 + val2
			posOut = listOfNumbers[programCounter+3]
			listOfNumbers[posOut] = result
			print("Add: Store sum at pos :",posOut,"value :",result)
			programCounter = programCounter + 4
		elif currentOp[0] == 2:		# Multiplication Operator
			if currentOp[1] == 0:	# position mode
				pos = listOfNumbers[programCounter+1]
				val1 = listOfNumbers[pos]
				print("Mult: Read parm 1 from pos :",pos,"value :",val1)
			elif currentOp[1] == 1:	# immediate mode
				val1 = listOfNumbers[programCounter+1]
			if currentOp[2] == 0:	# position mode
				pos = listOfNumbers[programCounter+2]
				val2 = listOfNumbers[pos]
				print("Mult: Read parm 2 from pos :",pos,"value :",val2)
			elif currentOp[2] == 1:	# immediate mode
				val2 = listOfNumbers[programCounter+2]
			if currentOp[3] != 0:	
				print("Should have been position mode not immediate mode")
				exit()
			result = val1 * val2
			posOut = listOfNumbers[programCounter+3]
			listOfNumbers[posOut] = result
			print("Stored product : ",result,"at :",posOut)
			programCounter = programCounter + 4
		elif currentOp[0] == 3:	# Input Operator
			pos = listOfNumbers[programCounter+1]
			listOfNumbers[pos] = inputVal
			print("Read input value :",inputVal)
			print("Storing at :",pos)
			programCounter = programCounter + 2
		elif currentOp[0] == 4:	# Output Operator
			print("*** Output value :",listOfNumbers[programCounter+1])
			programCounter = programCounter + 2
		elif currentOp[0] == 99:
			print("Program ended normally")
			exit()
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

inputVal = 1
# open file and read the content into an accumulated sum
with open('input.txt', 'r') as filehandle:  
	inLine = filehandle.readline()
	numbers = map(int, inLine.split(','))
	print(numbers)
processList(numbers)
exit()

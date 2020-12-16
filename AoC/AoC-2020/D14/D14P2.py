""" 

A0C 2020 Day 14 Part 2

"""

# def makeMemoryLocList(inProgram):
	# """
	# programLine[0] = instruction
	# programLine[1] = address
	# programLine[2] = value
	# add to list of addressed
	# """
	# global usedMemoryLocations
	# for programLine in inProgram:
		# if programLine[0] == 'mem':
			# if int(programLine[1]) not in usedMemoryLocations:
				# usedMemoryLocations.append(int(programLine[1]))
	
# def initMemoryContents():
	# """
	# Fill memory with 0's
	# """
	# global usedMemoryLocations
	# global memoryLocationValuesList
	# for memoryAddress in usedMemoryLocations:
		# # print('memoryAddress',memoryAddress)
		# memoryLine = []
		# memoryLine.append(int(memoryAddress))
		# memoryLine.append(0)
		# memoryLocationValuesList.append(memoryLine)
# def setMaskVals(maskString):
	# global orBitMask
	# global andBitMask
	# global preserveBitMask
	# # print('maskString',maskString)
	# newVal = 0
	# preserveBitMask = 0
	# andBitMask = 0
	# orBitMask = 0
	# for pos in maskString:
		# if pos == 'X':
			# preserveBitMask |= 1
		# elif pos == '0':
			# andBitMask |= 1
		# elif pos == '1':
			# orBitMask |= 1
		# else:
			# # print('mask err')
			# assert False,'mask err'
		# preserveBitMask <<= 1
		# andBitMask <<= 1
		# orBitMask <<= 1
	# preserveBitMask >>= 1
	# andBitMask >>= 1
	# orBitMask >>= 1
	# # print('preserveBitMask',preserveBitMask)
	# # print('andBitMask',andBitMask)
	# # print('orBitMask',orBitMask)
	# return

# def applyMask(dataVal):
	# """
	# int('11111111', 2) >>>> 255
	# bin(10) >>> '0b1010'
	# """
	# global orBitMask
	# global andBitMask
	# global preserveBitMask
	# # print('\ndataVal',dataVal)
	# valStr = bin(dataVal)[2:]
	# # print('valStr',valStr)
	
	# # print('orBitMask',bin(orBitMask)[2:])
	# # print('andBitMask',bin(andBitMask)[2:])
	# # print('preserveBitMask',bin(preserveBitMask)[2:])
	# newValue = dataVal
	# newValue &= preserveBitMask
	# newValue |= orBitMask
	# # print('newValue',newValue)
	# # assert False,'stop'
	# return newValue

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def parseProgramToList(inList):
	"""
	mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
	mem[8] = 11
	mem[7] = 101
	mem[8] = 0
	"""
	newProgList = []
	for row in inList:
		if row[0:2] == 'ma':
			newRow = row.split(' = ')
			progLine = []
			progLine.append(newRow[0])
			progLine.append(newRow[1])
			newProgList.append(progLine)
			## print('mask')
			pass
		elif row[0:2] == 'me':
			newRow = row.replace('[',',')
			newRow = newRow.replace('[',',')
			newRow = newRow.replace(']',',')
			newRow = newRow.replace(' = ',',')
			newLine = newRow.split(',')
			## print('split line',newLine)
			progLine = []
			progLine.append(newLine[0])
			progLine.append(int(newLine[1]))
			progLine.append(int(newLine[3]))
			newProgList.append(progLine)
			## print('mem',newRow)
			pass
		else:
			# print(row)
			assert False,'parse err'
	return newProgList
	
def getMemoryValue(address):
	"""
	Return value at location
	"""
	global memoryLocationValuesList
	for memRow in memoryLocationValuesList:
		if memPairVal in memRow:
			if memPairVal[0] == address:
				return memPairVal[1]
	else:
		assert False,'getMemoryValue error'
	return 0
	
def setMemoryValue(address,value):
	"""
	Set memory value
	"""
	global memoryLocationValuesList
	for memPairVal in memoryLocationValuesList:
		if memPairVal[0] == address:
			memPairVal[1] = value
			return
	else:
		# print('address',address)
		# print('value',value)
		assert False,'setMemoryValue error'
	return 0

def isMemoryExists(address):
	global memoryLocationValuesList
	global usedMemoryLocations
	
	
inList = readFileToListOfStrings('input.txt')
inProgram = parseProgramToList(inList)
usedMemoryLocations = []
memoryLocationValuesList = []

maskString = ''
maxCountXs = 0

def makeListOf1s(numOfFloatBits):
	## print('numOfFloatBits',numOfFloatBits)
	rangeSize = 2
	listOf1s = []
	for num in range(pow(2,numOfFloatBits)):
		## print('num',num)
		str1s = bin(num)[2:]
		## print('str1s',str1s)
#		listOf1s.append(str1s)
		lenStr1s = len(str1s)
		newStr1s = ''
		for x in range(numOfFloatBits-lenStr1s):
			newStr1s += '0'
		for x in range(len(str1s)):
			newStr1s += str1s[x]
		## print('newStr1s',newStr1s)
		listOf1s.append(newStr1s)
	## print('listOf1s',listOf1s)
	## print()
	return listOf1s

def makeListOfOffsets(listOf1s,trimmedFloatBits):
	## print('(makeListOfOffsets): listOf1s',listOf1s)
	## print('trimmedFloatBits',trimmedFloatBits)
	listOfOffsets = []
	trimOffset = 0
	for off in listOf1s:
		## print('off',off)
		listOf1sOffset = 0
		outStr = ''
		for trimBit in trimmedFloatBits:
			if trimBit == '0':
				outStr += '0'
			else:
				outStr += off[listOf1sOffset]
				listOf1sOffset += 1
		listOfOffsets.append(outStr)
	## print('listOfOffsets',listOfOffsets)
	offNums = []
	for offNum in listOfOffsets:
		num = int(offNum,2)
		offNums.append(num)
	## print('offNums',offNums)
	return offNums
		
def genAddrList(addr):
	"""
	int('11111111', 2) >>>> 255
	bin(10) >>> '0b1010'
	
	If the bitmask bit is 0, 
		the corresponding memory address bit 
		is unchanged.
	If the bitmask bit is 1, 
		the corresponding memory address bit 
		is overwritten with 1.
	If the bitmask bit is X, 
		the corresponding memory address bit 
		is floating.
	"""
	global maskString
	## print('addr',addr)
	## print('addr                                    ',bin(addr)[2:])
	## print('maskString',maskString)
	maskForce0 = maskString.replace('1','0')
	maskForce0 = maskForce0.replace('X','1') # Floating forces to zero
	## print('maskForce0',maskForce0)
	maskForce0Int = int(maskForce0,2)
	maskForce0Int = ~maskForce0Int
	addr = addr & maskForce0Int
	## print('addr                                      ',bin(addr)[2:])
	maskForce1 = maskString.replace('X','0')
	## print('maskForce1',maskForce1)
	maskForce1Int = int(maskForce1,2)
	baseAddress = addr | maskForce1Int
	## print('baseAddress                                    ',bin(baseAddress)[2:])
	## print('base address',baseAddress)
	floatBits = maskString.replace('1','0')
	floatBits = floatBits.replace('X','1')
	## print('float bits',floatBits)
	trimmedFloatBits = ''
	found1 = False
	for offset in range(len(floatBits)):
		if floatBits[offset] == '1':
			found1 = True
		if found1:
			trimmedFloatBits += floatBits[offset]
	## print('trimmedFloatBits',trimmedFloatBits)
	numOfFloatBits = trimmedFloatBits.count('1')
	## print('numOfFloatBits',numOfFloatBits)
	listOf1s = makeListOf1s(numOfFloatBits)
	listOfOffsets = makeListOfOffsets(listOf1s,trimmedFloatBits)
	# print('listOfOffsets',listOfOffsets)
	addressList = []
	for offset in listOfOffsets:
		addr = baseAddress + offset
		addressList.append(addr)
	# print('addressList',addressList)
	return addressList

for programLine in inProgram:
	# # print('progLine',programLine)
	if programLine[0] == 'mask':
		## print('set mask')
		maskString = programLine[1]
	if programLine[0] == 'mem':
		addrList = genAddrList(programLine[1])
		for addr in addrList:
			if addr not in usedMemoryLocations:
				usedMemoryLocations.append(addr)
				memLine = []
				memLine.append(addr)
				memLine.append(0)
				memoryLocationValuesList.append(memLine)
			setMemoryValue(addr,programLine[2])

sum = 0
for memVal in memoryLocationValuesList:
	## print(memVal)
	sum += memVal[1]

print('sum',sum)

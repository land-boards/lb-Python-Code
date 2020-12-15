""" 

A0C 2020 Day 14 Part 1

"""

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
			#print('mask')
			pass
		elif row[0:2] == 'me':
			newRow = row.replace('[',',')
			newRow = newRow.replace('[',',')
			newRow = newRow.replace(']',',')
			newRow = newRow.replace(' = ',',')
			newLine = newRow.split(',')
			#print('split line',newLine)
			progLine = []
			progLine.append(newLine[0])
			progLine.append(int(newLine[1]))
			progLine.append(int(newLine[3]))
			newProgList.append(progLine)
			#print('mem',newRow)
			pass
		else:
			print(row)
			assert False,'parse err'
	return newProgList
	
def makeMemoryLocList(inProgram):
	"""
	programLine[0] = instruction
	programLine[1] = address
	programLine[2] = value
	add to list of addressed
	"""
	global usedMemoryLocations
	for programLine in inProgram:
		if programLine[0] == 'mem':
			if int(programLine[1]) not in usedMemoryLocations:
				usedMemoryLocations.append(int(programLine[1]))
	
def initMemoryContents():
	"""
	Fill memory with 0's
	"""
	global usedMemoryLocations
	global memoryLocationValuesList
	for memoryAddress in usedMemoryLocations:
		#print('memoryAddress',memoryAddress)
		memoryLine = []
		memoryLine.append(int(memoryAddress))
		memoryLine.append(0)
		memoryLocationValuesList.append(memoryLine)

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
		print('address',address)
		print('value',value)
		assert False,'setMemoryValue error'
	return 0
	
def setMaskVals(maskString):
	global orBitMask
	global andBitMask
	global preserveBitMask
	print('maskString',maskString)
	newVal = 0
	preserveBitMask = 0
	andBitMask = 0
	orBitMask = 0
	for pos in maskString:
		if pos == 'X':
			preserveBitMask |= 1
		elif pos == '0':
			andBitMask |= 1
		elif pos == '1':
			orBitMask |= 1
		else:
			print('mask err')
			assert False,'mask err'
		preserveBitMask <<= 1
		andBitMask <<= 1
		orBitMask <<= 1
	preserveBitMask >>= 1
	andBitMask >>= 1
	orBitMask >>= 1
	print('preserveBitMask',preserveBitMask)
	print('andBitMask',andBitMask)
	print('orBitMask',orBitMask)
	return

def applyMask(dataVal):
	"""
	int('11111111', 2) >>>> 255
	bin(10) >>> '0b1010'
	"""
	global orBitMask
	global andBitMask
	global preserveBitMask
	print('\ndataVal',dataVal)
	valStr = bin(dataVal)[2:]
	print('valStr',valStr)
	
	print('orBitMask',bin(orBitMask)[2:])
	print('andBitMask',bin(andBitMask)[2:])
	print('preserveBitMask',bin(preserveBitMask)[2:])
	newValue = dataVal
	newValue &= preserveBitMask
	newValue |= orBitMask
	print('newValue',newValue)
	# assert False,'stop'
	return newValue

inList = readFileToListOfStrings('input.txt')
inProgram = parseProgramToList(inList)
usedMemoryLocations = []
makeMemoryLocList(inProgram)
memoryLocationValuesList = []
initMemoryContents()

orBitMask = 0
andBitMask = 0
preserveBitMask = 0

for programLine in inProgram:
	print('progLine',programLine)
	if programLine[0] == 'mask':
		print('set mask')
		setMaskVals(programLine[1])
	if programLine[0] == 'mem':
		# ['mem', '8', '11']
		print('alter mem',programLine)
		newVal = applyMask(programLine[2])
		setMemoryValue(programLine[1],newVal)

sum = 0
for memVal in memoryLocationValuesList:
	print(memVal)
	sum += memVal[1]

print('sum',sum)


		
""" 


"""

#DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileOfEquationsToList(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inLine = inLine.replace ('(',' ( ')
			inLine = inLine.replace (')',' ) ')
			newInLine = inLine.split(' ')
			newerLine = []
			for item in newInLine:
				debugPrint('item'+str(item))
				if item == '':
					pass
				elif item == '(':
					newerLine.append('(')
				elif item == ')':
					newerLine.append(')')
				elif item == '+':
					newerLine.append('+')
				elif item == '*':
					newerLine.append('*')
				else:
					newerLine.append(int(item))
			inList.append(list(newerLine))
	return inList

def dumpEqn(eqn,callingFcnName=''):
	if DEBUG_PRINT:
		if callingFcnName == '':
			print('(dumpEqn): ',end='')
		else:
			print(callingFcnName,': ',end='')
		for element in eqn:
			print(element,end='')
		print()

def countDepth(theRow):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	depth = 0
	maxDepth = 0
	dumpEqn(theRow,'(countDepth) passed')
	for cell in theRow:
		# debugPrint('cell : ' + str(cell))
		if cell == '(':
			depth += 1
			if depth > maxDepth:
				maxDepth = depth
		if cell == ')':
			depth -= 1
	DEBUG_PRINT = False
	debugPrint('(countDepth): maxDepth = ' + str(maxDepth))
	return maxDepth

def solveSingleLevelLeftToRight(singleLevelEqn):
	global DEBUG_PRINT
	DEBUG_PRINT = True
	debugPrint('(solveSingleLevelLeftToRight): input = ' + str(singleLevelEqn))
	result = 0
	operator = 'start'
	for item in singleLevelEqn:
		if item == '+':
			operator = 'plus'
			debugPrint('(solveSingleLevelLeftToRight): plus')
		elif item == '*':
			operator = 'multiply'
			debugPrint('(solveSingleLevelLeftToRight): multiply')
		elif operator == 'start':
			result = item
			operator = 'waitForOp'
			debugPrint('(solveSingleLevelLeftToRight): initial val ' + str(item))
		else:
			if operator == 'multiply':
				debugPrint('(solveSingleLevelLeftToRight): multiply, ' + str(result) + " " + str(item))
				result = result * item
				operator = '(solveSingleLevelLeftToRight): waitForOp'
			elif operator == 'plus':
				debugPrint('(solveSingleLevelLeftToRight): adding, ' + str(result) + ' ' + str(item))
				result = result + item
				operator = '(solveSingleLevelLeftToRight): waitForOp'
		debugPrint('(solveSingleLevelLeftToRight): accumuator result ' + str(result))
	debugPrint('(solveSingleLevelLeftToRight): returning result ' + str(result))
	DEBUG_PRINT = False
	return result

def solveSingleLevelPt2Pri(singleLevelEqn):
	global DEBUG_PRINT
	DEBUG_PRINT = True
	debugPrint('(solveSingleLevelPt2Pri): input = ' + str(singleLevelEqn))
	result = 0
	solvedForAdds = []
	operator = 'start'
	offset = 0
	while offset < len(singleLevelEqn)-1:
		print('offset',offset)
		if singleLevelEqn[offset+1] == '+':
			firstNum = singleLevelEqn.pop(offset)
			op = singleLevelEqn.pop(offset)
			secondNum = singleLevelEqn.pop(offset)
			singleLevelEqn.insert(offset,firstNum+secondNum)
			print('inserted',firstNum+secondNum)
		else:
			offset += 1
		print('singleLevelEqn',singleLevelEqn)
	if len(singleLevelEqn) == 1:
		return singleLevelEqn[0]
	product = 1
	offset = 0
	while offset < len(singleLevelEqn)-2:
		print('singleLevelEqn (2)',singleLevelEqn)
		product *= singleLevelEqn[offset]
		offset += 2
	if offset < len(singleLevelEqn):
		product *= singleLevelEqn[-1]
	print('product',product)
	# assert False,'stopped'
	return product

def evalAtDepth(theRow,searchDepth):
	""" evalAtDepth(theRow,searchDepth)
	"""
	global DEBUG_PRINT
	DEBUG_PRINT = False
	inInner = False
	solvedInner = False
	currentsearchDepth = 0
	leftParenAtsearchDepthOffset = 0
	rightParenAtsearchDepthOffset = 0
	newEqn = []
	dumpEqn(theRow,'\n(evalAtDepth) input')
	debugPrint('(evalAtDepth) ' + str(theRow))
	debugPrint('(evalAtDepth): searchDepth : ' + str(searchDepth))
	listOff = 0
	if DEBUG_PRINT:
		print('(evalAtDepth): digit at a time : ',end='')
	for item in theRow:
		if DEBUG_PRINT:
			print(item,end='')
		if (item == '('):
			debugPrint('(evalAtDepth): found left paren at searchDepth '+str(currentsearchDepth)+' at offset '+str(listOff))
			currentsearchDepth += 1
			if (currentsearchDepth == searchDepth):
				leftParenAtsearchDepthOffset = listOff
				debugPrint('(evalAtDepth): leftParenAtsearchDepthOffset ' + str(leftParenAtsearchDepthOffset))
				inInner = True
		elif (item == ')'):
			debugPrint('(evalAtDepth): found right paren at searchDepth '+str(currentsearchDepth)+' at offset '+str(listOff))
			if (currentsearchDepth == searchDepth):
				rightParenAtsearchDepthOffset = listOff
				debugPrint('\n(evalAtDepth): rightParenAtsearchDepthOffset ' + str(rightParenAtsearchDepthOffset))
				inInner = False
				solvedInner = True
			currentsearchDepth -= 1
		if solvedInner:
			break
		listOff += 1
	if DEBUG_PRINT:
		print()
	if (leftParenAtsearchDepthOffset == 0) and (rightParenAtsearchDepthOffset == 0):
		print()
		assert False,'(evalAtDepth) : Never found the right level'
	debugPrint('(evalAtDepth): inside ' + str(theRow[leftParenAtsearchDepthOffset+1:rightParenAtsearchDepthOffset]))
	innerVal = solveRow(theRow[leftParenAtsearchDepthOffset+1:rightParenAtsearchDepthOffset])
	# print('left of ',theRow[0:leftParenAtsearchDepthOffset])
	# print('val ',innerVal)
	# print('right of ',theRow[rightParenAtsearchDepthOffset+1:])
	for off in range(0,leftParenAtsearchDepthOffset):
		newEqn.append(theRow[off])
	newEqn.append(innerVal)
	for off in range(rightParenAtsearchDepthOffset+1,len(theRow)):
		newEqn.append(theRow[off])
	dumpEqn(newEqn,'(evalAtDepth): newEqn ')
	DEBUG_PRINT = False
	return newEqn

def solveRow(theRow):
	global DEBUG_PRINT
	DEBUG_PRINT = False
	newRow = []
	newRow = theRow
	dumpEqn(newRow,'(solveRow) newRow input')
	depth = countDepth(newRow)
	debugPrint('(solveRow): depth ' + str(depth))
	while depth > 0:
		debugPrint('(solveRow): In inner loop, depth ' + str(depth))
		newRow = evalAtDepth(newRow,depth)
		dumpEqn(newRow,'(solveRow) returned from evalAtDepth')
		depth = countDepth(newRow)
		debugPrint('(solveRow): depth (2) ' + str(depth))
		# input('\nHit enter')
	result = solveSingleLevelPt2Pri(newRow)
	debugPrint('(solveRow): result' + str(result))
	return result

#program
inList = readFileOfEquationsToList('input.txt')

total = 0
for row in inList:
	# for element in row:
		# print(element,end = '')
	# print('')
	rowVal = solveRow(row)
	print('(main): returned =',rowVal)
	total += rowVal

print('(main): total',total)

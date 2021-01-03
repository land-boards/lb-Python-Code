""" 
2020 D19 P1
"""

# DEBUG_PRINT = True
DEBUG_PRINT = False

def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileOfStringsToListOfLists(inFileName):
	global DEBUG_PRINT		# need to put in each function
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	debugPrint('(readFileOfStringsToListOfLists): inList - ' + str(inList))
	return inList

def formatInputList(inList):
	global DEBUG_PRINT		# need to put in each function
	top = []
	strBody = []
	# Input = '2: 12 16 | 41 26'
	# Output = [2, [12, 16], [41, 26]]
	for line in inList:
		if ':' in line:
			sp = line.split(' ')
			topLine = []
			topLine.append(int(line[0:line.find(':')]))
			newLine = line[line.find(':')+2:]
			newLine = newLine.replace('"','')
			newLineList = newLine.split(' ')
			newRow = []
			for item in newLineList:
				if item == '|':
					topLine.append(newRow)
					newRow = []
				elif 'a' <= item[0] <= 'z':
					newRow.append(item)
				elif '0' <= item[0] <= '9':
					newRow.append(int(item))
				else:
					print('wtf')
			topLine.append(newRow)
			top.append(topLine)
		elif line != '':
			strBody.append(line)
	top.sort(key=lambda r:r[0])

	rulesList = []
	for rule in top:
		if len(rule) == 2:
			rulesList.append(rule[1])
		else:
			newRule = []
			newRule.append(rule[1])
			newRule.append(rule[2])
			rulesList.append(newRule)
	debugPrint('(formatInputList): rulesList ' + str(top))
	debugPrint('(formatInputList): top ' + str(top))
	return rulesList,strBody

# Program start
inList = readFileOfStringsToListOfLists('input1.txt')
# print(inList)
rulesList,testValues = formatInputList(inList)
DEBUG_PRINT = True
debugPrint('(main): rulesList  : ' + str(rulesList))
debugPrint('(main): testValues : ' + str(testValues))

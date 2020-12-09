#1762 is too low

import itertools

DEBUG_PRINT = True
DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings()
debugPrint(inList)
newList = []
newLine = []
for row in inList:
	if row == '':
		newList.append(newLine)
		newLine = []
	else:
		newLine.append(row)
if newLine != []:
	newList.append(newLine)
debugPrint(newList)
# [['abc'], ['a', 'b', 'c'], ['ab', 'ac'], ['a', 'a', 'a', 'a'], ['b']]

charCount = 0

for group in newList:
	debugPrint('group')
	debugPrint(group)
	charsUsedStr = ''
	for person in group:
		for c in person:
			if (c > 'z') or (c < 'a'):
				assert False,'bad char'
			if c not in charsUsedStr:
				charsUsedStr += c
	debugPrint('chars used = '+charsUsedStr)
	for c in charsUsedStr:
		charWasUsedFlag = True
		for person in group:
			debugPrint('checking person '+person+' for '+c)
			if c not in person:
				debugPrint(c+' was not in ' + person)
				charWasUsedFlag = False
			else:
				debugPrint(c + ' was in ' + person)
				pass
		if charWasUsedFlag:
			debugPrint('char was used by all ' + c)
			charCount += 1
			debugPrint('charCount '+str(charCount))
		else:
			debugPrint('char was not used by all' + c)
print('charCount',charCount)

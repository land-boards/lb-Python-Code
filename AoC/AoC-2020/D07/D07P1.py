DEBUG_PRINT = True
#DEBUG_PRINT = False

import itertools

DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings():
	inList = []
	with open('input2.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

whereUsedList = []

def findWhereUsedAtCurrentLevel(linksList):
	foundNewOne = False
	for nha in whereUsedList:
		for link in linksList:
			if link[1] == nha:
				if link[0] not in whereUsedList:
					whereUsedList.append(link[0])
					foundNewOne = True
	return foundNewOne

def findAllLevelsWhereUsed(searchStr,linksList):
	debugPrint('linksList ' + str(linksList))
	whereUsedList.append(searchStr)
	debugPrint('whereUsedList ' + str(whereUsedList))
	moreToDo = True
	while moreToDo:
		moreToDo = findWhereUsedAtCurrentLevel(linksList)
		debugPrint('whereUsedList ' + str(whereUsedList))

inList = readFileToListOfStrings()
debugPrint(inList)
newList = []
for row in inList:
	newLine = row.replace('bags','bag')
	newLine = newLine.replace(' bag','')
	newLine = newLine.replace(' contain','')
	newLine = newLine.replace(',','')
	newLine = newLine.replace('.','')
	spLine = newLine.split(' ')
	newList.append(spLine)
for row in newList:
	debugPrint(row)
combList = []
for row in newList:
	state = 'lookingForAdjective'
	combRow = []
	for word in row:
		if state == 'lookingForAdjective':
			adj = word
			state = 'lookingForColor'
		elif state == 'lookingForColor':
			col = word
			state = 'lookingForNumber'
			combRow.append(adj+' '+col)
		elif state == 'lookingForNumber':
			num = word
			if num == 'no':
				state = 'done'
			else:
				combRow.append(int(num))
				state = 'lookingForAdjective'
		debugPrint('combRow ' + str(combRow))
	combList.append(combRow)
	
for row in combList:
	debugPrint(row)

linksList = []
for row in combList:
	state = 'lookingForFirstColor'
	firstColor = ''
	for element in row:
		if state == 'lookingForFirstColor':
			firstColor = element
			state = 'lookingForNumber'
		elif state == 'lookingForNumber':
			state = 'lookingForOtherColors'
			number = element
		elif state == 'lookingForOtherColors':
			state = 'lookingForNumber'
			currentColor = element
			line = '"'
			line += firstColor
			line += '" -> "'
			line += currentColor
			line += '"'
			print(line)
			linksRow = []
			linksRow.append(firstColor)
			linksRow.append(currentColor)
			linksRow.append(number)
			linksList.append(linksRow)
for row in linksList:
	debugPrint(row)

findAllLevelsWhereUsed('shiny gold',linksList)

for row in whereUsedList:
	debugPrint(row)
print('\newLinenumber of places pt 1',len(whereUsedList)-1)

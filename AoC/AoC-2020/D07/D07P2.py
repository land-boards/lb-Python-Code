DEBUG_PRINT = True
#DEBUG_PRINT = False
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

def printGraphText(linksList):
	debugPrint('\ndigraph G {')
	for pair in linksList:
		line = '"'
		line += pair[0]
		line += '" -> "'
		line += pair[1]
		line += '"'
		debugPrint(line)
	debugPrint('}\n')

def printGraphTextBack(linksList):
	debugPrint('\ndigraph G {')
	for pair in linksList:
		line = '"'
		line += pair[1]
		line += '" -> "'
		line += pair[0]
		line += '"'
		debugPrint(line)
	debugPrint('}\n')

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
			linksRow = []
			linksRow.append(firstColor)
			linksRow.append(currentColor)
			linksRow.append(number)
			linksList.append(linksRow)
debugPrint('linksList')
for row in linksList:
	print(row)

printGraphText(linksList)

# pointsList - list of the points (a queue)
pointsList = []
def addToPointsList(pointToAdd):
	debugPrint('added to points list'+pointToAdd)
	pointsList.append(pointToAdd)

def getFromPointsList():
	val = pointsList.pop()
	debugPrint('returning from points list' + val)
	return val
		
def isPointsListEmpty():
	return len(pointsList) == 0

# pairsList - list of the pairs
pairsList = []

def addToPairsList(pairToAdd):
	if pairToAdd not in pairsList:
		pairsList.append(pairToAdd)
	
addToPointsList('shiny gold')
while not isPointsListEmpty():
	currentPoint = getFromPointsList()
	debugPrint('got out '+ currentPoint)
	for pairOfPoints in linksList:
		#debugPrint('comparing against ' + pairOfPoints[0])
		if pairOfPoints[0] == currentPoint:
			debugPrint('found')
			addToPairsList(pairOfPoints)
			addToPointsList(pairOfPoints[1])

debugPrint(pairsList)
printGraphTextBack(pairsList)
		

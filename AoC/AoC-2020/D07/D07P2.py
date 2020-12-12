DEBUG_PRINT = True
DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

def readFileToListOfStrings(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def transformInList(inList):
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
	return combList

def printGraphText(linksList):
	"""
	LR_0 -> LR_2 [ label = "SS(B)" ];
	http://webgraphviz.com
	"""
	print('\ndigraph G {')
	for pair in linksList:
		line = '"' + pair[0] + '" -> "' + pair[1] + '" [ label = "' + str(pair[2]) + '" ];'
		print(line)
	print('}\n')

def printGraphTextBack(linksList):
	print('\ndigraph G {')
	for pair in linksList:
		line = '"'
		line += pair[1]
		line += '" -> "'
		line += pair[0]
		line += '" [ label = "'
		line += str(pair[2])
		line += '" ]'
		print(line)
	print('}\n')

def makeLinksList(inList):
	global DEBUG_PRINT
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
		debugPrint(row)
	return linksList

def getFromPointsList():
	global DEBUG_PRINT
	val = pointsList.pop()
	debugPrint('returning from points list' + val)
	return val
		
def isPointsListEmpty():
	return len(pointsList) == 0

def addToPairsList(pairToAdd):
	global DEBUG_PRINT
	global pairsList
	if pairToAdd not in pairsList:
		pairsList.append(pairToAdd)

def findListOfEndpoints(pairsList,nodeNamesInGraph):
	global DEBUG_PRINT
	endPoints = []
	for nodeName in nodeNamesInGraph:
		isDest = False
		for pair in pairsList:
			if pair[0] == nodeName:
				isDest = True
		if not isDest:
			endPoints.append(nodeName)
#	print('endPoints',endPoints)
	return endPoints

def findListOfStartpoints(pairsList,nodeNamesInGraph):
	global DEBUG_PRINT
	endPoints = []
	for nodeName in nodeNamesInGraph:
		isDest = False
		for pair in pairsList:
			if pair[1] == nodeName:
				isDest = True
		if not isDest:
			endPoints.append(nodeName)
#	print('endPoints',endPoints)
	return endPoints

def findAllNodeNamesInGraph(pairsList):
	global DEBUG_PRINT
	allNodeNames = []
	for pair in pairsList:
		if pair[0] not in allNodeNames:
			allNodeNames.append(pair[0])
		if pair[1] not in allNodeNames:
			allNodeNames.append(pair[1])
#	print('allNodeNames',allNodeNames)
	return allNodeNames

pointValuesList = []

def makePointValuesList():
	""" makePointValuesList(nodeNamesInGraph)
	"""
	global nodeNamesInGraph
	global pointValuesList
	for node in nodeNamesInGraph:
		pointValuesLine = []
		pointValuesLine.append(node)
		pointValuesLine.append(-1)
		pointValuesLine.append(-1)
		pointValuesList.append(pointValuesLine)
	return

def prefillEndPointValuesList():
	global pointValuesList
	global endPointsList
	# endPointsList ['faded blue', 'dotted black']
	# pointValuesList [['shiny gold', -1, -1], ['dark olive', -1, -1], ['vibrant plum', -1, -1], ['faded blue', -1, -1], ['dotted black', -1, -1]]
	# print('prefillEndPointValuesList: endPointsList',endPointsList)
	# print('prefillEndPointValuesList: pointValuesList', pointValuesList)
	for point in endPointsList:
		for pvl in pointValuesList:
			if point == pvl[0]:
				pvl[1] = 0
				pvl[2] = 1
	print('pointValuesList',pointValuesList)
	return
	
def runList():
	"""
	 pointValuesList [['shiny gold', -1, -1], ['dark olive', -1, -1], ['vibrant plum', -1, -1], ['faded blue', 0, 1], ['dotted black', 0, 1]]
	 pairsList [['shiny gold', 'dark olive', 1], ['shiny gold', 'vibrant plum', 2], ['vibrant plum', 'faded blue', 5], ['vibrant plum', 'dotted black', 6], ['dark olive', 'faded blue', 3], ['dark olive', 'dotted black', 4]]
	"""
	global pointsList
	global pairsList
	print('\nrunList: pointValuesList',pointValuesList)
	print('\nrunList: pairsList',pairsList)
	print('')
	for point in pointValuesList:
		if point[2] == -1:		# unsolved net
			#source shiny gold
			print('source',point[0])
			destsList = []
			for pairVal in pairsList:
				if pairVal[0] == point[0]:
					destsList.append(pairVal)
			#All destination pairs/values destPairVals [['shiny gold', 'dark olive', 1], ['shiny gold', 'vibrant plum', 2]]
			print('All destination pairs/values destPairVals',destsList)
			print('')
			allSolved = True
			sumVal = 0
			solvedList = []
			for destPairVal in destsList:
				for point2 in pointValuesList:
					if destPairVal[1] == point2[0]:
						if point2[2] == -1:
							allSolved = False
			print('solver',point[0])
			if allSolved:
				print('all predecessors were solved',point[0])
				for point3 in pointValuesList:
					if point3[0] == point[0]:
						point[1] = sum
						point[2] = sum+1
			else:
				print('not solved below',point[0])
			print('dests',destsList)
		else:
			print('already solved',point[0])
	assert False,''
	print('pointValuesList',pointValuesList)
	return

def solver():
#	global endPointsList
	global nodeNamesInGraph
	global pairsList
	makePointValuesList()
	# Add value to end points
	prefillEndPointValuesList()
	while pointValuesList[0][2] == -1:
		runList()
	return 0
	
# The program
inList = readFileToListOfStrings('input2.txt')
debugPrint(inList)
combList = transformInList(inList)
for row in combList:
	debugPrint(row)
linksList = makeLinksList(combList)

debugPrint('All connections')
printGraphTextBack(linksList)

# stack of points (pointsList)
pointsList = []

# pairsList - list of the pairs
pairsList = []
# add root
pointsList.append('shiny gold')

# Find all psirs used
while not isPointsListEmpty():
	currentPoint = getFromPointsList()
	debugPrint('got out '+ currentPoint)
	for pairOfPoints in linksList:
		#debugPrint('comparing against ' + pairOfPoints[0])
		if pairOfPoints[0] == currentPoint:
			debugPrint('found')
			#addToPairsList(pairOfPoints)
			if pairOfPoints not in pairsList:
				pairsList.append(pairOfPoints)
			pointsList.append(pairOfPoints[1])
			
DEBUG_PRINT = True

debugPrint('list of vertex pairs with weights used from root (pairsList)')
debugPrint(pairsList)
printGraphTextBack(pairsList)

nodeNamesInGraph = findAllNodeNamesInGraph(pairsList)
debugPrint('All of the node names used (nodeNamesInGraph)')
debugPrint(nodeNamesInGraph)

endPointsList = findListOfEndpoints(pairsList,nodeNamesInGraph)
debugPrint('End points of the graph (endPointsList)')
debugPrint(endPointsList)

total = solver()

#print('total',total)

'''
D16P1.py


'''
import time

# At start
startTime = time.time()

def parseInList(inList):
	parsedDict = {}
	nodesList = []
	for line in inList:
		splitLine = line.split(' ')
		# print('parseInList',splitLine)
		fromNode = splitLine[1]
		rate = splitLine[4]
		rate = int(rate[5:-1])
		cNodes = splitLine[9:]
		connectedNodes= []
		for node in cNodes:
			connectedNodes.append(node.replace(',',''))
		# print('fromNode',fromNode,end = ' ')
		# print('rate',rate, end = ' ')
		# print('connectedNodes', connectedNodes)
		parsedDict[fromNode] = connectedNodes
		nodesList.append([fromNode,rate,'closed']) 
	return nodesList, parsedDict

def readInFile(fileName):
	inList=[]
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)
	return inList

def printDiGraph(parsedDict):
	connList = []
	for node in parsedDict:
		# print('node',node,'dict',parsedDict[node])
		destNodes = parsedDict[node]
		for destNodes in destNodes:
			connList.append([node,destNodes])
	# print('connList',connList)
	# digraph G {
	  # "Welcome" -> "To"
	  # "To" -> "Web"
	  # "To" -> "GraphViz!"
	# }
	print('\ndigraph G {')
	for conns in connList:
		print(' "',end='')
		print(conns[0],end='')
		print('" -> "',end='')
		print(conns[1],end='')
		print('"')
	print('}')
	print()

# fileName = 'input2.txt'
# fileName = 'input.txt'
fileName = 'input1.txt'
inList = readInFile(fileName)
# nodesList = list of all nodes with pressure at node
#	[['AA', 0], ['BB', 13], ['CC', 2], ['DD', 20], ['EE', 3], ['FF', 0], ['GG', 0], ['HH', 22], ['II', 0], ['JJ', 21]]
# parsedDict = dict of from and to nodes
#	{'AA': ['DD', 'II', 'BB'], 'BB': ['CC', 'AA'], 'CC': ['DD', 'BB'], 'DD': ['CC', 'AA', 'EE'], 'EE': ['FF', 'DD'], 'FF': ['EE', 'GG'], 'GG': ['FF', 'HH'], 'HH': ['GG'], 'II': ['AA', 'JJ'], 'JJ': ['II']}
nodesList, parsedDict = parseInList(inList)
print('nodesList, len =',len(nodesList),nodesList)
print('parsedDict',parsedDict)
# printDiGraph(parsedDict)

# At end
print('time',time.time()-startTime)

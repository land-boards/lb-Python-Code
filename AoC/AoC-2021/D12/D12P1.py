# D12P1.py
# 2021 Advent of Code
# Day 12
# Part 1

from collections import defaultdict

def readFileToList(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip().split('-')
			inList.append(inLine)
	return inList

def dfs_paths(graph, start, goal):
	wstep, forstep = 0,0
	stack = [(start, [start])]
	while stack:
		wstep+=1
		print("{}:{} before (vertex, path) = stack.pop():{}".format(wstep, forstep, stack))
		(vertex, path) = stack.pop()
		print("{}:{} after (vertex, path) = stack.pop(): {}".format(wstep, forstep, stack))
		forstep=0
		for next in graph[vertex] - set(path):
			forstep+=1
			if next == goal:
				yield path + [next]
			else:
				stack.append((next, path + [next]))

def printDigraph(graphPairs):
	# [['start', 'A'], ['start', 'b'], ['A', 'c'], ['c', 'A'], ['A', 'b'], ['b', 'A'], ['b', 'd'], ['d', 'b'], ['A', 'end'], ['b', 'end']]
	print("\ndigraph G {")
	for row in graphPairs:
		print("  ",row[0],'->',row[1])
	print("}")

def isPointLowerCase(point):
	if 'A' <= point<= 'Z':
		return True
	return False

# Generate adjacency list for undirected graph
# https://towardsdatascience.com/search-algorithm-depth-first-search-with-python-1f10da161980
def generateAdjacencyList(edges):
	adjacencyList = defaultdict(list)
	for u, v in edges:
		adjacencyList[u].append(v)
		adjacencyList[v].append(u)
	return adjacencyList

visitedList = [[]]
visitedLinksCount = {}

def makeListOfPathsList(graph,startPoint):
	print("makeListOfPathsList: graph",graph)
	print("makeListOfPathsList: startPoint",startPoint)
	pathsList = [[]]
	seenPairs = []
	vertexList = [startPoint]
	for vertex in graph:
		print("vertex",vertex)
		ends = []
		for endPoint in graph[vertex]:
			print(vertex,endPoint)
			if [vertex,endPoint] not in seenPairs:
				seenPairs.append([vertex,endPoint])
	print("seenPairs",seenPairs)
	return pathsList 

def findAllPaths(startNode,endNode,adjacencyList):
	print("startNode",startNode)
	print("endNode",endNode)
	print("adjacencyList",adjacencyList)

inList = readFileToList("input3.txt")
print("Original - inList",inList)
allPointsList = []
for pair in inList:
	if pair[0] not in allPointsList:
		allPointsList.append(pair[0])
	if pair[1] not in allPointsList: 
		allPointsList.append(pair[1])
print("allPointsList",allPointsList)
pointsLettersToNumsDict = {}
pointsNumsToLettersDict = {}
nodeNum = 0
for node in allPointsList:
	# print("node",node)
	pointsLettersToNumsDict[node] = nodeNum
	pointsNumsToLettersDict[nodeNum] = node
	nodeNum += 1
print("pointsLettersToNumsDict",pointsLettersToNumsDict)
print("pointsNumsToLettersDict",pointsNumsToLettersDict)
pairsAsInts = []
for path in inList:
	pairsAsInts.append([pointsLettersToNumsDict[path[0]],pointsLettersToNumsDict[path[1]]])
print("pairsAsInts",pairsAsInts)
pointsAsIntsDict = {}
adjacencyList = generateAdjacencyList(pairsAsInts)
# print("adjList",adjacencyList)
# print("\nadjList")
# for node in adjacencyList:
	# print(node,adjacencyList[node])

# remove pathe from Destination
adjacencyList.pop(pointsLettersToNumsDict['end'])
# print("\nadjList")
# for node in adjacencyList:
	# print(node,adjacencyList[node])
# Remove paths out of the end
for node in adjacencyList:
	# print("node",node,"node list =",adjacencyList[node])
	theList = []
	hadStart = False
	for val in adjacencyList[node]:
		# print(" val",val)
		if val == pointsLettersToNumsDict['start']:
			# print("Hit start")
			hadStart = True
		else:
			theList.append(val)
	if hadStart:
		adjacencyList[node] = theList
print("\nadjList")
for node in adjacencyList:
	print(node,adjacencyList[node])
print("adjList",adjacencyList)
findAllPaths(pointsLettersToNumsDict['start'],pointsLettersToNumsDict['end'],adjacencyList)


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

# def depthFirst(graph, currentVertex, visited):
	# print("depthFirst: visited",end=' ')
	# for point in visited:
		# print(valuesDict[point],end = ' ')
	# print()
	# visited.append(currentVertex)
	# for vertex in graph[currentVertex]:
		# print("depthFirst: vertex",valuesDict[vertex])
		# if vertex not in visited:
			# depthFirst(graph, vertex, visited.copy())
	# visitedList.append(visited)

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

inList = readFileToList("input3.txt")
print("Original - inList",inList)
pointsList = []
for pair in inList:
	if pair[0] not in pointsList:
		pointsList.append(pair[0])
	if pair[1] not in pointsList: 
		pointsList.append(pair[1])
# print("pointsList",pointsList)
# quit()
pointsDict = {}
valuesDict = {}
nodeNum = 0
for node in pointsList:
	# print("node",node)
	pointsDict[node] = nodeNum
	valuesDict[nodeNum] = node
	visitedLinksCount[nodeNum] = 0
	nodeNum += 1
# print("pointsDict",pointsDict)
# print("valuesDict",valuesDict)
# print("visitedLinksCount",visitedLinksCount)
pairsAsInts = []
for path in inList:
	pairsAsInts.append([pointsDict[path[0]],pointsDict[path[1]]])
# print("pairsAsInts",pairsAsInts)
pointsAsIntsDict = {}
adjacencyList = generateAdjacencyList(pairsAsInts)
print("adjList",adjacencyList)

# depthFirst(adjacencyList, pointsDict['start'], [])
pathsList = makeListOfPathsList(adjacencyList, pointsDict['start'])
print("pathsList")
for path in pathsList:
	if path != []:
		if path[-1] == pointsDict['end']:
			for point in path:
				print(valuesDict[point],end=' ')
			print()
			

""" 
D12P2

Dijkstra's algorithm
https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html

465 is too high

"""

import sys
import time

# At start
startTime = time.time()

# The progra
startPos = (9999,9999)
endPos = (9999,9999)
row = 0

# Graph function
class Graph(object):
	def __init__(self, nodes, init_graph):
		self.nodes = nodes
		self.graph = init_graph		# unidirectional graph
		
		
	# def construct_graph(self, nodes, init_graph):
		# '''
		# This method makes sure that the graph is symmetrical. 
		# In other words, if there's a path from node A to B with a value V, 
		# it creates a path from node B to node A with a value V.	
		# '''
		# graph = {}
		# for node in nodes:
			# graph[node] = {}
		
		# graph.update(init_graph)
		
		# for node, edges in graph.items():
			# for adjacent_node, value in edges.items():
				# if graph[adjacent_node].get(node, False) == False:
					# graph[adjacent_node][node] = value
					
		#return graph
	
	def get_nodes(self):
		"Returns the nodes of the graph."
		return self.nodes
	
	def get_outgoing_edges(self, node):
		"Returns the neighbors of a node."
		connections = []
		for out_node in self.nodes:
			if self.graph[node].get(out_node, False) != False:
				connections.append(out_node)
		return connections
	
	def value(self, node1, node2):
		"Returns the value of an edge between two nodes."
		return self.graph[node1][node2]

# Dijkstra's algorithm
def dijkstra_algorithm(graph, start_node):
	unvisited_nodes = list(graph.get_nodes())
 
	# We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
	shortest_path = {}
 
	# We'll use this dict to save the shortest known path to a node found so far
	previous_nodes = {}
 
	# We'll use max_value to initialize the "infinity" value of the unvisited nodes   
	max_value = sys.maxsize
	for node in unvisited_nodes:
		shortest_path[node] = max_value
	# However, we initialize the starting node's value with 0   
	shortest_path[start_node] = 0
	
	# The algorithm executes until we visit all nodes
	while unvisited_nodes:
		# The code block below finds the node with the lowest score
		current_min_node = None
		for node in unvisited_nodes: # Iterate over the nodes
			if current_min_node == None:
				current_min_node = node
			elif shortest_path[node] < shortest_path[current_min_node]:
				current_min_node = node
				
		# The code block below retrieves the current node's neighbors and updates their distances
		neighbors = graph.get_outgoing_edges(current_min_node)
		for neighbor in neighbors:
			tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
			if tentative_value < shortest_path[neighbor]:
				shortest_path[neighbor] = tentative_value
				# We also update the best path to the current node
				previous_nodes[neighbor] = current_min_node
 
		# After visiting its neighbors, we mark the node as "visited"
		unvisited_nodes.remove(current_min_node)
	
	return previous_nodes, shortest_path
	
def print_result(previous_nodes, shortest_path, start_node, target_node):
	path = []
	node = target_node
	
	while node != start_node:
		path.append(node)
		node = previous_nodes[node]
 
	# Add the start node manually
	path.append(start_node)
	
	# print('path',path)
	reversePath = []
	for pathOff in range(len(path)-1,-1,-1):
		# print('pathVal',path[pathOff])
		reversePath.append(path[pathOff])
	# print('reversePath',reversePath)
	print('Length',len(path)-1)
	return(len(path)-1)
	
movesAround=((-1,0),(1,0),(0,-1),(0,1))
def possibleMovesFromCurrent(currentPoint):
	global sizeX
	global sizeY
	moves = []
	for movesDir in movesAround:
		checkX = currentPoint[0] + movesDir[0]
		checkY = currentPoint[1] + movesDir[1]
		if 0 <= checkX < sizeX:
			if 0 <= checkY < sizeY:
				moves.append((checkX,checkY))
	return(moves)

fileName = 'input.txt'
# fileName = 'input1.txt'

inList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		col = 0
		inLine = line.strip('\n')
		splitLine = []
		for inChar in inLine:
			if 'a' <= inChar <= 'z':
				currChar = ord(inChar)-ord('a')
			if inChar == 'S':
				startPos = (col,row)
				currChar = ord('a')-ord('a')
			elif inChar == 'E':
				endPos = (col,row)
				currChar = ord('z')-ord('a')
			splitLine.append(currChar)
			col += 1
		inList.append(splitLine)
		# print(splitLine)
		row += 1
print('start',startPos,'endPos',endPos)
# print('inList')
# for row in inList:
	# print(row)
sizeX = len(inList[0])
sizeY = len(inList)
print('sizeX, sizeY',sizeX,sizeY)
startingVal = 0
#possibleMovesFromCurrent = possibleMovesFromCurrent((sizeX-1,sizeY-1))
# print('All moves')
nodes = []
init_graph = {}
for node in nodes:
	init_graph[node] = {}
	
legalMovesList = []
for y in range(sizeY):
	for x in range(sizeX):
		allpossibleMovesFromCurrent = possibleMovesFromCurrent((x,y))
		for toMove in allpossibleMovesFromCurrent:
			fromMove = (x,y)
			fromX = x
			fromY = y
			toX = toMove[0]
			toY = toMove[1]
			# evaluate whether move is possible
			if inList[fromY][fromX] >= inList[toY][toX]-1:
				legalMovesList.append([fromMove,toMove,1])
			# else:
				# legalMovesList.append([fromMove,toMove,99999999])
			# print('from x,y',fromMove,inList[fromY][fromX],'to',toMove,inList[toY][toX],end=' ')
# print('legalMovesList')
# for move in legalMovesList:
	# print(move)
nodes = []
for nodePair in legalMovesList:
	if nodePair[0] not in nodes:
		nodes.append(nodePair[0])
	if nodePair[1] not in nodes:
		nodes.append(nodePair[1])
# print('nodes',nodes)

init_graph = {}
for node in nodes:
	init_graph[node] = {}
	
# print('init_graph (before)')
# for myN in init_graph:
	# print(myN)

for nodePair in legalMovesList:
	init_graph[nodePair[0]][nodePair[1]] = nodePair[2]

# print('init_graph (after)',init_graph)
# for myN in init_graph:
	# print(myN,"  ",init_graph[myN])
	
graph = Graph(nodes, init_graph)
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=startPos)
print('shortest_path',shortest_path[endPos])

# assert False

# rerun with all starting nodes
possibleStartingNodes = []
for y in range(sizeY):
	for x in range(sizeX):
		if inList[y][x] == 0:
			possibleStartingNodes.append((x,y))

# print('possible starting points',possibleStartingNodes)
solnSet = []
min = 9999
minStart = (0,0)
for startPos in possibleStartingNodes:
	print('startPos',startPos,end=' ')
	previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=startPos)
	res = shortest_path[endPos]
	if res < min:
		min = res
		minStart = startPos
	print('time',time.time()-startTime,'res',res,'min',min,'minStart',minStart)
	solnSet.append(res)

print('min',min)

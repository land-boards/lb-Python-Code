visitedList = [[]]

def depthFirst(graph, currentVertex, visited):
    visited.append(currentVertex)
    for vertex in graph[currentVertex]:
        if vertex not in visited:
            depthFirst(graph, vertex, visited.copy())
    visitedList.append(visited)

depthFirst(graph, 0, [])

graph = { 0 : [1, 2],
          1 : [3, 6, 0],
          2 : [4, 5, 0],
          3 : [1],
          4 : [6, 2],
          5 : [6, 2],
          6 : [1, 4, 5]}
		  
print(visitedList)

# It returns all the DFS paths.
# [[], [0, 1, 3], [0, 1, 6, 4, 2, 5], [0, 1, 6, 4, 2], [0, 1, 6, 4], [0, 1, 6, 5, 2, 4], [0, 1, 6, 5, 2], [0, 1, 6, 5], [0, 1, 6], [0, 1], [0, 2, 4, 6, 1, 3], [0, 2, 4, 6, 1], [0, 2, 4, 6, 5], [0, 2, 4, 6], [0, 2, 4], [0, 2, 5, 6, 1, 3], [0, 2, 5, 6, 1], [0, 2, 5, 6, 4], [0, 2, 5, 6], [0, 2, 5], [0, 2], [0]]

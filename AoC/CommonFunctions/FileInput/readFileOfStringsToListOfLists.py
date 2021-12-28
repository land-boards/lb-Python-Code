""" 
readFileOfStringsToListOfLists

Inputs like:
..##.......
#...#...#..
.#....#..#.

Output:
[['.', '.', '#', '#', '.', '.', '.', '.', '.', '.', '.'],
['#', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.'],
['.', '#', '.', '.', '.', '.', '#', '.', '.', '#', '.']]

"""

def readFileOfStringsToListOfLists(fileName):
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip(' ')
			inList.append(list(inLine))
	return inList


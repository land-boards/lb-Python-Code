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

def readFileOfStringsToListOfLists():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip(' ')
			inList.append(list(inLine))
	return inList


# Pt1-AoCDay24.py
# 2019 Advent of Code
# Day 24
# Part 1

"""
	--- Day 24: Planet of Discord ---
	You land on Eris, your last stop before reaching Santa. As soon as you do, your sensors start picking up strange life forms moving around: Eris is infested with bugs! With an over 24-hour roundtrip for messages between you and Earth, you'll have to deal with this problem on your own.

	Eris isn't a very large place; a scan of the entire area fits into a 5x5 grid (your puzzle input). The scan shows bugs (#) and empty spaces (.).

	Each minute, The bugs live and die based on the number of bugs in the four adjacent tiles:

	A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
	An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
	Otherwise, a bug or empty space remains the same. (Tiles on the edges of the grid have fewer than four adjacent tiles; the missing tiles count as empty space.) This process happens in every location simultaneously; that is, within the same minute, the number of adjacent bugs is counted for every tile first, and then the tiles are updated.

	Here are the first few minutes of an example scenario:

	Initial state:
	....#
	#..#.
	#..##
	..#..
	#....

	After 1 minute:
	#..#.
	####.
	###.#
	##.##
	.##..

	After 2 minutes:
	#####
	....#
	....#
	...#.
	#.###

	After 3 minutes:
	#....
	####.
	...##
	#.##.
	.##.#

	After 4 minutes:
	####.
	....#
	##..#
	.....
	##...
	To understand the nature of the bugs, watch for the first time a layout of bugs and empty spaces matches any previous layout. In the example above, the first layout to appear twice is:

	.....
	.....
	.....
	#....
	.#...
	To calculate the biodiversity rating for this layout, consider each tile left-to-right in the top row, then left-to-right in the second row, and so on. Each of these tiles is worth biodiversity points equal to increasing powers of two: 1, 2, 4, 8, 16, 32, and so on. Add up the biodiversity points for tiles with bugs; in this example, the 16th tile (32768 points) and 22nd tile (2097152 points) have bugs, a total biodiversity rating of 2129920.

	What is the biodiversity rating for the first layout that appears twice?
	
	32523825
"""

from __future__ import print_function

def initField():
	rawField = ['.......','...###.','..####.','....#..','..#..#.','.#.###.','.......']
	#rawField  = ['.......','.....#.','.#..#..','.#..##.','...#...','.#.....','.......']
	fieldList = []
	for row in rawField:
		fieldRow = []
		for cell in row:
			fieldRow.append(cell)
		fieldList.append(fieldRow)
	return fieldList

def countAdjacentHashes(row,col,oldField):
	hashesCount = 0
	if oldField[row-1][col] == '#':
		hashesCount += 1
	if oldField[row+1][col] == '#':
		hashesCount += 1
	if oldField[row][col-1] == '#':
		hashesCount += 1
	if oldField[row][col+1] == '#':
		hashesCount += 1
	return hashesCount

def newField(oldField):
	# print("newField: oldField")
	# printField(oldField)
	#print("")
	newFields = []
	newFields.append(oldField[0])
	for row in range(1,len(oldField)-1):
		newRow = []
		newRow.append('.')
		for col in range(1,len(oldField[0])-1):
			countOfHashes = countAdjacentHashes(row,col,oldField)
			if oldField[row][col] == '#':
				if countOfHashes == 1:
					newRow.append('#')
				else:
					newRow.append('.')
			elif oldField[row][col] == '.' and (countOfHashes == 1 or countOfHashes == 2):
				newRow.append('#')
			else:
				newRow.append(oldField[row][col])
		newRow.append('.')
		newFields.append(newRow)
	newFields.append(oldField[0])
	return(newFields)

def evalFieldVals(field):
	cellVal = 1
	total = 0
	for row in field[1:-1]:
		for col in row[1:-1]:
			if col == '#':
				total += cellVal
			cellVal *= 2
	#print("total",total)
	return(total)

def printField(field):
	for row in field[1:-1]:
		for col in row[1:-1]:
			print(col,end='')
		print("")

valsList = []

theField = initField()
stopRun = False

printField(theField)
print("")
val = evalFieldVals(theField)
valsList.append(val)

while not stopRun:
	theNewField = newField(theField)
	val = evalFieldVals(theNewField)
	if val in valsList:
		stopRun = True
		print("Field value",val)
	else:
		valsList.append(val)
	printField(theNewField)
	print("Field value",val)
	print("")
	theField = []
	for row in theNewField:
		newRow = []
		for col in row:
			newRow.append(col)
		theField.append(newRow)
	# print("copy")
	# printField(theField)
	# raw_input()

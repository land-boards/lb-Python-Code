""" 

AoC 2020 D24P1

181 too low

Cube coordinates f+-edblobgames.com/grids/hexagons/

"""

import math

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def parseInList():
	# print(inList)
	global inList
	newList = []
	for row in inList:
		#print(row)
		off = 0
		newRow = []
		while off < len(row):
			if row[off] == 'n' or row[off] == 's':
				newRow.append(row[off:off+2])
				off += 2
			elif row[off] == 'e' or row[off] == 'w':
				newRow.append(row[off])
				off += 1
		# print(newRow)
#		input('hit ret')
		newList.append(newRow)
	return newList

def initList(dirsLists):
	posList = []
	for row in dirsLists:
		# print('row',row)
		pos = [0,0,0]	# [e=1/w=-1,ne=1/sw=-1,nw=1/se=-1]
		for elem in row:
			if elem == 'e':
				pos[0] += 1
				pos[1] += -1
			elif elem == 'w':
				pos[0] += -1
				pos[1] += 1
			elif elem == 'ne':
				pos[0] += 1
				pos[2] += -1
			elif elem == 'sw':
				pos[0] += -1
				pos[2] += 1
			elif elem == 'nw':
				pos[1] += 1
				pos[2] += -1
			elif elem == 'se':
				pos[1] += -1
				pos[2] += 1
		# print('pos',pos)
		foundAtPos = False
		for item in posList:
			if item[0] == pos:
				oldColor = item[1]
				if oldColor == 'white':
					color = 'black'
				else:
					color = 'white'
				item[1] = color
				foundAtPos = True
				# print('was already in the list',pos,'updating color to',color)
		if not foundAtPos:
			newLineVal = []
			newLineVal.append(pos)
			newLineVal.append('black')
			posList.append(newLineVal)
			# print('new at',pos,'with color black')
	# print('posList',posList)
	return posList

def conwayIt(inList):
	outList = inList
	return outList

# program follows
# inList = readFileToListOfStrings('input.txt')
inList = readFileToListOfStrings('input1.txt')
# inList = ['esenee','esew','nwwswee']
# inList = ['nwwswee']
dirsLists = parseInList()
posList = initList(dirsLists)
for loopCount in range (1,10):
	print('loop count',loopCount)
	posList = conwayIt(posList)
	blackCount = 0
	for row in posList:
		if row[1] == 'black':
			blackCount += 1
	print('black',blackCount)

""" 

AoC 2020 D24P1

181 too low

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
		print(newRow)
#		input('hit ret')
		newList.append(newRow)
	return newList

def addOffsetToPoint(point,offset):
	newPoint = []
	newPoint.append(point[0]+offset[0])
	newPoint.append(point[1]+offset[1])
	newPoint.append(point[2]+offset[2])
	return newPoint

def transformPoint(point):
	print('\nreduce point',point)
	if point[0] == 0 or point[1] == 0 or point[2] == 0:
		print('returning untransformed point',point)
		return point
	elif point[1] > 0 and point[2] < 0:
		print('move east',point)
		while point[1] > 0 and point[2] < 0:
			point = addOffsetToPoint(point,[1,-1,1])
		print('new point',point)
		return point
	elif point[1] < 0 and point[2] > 0:
		print('move west',point)
		while point[1] < 0 and point[2] > 0:
			point = addOffsetToPoint(point,[-1,1,-1])
		print('new point',point)
		return point
	elif point[0] != 0 and point[1] < 0 and point[2] < 0:
		print('move east-ish',point)
		while point[1] > 0 and point[2] > 0:
			point = addOffsetToPoint(point,[1,-1,1])
		print('new point',point)
		return point
	elif point[0] != 0 and point[1] < 0 and point[2] < 0:
		print('move west-ish',point)
		while point[1] < 0 and point[2] < 0:
			point = addOffsetToPoint(point,[-1,1,-1])
		print('new point',point)
		return point
	else:
		print('untransformed point',point)
		return point
#		assert False,'transformPoint'
	
# inList = readFileToListOfStrings('input.txt')
# inList = readFileToListOfStrings('input1.txt')
# inList = ['esenee','esew','nwwswee']
inList = ['nwwswee']
dirsLists = parseInList()
posList = []
for row in dirsLists:
	pos = [0,0,0]	# [e=1/w=-1,ne=1/sw=-1,nw=1/se=-1]
	for elem in row:
		if elem == 'e':
			pos[0] += 1
		elif elem == 'w':
			pos[0] += -1
		elif elem == 'ne':
			pos[1] += 1
		elif elem == 'sw':
			pos[1] += -1
		elif elem == 'nw':
			pos[2] += 1
		elif elem == 'se':
			pos[2] += -1
		else:
			assert False,'parse error'
		# print('pos',pos)
	if pos not in posList:
		posList.append(pos)
	else:
		print('was already in the list',pos)
print('posList [e=1/w=-1,ne=1/sw=-1,nw=1/se=-1]\n',posList)

pointsList = []
for row in posList:
	newPoint = transformPoint(row)
	if newPoint not in pointsList:
		pointsList.append(newPoint)
	else:
		print('already in list')
white = 0
black = 0
for row in pointsList:
	val = row[0] + row[1] + row[2]
	if math.remainder(val,2) == 0:
		white += 1
	else:
		black += 1# print('\nTotals\nblack',black)
print('white',white)
	
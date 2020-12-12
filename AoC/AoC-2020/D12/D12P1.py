""" 

readFileToListOfStrings

"""

def readFileToListOfStrings():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings()
print(inList)
directionsList = []
for row in inList:
	listRow = []
	listRow.append(row[0])
	listRow.append(int(row[1:]))
	directionsList.append(listRow)

print('directionsList',directionsList)
pX = 0
pY = 0
dir = 90

for direction in directionsList:
	print(direction)
	if direction[0] == 'N':
		pY += direction[1]
	elif direction[0] == 'S':
		pY -= direction[1]
	elif direction[0] == 'E':
		pX += direction[1]
	elif direction[0] == 'W':
		pX -= direction[1]
	elif direction[0] == 'L':
		dir = dir - direction[1]
		dir = dir % 360
	elif direction[0] == 'R':
		dir = dir + direction[1]
		dir = dir % 360
	elif direction[0] == 'F':
		if dir == 0:
			pY += direction[1]
		elif dir == 90:
			pX += direction[1]
		elif dir == 180:
			pY -= direction[1]
		elif dir == 270:
			pX -= direction[1]
	else:
		assert False,'parse error'
	print('dir =',dir,end = ' ,')
	print('x =',pX,', y =',pY)

print(pX,pY)
print(abs(pX)+abs(pY))

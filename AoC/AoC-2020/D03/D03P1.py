# 2020D3P1
# 81 is not right

def readFileOfStringsToListOfLists():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(list(inLine))
	return inList

def checkForTree(xpos,ypos,inList):
	print('check at',xpos,ypos,end=' ')
	if inList[ypos][xpos] == '#':
		print('found tree')
		return True
	print('no tree')
	return False

inList = readFileOfStringsToListOfLists()
for row in inList:
	print(row)
rows = len(inList)
columns = len(inList[0])
print('rows',rows)
print('columns',columns)
numberOfTrees = 0
xPos = 0
yPos = 0
deltaX = 3
deltaY = 1
while yPos < rows-1:
	xPos += deltaX
	yPos += deltaY
	if xPos > columns-1:
		xPos = xPos % (columns)
		print('modulo')
	if checkForTree(xPos,yPos,inList):
		numberOfTrees += 1
print('trees',numberOfTrees)

	
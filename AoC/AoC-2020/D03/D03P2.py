# 2020 D03P2
# 529 is too low
# 3638606400 is right

def readFileOfStringsToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(list(inLine))
	return inList

def checkForTree(xpos,ypos,inList):
	#print('check at',xpos,ypos,end=' ')
	if inList[ypos][xpos] == '#':
		#print('found tree')
		return True
	#print('no tree')
	return False

def countTreesOnWayDown(deltaX,deltaY,inList):
	xPos = 0
	yPos = 0
	numberOfTrees = 0
	while yPos < rows-1:
		xPos += deltaX
		yPos += deltaY
		if xPos > columns-1:
			xPos = xPos % (columns)
			#print('modulo')
		if checkForTree(xPos,yPos,inList):
			numberOfTrees += 1
	return numberOfTrees	

inList = readFileOfStringsToList()
for row in inList:
	print(row)
rows = len(inList)
columns = len(inList[0])
print('rows',rows)
print('columns',columns)
numberOfTrees1 = countTreesOnWayDown(1,1,inList)
numberOfTrees2 = countTreesOnWayDown(3,1,inList)
numberOfTrees3 = countTreesOnWayDown(5,1,inList)
numberOfTrees4 = countTreesOnWayDown(7,1,inList)
numberOfTrees5 = countTreesOnWayDown(1,2,inList)
totalTrees = numberOfTrees1 * numberOfTrees2 * numberOfTrees3 * numberOfTrees4 * numberOfTrees5
print('trees',totalTrees)

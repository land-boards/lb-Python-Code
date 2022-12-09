""" 
D08P2

30373
25512
65332
33549
35390
"""

fileName = 'input.txt'
# fileName = 'input1.txt'

moveDirs = ((1,0),(-1,0),(0,1),(0,-1))
def countTrees(treeX,treeY):
	global xSize
	global ySize
	treeVal = treeList[treeY][treeX]
	# print('***checking',treeX,treeY,'height',treeVal,end=' ')
	# look up
	stopLooking = False
	treeCount = 0
	# print('looking up')
	upScore = 0
	for yVal in range(treeY-1,-1,-1):
		# print('checking tree at',treeX,yVal)
		if (treeList[yVal][treeX] >= treeVal) and (not stopLooking):
			stopLooking = True
			upScore += 1
			# print('stop looking at',treeX,yVal,treeList[yVal][treeX])
		elif not stopLooking:
			upScore += 1
			# print('counting tree at',treeX,yVal,treeList[yVal][treeX])
		# else:
			# print('skipping tree at',treeX,yVal,treeList[yVal][treeX])
	# print('upScore',upScore)
	# Look down
	stopLooking = False
	# print('looking down')
	downScore = 0
	for yVal in range(treeY+1,ySize,+1):
		# print('checking tree at',treeX,yVal)
		if (treeList[yVal][treeX] >= treeVal) and (not stopLooking):
			stopLooking = True
			downScore += 1
			# print('stop looking at',treeX,yVal,treeList[yVal][treeX])
		elif not stopLooking:
			downScore += 1
			# print('counting tree at',treeX,yVal,treeList[yVal][treeX])
		# else:
			# print('skipping tree at',treeX,yVal,treeList[yVal][treeX])		
	# print('downScore',downScore)
	# Look left
	stopLooking = False
	# print('looking left')
	leftScore = 0
	for xVal in range(treeX-1,-1,-1):
		# print('checking tree at',xVal,treeY)
		if (treeList[treeY][xVal] >= treeVal) and (not stopLooking):
			stopLooking = True
			leftScore += 1
			# print('stop looking at',xVal,treeY,treeList[treeY][xVal])
		elif not stopLooking:
			leftScore += 1
			# print('counting tree at',xVal,treeY,treeList[treeY][xVal])
		# else:
			# print('skipping tree at',xVal,treeY,treeList[treeY][xVal])
	# print('leftScore',leftScore)
	# Look right
	stopLooking = False
	# print('looking right')
	rightScore = 0
	for xVal in range(treeX+1,xSize,+1):
		# print('checking tree at',xVal,treeY)
		if (treeList[treeY][xVal] >= treeVal) and (not stopLooking):
			stopLooking = True
			rightScore += 1
			# print('stop looking at',xVal,treeY,treeList[treeY][xVal])
		elif not stopLooking:
			rightScore += 1
			# print('counting tree at',xVal,treeY,treeList[treeY][xVal])
		# else:
			# print('skipping tree at',xVal,treeY,treeList[treeY][xVal])		
	# print('rightScore',rightScore)
	treeTotalScore = upScore * downScore * leftScore * rightScore
	# print('treeTotalScore',treeTotalScore)
	return treeTotalScore

treeList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		lineList=[]
		for inChar in inLine:
			lineList.append(int(inChar))
		treeList.append(lineList)
# print(treeList)
xSize = len(treeList[0])
ySize=len(treeList)

# countTrees(2,3)
# assert False,'stop'

maxtrees = 0
for treeY in range(ySize):
	for treeX in range(xSize):
		treeScore = countTrees(treeX,treeY)
		if treeScore > maxtrees:
			maxtrees = treeScore

print('max score',maxtrees)

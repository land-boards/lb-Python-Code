""" 
D09P2
2224 is too low
2191 can't be right
2427 is wrong
2376 is the right number
2500 is too high
"""
import time

# At start
startTime = time.time()

tailPosArray = []

def moveTailSingleStep(headX,headY,tailX,tailY):
	if (abs(headY-tailY) == 1) and (abs(headX-tailX) == 1):
		return tailX,tailY
	if (headY == tailY) and (headX == tailX):
		return tailX,tailY
	if headY == tailY:	# same colmn
		if headX > tailX+1:
			tailX += 1
		elif headX < tailX-1:
			tailX -= 1
	elif headX == tailX:	# same row
		if headY > tailY+1:
			tailY += 1
		elif headY < tailY-1:
			tailY -= 1
	else:	# diag
		if headY > tailY:
			tailY += 1
		elif headY < tailY:
			tailY -= 1
		if headX > tailX:
			tailX += 1
		elif headX < tailX:
			tailX -= 1
		else:
			assert False,'did not move'
	return tailX,tailY
	
moves={'U':(0,1),'D':(0,-1),'R':(1,0),'L':(-1,0)}
def moveHeadAndTail(headX,headY,dir,distMovedHead):
	global numTails
	# print('moveHeadAndTail: tailPosArray (before)',tailPosArray)
	moveX = moves[dir][0]
	moveY = moves[dir][1]
	# print('before moving head')
	# printPosArray(headX,headY,tailPosArray)
	for _ in range(distMovedHead):
		headX += moveX
		headY += moveY
		# print('after moving head, before moving tail')
		# printPosArray(headX,headY,tailPosArray)
		for tailNum in range(numTails):
			if tailNum == 0:
				tailX = tailPosArray[0][0]
				tailY = tailPosArray[0][1]
				newTailX,newTailY = moveTailSingleStep(headX,headY,tailX,tailY)
			else:
				newTailX,newTailY = moveTailSingleStep(tailPosArray[tailNum-1][0],tailPosArray[tailNum-1][1],tailPosArray[tailNum][0],tailPosArray[tailNum][1])
			if tailNum == numTails - 1:
				# print('moveHeadAndTail: move newTailX newTailY',newTailX,newTailY)
				if [newTailX,newTailY] not in tails:
					tails.append([newTailX,newTailY])
				# tails.append([newTailX,newTailY])
			tailPosArray[tailNum] = [newTailX,newTailY]
		# print('after moving tails')
	# printPosArray(0,0,tailPosArray)
	# input('hit key')
	return headX,headY

def printPosArray(headX,headY,posArr):
	# print(posArr)
	# global headX
	# global headY
	maxX = 0
	maxY = 0
	minX = 0
	minY = 0
	for point in posArr:
		if point[0] > maxX:
			maxX = point[0]
		if point[0] < minX:
			minX = point[0]
		if point[1] > maxY:
			maxY = point[1]
		if point[1] < minY:
			minY = point[1]
		# if headX > maxX:
			# maxX = headX
		# if headX < minX:
			# minX = headX
		# if headY > maxY:
			# maxY = headY
		# if headY < minY:
			# minY = headY
	# print('minX,xmaxX,minY,maxY',minX,maxX,minY,maxY)
	for y in range(maxY,minY-1,-1):
		for x in range(minX,maxX+1):
			gotIt = False
			if [x,y] == [0,0]:
				print('S',end='')
			elif [x,y] in posArr:
				for num in range(len(posArr)):
					if posArr[num] == [x,y] and not gotIt:
						print('#',end='')
						# print(num+1,end='')
						gotIt = True
			# elif headX == x and headY == y:
				# print('H',end='')
			else:
				print('.',end='')
		print()
	print()

fileName = 'input.txt'
# fileName = 'input3.txt'
print('fileName',fileName)
numTails = 10	# 9 in example, 10 in problem
print('Number of tail knots',numTails)

inList=[]
headX = 0
headY = 0
tailX= 0
tailY= 0
tails=[]	# tailX,tailY pairs
# Initialize the positions of the tails to 0,0
tailPosArray = []
for tailNum in range(numTails):
	tailPosArray.append([0,0])

with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		# print('*********** inLine: ',inLine)
		dir = inLine[0]
		distMovedHead = int(inLine[2:])
		headX,headY = moveHeadAndTail(headX,headY,dir,distMovedHead)
# printPosArray(headX,headY,tails)

# print('tailPosArray',tailPosArray)
# print(tails)
print('visited',len(tails),'spots')
endTime = time.time()
print('time',endTime-startTime)
# printPosArray(0,0,tails)

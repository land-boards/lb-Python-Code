""" 
D22P2
"""


def getNewDir(currentDir,move):
	# Right turns
	if currentDir == '>' and move == 'R':
		return 'v',0,1
	elif currentDir == '<' and move == 'R':
		return '^',0,-1
	elif currentDir == '^' and move == 'R':
		return '>',1,0
	elif currentDir == 'v' and move == 'R':
		return '<',-1,0
	# Left turns
	elif currentDir == '>' and move == 'L':
		return '^',0,-1
	elif currentDir == '<' and move == 'L':
		return 'v',0,1
	elif currentDir == '^' and move == 'L':
		return '<',-1,0
	elif currentDir == 'v' and move == 'L':
		return '>',1,0
	
	assert False,'newDir: bad'

def getWrapNextLoc(currentDir,currentX,currentY):
	debug_getWrapNextLoc = False
	sizeX = len(newMap[0])
	sizeY = len(newMap)
	if debug_getWrapNextLoc:
		print('sizeX,sizeY',sizeX,sizeY)
	if currentDir == '>':
		xPos = 0
		while newMap[currentY][xPos] != '.':
			if newMap[currentY][xPos] == '#':
				return False,currentX,currentY
			xPos += 1
		return True,xPos,currentY
	elif currentDir == '<':
		xPos = sizeX-1
		while newMap[currentY][xPos] != '.':
			if newMap[currentY][xPos] == '#':
				return False,currentX,currentY
			xPos -= 1
		return True,xPos,currentY
	elif currentDir == '^':
		yPos = sizeY - 1
		while newMap[yPos][currentX] != '.':
			if newMap[yPos][currentX] == '#':
				return False,currentX,currentY
			yPos -= 1
		return True,currentX,yPos
	elif currentDir == 'v':
		yPos = 0
		if debug_getWrapNextLoc:
			print('getWrapNextLoc: currentX,yPos',currentX,yPos,'newMap[yPos][currentX]',newMap[yPos][currentX])
		while newMap[yPos][currentX] != '.':
			if debug_getWrapNextLoc:
				print('getWrapNextLoc: currentX,yPos',currentX,yPos,'newMap[yPos][currentX]',newMap[yPos][currentX])
			if newMap[yPos][currentX] == '#':
				if debug_getWrapNextLoc:
					print('getWrapNextLoc (2): currentX,currentY',currentX,currentY)
				return False,currentX,currentY
			yPos += 1
		if debug_getWrapNextLoc:
			print('getWrapNextLoc: found ',newMap[yPos][currentX],'at',currentX,yPos)
			for row in newMap:
				print(row)
	#		assert False
		return True,currentX,yPos
		
		
	assert False,'\ngetWrapNextLoc: stop'

def movePlayer(currentDir,posX,posY,deltaX,deltaY,distance):
	debug_movePlayer = False
	if debug_movePlayer:
		print('currentDir',currentDir,'move from',posX,posY,end=' ')
	endX=posX+(deltaX * distance)
	endY=posY+(deltaY * distance)
	if debug_movePlayer:
		print('try to move to',endX,endY)
	newX = posX
	newY = posY
	steps = 0
	if deltaY == 0:
		while steps < distance:
			if newMap[posY][newX+deltaX] == '.':
				newX += deltaX
				if debug_movePlayer:
					print('movePlayer: move in x to',newX)
				steps += 1
			else:
				if debug_movePlayer:
					print('movePlayer: newX',newX)
				if newMap[posY][newX+deltaX] == '#':
					if debug_movePlayer:
						print('wall at x =',newX+deltaX)
						print('movePlayer: returns x,y',newX,newY)
					return newX,newY
				elif newMap[posY][newX+deltaX] == 'W':
					if debug_movePlayer:
						print('movePlayer: wrap in X')
					keepStepping,newX,newY=getWrapNextLoc(currentDir,newX,newY)
					if not keepStepping:
						return newX,newY
					if debug_movePlayer:
						print('movePlayer: getWrapNextLoc returned newX,newY,keepStepping',keepStepping,newX,newY)
					steps += 1
	elif deltaX == 0:
		while steps < distance:
			if newMap[newY+deltaY][posX] == '.':
				newY += deltaY
				if debug_movePlayer:
					print('movePlayer: move in y to',newY)
				steps += 1
			else:
				if debug_movePlayer:
					print('movePlayer: newY',newY,'newMap[newY+deltaY][posX]',newMap[newY+deltaY][posX])
				if newMap[newY+deltaY][posX] == '#':
					if debug_movePlayer:
						print('movePlayer: wall at y = ',newY+deltaY)
					return newX,newY
				elif newMap[newY+deltaY][posX] == 'W':
					if debug_movePlayer:
						print('movePlayer: wrap in Y')
					keepStepping,newX,newY=getWrapNextLoc(currentDir,newX,newY)
					if not keepStepping:
						return newX,newY
					if debug_movePlayer:
						print('movePlayer: getWrapNextLoc returned newX,newY,keepStepping',keepStepping,newX,newY)
					steps += 1
				else:
					assert False
	return newX,newY
	# newX = endX
	# newY = endY
	# return newX,newY
	
fileName="input1.txt"
# fileName="input.txt"

map = []
debug_main = False
with open(fileName, 'r') as filehandle:  
	state = 'map'
	for inLine in filehandle:
		inLine = inLine.strip('\n')
		# print(inLine)
		if inLine == '':
			state = 'dirs'
			# print('state dirs')
		else:
			if state == 'map':
				mapLine = []
				for ch in inLine:
					if ch == ' ':
						mapLine.append('W')	# Wrap char
					elif ch != '\n':
						mapLine.append(ch)
				map.append(mapLine)
			elif state ==  'dirs':
				dirs=inLine

# Pad the rows to all be the same length
maxX=len(map[0])
for line in map:
	if len(line) > maxX:
		maxX = len(line)
for line in map:
	if len(line) < maxX:
		padCount=maxX-len(line)
		for ct in range(padCount):
			line.append('W')

print(map)
xSize = len(map[0])
ySize = len(map)
surface=1
print('x,y',xSize,ySize)
quadrantList = []
print('Quadrant map')
if fileName=="input1.txt":
	blockXSize = 4
	blockYSize = 4
elif fileName=="input.txt":
	blockXSize = 50
	blockYSize = 50
for y in range(0,ySize,blockYSize):
	for x in range(0,xSize,blockXSize):
		if map[y][x] != 'W':
			print(surface,end=' ')
			surface += 1
			quadrantList.append([x,y,x+blockXSize-1,y+blockYSize-1])
		else:
			print('W',end = ' ')
	print()
print('quadrantList',quadrantList)
if fileName=="input1.txt":
	nextQuadrant =  {
	(1,'>'):3,(1,'<'):'tbd',(1,'^'):'tbd',(1,'v'):'tbd',
	(2,'>'):3,(2,'<'):'tbd',(2,'^'):'tbd',(2,'v'):'tbd',
	(3,'>'):3,(3,'<'):'tbd',(3,'^'):'tbd',(3,'v'):'tbd',
	(4,'>'):3,(4,'<'):'tbd',(4,'^'):'tbd',(4,'v'):'tbd',
	(5,'>'):3,(5,'<'):'tbd',(5,'^'):'tbd',(5,'v'):'tbd',
	(6,'>'):3,(6,'<'):'tbd',(6,'^'):'tbd',(6,'v'):'tbd'
	}
elif fileName=="input.txt":
	nextQuadrant = {
	(1,'>'):2, (1,'<'):'tbd', (1,'^'):'tbd', (1,'v'):'tbd',
	(2,'>'):2, (2,'<'):'tbd', (2,'^'):'tbd', (2,'v'):'tbd',
	(3,'>'):2, (3,'<'):'tbd', (3,'^'):'tbd', (3,'v'):'tbd',
	(4,'>'):2, (4,'<'):'tbd', (4,'^'):'tbd', (4,'v'):'tbd',
	(5,'>'):2, (5,'<'):'tbd', (5,'^'):'tbd', (5,'v'):'tbd',
	(6,'>'):2, (6,'<'):'tbd', (6,'^'):'tbd', (6,'v'):'tbd',
	}
print(nextQuadrant)
assert False

# Pad the entire map with W (wap)
endLine = []
for off in range(maxX+2):
	endLine.append('W')
	
newMap = []
newMap.append(list(endLine))
for y in range(len(map)):
	newLine = []
	newLine.append('W')
	for x in range(maxX):
		newLine.append(map[y][x])
	newLine.append('W')
	newMap.append(newLine)
newMap.append(list(endLine))

if debug_main:
	# print('maxX',maxX)
	print('newMap')
	for line in newMap:
		print(line)
dirList = []
num=0
for ch in dirs:
	if '0' <= ch <= '9':
		dig = ord(ch) - ord('0')
		num = num * 10 + dig
	else:
		dirList.append(num)
		dirList.append(ch)
		num = 0
map = []
dirList.append(num)
# Find first
posX = 1
posY = 1
for x in range(len(newMap[1])):
	if (posX == 1) and (newMap[posY][x] == '.'):
		posX = x
		break
initDir = '>'
if debug_main:
	print('initDir',initDir)
	print('posX =',posX,'posY =',posY)
	print(dirs)
	print(dirList)
currentDir='>'
deltaX,deltaY = 1,0
for movement in dirList:
	# print(movement)
	if isinstance(movement,int):
		if debug_main:
			print('distance',movement)
		posX,posY = movePlayer(currentDir,posX,posY,deltaX,deltaY,movement)
		if debug_main:
			print()
	else:
		if debug_main:
			print('Dir (before',currentDir,end=' ')
		currentDir,deltaX,deltaY = getNewDir(currentDir,movement)
		if debug_main:
			print('currentDir (after)',currentDir)

#  0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
facingVal={'>':0,'v':1,'<':2,'^':3}
val=facingVal[currentDir]
if debug_main:
	print('x y ',posX,posY,'dir',val)
result = (1000*posY) + (4*posX) + val
print('result',result)

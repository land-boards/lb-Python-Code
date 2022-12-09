""" 
D09P1

"""

moves={'U':(0,1),'D':(0,-1),'R':(1,0),'L':(-1,0)}
#print(moves)

tailPos = []

def moveTail():
	global headX
	global headY
	global tailX
	global tailY
	# print('moveTail (before): head',headX,headY,'tail',tailX,tailY)
	if headY == tailY:
		print('moveTail: in same row')
		if headX > tailX+1:
			tailX += 1
		elif headX < tailX-1:
			tailX -= 1
	elif headX == tailX:
		print('moveTail: in same col')
		if headY > tailY+1:
			tailY += 1
		elif headY < tailY-1:
			tailY -= 1
	else:
		print('moveTail: diff row/col')
		if headY > tailY+1:
			tailX = headX
			tailY += 1
		elif headY < tailY-1:
			tailX = headX
			tailY -= 1
		elif headX > tailX+1:
			tailX += 1
			tailY = headY
		elif headX < tailX-1:
			tailX -= 1
			tailY = headY
		else:
			print('OK, no move')
	if (tailX,tailY) not in tailPos:
		tailPos.append((tailX,tailY))
	print('moveTail (after): head',headX,headY,'tail',tailX,tailY)
	
def moveHeadTail(dir,dist):
	global headX
	global headY
	global tailX
	global tailY
	# print(moves[dir])
	moveX = moves[dir][0]
	moveY = moves[dir][1]
	for step in range(dist):
		headX += moveX
		headY += moveY
		moveTail()
		# print('main: head',headX,headY,'tail',tailX,tailY)

fileName = 'input.txt'
# fileName = 'input1.txt'

inList=[]
headX = 0
headY = 0
tailX= 0
tailY= 0
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		dir = inLine[0]
		distMovedHead = int(inLine[2:])
		print('main:',dir,distMovedHead)
		moveHeadTail(dir,distMovedHead)

print(tailPos)
print('visited',len(tailPos),'spots')

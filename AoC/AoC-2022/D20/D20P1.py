""" 
D20P1

7350 is too low

"""

def readInList():
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip()
			inList.append(int(inLine))
	return inList

def findOffsetInList(val,inList):
	i = 0
	for testVal in inList:
		if testVal == val:
			# print('val',val,'is at offset',i)
			return i
		i += 1
	print('findOffsetInList: Didnt find val',val)
	assert False

fileName="input.txt"
# fileName="input1.txt"

inList = readInList()
moveList = list(inList)
print('@start')
print('inList',inList[0:10])
print()
# print('sorted(inList)',sorted(inList))

listLen = len(inList)
print('listLen',listLen)
moveFromCol = 0
for moveOff in range(len(inList)):
	val = inList[moveOff]
	print('move#',moveOff,'move value',val,end=' moves ')
	moveFromOffset = findOffsetInList(val,moveList)
	print('from offset',moveFromOffset,end=' ')
	moveToOffset = val + moveFromOffset + 1
	print('to offset (before)',moveToOffset,end=', ')	
	if moveToOffset > listLen:
		moveToOffset = moveToOffset - (listLen-1)
	else:
		while moveToOffset < 0:
			moveToOffset = (listLen-1) + moveToOffset
	if moveFromOffset > moveToOffset:
		moveToOffset -= 1
	print('to offset',moveToOffset)
	if (moveToOffset > moveFromOffset):
		moveList.insert(moveToOffset,val)
		moveList.pop(moveFromOffset)
	elif moveToOffset == 0:
		moveList.append(val)
		moveList.pop(moveFromOffset)
	elif moveToOffset < moveFromOffset:
		moveList.insert(moveToOffset,val)
		moveList.pop(moveFromOffset+1)
	for i in moveList[0:10]:
		print(i,end=', ')
	print('')
	print('')

start = findOffsetInList(0,moveList)
n1 = moveList[(start+1000)%listLen]
n2 = moveList[(start+2000)%listLen]
n3 = moveList[(start+3000)%listLen]
print(n1,n2,n3)
print('sum',n1+n2+n3)

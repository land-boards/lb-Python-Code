#inStr = '284573961'		# My input

def getCups():
	global q
	

inStr = '389125467'		# Example
q = []
for element in inStr:
	q.append(int(element))
moves = 10
currentCupPtr = 0
while moves > 0:
	print('\nMove',11-moves)
	print('cups:',q)
	cupList = []
	for i in range(3):
		getCupOffset = currentCupPtr + 1 + i
		if getCupOffset > 8:
			getCupOffset = 0
		cupList.append(q[getCupOffset])
	print('pick up:',cupList)
	valueAtPoint = q[currentCupPtr]
	print('value at the point',currentCupPtr,'is',valueAtPoint)
	lookingForValue = valueAtPoint - 1
	print('Starting looking for value',lookingForValue)
	for cupToRemove in cupList:
		q.remove(cupToRemove)
	# print('q after removal',q)
	if lookingForValue in cupList:
		while lookingForValue in cupList:
			print('looking for this',lookingForValue)
			lookingForValue -= 1
			if lookingForValue == 0:
				lookingForValue = 9
		print('found val',lookingForValue)
		offset = lookingForValue
		print('destination (looking for value) after adjustment',lookingForValue)
		for offset in range(len(q)):
			if q[offset] == lookingForValue:
				break
		offset += 1
		print('insert at offset',offset)
	else:
		offset = lookingForValue
		print('destination (looking for value) after adjustment',offset)
		for offset in range(len(q)):
			if q[offset] == lookingForValue:
				break
		offset += 1
		print('insert at offset',offset)
	for val in range(3):
		q.insert(offset,cupList[2-val])	# insert backwards
	currentCupPtr += 1
	if currentCupPtr > 9:
		currentCupPtr = 0
	moves -= 1
	
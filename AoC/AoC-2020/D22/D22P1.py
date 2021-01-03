""" 

D22P1

"""

import collections

playa1Deque = collections.deque([])
playa2Deque = collections.deque([])

def readToLists(fileName):
	""" Cards are added to the right in the deque
	"""
	global playa1Deque
	global playa2Deque
	stateList = ['inWaitPlayer1','inList1','inWaitPlayer2','inList2']
	state = 'inWaitPlayer1'
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			line = line.strip()
			if state == 'inWaitPlayer1':
				state = 'inList1'
			elif state == 'inList1':
				if line != '':
					playa1Deque.append(int(line.strip()))
				else:
					state = 'inWaitPlayer2'
			elif state == 'inWaitPlayer2':
				state = 'inList2'
			elif state == 'inList2':
				playa2Deque.append(int(line.strip()))
	return

def calculateResult():
	global playa1Deque
	global playa2Deque
	productSum = 0
	if len(playa1Deque) != 0:
		# print('Playa 1 deque',playa1Deque)
		val = len(playa1Deque)
		for listItem in playa1Deque:
			productSum += val*listItem
			val -= 1
	else:
		# print('Playa 2 deque',playa2Deque)
		val = len(playa2Deque)
		for listItem in playa2Deque:
			productSum += val*listItem
			val -= 1
	return productSum

def playRound(p1Deque,p2Deque):
	"""
	Cards are removed from the left and added to the right of the deck
	"""
	topCardPlaya1 = p1Deque.popleft()
	topCardPlaya2 = p2Deque.popleft()
	if topCardPlaya1 > topCardPlaya2:
		p1Deque.append(topCardPlaya1)
		p1Deque.append(topCardPlaya2)
	else:
		p2Deque.append(topCardPlaya2)
		p2Deque.append(topCardPlaya1)
	if ((len(p1Deque) == 0) or (len(p2Deque) == 0)):
		return True
	return False

# Program follows
readToLists('input.txt')

while not playRound(playa1Deque,playa2Deque):
	pass
	
productSum = calculateResult()
print('productSum',productSum)

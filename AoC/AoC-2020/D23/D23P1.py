class CircularQueue:

	#Constructor
	def __init__(self):
		self.queue = list()
		self.currentCup = 0
		self.maxSize = 9

	#Adding elements to the queue
	def enqueue(self,data):
		if self.size() >= self.maxSize:
			assert False,'Queue already Full!'
		self.queue.append(data)
		return True

	#Adding elements to the queue
	def insertqueue(self,offset,data):
		# print('before insert ',end='')
		# self.printQueue()
		# print('inserting val',data,'at listSpot',self.currentCup + offset)
		if self.size() > self.maxSize:
			assert False,'Queue too full!'
		self.queue.insert(offset,data)
		# print('after insert ',end='')
		# self.printQueue()
		return True

	#Removing elements from the queue
	def dequeueRemove(self,offset=0):
		if self.size()==0:
			assert False, 'Queue Empty!'
		data = self.queue[(self.currentCup+offset) % self.size()]
		self.queue.remove(data)
		return data

	#Return element at currentCup from the queue
	def dequeue(self,offset=0):
		if self.size()==0:
			assert False, 'Queue Empty!'
		data = self.queue[(self.currentCup+offset) % self.size()]
		return data

	#Calculating the size of the queue
	def size(self):
		DEBUG_SIZE = False
		return len(self.queue)
		
	def advancePointer(self):
		self.currentCup = (self.currentCup + 1) % self.size()
		print('New cup pointer',self.currentCup)
		
	def printQueue(self):
		print(self.queue)
		
	def isInQueue(self,valToCheck):
		if valToCheck in self.queue:
			# print('(isInQueue) : Is in queue val',valToCheck)
			return True
		else:
			# print('(isInQueue) : Not in queue val',valToCheck)
			return False

	def getOffsetOfValue(self,valToFind):
		for i in range(len(q.queue)):
			if q.queue[i] == valToFind:
				return i
		assert False,"couldn't find"
				
q = CircularQueue()
#inStr = '284573961'		# My input
inStr = '389125467'		# Example
for element in inStr:
	q.enqueue(int(element))
moves = 10
currentCupPtr = 0
while moves > 0:
	print('\nmove',11-moves)
	print('cups : ',end='')
	q.printQueue()
	print('currentCupPtr',currentCupPtr,'curr cup val',q.queue[q.currentCup])
	lookingFor = q.queue[q.currentCup] - 1
	print('Initially looking for cup',lookingFor)
	cup1 = q.dequeue(1)
	# print('cup1',cup1)
	cup2 = q.dequeue(2)
	# print('cup2',cup2)
	cup3 = q.dequeue(3)
	cupList = [cup1,cup2,cup3]
	print('pick up',cup1,cup2,cup3)
	# print('queue after removal ',end='')
	# q.printQueue()
	matchedCup = False
	newQueueOffset = 0
	if lookingFor not in cupList:
		print('value',lookingFor,'is in not in the cupList')
		while not matchedCup:
			checkingCup = q.dequeue(newQueueOffset)
			# print('checking cup value',checkingCup,end = ' ')
			if checkingCup == lookingFor:
				# print('matched')
				matchedCup = True
			# else:
				# print('not matched')
			newQueueOffset += 1
			if newQueueOffset > q.size():
				newQueueOffset = 0
	else:
		print('value',lookingFor,'is not in the queue')
		lookingFor -= 1
		if lookingFor < 1:
			lookingFor = 6
		print('lookingFor cup',lookingFor)
		while not q.isInQueue(lookingFor):
			print('checking for',lookingFor)
			lookingFor -= 1
			if lookingFor == 0:
				lookingFor = 9
		print('destination :',lookingFor)
		newQueueOffset = q.getOffsetOfValue(lookingFor) + 1
		print('found at offset',newQueueOffset-1,'in queue')
		# assert False,'deal with it'
	print('newQueueOffset',newQueueOffset)
	q.dequeueRemove(1)
	q.dequeueRemove(1)
	q.dequeueRemove(1)
	q.insertqueue(newQueueOffset % q.maxSize,cup1)
	q.insertqueue((newQueueOffset+1) % q.maxSize,cup2)
	q.insertqueue((newQueueOffset+2) % q.maxSize,cup3)
	q.printQueue()
	q.advancePointer()
	moves -= 1

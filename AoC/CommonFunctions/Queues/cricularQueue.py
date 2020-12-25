class CircularQueue:

	#Constructor
	def __init__(self):
		self.queue = list()
		self.head = 0
		self.tail = 0
		self.maxSize = 8

	#Adding elements to the queue
	def enqueue(self,data):
		if self.size() == self.maxSize-1:
			return ("Queue Full!")
		self.queue.append(data)
		self.tail = (self.tail + 1) % self.maxSize
		return True

	#Removing elements from the queue
	def dequeue(self):
		if self.size()==0:
			return ("Queue Empty!") 
		data = self.queue[self.head]
		self.head = (self.head + 1) % self.maxSize
		return data

	#Calculating the size of the queue
	def size(self):
		if self.tail>=self.head:
			return (self.tail-self.head)
		return (self.maxSize - (self.head-self.tail))
		
	def printQueue(self):
		print('queue',self.queue)

q = CircularQueue()
#inStr = '284573961'		# My input
inStr = '389125467'		# Example
for element in inStr:
	q.enqueue(element)
q.printQueue()

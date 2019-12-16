# https://www.youtube.com/watch?v=ob4faIum4kQ

from queue import PriorityQueue

class State(object):

	'''
	Author: Kevin Pulido
	27-Sept-2017

	Steps:
	1) Generate a list of all possible next Steps toward goal from current position
	2) Store Children in PriorityQueue based on distance to goal, closest first
	3) Select closest child and Repeat until goal reached or no more Children
	'''

	def __init__(self, value, parent,
				 start = 0,
				 goal = 0):

		self.children = []
		self.parent = parent
		self.value = value
		self.dist = 0

		if parent:
			self.start  = parent.start
			self.goal   = parent.goal
			self.path   = parent.path[:]
			self.path.append(value)
		else:
			self.path   = [value]
			self.start  = start
			self.goal   = goal

	def GetDistance(self):
		pass

	def CreateChildren(self):
		pass

class State_String(State):
	def __init__(self,value,parent,
				 start = 0,
				 goal = 0):

		super(State_String, self).__init__(value, parent, start, goal)
		self.dist = self.GetDistance()

	def GetDistance(self):

		if self.value == self.goal:
			return 0
		dist = 0
		for i in range(len(self.goal)):
			letter = self.goal[i]
			try:
				dist += abs(i - self.value.index(letter))
			except:
				dist += abs(i - self.value.find(letter))
		return dist

	def CreateChildren(self):
		if not self.children:
			for i in range(len(self.goal)-1):
				val = self.value
				val = val[:i] + val[i+1] + val[i] + val[i+2:]
				child = State_String(val, self)
				self.children.append(child)

class AStar_Solver:
	def __init__(self, start , goal):
		self.path		  = []
		self.visitedQueue  = []
		self.priorityQueue = PriorityQueue()
		self.start		 = start
		self.goal		  = goal

	def Solve(self):
		startState = State_String(self.start,
								  0,
								  self.start,
								  self.goal)

		count = 0
		self.priorityQueue.put((0,count,startState))

		while(not self.path and self.priorityQueue.qsize()):
			closestChild = self.priorityQueue.get()[2]
			closestChild.CreateChildren()
			self.visitedQueue.append(closestChild.value)

			for child in closestChild.children:
				if child.value not in self.visitedQueue:
					count +=1
					if not child.dist:
						self.path = child.path
						break
					self.priorityQueue.put((child.dist,count,child))

		if not self.path:
			print("Goal of %s is not possible!" % (self.goal))

		return self.path


if __name__ == "__main__":
	start1 = "edcba"
	goal1  = "abcde"
	print("Starting...")

	a = AStar_Solver(start1, goal1)
	a.Solve()

	for i in range(len(a.path)):
		print("{0}) {1}".format(i, a.path[i]))
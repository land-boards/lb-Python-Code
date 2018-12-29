# Pt1-AoCDay9.py
# 2018 Advent of Code
# Day 9
# Part 1
# https://adventofcode.com/2018/day/9

import time
import os

"""

--- Day 9: Marble Mania ---
You talk to the Elves while you wait for your navigation system to initialize. To pass the time, they introduce you to their favorite marble game.

The Elves play this game by taking turns arranging the marbles in a circle according to very particular rules. The marbles are numbered starting with 0 and increasing by 1 until every marble has a number.

First, the marble numbered 0 is placed in the circle. At this point, while it contains only a single marble, it is still a circle: the marble is both clockwise from itself and counter-clockwise from itself. This marble is designated the current marble.

Then, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles that are 1 and 2 marbles clockwise of the current marble. (When the circle is large enough, this means that there is one marble between the marble that was just placed and the current marble.) The marble that was just placed then becomes the current marble.

However, if the marble that is about to be placed has a number which is a multiple of 23, something entirely different happens. First, the current player keeps the marble they would have placed, adding it to their score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed from the circle and also added to the current player's score. The marble located immediately clockwise of the marble that was removed becomes the new current marble.

For example, suppose there are 9 players. After the marble with value 0 is placed in the middle, each player (shown in square brackets) takes a turn. The result of each of those turns would produce circles of marbles like this, where clockwise is to the right and the resulting current marble is in parentheses:

[-] (0)
[1]  0 (1)
[2]  0 (2) 1 
[3]  0  2  1 (3)
[4]  0 (4) 2  1  3 
[5]  0  4  2 (5) 1  3 
[6]  0  4  2  5  1 (6) 3 
[7]  0  4  2  5  1  6  3 (7)
[8]  0 (8) 4  2  5  1  6  3  7 
[9]  0  8  4 (9) 2  5  1  6  3  7 
[1]  0  8  4  9  2(10) 5  1  6  3  7 
[2]  0  8  4  9  2 10  5(11) 1  6  3  7 
[3]  0  8  4  9  2 10  5 11  1(12) 6  3  7 
[4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7 
[5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7 
[6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
[7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15 
[8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15 
[9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15 
[1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15 
[2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15 
[3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15 
[4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15 
[5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15 
[6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15 
[7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15
The goal is to be the player with the highest score after the last marble is used up. Assuming the example above ends after the marble numbered 25, the winning score is 23+9=32 (because player 5 kept marble 23 and removed marble 9, while no other player got any points in this very short example game).

Here are a few more examples:

10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
What is the winning Elf's score?

464 players; last marble is worth 71730 points

max player score 380705

That's the right answer! You are one gold star closer to fixing the time stream.

"""

#####################################################################################
## Functions which operate on the marbles list
## listOfMarbles is a linked list with links in both directions
## 	marble = [marbleNumber,marbleToLeft,marbleToRight,playerNumber]
	
MARBLE_VALUE = 0
MARBLE_NODE_TO_THE_LEFT = 1
MARBLE_NODE_TO_THE_RIGHT = 2
PLAYER_NUMBER = 3

class MarblesClass():
	"""The class that handles the marble lists
	
	"""
	## Class values
	currentPlayerNumber = 0
	currentMarbleValue = 0
	nextMarblePointer = 0
	listOfMarbles = []
	playersAndScores = []
	currentMarblePointer = 0
	
	def initializePlayersAndScores(self,numberOfPlayers):
		"""Creates a list of player scores
		List is one longer than the number of players since the player numbers 
		go from 1 to the number of players.
		Player 0 is non-existent.
		
		:param numberOfPlayers: This is a feature of the problem set - known number of players
		"""
		debug_initializePlayersAndScores = False
		for player in xrange(numberOfPlayers+1):
			playerScore = 0
			self.playersAndScores.append(playerScore)
		if debug_initializePlayersAndScores:
			print 'initializePlayersAndScores: Initialized the player scores for',player,'players'
		return

	def dumpEverything(self):
		print 'vvvvvvvvvvv BEGIN ALL VALUES vvvvvvvvvvv'
		print 'lastMarbleValue',lastMarbleValue
		print 'currentPlayerNumber',self.getCurrentPlayerNumber()
		print 'currentMarbleValue',self.currentMarbleValue
		print 'nextMarblePointer',self.nextMarblePointer
		print 'currentMarblePointer',self.currentMarblePointer
		print 'listOfMarbles in link order'
		print self.dumpMarblesOrder()
		print 'playersAndScores'
		self.dumpPlayersScores()
		print '^^^^^^^^^^^ END ALL VALUES ^^^^^^^^^^^'
		
	def getMarbleNumberFromNode(self,nodeNumber):
		return self.listOfMarbles[nodeNumber][0]
	
	def dumpMarblesList(self):
		"""Dump out a table of the marbles links in node order (not the same as playing order)
		"""
		print 'NodeNumber MarbleValue leftMarbleNode rightMarbleNode playerNumber'
		i = 0
		for marbleListEntry in self.listOfMarbles:
			print '%6d' % (i),
			print '%10d' % (self.getMarbleNumberFromNode(i)),
			print '%12d' % (self.listOfMarbles[i][1]),
			print '%14d' % (self.listOfMarbles[i][2]),
			print '%13d' % (self.listOfMarbles[i][3]),
			print
			i += 1
		print '\n'
		
	def dumpMarblesOrder(self):
		"""Go through the marbles by the node numbers
		"""
		startingMarbleNumber = 0	# Always starts with the first marble (0)
		print '[',
		print self.currentPlayerNumber-1,
		print ']',startingMarbleNumber,
		marbleNodeToTheRight = self.listOfMarbles[0][2]		# next marble
		while marbleNodeToTheRight != startingMarbleNumber:	# stop when list wraps back to start of the nodes
			print self.listOfMarbles[marbleNodeToTheRight][0],
			marbleNodeToTheRight = self.listOfMarbles[marbleNodeToTheRight][2]	# get the next marble to the right
		print '\n'
		
	def dumpPlayersScores(self):
		"""Dump out the player scores
		"""
		print 'players scores are:'
		for player in xrange(1,len(self.playersAndScores)):
			print 'player',player,'score',self.playersAndScores[player]
	
	def addFirstMarbleToCircle(self):
		"""
		The first marble is not placed by any player so using player 0 to represent that player.
		
		:returns: the nextMarblePointer
		"""
		debug_addFirstMarbleToCircle = False
		if debug_addFirstMarbleToCircle:
			print 'addFirstMarbleToCircle: empty circle case'
		self.appendMarbleToMarbleList(self.currentMarbleValue,0,0,self.currentPlayerNumber)
		if debug_addFirstMarbleToCircle:
			print 'addFirstMarbleToCircle: marble circle after inserting first marble'
			self.dumpEverything()
		return
	
	def appendMarbleToMarbleList(self,marbleValue,nodeToTheLeft,nodeToTheRight,playerNumber):
		"""Append the marble to the marble list.
		The pointer to the left and right marble nodes is not yet initialized.
		
		:returns: marbleNodeNumber of the node that was just added
		"""
		debug_appendMarbleToMarbleList = False
		self.listOfMarbles.append([marbleValue,nodeToTheLeft,nodeToTheRight,playerNumber])
		if debug_appendMarbleToMarbleList:
			print 'appendMarbleToMarbleList: reached function'
			print 'appendMarbleToMarbleList: marbleValue',marbleValue
			print 'appendMarbleToMarbleList: nodeToTheLeft',nodeToTheLeft
			print 'appendMarbleToMarbleList: nodeToTheRight',nodeToTheRight
			print 'appendMarbleToMarbleList: playerNumber',playerNumber
			print 'appendMarbleToMarbleList: ',self.listOfMarbles[len(self.listOfMarbles)-1]
		self.incMarbleNumberAndValue()
		self.incNextPlayerNumber()
		return (len(self.listOfMarbles) - 1)	# pointer to the node that was just added
	
	def insertMarbleIntoCircle(self):
		"""insertMarbleIntoCircle - insert the marble nodes
		Marble Node [marbleValue,marbleNodeToTheLeft,marbleNodeToTheRight,playerNumber]
		"""
		debug_insertMarbleIntoCircle = False
		if debug_insertMarbleIntoCircle:
			print 'insertMarbleIntoCircle: currentMarblePointer',self.currentMarblePointer
			print 'insertMarbleIntoCircle: nextMarblePointer',self.nextMarblePointer
		marbleOneAwayListEntry = self.listOfMarbles[self.currentMarblePointer][MARBLE_NODE_TO_THE_RIGHT]
		if debug_insertMarbleIntoCircle:
			print 'insertMarbleIntoCircle: marble one entry away is marble',marbleOneAwayListEntry
		marbleTwoAwayListEntry = self.listOfMarbles[marbleOneAwayListEntry][MARBLE_NODE_TO_THE_RIGHT]
		if debug_insertMarbleIntoCircle:
			print 'insertMarbleIntoCircle: marble two entries away is marble',marbleTwoAwayListEntry
		newMarbleNumber = self.appendMarbleToMarbleList(self.currentMarbleValue, marbleOneAwayListEntry,marbleTwoAwayListEntry,self.currentPlayerNumber)
		self.listOfMarbles[marbleTwoAwayListEntry][MARBLE_NODE_TO_THE_LEFT] = newMarbleNumber
		self.listOfMarbles[marbleOneAwayListEntry][MARBLE_NODE_TO_THE_RIGHT] = newMarbleNumber
		if debug_insertMarbleIntoCircle:
			print 'insertMarbleIntoCircle: new marble node number is',newMarbleNumber
		self.currentMarblePointer = newMarbleNumber
		if debug_insertMarbleIntoCircle:
			self.dumpMarblesList()
			self.dumpEverything()
		return

	def addNormalMarbleToCircle(self):
		debug_addNormalMarbleToCircle = False
		self.insertMarbleIntoCircle()
		if debug_addNormalMarbleToCircle:
			print 'addNormalMarbleToCircle: after operation currentMarblePointer',self.currentMarblePointer
			print 'addNormalMarbleToCircle: after operation nextMarblePointer',self.nextMarblePointer
			print 'addNormalMarbleToCircle: nextMarblePointer ',self.nextMarblePointer
			self.dumpMarblesList()
		return self.nextMarblePointer
		
	def incMarbleNumberAndValue(self):
		if self.currentMarbleValue > lastMarbleValue:
#			self.dumpPlayersScores()
			print 'max player score',self.getMaxPlayerScore()
			exit()
		self.nextMarblePointer += 1
		self.currentMarbleValue += 1

	def getMaxPlayerScore(self):
		maxPlayerScore = 0
		for player in xrange(1,len(self.playersAndScores)):
			if self.playersAndScores[player] > maxPlayerScore:
				maxPlayerScore = self.playersAndScores[player]
		return maxPlayerScore
	
	def add23rdMarbleToCircle(self):
		"""The 23rd marble is a special case.
		If the marble that is about to be placed has a number  which is a multiple of 23, 
		something entirely different happens.  
		1 - The current player keeps the marble they would have placed, adding it to their score.
		2 - The marble 7 marbles counter-clockwise from the current marble is removed from the circle 
		and also added to the current player's score. 
		3 - The marble located immediately clockwise of the marble that was removed becomes the new current marble.
		"""
		debug_add23rdMarbleToCircle = False
		if debug_add23rdMarbleToCircle:
			print '*****************\nadd23rdMarbleToCircle: reached function'
			self.dumpEverything()
		if debug_add23rdMarbleToCircle:
			print 'add23rdMarbleToCircle: player',self.currentPlayerNumber,'value from marble not being added to circle',self.playersAndScores[self.currentPlayerNumber]
		# step to the left to get to the marble to collect and spot to insert next marble at
		nextPlayer = self.listOfMarbles[self.currentMarblePointer][1]
		nextPlayer = self.listOfMarbles[nextPlayer][1]
		nextPlayer = self.listOfMarbles[nextPlayer][1]
		nextPlayer = self.listOfMarbles[nextPlayer][1]
		nextPlayer = self.listOfMarbles[nextPlayer][1]
		nextPlayer = self.listOfMarbles[nextPlayer][1]
		rightHandNode = nextPlayer
		nextPlayer = self.listOfMarbles[nextPlayer][1]
		nodeToRemove = nextPlayer
		nextPlayer = self.listOfMarbles[nextPlayer][1]
		leftHandNode = nextPlayer
		if debug_add23rdMarbleToCircle:
			print 'add23rdMarbleToCircle: right hand node',rightHandNode,'node',self.listOfMarbles[rightHandNode]
			print 'add23rdMarbleToCircle: remove marble at node',nodeToRemove,'node',self.listOfMarbles[nodeToRemove]
			print 'add23rdMarbleToCircle: left hand node',leftHandNode,'node',self.listOfMarbles[leftHandNode]
			print 'add23rdMarbleToCircle: connecting the marbles to the left and right of the node to remove together'
		self.listOfMarbles[rightHandNode][1] = leftHandNode
		self.listOfMarbles[leftHandNode][2] = rightHandNode
		marble23Value = self.currentMarbleValue
		marble23Value += self.getMarbleNumberFromNode(nodeToRemove)
		self.playersAndScores[self.currentPlayerNumber] = self.playersAndScores[self.currentPlayerNumber] + marble23Value  
		if debug_add23rdMarbleToCircle:
			print 'add23rdMarbleToCircle: player',self.currentPlayerNumber,'value after adding marble removed from circle',self.playersAndScores[self.currentPlayerNumber]
		self.currentMarblePointer = rightHandNode
		if debug_add23rdMarbleToCircle:
			print 'add23rdMarbleToCircle: the new marble pointer value is',self.currentMarblePointer
		self.currentMarbleValue += 1
		self.incNextPlayerNumber()
		self.nextMarblePointer = rightHandNode	# pointer gets moved to the node to the left
		if debug_add23rdMarbleToCircle:
			print 'add23rdMarbleToCircle: the next marble value will be',self.currentMarbleValue
			print 'add23rdMarbleToCircle: the next player number will be',self.currentPlayerNumber
			print 'add23rdMarbleToCircle: the next marble node will be',self.nextMarblePointer
			print 'add23rdMarbleToCircle: after function has finished'
		if debug_add23rdMarbleToCircle:
			self.dumpEverything()
		# print '.',
		return self.nextMarblePointer
		
	def addMarbleToCircle(self):
		"""Add another marble to the listOfMarbles
		There are three different situations with inserting marbles.
		The first marble to insert.
		The increments of 23 marble to insert.
		Any other number of marble.
		listOfMarbles has elements [marbleNumber,marbleToLeft,marbleToRight,playerNumber]
		"""
		debug_addMarbleToCircle = False
		if debug_addMarbleToCircle:
			print 'addMarbleToCircle: nextMarblePointer',self.nextMarblePointer
			print 'addMarbleToCircle: currentMarblePointer',self.currentMarblePointer
		if self.listOfMarbles == []:	# empty circle case
			if debug_addMarbleToCircle:
				print 'addMarbleToCircle: first marble case'
			self.addFirstMarbleToCircle()
		elif self.currentMarbleValue % 23 == 0:
			if debug_addMarbleToCircle:
				print 'addMarbleToCircle: 23rd marble case'
			self.add23rdMarbleToCircle()
		else:
			if debug_addMarbleToCircle:
				print 'addMarbleToCircle: normal marble case'
			self.addNormalMarbleToCircle()

	def incNextPlayerNumber(self):
		debug_incNextPlayerNumber = False
		if debug_incNextPlayerNumber:
			print 'incNextPlayerNumber: incrementing player number before incrementing',self.currentPlayerNumber
		if self.currentPlayerNumber < numberOfPlayers:
			self.currentPlayerNumber += 1
			if debug_incNextPlayerNumber:
				print 'incNextPlayerNumber: able to go to next player'
		else:
			self.currentPlayerNumber = 1
			if debug_incNextPlayerNumber:
				print 'incNextPlayerNumber: looped back to the first player'
		if debug_incNextPlayerNumber:
			print 'incNextPlayerNumber: after incrementing is',self.currentPlayerNumber
		return self.currentPlayerNumber

	## 	# Access methods for functions outside the class to get these values
	
	def getCurrentMarbleNumber(self):
		"""Return the marbleNumber
		
		:returns: nextMarblePointer after the increment
		"""
		return self.nextMarblePointer

	def getCurrentPlayerNumber(self):	# Access method for functions outside the class to get this value
		"""Return the Current Player Number
		
		:returns: nextMarblePointer after the increment
		"""
		return self.currentPlayerNumber

########################################################################
## Code

# values from the original example
# numberOfPlayers = 9
# lastMarbleValue = 32

# values from the problem
numberOfPlayers = 464
lastMarbleValue = 71730

# values from the 2nd example
# numberOfPlayers = 10
# lastMarbleValue = 1618

debug_main = False

if debug_main:
	os.system('cls')
	print 'main: there are',numberOfPlayers,'players'
	print 'main: the last marble value will be',lastMarbleValue

Marbles = MarblesClass()	# Create the marbles class
Marbles.initializePlayersAndScores(numberOfPlayers)
Marbles.addMarbleToCircle()	# Add the first marble to the list

while True:
	if debug_main:
		print 'main: ',
		Marbles.dumpMarblesOrder()
		#print 'main: current marble number',Marbles.getCurrentMarbleNumber()
		#print 'main: current player number',Marbles.getCurrentPlayerNumber()
		#os.system('pause')
	Marbles.addMarbleToCircle()
	
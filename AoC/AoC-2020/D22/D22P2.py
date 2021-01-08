"""
AoC 2020 D22 Pt2
	Needed help with recursion
	Watched video at: https://www.youtube.com/watch?v=7pZeSfFBQRo
"""

from collections import deque

def readToLists(fileName):
	""" Cards are added to the right in the deque
	Returns the two decks of cards
	"""
	playa1Deck = deque()
	playa2Deck = deque()
	stateList = ['inWaitPlayer1','inList1','inWaitPlayer2','inList2']
	state = 'inWaitPlayer1'
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			line = line.strip()
			if state == 'inWaitPlayer1':
				state = 'inList1'
			elif state == 'inList1':
				if line != '':
					playa1Deck.append(int(line.strip()))
				else:
					state = 'inWaitPlayer2'
			elif state == 'inWaitPlayer2':
				state = 'inList2'
			elif state == 'inList2':
				playa2Deck.append(int(line.strip()))
	return playa1Deck,playa2Deck

def calculateResult(hand):
	productSum = 0
	val = len(hand)
	for listItem in hand:
		productSum += val*listItem
		val -= 1
	return productSum

def playRecursiveCombat(deck1, deck2):
	# Called with the two decks
	# Returns winner number and the winner's hand
	numberOfCards = len(deck1) + len(deck2)
	gameHistory = []
	while len(deck1) != 0 and len(deck2) != 0:
		# Handle the history
		if (tuple(deck1), tuple(deck2)) in gameHistory:
			return 1, None
		gameHistory.append((tuple(deck1), tuple(deck2)))
		# Get the current cards
		card1 = deck1.popleft()
		card2 = deck2.popleft()
		# Handle the case where the lengths match
		if card1 <= len(deck1) and card2 <= len(deck2):
			subDeck1 = deque(list(deck1)[:card1])
			subDeck2 = deque(list(deck2)[:card2])
			# Play sub-game, dummyHand is not used
			winnerOfHand,dummyHand = playRecursiveCombat(subDeck1, subDeck2)
		else:
			if card1 > card2:
				winnerOfHand = 1
			else:
				winnerOfHand = 2
		# Put the cards at the back of the winner's deck
		if winnerOfHand == 1:
			deck1.append(card1)
			deck1.append(card2)
		else:
			deck2.append(card2)
			deck2.append(card1)
	# Winner's deck is the deck that is not empty
	if len(deck2) == 0:
		return 1, deck1
	return 2, deck2

hand1,hand2 = readToLists('input.txt')
winnerOfHand, winningDeck = playRecursiveCombat(hand1, hand2)
productSum = calculateResult(winningDeck)
print(productSum)

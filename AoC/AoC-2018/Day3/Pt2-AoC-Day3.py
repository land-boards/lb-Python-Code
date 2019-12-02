# Pt1-AoCDay3.py
# 2018 Advent of Code
# Day 3
# Part 1
# https://adventofcode.com/2018/day/3

import time
import re

"""

--- Part Two ---
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?

Your puzzle answer was 567.

"""

def checkOverlap(card1,card2):
	"""checkOverlap - Check the two cards for overlap
	cardX format [cardNumber,startX,startY,endX,endY]
	
	Example which overlaps
		card1 = [1, 1, 3, 4, 6]
		card2 = [2, 3, 1, 6, 4]
	
	:returns: True if the cards overlap, False if there's no overlap
	"""
	#print 'checkOverlap: checking card',card1,'vs card',card2
	leftX = 1
	lowerY = 2
	rightX = 3
	upperY = 4
	if card1[leftX] > card2[rightX]:
		return False
	elif card1[rightX] < card2[leftX]:
		return False
	elif card1[lowerY] > card2[upperY]:
		return False
	elif card1[upperY] < card2[lowerY]:
		return False
	else:
		#print 'overlaps'
		return True
	
def parseLine(claimCardRaw):
	"""parseLine example line 
	#1 @ 7,589: 24x11
	:returns: [cardID,startX,startY,endX,endY]
	"""
	print 'claimCardRaw',claimCardRaw
	inputLineList = re.split('[\D]+',claimCardRaw[1:])		# make this really easy
	print 'inputLineList',inputLineList
	accumCardNumber = int(inputLineList[0])
	accumStartX = int(inputLineList[1])
	accumStartY = int(inputLineList[2])
	accumSizeX = int(inputLineList[3])
	accumSizeY = int(inputLineList[4])
	listToReturn = []
	listToReturn.append(accumCardNumber)
	listToReturn.append(accumStartX)
	listToReturn.append(accumStartY)
	listToReturn.append(accumStartX + accumSizeX - 1)
	listToReturn.append(accumStartY + accumSizeY - 1)
	print 'list',listToReturn
	return listToReturn

def isCardInArea(xValue,yValue,checkingCard):
	"""isCardInArea - check to see if the current card is at a particular point
	:returns: True if the x,y point is in the card
	"""
	cardStartX = checkingCard[0]
	cardStartY = checkingCard[1]
	cardEndX = checkingCard[2]
	cardEndY = checkingCard[3]
	if xValue < cardStartX:
		return False
	if xValue > cardEndX:
		return False
	if yValue < cardStartY:
		return False
	if yValue > cardEndY:
		return False
	#print 'Card',checkingCard,'is at point (',xValue,',',yValue,')'
	return True

# define an empty list
claimCards = []
overlappingCards = 0	# Total of overlapping cards

print 'Reading in file',time.strftime('%X %x %Z')

# open file and read the content into an accumulated sum
with open('input.txt', 'r') as filehandle:  
	for line in filehandle:
		claimCards.append(parseLine(line.strip('\n\r')))

#print 'claimCards',claimCards

overlappingCards = []
overlappingCardCount = 0
overlappingAreas = []
cardNumber2 = 0
print 'Getting list of overlapping areas',time.strftime('%X %x %Z')
for card1 in claimCards:
	cardNumber2 += 1
	for card2 in claimCards[cardNumber2:]:
		if checkOverlap(card1,card2):
			#print 'Card 1',card1, 
			#print 'overlaps Card 2',card2
			if card1 not in overlappingCards:
				overlappingCards.append(card1)
				overlappingCardCount += 1
			if card2 not in overlappingCards:
				overlappingCards.append(card2)
				overlappingCardCount += 1
		cardNumber2 != 1
#print 'Overlapping card count',overlappingCardCount
sortedOverlappingCards = sorted(overlappingCards, key = lambda errs: errs[0])		# sort by first column
#print 'claimCards',claimCards
#print 'sortedOverlappingCards',sortedOverlappingCards
cardNumber = 0
#print 'number Of OverlappingCards', len(sortedOverlappingCards)
for cards in claimCards:
	if cards[0] != sortedOverlappingCards[cardNumber][0]:
		print 'Finished',time.strftime('%X %x %Z')
		print 'Unmatched card has no overlap, number', sortedOverlappingCards[cardNumber][0]-1
		exit();
	cardNumber += 1
	#print 'cards',cards
	#print 'cardNumber',cardNumber
	if cardNumber >= len(sortedOverlappingCards):
		print 'Finished',time.strftime('%X %x %Z')
		print 'Unmatched cards is the last card, number',cardNumber+1
		exit()

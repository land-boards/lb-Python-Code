# Pt1-AoCDay3.py
# 2018 Advent of Code
# Day 3
# Part 1
# https://adventofcode.com/2018/day/3

import time

"""
--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:
  - The number of inches between the left edge of the fabric and the left edge of the rectangle.
  - The number of inches between the top edge of the fabric and the top edge of the rectangle.
  - The width of the rectangle in inches.
  - The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:
...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

Visually, these claim the following areas:
........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?

Your puzzle answer was 117948.

[558, 359, 635, 380, 652], 
[559, 720, 943, 745, 958], 
[560, 921, 56, 943, 82], 
[561, 331, 37, 342, 51], 
[562, 417, 484, 445, 497], 
[563, 648, 30, 673, 52], 
[564, 392, 301, 413, 318], 
[565, 562, 763, 574, 773], 
[566, 460, 608, 482, 621], 
[568, 499, 532, 510, 560], 
[569, 7, 29, 13, 39], [570, 690,
 317, 701, 331], [571, 769, 954, 778, 973], [572, 29, 947, 54, 973], [573, 206,
815, 223, 830], [574, 314, 279, 329, 307], [575, 471, 449, 493, 469], [576, 49,
920, 67, 947], [577, 202, 396, 230, 405], [578, 241, 571, 261, 596], [579, 596,
129, 608, 156], [580, 457, 927, 470, 948], [581, 584, 915, 594, 934], [582, 417,
 458, 443, 476], [583, 721, 311, 742, 331], [584, 503, 21, 525, 48], [585, 826,
538, 854, 562], [586, 773, 512, 797, 523], [587, 479, 444, 491, 463], [588, 109,

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
	"""parseLine example line #1 @ 7,589: 24x11
	:returns: [startX,startY,endX,endY]
	"""
#	print 'parsing',claimCardRaw
	parseCharColumn = 0
	if claimCardRaw[parseCharColumn] != '#':
		print 'first character in the row should be pound'
		cardRawValue = [-1,0,0,0,0]
#	else:
#		print 'got a pound'
	parseCharColumn += 1
	accumCardNumber = 0
	while claimCardRaw[parseCharColumn] != ' ':
		currentDigit = ord(claimCardRaw[parseCharColumn]) - ord('0')
		accumCardNumber = accumCardNumber * 10
		accumCardNumber += currentDigit
		parseCharColumn += 1
#	print 'Card number',accumCardNumber
	parseCharColumn += 1
	if claimCardRaw[parseCharColumn] != '@':
		print 'character should be asterisk'
		cardRawValue = [-1,0,0,0,0]
	parseCharColumn += 1
	parseCharColumn += 1
	accumStartX = 0
	while claimCardRaw[parseCharColumn] != ',':
		currentDigit = ord(claimCardRaw[parseCharColumn]) - ord('0')
		accumStartX = accumStartX * 10
		accumStartX += currentDigit
		parseCharColumn += 1
#	print 'startX',accumStartX
	parseCharColumn += 1
	accumStartY = 0
	while claimCardRaw[parseCharColumn] != ':':
		currentDigit = ord(claimCardRaw[parseCharColumn]) - ord('0')
		accumStartY = accumStartY * 10
		accumStartY += currentDigit
		parseCharColumn += 1
#	print 'startY',accumStartY
	parseCharColumn += 1
	parseCharColumn += 1
	accumSizeX = 0
	while claimCardRaw[parseCharColumn] != 'x':
		currentDigit = ord(claimCardRaw[parseCharColumn]) - ord('0')
		accumSizeX = accumSizeX * 10
		accumSizeX += currentDigit
		parseCharColumn += 1
#	print 'sizeX',accumSizeX
	parseCharColumn += 1
	accumSizeY = 0
	while parseCharColumn < len(claimCardRaw):
		currentDigit = ord(claimCardRaw[parseCharColumn]) - ord('0')
		accumSizeY = accumSizeY * 10
		accumSizeY += currentDigit
		parseCharColumn += 1
#	print 'sizeY',accumSizeY
	listToReturn = []
	listToReturn.append(accumCardNumber)
	listToReturn.append(accumStartX)
	listToReturn.append(accumStartY)
	listToReturn.append(accumStartX + accumSizeX - 1)
	listToReturn.append(accumStartY + accumSizeY - 1)
#	print 'list',listToReturn
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
print 'Overlapping card count',overlappingCardCount
sortedOverlappingCards = sorted(overlappingCards, key = lambda errs: errs[0])		# sort by first column
print 'claimCards',claimCards
print 'sortedOverlappingCards',sortedOverlappingCards
cardNumber = 0
for cards in claimCards:
	if cards[0] != sortedOverlappingCards[cardNumber][0]:
		print 'Card number has no overlap', sortedOverlappingCards[cardNumber][0]-1
		exit();
	cardNumber += 1

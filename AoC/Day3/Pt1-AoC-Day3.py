# Pt1-AoCDay3.py
# 2018 Advent of Code
# Day 3
# Part 1

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

"""

def getOverlappingArea(card1,card2):
	"""getOverlappingArea
	"""
	startX = 0
	startY = 1
	endX = 2
	endY = 3
	x1 = card2[startX]
	x2 = card1[endX-1]
	y1 = card2[startY]
	y2 = card1[endY-1]
	return [x1,y1,x2,y2]

def isPointInRectangle(card,checkX,checkY):
	"""isPointInRectangle
	[1, 2, 4, 5] x, y = 3 , 1
	"""
	print 'checking card',card,'x, y =',checkX,',',checkY
	boxStartX = card[0]
	boxStartY = card[1]
	boxEndX = card[2]
	boxEndY = card[3]
	if (checkX >= boxStartX) and (checkX <= boxEndX):
		if (checkY >= boxStartY) and (checkY <= boxEndY):
			print 'point',checkX,checkY,' is in box',card
			return True
	return False

def checkOverlap(card1,card2):
	"""checkOverlap - Check the two cards for overlap
	cardX format [cardNumber,startX,startY,endX,endY]
	
	Example which overlaps
		card1 = [1, 1, 3, 4, 6]
		card2 = [2, 3, 1, 6, 4]
	
	:returns: True if the cards overlap, False if there's no overlap
	"""
	print 'checking card',card1,'vs card',card2
	if isPointInRectangle(card1,card2[0],card2[1]):
		print 'overlaps'
	if isPointInRectangle(card1,card2[2],card2[3]):
		print 'overlaps'
	if isPointInRectangle(card2,card1[0],card1[1]):
		print 'overlaps'
	if isPointInRectangle(card2,card1[2],card1[3]):
		print 'overlaps'
	print 'does not overlap'
	return False
	
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
#	listToReturn.append(accumCardNumber)
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
	cardStartX = checkingCard[1]
	cardStartY = checkingCard[2]
	cardEndX = checkingCard[3]
	cardEndY = checkingCard[4]
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
with open('input2.txt', 'r') as filehandle:  
	for line in filehandle:
		claimCards.append(parseLine(line.strip('\n\r')))

print 'claimCards',claimCards

overlappingCards = []
overlappingCardCount = 0
overlappingAreas = []
cardNumber2 = 0
print 'Getting list of overlapping areas',time.strftime('%X %x %Z')
for card1 in claimCards:
	cardNumber2 += 1
	for card2 in claimCards[cardNumber2:]:
		if checkOverlap(card1,card2):
			print 'Card 1',card1
			print 'Card 2',card2
			if card1[0] not in overlappingCards:
				overlappingCards.append(card1)
				overlappingCardCount += 1
			overlappingArea = getOverlappingArea(card1,card2)
			overlappingAreas.append(overlappingArea)
			
		cardNumber2 != 1
print 'Overlapping card count',overlappingCardCount
print '\nList of overlapping cards',overlappingCards
print '\nList of overlapping areas',overlappingAreas

# Cycle through all 1000x1000 locations to count how many times each cell is in a list

print 'Starting matrix check',time.strftime('%X %x %Z')
totalCellsWithMoreThanOne = 0
yValue = 0
while yValue < 100:
	print '.',
	xValue = 0
	while xValue < 100:
		cardCountInArea = 0
		for checkingCard in overlappingCards:
			print 'checkingCard',checkingCard
			if isCardInArea(xValue,yValue,checkingCard):
				cardCountInArea += 1
		if cardCountInArea > 1:
			totalCellsWithMoreThanOne += 1
		xValue += 1
	yValue += 1
print '\nEnded',time.strftime('%X %x %Z')
print 'Total Cells With More Than One', totalCellsWithMoreThanOne

# Pt1-AoCDay3.py
# 2018 Advent of Code
# Day 3
# Part 1

def getOverlappingArea(card1,card2):
	startX = 1
	startY = 2
	endX = 3
	endY = 4
	x1 = card2[startX]
	x2 = card1[endX]
	y1 = card2[startY]
	y2 = card1[endY]

def checkOverlap(card1,card2):
	"""checkOverlap - Check the two cards for overlap
	cardX format [cardNumber,startX,startY,endX,endY]
	:returns: True if the cards overlap, False if there's no overlap
	"""
	startX = 1
	startY = 2
	endX = 3
	endY = 4
	#print 'Checking card overlap'
	if (card2[startX] > card1[startX] ) and (card2[startX] < card1[endX]):
		if (card2[startY] > card1[startY]) and (card2[startY] < card1[endY]):
			print 'overlaps'
			return True
#	print 'does not overlap'
	return False
	
def parseLine(claimCardRaw):
	"""parseLine example line #1 @ 7,589: 24x11
	:returns: [cardNumber,startX,startY,endX,endY]
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
	listToReturn.append(accumStartX + accumSizeX)
	listToReturn.append(accumStartY + accumSizeY)
#	print 'list',listToReturn
	return listToReturn

# define an empty list
claimCards = []
overlappingCards = 0	# Total of overlapping cards

# open file and read the content into an accumulated sum
with open('input.txt', 'r') as filehandle:  
	for line in filehandle:
		claimCards.append(parseLine(line.strip('\n\r')))

#print claimCards

overlappingCards = []
overlappingCardCount = 0
overlappingAreas = []
cardNumber2 = 0
for card1 in claimCards:
	cardNumber2 += 1
	for card2 in claimCards[cardNumber2:]:
		if checkOverlap(card1,card2):
			overlappingCardCount += 1
			print 'Card 1',card1
			print 'Card 2',card2
			overlappingCards.append(card1)
			overlappingArea = getOverlappingArea(card1,card2)
			overlappingAreas.append(overlappingArea)
		cardNumber2 != 1
print 'Overlapping card count',overlappingCardCount
print 'List of overlapping cards',overlappingCards

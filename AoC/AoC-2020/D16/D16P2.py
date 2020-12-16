""" 

AoC 2020 D16 P2

"""

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings('input2.txt')

stateList = ['headerBlock','myTicketHeader','myTicketVal','blank1','nearby','ticketsList','done']
state = 0
rulesList = []
myTicketList = []
nearbyTicketValuesList = []
nearbyTicketsList = []

for row in inList:
	# print(stateList[state])
	if stateList[state] == 'headerBlock':
		if row == '':
			state += 1
		else:
			ruleName = row[0:row.find(':')]
			#print('field name =',ruleName)
			restOfRule = row[row.find(':')+2:]
			restOfRule = restOfRule.replace(' ',',')
			restOfRule = restOfRule.replace('-',',')
			restOfRule = restOfRule.replace('or',',')
			ruleSplit = restOfRule.split(',')
			ruleLine = []
			ruleLine.append(ruleName)
			ruleLine.append(int(ruleSplit[0]))
			ruleLine.append(int(ruleSplit[1]))
			ruleLine.append(int(ruleSplit[4]))
			ruleLine.append(int(ruleSplit[5]))
			rulesList.append(ruleLine)
	elif stateList[state] == 'myTicketHeader':
		if row != 'your ticket:':
			assert False,'Your ticket missing'
		state += 1
	elif stateList[state] == 'myTicketVal':
		ruleSplit = row.split(',')
		# print('myTicketVal - ruleSplit',ruleSplit)
		for ticketString in ruleSplit:
			myTicketList.append(int(ticketString))
		state += 1
	elif stateList[state] == 'blank1':
		if row != '':
			assert False,'blank1 error'
		state += 1		
	elif stateList[state] == 'nearby':
		if row != 'nearby tickets:':
			assert False,'Your ticket missing'
		state += 1
	elif stateList[state] == 'ticketsList':
		ruleSplit = row.split(',')
		# print('myTicketVal - ruleSplit',ruleSplit)
		for ticketString in ruleSplit:
			nearbyTicketValuesList.append(int(ticketString))
			line = []
		for item in ruleSplit:
			line.append(int(item))
		nearbyTicketsList.append(line)

# print('rulesList',rulesList)
# print('myTicketList -',myTicket)List)
# print('nearbyTicketValuesList -',nearbyTicketValuesList)
# print('nearbyTicketsList',nearbyTicketsList)

goodTicketCount = 0
badTicketCount = 0

# rulesList [['class', 1, 3, 5, 7], ['row', 6, 11, 33, 44], ['seat', 13, 40, 45, 50]]
# nearbyTicketValuesList [7, 3, 47, 40, 4, 50, 55, 2, 20, 38, 6, 12]
# rangesList [[1, 3], [5, 7], [6, 11], [33, 44], [13, 40], [45, 50]]
rangesList = []
for rule in rulesList:
	rangesLine = []
	rangesLine.append(rule[1])
	rangesLine.append(rule[2])
	rangesList.append(rangesLine)
	rangesLine = []
	rangesLine.append(rule[3])
	rangesLine.append(rule[4])
	rangesList.append(rangesLine)
#print('rangesList',rangesList)
badTicketSum = 0

goodValues = []
goodTickets = []

# goodValues [7, 3, 47, 40, 50, 2, 20, 38, 6]
for nearbyTicket in nearbyTicketsList:
	ticketAllGood = True
	for ticketVal in nearbyTicket:
		ticketGood = False
		for range in rangesList:
			if range[0] <= ticketVal <= range[1]:
				ticketGood = True
		if not ticketGood:
			badTicketSum += ticketVal
			ticketAllGood = False
		else:
			goodValues.append(ticketVal)
	if ticketAllGood:
		goodTickets.append(nearbyTicket)
			
#print('goodValues',goodValues)
# print('badTicketSum',badTicketSum)

goodTickets = [[3, 9, 18], [15, 1, 5], [5, 14, 9]]
# print('goodTickets',goodTickets)
# print('goodTickets[0] =',goodTickets[0])
recLen = len(goodTickets[0])
print('len goodTickets[0] =',recLen)

ticketFieldValuesMinMaxRange = []
fieldOff = 0
while fieldOff < recLen:
	valMin = goodTickets[0][fieldOff]
	valMax = goodTickets[0][fieldOff]
	valPair = []
	valPair.append(valMin)
	valPair.append(valMax)
	ticketFieldValuesMinMaxRange.append(valPair)
	fieldOff += 1

# ticketFieldValuesMinMaxRange [[3, 3], [9, 9], [18, 18]]
print('ticketFieldValuesMinMaxRange',ticketFieldValuesMinMaxRange)	
# goodTickets [[3, 9, 18], [15, 1, 5], [5, 14, 9]]
print('goodTickets',goodTickets)

for goodTicket in goodTickets:
	print('goodTicket',goodTicket[1:])
	for ticketFieldValues in ticketFieldValuesMinMaxRange:
		print('ticketFieldValues',ticketFieldValues)
		for ticketField in goodTicket:
			print('ticketField',ticketField)
			if ticketField < ticketFieldValues[0]:
				ticketFieldValues[0] = ticketField
			elif ticketField > ticketFieldValues[1]:
				ticketFieldValues[1] = ticketField
	assert False,'stopped'
print('ticketFieldValuesMinMaxRange',ticketFieldValuesMinMaxRange)

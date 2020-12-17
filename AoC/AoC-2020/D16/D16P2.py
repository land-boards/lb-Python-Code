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

inList = readFileToListOfStrings('input.txt')

stateList = ['headerBlock','myTicketHeader','myTicketVal','blank1','nearby','ticketsList','done']
state = 0
rulesList = []
myTicketList = []
nearbyTicketValuesList = []
nearbyTicketsList = []

for row in inList:
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
		for myRange in rangesList:
			if myRange[0] <= ticketVal <= myRange[1]:
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

# goodTickets = [[3, 9, 18], [15, 1, 5], [5, 14, 9]]
recLen = len(goodTickets[0])

ticketFieldValuesRange = []
fieldOff = 0
while fieldOff < recLen:
	ticketFieldValuesRange.append([goodTickets[0][fieldOff]])
	fieldOff += 1

# ticketFieldValuesRange [[3, 3], [9, 9], [18, 18]]
# goodTickets = [[3, 9, 18], [15, 1, 5], [5, 14, 9]]

# goodTickets [[3, 9, 18], [15, 1, 5], [5, 14, 9]]
# should make [[3,15,5],[9,1,14],[18,5,9]]
print('ticketFieldValuesRange',ticketFieldValuesRange)
for goodTicket in goodTickets[1:]:
	#print('goodTicket',goodTicket)
	numRecs = len(ticketFieldValuesRange)
	for recNum in range(numRecs):
		#print('goodTicket[recNum]',goodTicket[recNum])
		ticketFieldValuesRange[recNum].append(goodTicket[recNum])
# ticketFieldValuesRange [[3, 15, 5], [9, 1, 14], [18, 5, 9]]
#print('ticketFieldValuesRange',ticketFieldValuesRange)
# rulesList [['class', 0, 1, 4, 19], ['row', 0, 5, 8, 19], ['seat', 0, 13, 16, 19]]
#print('rulesList',rulesList)

valsOffset = 0
departuresList = []
for ticketVals in ticketFieldValuesRange:
	print('ticketVals valsOffset',valsOffset)
	ruleNum = 0
	for rule in rulesList:
		matchedAll = True
		#print('rule',ruleNum,rule)
		for ticket in ticketVals:
			#print('ticket',ticket)
			if (rule[1] <= ticket <= rule[2]) or (rule[3] <= ticket <= rule[4]):
				pass
			else:
				matchedAll = False
				#print('not matched')
		ruleNum += 1
		if matchedAll and ('depart' in rule[0]):
			#print('ticketVals valsOffset',valsOffset)
			print('matched',ruleNum,rule[0])
	valsOffset += 1
	
# [1] ticketVals valsOffset 19 = matched 4 departure track (107)
# [2] ticketVals valsOffset 11 = matched 5 departure date (179)
# [3] ticketVals valsOffset 13 = matched 6 departure time (89)
# [4] ticketVals valsOffset 2 = matched 1 departure location (83)
# [5] ticketVals valsOffset 4 = matched 2 departure station (109)
# [6] ticketVals valsOffset 0 = matched 3 departure platform (103)
# 1588432009897 = too low
# or 
# [6] ticketVals valsOffset 1 = matched 3 departure platform (197)
# or 
# ticketVals valsOffset 12 = matched 3 departure platform
# [6] ticketVals valsOffset 14 =  matched 3 departure platform
#
# 3038068989803 = too low
# product = 

# myTicketList [11, 12, 13]
# print('myTicketList',myTicketList)

for offset in range(len(myTicketList)):
	print('myTicketList',offset,myTicketList[offset])

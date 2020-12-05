# D05P2
# 522

def readFileOfStringsToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	return inList

#inList = ['BBFFBFBLRR','BFFFFBFRRR']
#print(inList)
inList = readFileOfStringsToList()
maxSeat = 0
seatList = []
for line in inList:
	seatVal = 0
	seatBit = 512
	for charVal in line:
		if (charVal == 'B') or (charVal == 'R'):
			seatVal += seatBit
		seatBit >>= 1
	seatList.append(seatVal)
seatList.sort()
firstSeat = seatList[0]
lastSeat = seatList[-1]
print('firstSeat',firstSeat)
print('lastSeat',lastSeat)
for seatNum in range(firstSeat,lastSeat):
	if seatNum not in seatList:
		print('open seat',seatNum)

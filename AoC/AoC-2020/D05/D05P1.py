# D05P1

def readFileOfStringsToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	return inList

inList = readFileOfStringsToList()
#inList = ['BBFFBFBLRR','BFFFFBFRRR']
#print(inList)
# 'BBFBBFFLLL'
#  6310000
#  4268421  
maxSeat = 0
for line in inList:
	seatRowVal = 0
	seatColVal = 0
	rowVal = 64
	colVal = 4
	print(line)
	for charVal in line:
		#print('charVal',charVal)
		if charVal == 'B':
			#print('got B')
			seatRowVal += rowVal
			rowVal >>= 1
		elif charVal == 'F':
			rowVal >>= 1
		elif charVal == 'R':
			seatColVal += colVal
			colVal >>= 1
		elif charVal == 'L':
			colVal >>= 1
		else:
			assert False,'weird'
	seatVal = (8*seatRowVal) + (seatColVal)
	print('seatVal',seatVal)
	if seatVal > maxSeat:
		maxSeat = seatVal
print('maxSeat',maxSeat)

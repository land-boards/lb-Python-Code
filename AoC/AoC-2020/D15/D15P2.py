""" 

AoC 2020 D15 P1

"""

# startingNumbers = [0,3,6]
# numberOfTurns = 2020
startingNumbers = [5,2,8,16,18,0,1]
numberOfTurns = 30000000
turn = 0

numberSeries = []
foundNumbers = []
foundNumbersCount = 0

for num in startingNumbers:
	numberSeries.append(num)
	foundNumbers.append(num)
	foundNumbersCount += 1
	turn += 1

while turn < numberOfTurns:
	if turn % 1000 == 0:
		print(turn)
	if numberSeries[-1] not in foundNumbers[:-1]:
		numberSeries.append(0)
	else:
		foundOffset = 0
		lookingForLastNumber = numberSeries[-1]
		delta1 = 0
		delta2 = 0
		for searchNum in range(turn-1,-1,-1):
			#print('checking',searchNum)
			if numberSeries[searchNum] == lookingForLastNumber:
				delta2 = delta1
				delta1 = searchNum
			if delta2 != 0:
				deltasDelta = delta2-delta1
				numberSeries.append(deltasDelta)
				deltasOffset = 0
				foundDeltasDelta = False
				while deltasOffset < foundNumbersCount-1:
					if deltasDelta == foundNumbers[deltasOffset]:
						foundDeltasDelta = True
						break
					deltasOffset += 1
				if not foundDeltasDelta:
					foundNumbers.append(deltasDelta)
					foundNumbersCount += 1
				break
	turn += 1
	#print(numberSeries)
	#input('hit key')
print(numberSeries[-1])

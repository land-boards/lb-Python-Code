# D03P1.py
# 2021 Advent of Code
# Day 3
# Part 1

"""
"""
# readFileToListOfStrings
def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings('input.txt')
print(inList)
for row in inList:
	print(row)
numberOfBits = len(inList[0])
print("numberOfBits",numberOfBits)
zeroBitsCount = []
oneBitsCount = []
for bitNum in range(numberOfBits):
	onesCount = 0
	zerosCount = 0
	for row in inList:
		if row[bitNum] == '1':
			onesCount += 1
		else:
			zerosCount += 1
	zeroBitsCount.append(zerosCount)
	oneBitsCount.append(onesCount)
print("zeroBitsCount",zeroBitsCount)
print("oneBitsCount",oneBitsCount)
gammaRate = []
epsilonRate = []
for bitNum in range(numberOfBits):
	if zeroBitsCount[bitNum] > oneBitsCount[bitNum]:
		gammaRate.append('0')
		epsilonRate.append('1')
	else:
		gammaRate.append('1')
		epsilonRate.append('0')
print("gammaRate",gammaRate)
print("epsilonRate",epsilonRate)
gammaString = ''.join(gammaRate)
epsilonString = ''.join(epsilonRate)
print("gammaString",gammaString)
print("epsilonString",epsilonString)
gammaDecimal = int(gammaString,2)
epsilonDelta = int(epsilonString,2)
print("gammaDecimal",gammaDecimal)
print("epsilonDelta",epsilonDelta)
print("product",gammaDecimal*epsilonDelta)

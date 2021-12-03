# D03P2.py
# 2021 Advent of Code
# Day 3
# Part 2

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

inList = readFileToListOfStrings('input1.txt')
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
oxygenArray = []
for bitNum in range(numberOfBits):
	if zeroBitsCount[bitNum] > oneBitsCount[bitNum]:
		oxygenArray.append('0')
	elif zeroBitsCount[bitNum] < oneBitsCount[bitNum]:
		oxygenArray.append('1')
	else:
		oxygenArray.append('X')
print("oxygenArray",oxygenArray)

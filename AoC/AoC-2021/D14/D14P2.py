# D14P2.py
# 2021 Advent of Code
# Day 14
# Part 2
import time

# At start
startTime = time.time()

def readFileToList(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	return inList

def doInsertions(strVal,insertionsList):
	newString = ''
	for strPos in range(len(strVal)-1):
		newString += strVal[strPos]
		# strCheck = ''+ strVal[strPos] + strVal[strPos+1]
		# print("strCheck",strCheck)
		newString += insertionsList[strVal[strPos]+strVal[strPos+1]]
		# newString += strVal[strPos+1]
	# print("newString",newString)
	newString += strVal[-1]
	return newString

def makeEmptyPairsCountDict(insertions):
	emptyPairsCount = {}
	for row in insertions:
		emptyPairsCount[row] = 0
	return emptyPairsCount
	

loopCount = 40
inList = readFileToList("input.txt")
# print(inList)
initStr = inList[0]
# print(initStr)

insertions = {}
for row in inList[2:]:
	insVal = row.split(' -> ')
	insertions[insVal[0]] = [insVal[0][0]+insVal[1],insVal[1]+insVal[0][1]]
# print("insertions",insertions)

emptyPairsCount = makeEmptyPairsCountDict(insertions)
pairsCount = emptyPairsCount
	
for charOffset in range(len(initStr)-1):
	chars = initStr[charOffset] + initStr[charOffset+1]
	pairsCount[chars] += 1
# print("pairsCount",pairsCount)

count = 0
while count < loopCount:
	loopPairsCount = makeEmptyPairsCountDict(insertions)
	for item in pairsCount:
		# print("item",item,end = ' ')
		pairVals = insertions[item]
		# print("pairVals",pairVals)
		loopPairsCount[pairVals[0]] += pairsCount[item]
		loopPairsCount[pairVals[1]] += pairsCount[item]
	# print("loopPairsCount",loopPairsCount)
	pairsCount = loopPairsCount
	count += 1
# print("pairsCount",pairsCount)

lettersList = {}
for pair in pairsCount:
	# print(pair,pairsCount[pair])
	if pair[0] not in lettersList:
		lettersList[pair[0]] = pairsCount[pair]
	else:
		lettersList[pair[0]] += pairsCount[pair]
	if pair[1] not in lettersList:
		lettersList[pair[1]] = pairsCount[pair]
	else:
		lettersList[pair[1]] += pairsCount[pair]
# print("lettersList",lettersList)
numsList = []
for letter in lettersList:
	# print("Letter",letter," ", int(lettersList[letter]/2+0.5))
	numsList.append(int(lettersList[letter]/2+0.5))
# print("numsList",numsList)
maxVal = max(numsList)
minVal = min(numsList)
val = maxVal - minVal
print(val)
endTime = time.time()
print('time',endTime-startTime)

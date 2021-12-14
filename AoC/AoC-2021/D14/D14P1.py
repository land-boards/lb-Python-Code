# D14P1.py
# 2021 Advent of Code
# Day 14
# Part 1

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

inList = readFileToList("input1.txt")
# print(inList)
initStr = inList[0]
print(initStr)

insertions = {}
for row in inList[2:]:
	insVal = row.split(' -> ')
	insertions[insVal[0]] = insVal[1]
# print(insertions)


count = 1
maxCount = 18
newStr = initStr
stepCount = []
while count <= maxCount:
	charsCountDict = {}
	for charVal in initStr:
		if charVal not in charsCountDict:
			charsCountDict[charVal] = 0
		for charVal in insertions:
			print("charVal",charVal)
			if insertions[charVal] not in charsCountDict:
				charsCountDict[insertions[charVal]] = 0
		# print("charsCountDict (init)",charsCountDict)
	newStr = doInsertions(newStr,insertions)
	print("After step:",count,end = ' ')
	print("newStr",newStr)
	count += 1
	# print("len of newStr",len(newStr))
	maxVal = 0
	minVal = len(newStr)
	for charVal in charsCountDict:
		charsCountDict[charVal] = newStr.count(charVal)
		if charsCountDict[charVal] < minVal:
			minVal = charsCountDict[charVal]
		if charsCountDict[charVal] > maxVal:
			maxVal = charsCountDict[charVal]
	print("charsCountDict",charsCountDict)
	# print("minVal",minVal)
	# print("maxVal",maxVal)
	print("answer =",maxVal-minVal)
	dictLine = charsCountDict
	stepCount.append(dictLine)
for row in stepCount:
	print(row)
# print("newStr",newStr)
charsCountDict = {}
for charVal in newStr:
	if charVal not in charsCountDict:
		charsCountDict[charVal] = 0

maxVal = 0
minVal = len(newStr)
for charVal in charsCountDict:
	charsCountDict[charVal] = newStr.count(charVal)
	if charsCountDict[charVal] < minVal:
		minVal = charsCountDict[charVal]
	if charsCountDict[charVal] > maxVal:
		maxVal = charsCountDict[charVal]
print("charsCountDict",charsCountDict)
print("minVal",minVal)
print("maxVal",maxVal)
print("answer =",maxVal-minVal)

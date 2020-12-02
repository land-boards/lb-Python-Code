def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def parseList(listElements, splitChar, list):
	newList = []
	for line in list:
		splitInLine = line.split(splitChar)
		newLine = []
		for element in listElements:
			newLine.append(splitInLine[element])
		newList.append(newLine)
	return newList

inList = readFileToList()
parsedList = parseList([0,1,2],' ',inList)
print(parsedList)
newList2 = []
for listElement in parsedList:
	listRow = []
	minMax = listElement[0].split('-')
	minVal = int(minMax[0])
	maxVal = int(minMax[1])
	charTest = listElement[1][0]
	pwd = listElement[2]
	listRow.append(minVal)
	listRow.append(maxVal)
	listRow.append(charTest)
	listRow.append(pwd)
	newList2.append(listRow)
print(newList2)
count = 0
for row in newList2:
	countInRow = row[3].count(row[2])
	if (countInRow >= row[0]) and (countInRow <= row[1]):
		count += 1
print('count',count)


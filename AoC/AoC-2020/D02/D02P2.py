# 479 is too low

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

def formPwdList(parsedList):
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
	return newList2

inList = readFileToList()
parsedList = parseList([0,1,2],' ',inList)
print(parsedList)
count = 0
newList2 = formPwdList(parsedList)
for row in newList2:
	colToCheck1 = row[0] - 1
	colToCheck2 = row[1] - 1
	if ((row[3][colToCheck1] == row[2]) and (row[3][colToCheck2] != row[2])) or ((row[3][colToCheck1] != row[2]) and (row[3][colToCheck2] == row[2])):
		count += 1
print('count',count)


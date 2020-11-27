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

theList = parseList([1,5,3],' ',['acc bee czz dyy ekk fvg','58 36 24 59 63 71'])
print(theList)

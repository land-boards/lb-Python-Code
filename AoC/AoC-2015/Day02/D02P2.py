# 2015 Day 2, Part 2

#

def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inLine = inLine.split('x')
			inList.append(inLine)
	#print(inList)
	return inList

def min2Of3(listOfNums):
	newList = sorted(listOfNums)
	return [newList[0],newList[1]]

inList = readFileToList()
# print(inList)
ribbonLengthTotal = 0
for package in inList:
	length = int(package[0])
	width = int(package[1])
	height = int(package[2])
	shortSides=min2Of3([length,width,height])
	ribbonLength = (2*shortSides[0]) + (2*shortSides[1]) + (length*width*height)
	ribbonLengthTotal += ribbonLength
print("ribbonLengthTotal",ribbonLengthTotal)

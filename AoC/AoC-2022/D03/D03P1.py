""" 
D03P1

"""

fileName = 'input.txt'
invList = []
lineCount = 0
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		#print(inLine)
		if inLine != '':
			newLine = []
			halfLineLen = int(len(inLine)/2)
			newLine.append(inLine[0:halfLineLen])
			newLine.append(inLine[halfLineLen:])
			#print(newLine)
			invList.append(newLine)
			lineCount += 1
print(lineCount)
#print(invList)
commonItems = []
for sacks in invList:
	firstSack = sacks[0]
	secondSack = sacks[1]
	print(firstSack,secondSack, end = ' ')
	commonItem = ''
	for item in firstSack:
		if item in secondSack:
			if commonItem == '':
				commonItem = item
				commonItems.append(commonItem)
	print(commonItems)
sum = 0
for item in commonItems:
	val = 0
	if 'a' <= item <= 'z':
		val = ord(item) - ord('a') + 1
	elif 'A' <= item <= 'Z':
		val = ord(item) - ord('A') + 27
	if val == 0:
		assert False,"Bad input"
	print(item,val)
	sum += val

print("sum",sum)
			
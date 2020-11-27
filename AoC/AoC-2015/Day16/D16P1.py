# 
# 

def readFileToList():
	with open('input.txt', 'r') as filehandle:  
		inLine = []
		for line in filehandle:
			inLineList = []
			inLineRow = line.split(' ')
			inLineList.append(int(inLineRow[1][:-1]))			# 0 - Sue number
			inLineList.append(inLineRow[2][0:-1])				# 1 - Item 1
			inLineList.append(int(inLineRow[3][:-1]))			# 2 - Qty Item 1
			inLineList.append(inLineRow[4][0:-1])				# 3 - Item 2
			inLineList.append(int(inLineRow[5].strip()[:-1]))		# 4 - Qty Item 2
			inLineList.append(inLineRow[6][0:-1])				# 5 - Item 3
			inLineList.append(int(inLineRow[7].strip()))			# 6 - Qty Item 3
			#print(inLineList)
			inLine.append(inLineList)
		return inLine

resultList = [['children',3],['cats',7],['samoyeds',2],['pomeranians',3],['akitas',0],['vizslas',0],['goldfish',5],['trees',3],['cars',2],['perfumes',1]]

def checkItemMatch(item,qty):
	for result in resultList:
		if (item == result[0]) and (qty == result[1]):
			return True
	return False

def checkRow(sueRow,inList):
	if not checkItemMatch(sueRow[1],sueRow[2]):
		return False
	if not checkItemMatch(sueRow[3],sueRow[4]):
		return False
	if not checkItemMatch(sueRow[5],sueRow[6]):
		return False
	return True

inList = readFileToList()
for sueRow in inList:
	if checkRow(sueRow,inList):
		print(sueRow)
	
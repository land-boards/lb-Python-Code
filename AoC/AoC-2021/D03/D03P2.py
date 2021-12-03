# D03P2.py
# 2021 Advent of Code
# Day 3
# Part 2

"""
readFileToListOfStrings()
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

def bitsCount(checkList,checkBit):
	onesCount = 0
	zerosCount = 0
	print("bitsCount: checkList",checkList)
	for valToCheck in checkList:
		if valToCheck[checkBit] == '1':
			onesCount += 1
		if valToCheck[checkBit] == '0':
			zerosCount += 1
	return onesCount, zerosCount

def removeVals(myList,bitChk,bitVal):
	retList = []
	for item in myList:
		# print("bitChk ",bitChk)
		# print("item[bitChk] ",item[bitChk])
		# print("bitVal ",bitVal)
		if item[bitChk] != bitVal:
			retList.append(item)
		else:
			print("removing ",item)
	print("removeVals: retList =",retList)
	return retList

inList = readFileToListOfStrings('input.txt')
print("inList",inList)
for row in inList:
	print(row)
numberOfBits = len(inList[0])
print("numberOfBits",numberOfBits)

oxyList = list(inList)
for checkBit in range(numberOfBits):
	onesCount, zerosCount = bitsCount(oxyList,checkBit)
	print("1s 0s =",onesCount, zerosCount)
	if len(oxyList) == 1:
		break
	if onesCount < zerosCount:
		oxyList = removeVals(oxyList,checkBit,'1')
	elif onesCount > zerosCount:
		oxyList = removeVals(oxyList,checkBit,'0')
	elif onesCount == zerosCount:
		oxyList = removeVals(oxyList,checkBit,'0')

co2List = list(inList)
for checkBit in range(numberOfBits):
	onesCount, zerosCount = bitsCount(co2List,checkBit)
	print("1s 0s =",onesCount, zerosCount)
	if len(co2List) == 1:
		break
	if onesCount < zerosCount:
		co2List = removeVals(co2List,checkBit,'0')
	elif onesCount > zerosCount:
		co2List = removeVals(co2List,checkBit,'1')
	elif onesCount == zerosCount:
		co2List = removeVals(co2List,checkBit,'1')

print("oxyList",oxyList)
print("co2List",co2List)
oxyNum = int(oxyList[0],2)
co2Num = int(co2List[0],2)
print("product",oxyNum*co2Num)

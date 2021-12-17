# DXXP1.py
# 2021 Advent of Code
# Day XX
# Part 1

import time

# At start
startTime = time.time()

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = ''
	with open(fileName, 'r') as filehandle:  
		for charIn in filehandle:
			if charIn != '\n':
				inList += charIn
	return inList

def toBin(hexVal):
	if hexVal == '0':
		return '0000'
	elif hexVal == '1':
		return '0001'
	elif hexVal == '2':
		return '0010'
	elif hexVal == '3':
		return '0011'
	elif hexVal == '4':
		return '0100'
	elif hexVal == '5':
		return '0101'
	elif hexVal == '6':
		return '0110'
	elif hexVal == '7':
		return '0111'
	elif hexVal == '8':
		return '1000'
	elif hexVal == '9':
		return '1001'
	elif hexVal == 'A':
		return '1010'
	elif hexVal == 'B':
		return '1011'
	elif hexVal == 'C':
		return '1100'
	elif hexVal == 'D':
		return '1101'
	elif hexVal == 'E':
		return '1110'
	elif hexVal == 'F':
		return '1111'
	else:
		print('toBin: Parse Error',hexVal)

def extractPacketHeader(binStr,stringOffset):
	vVal = binStr[stringOffset:stringOffset+3]
	tVal = binStr[stringOffset+3:stringOffset+6]
	stringOffset += 6
	print("\nPacket Header")
	print(" vVal",vVal)
	print(" tVal",tVal)
	return stringOffset,vVal,tVal
	
def printPacketVal(vVal,tVal,aVal,bVal,cVal):
	print("(v) Packet Version",vVal)
	print("(t) Packet Type   ",tVal)
	print("(L) Packet Length ",aVal)
	print("(b) Subpacket (1) ",bVal)
	print("(c) Subpacket (2) ",cVal)

def hexToBin(hexStr):
	binStr = ''
	for charVal in hexStr:
		if charVal != '\n':
			binStr += toBin(charVal)
	return binStr

def strToBin(literalValString):
	literalNum = 0
	for val in literalValString:
		literalNum = literalNum << 1
		if val == '1':
			literalNum += 1
	return literalNum

def parseLiteralPacket(binStr,stringOffset):
	print("binStr[stringOffset:]",binStr[stringOffset:])
	literalValString = ''
	aVal = binStr[stringOffset:stringOffset+5]
	print("aVal",aVal)
	if aVal[0] == '1':
		literalValString = aVal[1:]
	bVal = binStr[stringOffset+5:stringOffset+10]
	print("bVal",bVal)
	if bVal[1] == '1':
		literalValString += bVal[1:]
	cVal = binStr[stringOffset+10:stringOffset+15]
	print("cVal",cVal)
	literalValString += cVal[1:]
	print("literalValString",literalValString)
	stringOffset += 15
	literalNum = strToBin(literalValString)
	print("literalNum",literalNum)
	print("Pad ",end='')
	while ((stringOffset < len(binStr) and binStr[stringOffset] == '0')):
		print(binStr[stringOffset],end='')
		stringOffset += 1
	print()
	return stringOffset,literalNum

def parseOperatorPacket(binStr,tVal,stringOffset):
	print("\nOperator packet")
	print("  Type",tVal)
	if binStr[stringOffset] == '0':
		subPacketLengthStr = binStr[stringOffset+1:stringOffset+16]
		# print("  subPacketLengthStr",subPacketLengthStr)
		subPacketCount = strToBin(subPacketLengthStr)
		print("  subPacketCount",subPacketCount)
	stringOffset += subPacketCount
	return stringOffset

# inList = readFileToListOfStrings('input.txt')
# inList = 'D2FE28'
inList = '38006F45291200'
binStr = hexToBin(inList)

stringOffset = 0
while stringOffset < len(binStr):
	stringOffset,vVal,tVal = extractPacketHeader(binStr,stringOffset)
	if tVal == '100':
		stringOffset,literalNum = parseLiteralPacket(binStr,stringOffset)
	else:
		stringOffset = parseOperatorPacket(binStr,tVal,stringOffset)

endTime = time.time()
print('time',endTime-startTime)

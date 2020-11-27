# D10P1

def countDigits(strToCount):
	firstChar = strToCount[0]
	letterCount = 0
	for consLtrCnt in range(len(strToCount)):
		if strToCount[consLtrCnt] == firstChar:
			letterCount += 1
		else:
			return letterCount
	return letterCount
	

InputStr = '1113122113'

# loops = 5

# for loopCount in range(loops):
	# print("loopCounxt",loopCount)

loopCount = 40
while loopCount > 0:
	strPtr = 0
	newStr = ''
	while(strPtr < len(InputStr)):
		repCount = countDigits(InputStr[strPtr:])
#		print("count",repCount,"of",InputStr[strPtr])
		newStr += str(repCount)
		newStr += InputStr[strPtr]
		strPtr += repCount
	InputStr = newStr
#	print("InputStr",InputStr)
	loopCount -= 1

print("len",len(InputStr))
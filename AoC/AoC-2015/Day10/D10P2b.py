# D10P2
# Pass pointer to the list rather than slicing
# https://accidentallyquadratic.tumblr.com

InputStr = '1113122113'

def countDigits(strptr):
	firstChar = InputStr[strptr]
	letterCount = 0
	for consLtrCnt in range(strptr,len(InputStr)):
		if InputStr[consLtrCnt] == firstChar:
			letterCount += 1
		else:
			return letterCount
	return letterCount
	
loopCount = 50
while loopCount > 0:
	strPtr = 0
	newStr = ''
	#print(loopCount)
	while(strPtr < len(InputStr)):
		repCount = countDigits(strPtr)
		#print("count",repCount,"of",InputStr[strPtr])
		newStr += str(repCount)
		newStr += InputStr[strPtr]
		strPtr += repCount
	InputStr = newStr
#	print("InputStr",InputStr)
	loopCount -= 1
	print(loopCount,"len",len(InputStr))

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
	

InputStr = '1112'

# loops = 5

# for loopCount in range(loops):
	# print("loopCount",loopCount)

print(countDigits(InputStr))

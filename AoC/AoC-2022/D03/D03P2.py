""" 
D02P1

"""

def valOfChar(item):
	if 'a' <= item <= 'z':
		val = ord(item) - ord('a') + 1
	elif 'A' <= item <= 'Z':
		val = ord(item) - ord('A') + 27
	if val == 0:
		assert False,"Bad input"
	return val

fileName = 'input.txt'
invList = []
lineCount = 0
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		if inLine != '':
			invList.append(inLine)
			lineCount += 1
print(invList)
sumVals = 0
for elvesSet in range(0,len(invList),3):
	print("set")
	print(invList[elvesSet])
	print(invList[elvesSet+1])
	print(invList[elvesSet+2])
	badgeVal = ''
	for checkChar in invList[elvesSet]:
		if (checkChar in invList[elvesSet+1]) and (checkChar in invList[elvesSet+2]):
			if badgeVal == '':
				print(checkChar,valOfChar(checkChar))
				badgeVal = checkChar
				sumVals += valOfChar(checkChar)
print("Sum",sumVals)
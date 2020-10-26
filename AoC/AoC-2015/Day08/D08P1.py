#985 is too low
def readFileToList():
	inList = []
	with open('input1.txt', 'r', encoding='utf-8') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def countStorageSpaceForLine(line,reallyLongString):
	charCount = 0
	localStr = ''
	for charVal in line[1:-1]:
		# print(charVal,end='')
		charCount += 1
		localStr += charVal
	return(charCount,localStr)
	
inList = readFileToList()
#inList = ['""','"abc"','"aaa\"aaa"','"\x27"']
#print(inList)
count = 0
for line in inList:
	count += len(line)
print("count of total chars",count)
storageSpace = 0
reallyLongString = ''
for line in inList:
	pairOfThings = countStorageSpaceForLine(line,reallyLongString)
	print("pairOfThings",pairOfThings)
	storageSpace += pairOfThings[0]
	reallyLongString += pairOfThings[1]
print
print("reallyLongString",reallyLongString)
print("raw storageSpace",storageSpace)
compCount = 0
charToCheckOffset = 0
while charToCheckOffset < len(reallyLongString):
	print("Current char is :",reallyLongString[charToCheckOffset])
	if reallyLongString[charToCheckOffset] == '\\':
		print("Got backslash")
		if (reallyLongString[charToCheckOffset+1] == 'x'):
			print("Got x, Offset = 4")
			charToCheckOffset += 4
		elif reallyLongString[charToCheckOffset+1] == '\""':
			print("Got backslash Offset = 2")
			charToCheckOffset += 2
		elif reallyLongString[charToCheckOffset+1] == '\\"':
			print("Offset = 2")
			charToCheckOffset += 2
		else:
			charToCheckOffset += 1
	else:
		charToCheckOffset += 1
	compCount += 1
compCount -= 1
print("compCount",compCount)
print("Delta =",count-compCount)

#985 is too low
#1245 is too low
#1512 is too high
fileLen = 0
def readFileToList():
	global fileLen
	inList = []
	with open('input1.txt', 'r', encoding='utf-8') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
			fileLen += len(inLine)
			print("fileLen",fileLen)
	return inList

def countStorageSpaceForLine(line,reallyLongString):
	charCount = 0
	localStr = ''
	for charVal in line:
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
storeCount = 0
charToCheckOffset = 0
while charToCheckOffset < len(reallyLongString):
	print("Current char is :",reallyLongString[charToCheckOffset])
	if reallyLongString[charToCheckOffset] == '\\':
		print("Got backslash")
		if (reallyLongString[charToCheckOffset+1] == 'x'):
			print("Got x, Offset = 4")
			charToCheckOffset += 4
			storeCount += 1
		elif reallyLongString[charToCheckOffset+1] == '"':
			print("Got quote, offset = 2")
			charToCheckOffset += 2
			storeCount += 1
		elif reallyLongString[charToCheckOffset+1] == '\\"':
			print("Offset = 2")
			charToCheckOffset += 2
			storeCount += 1
		else:
			storeCount += 1
			charToCheckOffset += 2
	else:
		charToCheckOffset += 1
		storeCount += 1
# storeCount -= 1
print("storeCount",storeCount)
print("count",count)
print("fileLen",fileLen)
print("Delta =",count-storeCount)

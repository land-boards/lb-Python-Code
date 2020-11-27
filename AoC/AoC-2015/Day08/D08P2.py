# 

fileLen = 0
def readFileToList():
	global fileLen
	inList = []
	with open('input.txt', 'r', encoding='utf-8') as filehandle:  
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
#print(inList)
count = 0
for line in inList:
	count += len(line)
print("count of total chars",count)
storageSpace = 0
print("inList",inList)
outList = []
expandedSpace = 0
for line in inList:
	outLine = ''
	outLine += '"'
	expandedSpace += 1
	for inChar in line:
		if inChar == '"':
			outLine += '\\"'
			expandedSpace += 2
		elif inChar == '\\':
			outLine += '\\\\'
			expandedSpace += 2
		else:
			outLine += inChar
			expandedSpace += 1
		storageSpace += 1
	outLine += '"'
	expandedSpace += 1
	print("outLine",outLine)
print("storageSpace",storageSpace)
print("expandedSpace",expandedSpace)
print("expandedSpace-storageSpace",expandedSpace-storageSpace)


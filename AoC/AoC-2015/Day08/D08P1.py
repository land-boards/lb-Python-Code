#65535 is too hogh
def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def countStorageSpaceForLine(line):
	return 0
	
# inList = readFileToList()
inList = ['""','"abc"','"aaa\"aaa"','"\x27"']
print(inList)
count = 0
for line in inList:
	count += len(line)
print("count of total chars",count)
storageSpace = 0
for line in inList:
	storageSpace += countStorageSpaceForLine(line)
	
""" 
2020 D19 P1
"""

def readFileOfStringsToListOfLists(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inList.append(inLine)
	return inList

inList = readFileOfStringsToListOfLists('input.txt')
# print(inList)

top = []
strBody = []
# '2: 12 16 | 41 26'
for line in inList:
	if ':' in line:
		sp=line.split(' ')
		topLine = []
		topLine.append(int(line[0:line.find(':')]))
		newLine = line[line.find(':')+2:]
		newLine = newLine.replace('"','')
		newLineList = newLine.split(' ')
		topLine += newLineList
		top.append(topLine)
	elif line == '':
		pass
	else:
		strBody.append(line)

top.sort(key=lambda r:r[0])
print('top',top)
print('strBody',strBody)

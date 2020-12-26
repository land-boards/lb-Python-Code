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

# Program start
inList = readFileOfStringsToListOfLists('input.txt')
# print(inList)

top = []
strBody = []
# Input = '2: 12 16 | 41 26'
# Output = [2, [12, 16], [41, 26]]
for line in inList:
	if ':' in line:
		sp = line.split(' ')
		topLine = []
		topLine.append(int(line[0:line.find(':')]))
		newLine = line[line.find(':')+2:]
		newLine = newLine.replace('"','')
		newLineList = newLine.split(' ')
		newRow = []
		for item in newLineList:
			try:
				val = int(item)
				newRow.append(val)
				# print('was int')
			except:
				if item != '|':
					newRow.append(item)
					# print('not an int')
			if item == '|':
				topLine.append(newRow)
				newRow = []
		topLine.append(newRow)
		top.append(topLine)
	elif line == '':
		pass
	else:
		strBody.append(line)
top.sort(key=lambda r:r[0])
# for rule in top:
	# print(rule)
# assert False,'Done'

rulesList = []
for rule in top:
	if len(rule) == 2:
		rulesList.append(rule[1])
	else:
		newRule = []
		newRule.append(rule[1])
		newRule.append(rule[2])
		rulesList.append(newRule)
print('Rules')
for rule in rulesList:
	print(rule)

print('rulesList[7]',rulesList[7])
# print('strBody',strBody)

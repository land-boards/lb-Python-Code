""" 
D21P1
"""

# fileName="input1.txt"
fileName="input.txt"

inDir = {}
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		inLine = inLine.split(' ')
		# print(inLine)
		monkeyName = inLine[0][0:-1]
		if len(inLine) == 2:
			immed = int(inLine[1])
			inDir[monkeyName] = immed
		else:
			monkey1 = inLine[1]
			op = inLine[2]
			monkey2 = inLine[3]
			inDir[monkeyName] = [monkey1,op,monkey2]
print(inDir)
print (inDir['root'])
print (len(inDir['root']))
for item in inDir:
	print(item,inDir[item])
while isinstance(inDir['root'],list):
	for item in inDir:
		if isinstance(inDir[item],list):
			monkey1 = inDir[item][0]
			op = inDir[item][1]
			monkey2 = inDir[item][2]
			print('monkey1',monkey1,', op',op,', monkey1',monkey1)
			if (not isinstance(inDir[monkey1],list)) and (not isinstance(inDir[monkey2],list)):
				if op == '+':
					result = inDir[monkey1] + inDir[monkey2]
				elif op == '-':
					result = inDir[monkey1] - inDir[monkey2]
				elif op == '/':
					result = inDir[monkey1] / inDir[monkey2]
				elif op == '*':
					result = inDir[monkey1] * inDir[monkey2]
				inDir[item] = result
				print('solved',inDir[item])
			
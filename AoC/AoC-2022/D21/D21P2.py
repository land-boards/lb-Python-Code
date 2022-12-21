""" 
D21P2
"""

def isSolved(item):
	global inDir
	if not isinstance(inDir[item],list):
		return True
	return False
	
def doOp(val1,op,val2):
	if op == '+':
		result = val1 + val2
	elif op == '-':
		result = val1 - val2
	elif op == '/':
		result = val1 / val2
	elif op == '*':
		result = val1 * val2
	return int(result)
	
def isEqual(val1,val2):
	if val1 == val2:
		return True
	return False

# fileName="input1.txt"
fileName="input.txt"

inDir = {}
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		inLine = inLine.split(' ')
		monkeyName = inLine[0][0:-1]
		if len(inLine) == 2:
			immed = int(inLine[1])
			inDir[monkeyName] = immed
		else:
			monkey1 = inLine[1]
			op = inLine[2]
			monkey2 = inLine[3]
			inDir[monkeyName] = [monkey1,op,monkey2]

# inDir['humn'] = 3592056845086
inDir['humn'] = 3_592_056_845_086
keepRunning = True
while keepRunning:
	for item in inDir:
		if isinstance(inDir[item],list) and item != 'root':
			monkey1 = inDir[item][0]
			op = inDir[item][1]
			monkey2 = inDir[item][2]
			if (isSolved(monkey1)) and (isSolved(monkey2)):
				result = doOp(inDir[monkey1],op,inDir[monkey2])
				inDir[item] = int(result)
	ml = inDir['root']
	if (isSolved(inDir['root'][0])) and (isSolved(inDir['root'][2])):
		keepRunning = False
monkeyL = inDir['root']
print('monkeyL',monkeyL)
val1 = inDir[monkeyL[0]]
val2 = inDir[monkeyL[2]]
print("inDir['humn']",inDir['humn'],'val1',val1,'val2',val2,'diff',val1-val2)
if isEqual(val1,val2):
	print('Equal')
else:
	print('Not Equal')

""" 
D13P1


"""

fileName = 'input.txt'
# fileName = 'input1.txt'

# recursive comparison to descend into list
def comparePackets(a,b):
	# print('comparePackets:',a,b)
	if isinstance(a,int) and isinstance(b,list):
		a = [a]
	elif isinstance(a,list) and isinstance(b,int):
		b = [b]
	elif isinstance(a,int) and isinstance(b,int):
		if a < b:
			return 'LT'
		elif a == b:
			return 'EQ'
		return 'GT'
	if isinstance(a, list) and isinstance(b, list):
		i = 0
		while i < len(a) and i < len(b):
			x = comparePackets(a[i], b[i])
			if x == 'GT':
				return 'GT'
			if x == 'LT':
				return 'LT'

			i += 1

		if i == len(a):
			if len(a) == len(b):
				return 'EQ'
			return 'LT'  # a ended first
		return 'GT'

inList=[]
theList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		if inLine!='':
			theList.append(inLine.strip())
		else:
			# print('eval',eval(theList))
			inList.append(theList)
			theList=[]
		# print(inLine)
	inList.append(theList)
print('theList')
newList = []
# Use eval to translate input strings into valid Python objects
for line in inList:
	# print('line',line)
	# print('eval(line)',eval(line))
	lineList = []
	for object in line:
		print('object',object,'eval',eval(object))
		lineList.append(eval(object))
	newList.append(lineList)
print('newList')
sum = 0
index = 1
for line in newList:
	print(line)
	print('Pair',index, end=' ')
	val = comparePackets(line[0],line[1])
	print('val',val)
	if val == 'LT':
		sum += index
	index +=1
print('sum',sum)

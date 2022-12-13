""" 
D13P2


"""

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

fileName = 'input.txt'
# fileName = 'input1.txt'

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
# print('theList')
newList = []
# Use eval to translate input strings into valid Python objects
for line in inList:
	# print('line',line)
	lineList = []
	for object in line:
		# print('object',object,'eval',eval(object))
		lineList.append(eval(object))
	newList.append(lineList)
# print('newList')
index = 1
orderedList = []
for line in newList:
	# print(line)
	# print('Pair',index, end=' ')
	val = comparePackets(line[0],line[1])
	# print('val',val)
	if val == 'LT':
		orderedList.append(line[0])
		orderedList.append(line[1])
	else:
		orderedList.append(line[1])
		orderedList.append(line[0])
# print('orderedList(LT2)')
lt2List=[]
for item in orderedList:
	# print(item)
	val = comparePackets(item,[[2]])
	# print(val)
	if val == 'LT':
		lt2List.append(item)
# print('LT2')
# for item in lt2List:
	# print(item)
lt6List=[]
for item in orderedList:
	# print(item)
	val = comparePackets(item,[[6]])
	# print(val)
	if val == 'LT':
		lt6List.append(item)
# for item in lt6List:
	# print(item)
# print('len(lt2List)',len(lt2List)+1)
# print('len(lt6List)',len(lt6List)+2)
print('decoderKey',(len(lt2List)+1)*(len(lt6List)+2))

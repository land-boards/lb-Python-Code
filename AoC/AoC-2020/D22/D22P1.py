""" 

D22P1

"""

list1 = []
list2 = []

def readToLists(fileName):
	"""
	"""
	global list1
	global list2
	stateList = ['inWaitPlayer1','inList1','inWaitPlayer2','inList2']
	state = 'inWaitPlayer1'
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			line = line.strip()
			if state == 'inWaitPlayer1':
				# print('Playa 1')
				state = 'inList1'
			elif state == 'inList1':
				if line != '':
					list1.append(int(line.strip()))
				else:
					state = 'inWaitPlayer2'
			elif state == 'inWaitPlayer2':
				# print('Playa 2')
				state = 'inList2'
			elif state == 'inList2':
				list2.append(int(line.strip()))
	return

readToLists('input.txt')
# print('start list')
# print(list1)
# print(list2)

while (len(list1) != 0) and (len(list2) != 0):
	topCardPlaya1 = list1[0]
	topCardPlaya2 = list2[0]
	# print('comparing',topCardPlaya1,'to',topCardPlaya2)
	if topCardPlaya1 > topCardPlaya2:
		list1.append(topCardPlaya1)
		list1.append(topCardPlaya2)
		list1.pop(0)
		list2.pop(0)
		# print('Playa 1 wins')
	else:
		list2.append(topCardPlaya2)
		list2.append(topCardPlaya1)
		list1.pop(0)
		list2.pop(0)	
		# print('Playa 2 wins')
	# print('next list')
	# print(list1)
	# print(list2)

productSum = 0
if len(list1) != 0:
	print('Playa 1',list1)
	val = len(list1)
	for listItem in list1:
		productSum += val*listItem
		val -= 1
else:
	print('Playa 2',list2)
	val = len(list2)
	for listItem in list2:
		productSum += val*listItem
		val -= 1
	
print('productSum',productSum)

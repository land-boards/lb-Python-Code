my_dict = {}

myList = [5,2,8,16,18,0,1]
lastEntryCount = 30000000

listValCounter = 0
lastVal = 0

# Load seed values from myList
for listOffset in range(len(myList)):
	theNum = myList[listValCounter]
	if theNum not in my_dict:
		my_dict[theNum] = [listValCounter]
	else:
		my_dict[theNum].append(listValCounter)
	listValCounter += 1
	lastVal = theNum
print('my_dict',my_dict)
print('lastVal',lastVal)
#assert False,''

while listValCounter < lastEntryCount:
	if listValCounter & 0xffff == 0:
		print(listValCounter)
	# print('my_dict[lastVal]',my_dict[lastVal])
	if len(my_dict[lastVal]) == 1:
		my_dict[0].append(listValCounter)
		lastVal = 0
		# print('my_dict',my_dict)
		# print()
	elif len(my_dict[lastVal]) > 1:
		countList = my_dict[lastVal]
		lastVal = countList[-1]-countList[-2]
		if lastVal not in my_dict:
			my_dict[lastVal] = [listValCounter]
		else:
			my_dict[lastVal].append(listValCounter)
		# print('lastVal',lastVal)
		# print('my_dict',my_dict)
		# assert False,'done'
	listValCounter += 1
print('my_dict[lastVal]',my_dict[lastVal])
#print('my_dict',my_dict)
# assert False,'ended'		
print
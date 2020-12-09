with open('input.txt') as f:
	lines = f.read().splitlines()
print(lines)
print()

newList = []
for numStr in lines:
	newList.append(int(numStr))
print (newList)

for firstNum in newList:
	for secondNum in newList:
		if firstNum + secondNum == 2020:
			print('one of the numbers',firstNum)
			print('the other number',secondNum)
			result = firstNum * secondNum
			print('result',result)
			
			
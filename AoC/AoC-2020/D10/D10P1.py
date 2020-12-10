# D10P1.py
# 2020 Advent of Code
# Day 10
# Part 1

"""
"""

# open file and read the content into an accumulated sum
def readListOfInts():
	newList = []
	with open('input.txt', 'r') as filehandle:  
		for lineIn in filehandle:
			newList.append(int(lineIn.strip()))
	#print('newList',newList)
	return newList

adapterJoltages = readListOfInts()
#print('adapterJoltages',adapterJoltages)
adapterJoltages.sort()
print('adapterJoltages',adapterJoltages)
if adapterJoltages[0] == 1:
	countOfOnes = 1
	countOfThrees = 0
else:
	countOfOnes = 0
	countOfThrees = 1
for adapterOffset in range(0,len(adapterJoltages)-1):
	if (adapterJoltages[adapterOffset+1] - adapterJoltages[adapterOffset]) == 1:
		print('Diff of 1 from',adapterJoltages[adapterOffset],'to',adapterJoltages[adapterOffset+1])
		countOfOnes += 1
	if (adapterJoltages[adapterOffset+1] - adapterJoltages[adapterOffset]) == 3:
		print('Diff of 3 from',adapterJoltages[adapterOffset],'to',adapterJoltages[adapterOffset+1])
		countOfThrees += 1
countOfThrees += 1
print('countOfOnes',countOfOnes)
print('countOfThrees',countOfThrees)
print('product',countOfOnes*countOfThrees)
# D02P1.py
# 2021 Advent of Code
# Day 2
# Part 1

"""
"""

# readFileToListOfStrings
def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings('input.txt')
print(inList)
# for row in inList:
	# print(row)

xPos = 0
yPos = 0
zPos = 0

for row in inList:
	line = row.split()
	dirVal = line[0]
	numVal = int(line[1])
	print(dirVal,numVal)
	if dirVal == 'up':
		zPos -= numVal
	elif dirVal == 'down':
		zPos += numVal
	elif dirVal == 'forward':
		xPos += numVal
print('xPos',xPos)
print('yPos',yPos)
print('zPos',zPos)
print('product',xPos*zPos)


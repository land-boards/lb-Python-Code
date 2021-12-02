# D02P2.py
# 2021 Advent of Code
# Day 2
# Part 2

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
#inList = ['forward 5','down 5','forward 8','up 3']
print(inList)
# for row in inList:
	# print(row)

xPos = 0
yPos = 0
zPos = 0
aimVal = 0

for row in inList:
	line = row.split()
	dirVal = line[0]
	numVal = int(line[1])
	print(dirVal,numVal)
	if dirVal == 'up':
		aimVal -= numVal
	elif dirVal == 'down':
		aimVal += numVal
	elif dirVal == 'forward':
		xPos += numVal
		zPos += aimVal * numVal
print('xPos',xPos)
print('yPos',yPos)
print('zPos',zPos)
print('aimVal',aimVal)
print('product',xPos*zPos)

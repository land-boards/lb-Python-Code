""" 
D08P1

30373
25512
65332
33549
35390
"""

fileName = 'input.txt'
# fileName = 'input1.txt'

inList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		lineList=[]
		for inChar in inLine:
			lineList.append(int(inChar))
		inList.append(lineList)
print(inList)
xSize = len(inList[0])
ySize=len(inList)
highestCount = 0
# l-r,t-b
highList=[]
for scanX in range(xSize):
	maxHeight=-1
	for scanY in range(ySize):
		if inList[scanY][scanX] > maxHeight:
			maxHeight = inList[scanY][scanX]
			if (scanX,scanY) not in highList:
				highList.append((scanX,scanY))
			maxHeight = inList[scanY][scanX]

for scanX in range(xSize):
	maxHeight=-1
	for scanY in range(ySize-1,0,-1):
		if inList[scanY][scanX] > maxHeight:
			maxHeight = inList[scanY][scanX]
			if (scanX,scanY) not in highList:
				highList.append((scanX,scanY))
			maxHeight = inList[scanY][scanX]
# print('highList (vert)',highList)

for scanY in range(ySize):
	maxHeight=-1
	for scanX in range(xSize):
		if inList[scanY][scanX] > maxHeight:
			maxHeight = inList[scanY][scanX]
			if (scanX,scanY) not in highList:
				highList.append((scanX,scanY))
			maxHeight = inList[scanY][scanX]

for scanY in range(ySize-1,0,-1):
	maxHeight=-1
	for scanX in range(xSize-1,0,-1):
		if inList[scanY][scanX] > maxHeight:
			maxHeight = inList[scanY][scanX]
			if (scanX,scanY) not in highList:
				highList.append((scanX,scanY))
			maxHeight = inList[scanY][scanX]

print('highList',highList)
print('tree count',len(highList))

# 2015 Day 2, Part 1

#

with open('input.txt', 'r') as filehandle:  
	inList = []
	for line in filehandle:
		line = line.strip('\n')
		inLine = line.split('x')
		inList.append(inLine)
print(inList)
totalArea = 0
for package in inList:
	length = int(package[0])
	width = int(package[1])
	heigth = int(package[2])
	areaA = 2*length*width
	areaB = 2*width*heigth
	areaC = 2*heigth*length
	slack=min(areaA,areaB,areaC)/2
	packageArea= areaA+areaB+areaC+slack
	totalArea += packageArea
print("totalArea",totalArea)
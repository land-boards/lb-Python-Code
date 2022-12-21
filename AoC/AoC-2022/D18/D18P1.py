""" 
D18P1
"""

fileName="input.txt"
# fileName="input1.txt"

inList = []
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		inStrs = inLine.split(',')
		inInts=[]
		for str in inStrs:
			inInts.append(int(str))
		inList.append(inInts)
print(inList)
totalSurfaces = 6 * len(inList)
print('totalSurfaces',totalSurfaces)
# minDimX = inList[0][0]
# minDimY = inList[0][1]
# minDimZ = inList[0][2]
# maxDimX = inList[0][0]
# maxDimY = inList[0][1]
# maxDimZ = inList[0][2]
# for cube in inList:
	# if cube[0] < minDimX:
		# minDimX = cube[0]
	# if cube[1] < minDimY:
		# minDimY = cube[1]
	# if cube[2] < minDimZ:
		# minDimZ = cube[2]
	# if cube[0] > maxDimX:
		# maxDimX = cube[0]
	# if cube[1] > maxDimY:
		# maxDimY = cube[1]
	# if cube[2] > maxDimZ:
		# maxDimZ = cube[2]
# print('min xyz',minDimX,minDimY,minDimZ)
# print('max xyz',maxDimX,maxDimY,maxDimZ)
# for z in range(minDimZ,maxDimZ+1):
	# for y in range(minDimY,maxDimY+1):
		# for x in range(minDimX,maxDimX+1):
			# loc = [x,y,z]
touching = 0
adjList = [[-1,0,0],[1,0,0],[0,-1,0],[0,1,0],[0,0,-1],[0,0,1]]
for fromCube in inList:
	for dirToCheck in adjList:
		checkLoc = [fromCube[0]+dirToCheck[0],fromCube[1]+dirToCheck[1],fromCube[2]+dirToCheck[2]]
		if checkLoc in inList:
			touching += 1
print('touching',touching)
print('Not connected',totalSurfaces-touching)

""" 
D18P2
3336 is too high
2074 is right
"""

# fileName="input.txt"
fileName="input1.txt"

# adjList = [[-1,0,0],[1,0,0],[0,-1,0],[0,1,0],[0,0,-1],[0,0,1]]
def countNeighbors(loc):
	neighborCount = 0
	for neigborLoc in adjList:
		checkLoc = [loc[0]+neigborLoc[0],loc[1]+neigborLoc[1],loc[2]+neigborLoc[2]]
		if checkLoc in inList:
			neighborCount += 1
	return neighborCount

openCubes = []

def countOpens(loc):
	openFaces = 0
	for neigborLoc in adjList:
		checkLoc = [loc[0]+neigborLoc[0],loc[1]+neigborLoc[1],loc[2]+neigborLoc[2]]
		if checkLoc not in inList:
			if checkLoc not in emptyCubes:
				openFaces += 1
				if checkLoc not in openCubes:
					openCubes.append(checkLoc)
			# else:
				# print('countOpens: empty cube at',checkLoc)
	return openFaces

inList = []
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		inStrs = inLine.split(',')
		inInts=[]
		for str in inStrs:
			inInts.append(int(str))
		inList.append(inInts)
# print(inList)
cubeCount = len(inList)
print('cubeCount',cubeCount)
adjList = [[-1,0,0],[1,0,0],[0,-1,0],[0,1,0],[0,0,-1],[0,0,1]]
voidCube = []
for z in range(20):
	for y in range(20):
		for x in range(20):
			checkLoc = [x,y,z]
			if checkLoc not in inList:
				if countNeighbors(checkLoc) == 6:
					if checkLoc not in voidCube:
						voidCube.append(checkLoc)
# print('cubeCount',cubeCount)
print('len(voidCube)',len(voidCube))
# print('void cubes',voidCube)
print(len(voidCube)+cubeCount)

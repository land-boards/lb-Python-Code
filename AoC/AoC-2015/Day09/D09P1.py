# 201 is too high
# 198 too high
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

fileLen = 0
def readFileToList():
	global fileLen
	inList = []
	with open('input.txt', 'r', encoding='utf-8') as filehandle:  
		for line in filehandle:
			inLineStr = line.rstrip()
			inLineSplit = inLineStr.split(' ')
			inLine = []
			inLine.append(inLineSplit[0])
			inLine.append(inLineSplit[2])
			inLine.append(inLineSplit[4])
			inList.append(inLine)
			inLine = []
			inLine.append(inLineSplit[2])
			inLine.append(inLineSplit[0])
			inLine.append(inLineSplit[4])
			inList.append(inLine)
	return inList

def getIndexPlace(place,placeList):
#	print("place",place,end='')
#	print("placeList",placeList)
	for placeOffset in range(len(placeList)):
		if place == placeList[placeOffset]:
#			print('=',placeOffset)
			return placeOffset
	print("error")
			
inList = readFileToList()
#print("inList",inList)
# for row in inList:
	# print(row[0],'->',row[1],'[ label = ',row[2],']')
placeList = []
for path in inList:
	if path[0] not in placeList:
		placeList.append(path[0])
	if path[1] not in placeList:
		placeList.append(path[1])
print("placeList")
for i in range(len(placeList)):
	print(i,placeList[i])

distance_matrix = np.array([
    [   0, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
    [9999,    0, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
    [9999, 9999,    0, 9999, 9999, 9999, 9999, 9999, 9999],
    [9999, 9999, 9999,    0, 9999, 9999, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999,    0, 9999, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999,    0, 9999, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999,    0, 9999, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999,    0, 9999],
    [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999,    0],
])

print("inList",inList)
#
#print("placeList",placeList)
for pairInList in inList:
	y = getIndexPlace(pairInList[0],placeList)
	x = getIndexPlace(pairInList[1],placeList)
	dist = pairInList[2]
	distance_matrix[y+1][x+1] = int(dist)

print(distance_matrix)
permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
print(permutation, distance-(2*9999))

"""
Look at a particular location locX,locY and make a list of legal adjacent locations
Calling function can iterate over the list of offsets
minX,maxX and minY,maxY are the array bounds
includeDiags - Include diagonals in the list
Makes a list of [[y,x],...] pairs
"""

def makeLegalNeighboringValsList(locX,locY,minX,maxX,minY,maxY,includeDiags=True):
	legalNeighboringValsList = []
	# print("makeLegalNeighboringValsList: x,y",locX,locY)
	if includeDiags:
		offSetList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
	else:
		offSetList = [[-1,0],[0,-1],[0,1],[1,0]]
	#print("offSetList",offSetList)
	for offsetPair in offSetList:
		rowValPair = []
		if (((offsetPair[0] + locY) >= minY) and ((offsetPair[0] + locY) <= maxY)):
			if (((offsetPair[1] + locX) >= minX) and ((offsetPair[1] + locX) <= maxX)):
				rowValPair.append(offsetPair[0] + locY)
				rowValPair.append(offsetPair[1] + locX)
				legalNeighboringValsList.append(rowValPair)
	# print("makeLegalNeighboringValsList: legalNeighboringValsList",legalNeighboringValsList)
	return(legalNeighboringValsList)

# Test code
print("0,0 (w diags) ",makeLegalNeighboringValsList(0,0,0,9,0,9,True))
print("0,0 (no diags)",makeLegalNeighboringValsList(0,0,0,9,0,9,False))
print("1,1 (w diags) ",makeLegalNeighboringValsList(1,1,0,9,0,9))
print("9,9 (w diags) ",makeLegalNeighboringValsList(9,9,0,9,0,9))

# 0,0 (w diags)  [[0, 1], [1, 0], [1, 1]]
# 0,0 (no diags) [[0, 1], [1, 0]]
# 1,1 (w diags)  [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
# 9,9 (w diags)  [[8, 8], [8, 9], [9, 8]]

#Alternate method
def padArray(arrayIn,padChar):
	arrayOut = []
	arrayWidthPlusPad = len(arrayIn[0]) + 2
	arrayHeight = len(arrayIn)
	newRow = []
	for charVal in range(arrayWidthPlusPad):
		newRow.append(padChar)
	arrayOut.append(newRow)
	for row in arrayIn:
		newRow = []
		newRow.append(padChar)
		for charVal in row:
			newRow.append(charVal)
		newRow.append(padChar)
		arrayOut.append(newRow)
	newRow = []
	for charVal in range(arrayWidthPlusPad):
		newRow.append(padChar)
	arrayOut.append(newRow)
	return arrayOut	


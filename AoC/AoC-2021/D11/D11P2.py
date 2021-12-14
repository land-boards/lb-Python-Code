# D11P2.py
# 2021 Advent of Code
# Day 11
# Part 2

def readFileToList(inFileName):
	inList = []
	with open(inFileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.rstrip()
			inRow = []
			for charVal in inLine:
				inRow.append(int(charVal))
			inList.append(inRow)
	return inList

def printOctopusArray(inList):
	for rowOffset in range(len(inList)):
		for colOffset in range(len(inList[0])):
			print(inList[rowOffset][colOffset],end='')
		print()
	print()

def countFlashedVals(inList):
	count = 0
	for rowOffset in range(len(inList)):
		for colOffset in range(len(inList[0])):
			if inList[rowOffset][colOffset] == 0:
				count += 1
	return count
	
def incrementOctopusArray(inList):
	outList = list(inList)
	for rowOffset in range(len(outList)):
		for colOffset in range(len(outList[0])):
			outList[rowOffset][colOffset] += 1
	return outList
	
def makeLegalNeighboringValsList(locX,locY,minX,maxX,minY,maxY,includeDiags=True):
	# Look at a particular location and make a list of legal adjacent locations
	# Makes a list of [y,x] pairs
	legalNeighboringVasList = []
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
				legalNeighboringVasList.append(rowValPair)
	# print("makeLegalNeighboringValsList: legalNeighboringVasList",legalNeighboringVasList)
	return(legalNeighboringVasList)

def flashOctopusArray(inList):
	outList = list(inList)
	moreToFlash = True
	while (moreToFlash):
		moreToFlash = False
		for rowOffset in range(len(outList)):
			outRow = []
			for colOffset in range(len(outList[0])):
				if outList[rowOffset][colOffset] > 9:
					outList[rowOffset][colOffset] = 0
					validPositions = makeLegalNeighboringValsList(colOffset,rowOffset,0,len(outList[0])-1,0,len(outList)-1,True)
					for posYX in validPositions:
						if outList[posYX[0]][posYX[1]] != 0:
							outList[posYX[0]][posYX[1]] += 1
							moreToFlash = True
		# print("Here")
	return outList

def checkAllFlashed(inList):
	for rowOffset in range(len(inList)):
		for colOffset in range(len(inList[0])):
			if inList[rowOffset][colOffset] != 0:
				return False
	return True
	

# print("0,0",makeLegalNeighboringValsList(0,0,0,9,0,9,True))
# print("0,0",makeLegalNeighboringValsList(0,0,0,9,0,9,False))
# print("1,1",makeLegalNeighboringValsList(1,1,0,9,0,9))
# print("9,9",makeLegalNeighboringValsList(9,9,0,9,0,9))
# quit()

inList = readFileToList("input.txt")
allFlashed = False
stepCount = 0
while not allFlashed:
	print("stepCount",stepCount)
	printOctopusArray(inList)
	inList = incrementOctopusArray(inList)
	inList = flashOctopusArray(inList)
	if checkAllFlashed(inList):
		break
	stepCount += 1
print("Done at stepCount",stepCount+1)
printOctopusArray(inList)


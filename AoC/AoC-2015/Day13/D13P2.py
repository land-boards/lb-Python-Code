#618
import itertools

# Alice would lose 57 happiness units by sitting next to Bob.

def readFileToList():
	with open('input.txt', 'r') as filehandle:  
		inLine = []
		for line in filehandle:
			inLineList = []
			inLineRow = line.split(' ')
			inLineList.append(inLineRow[0])			# 0 - Alice
			if (inLineRow[2] == 'gain'):			# + gain
				inLineList.append(int(inLineRow[3]))
			else:									# lose
				inLineList.append(-1*int(inLineRow[3]))
			inLineList.append((inLineRow[10].strip())[:-1])		# 2 - Bob
			inLine.append(inLineList)
		return inLine

def makeListOfNames(inList):
	nameList = []
	for row in inList:
		if row[0] not in nameList:
			nameList.append(row[0])
		if row[2] not in nameList:
			nameList.append(row[2])
	return nameList

def evalNamePairVal(name1,name2,inList):
	for row in inList:
		if (row[0] == name1) and (row[2] == name2):
			#print(name1,name2,row[1])
			return row[1]
	assert False,"huh"

def computeHappinessScore(listOfNames,inList):
	happinessScore = 0
	for nameOffset in range(len(listOfNames)-1):
		happinessScore += evalNamePairVal(listOfNames[nameOffset],listOfNames[nameOffset+1],inList)
		happinessScore += evalNamePairVal(listOfNames[nameOffset+1],listOfNames[nameOffset],inList)
	happinessScore += evalNamePairVal(listOfNames[-1],listOfNames[0],inList)
	happinessScore += evalNamePairVal(listOfNames[0],listOfNames[-1],inList)
	return happinessScore

inList = readFileToList()
names = makeListOfNames(inList)

print(inList)
print(names)
namesLists = list(itertools.permutations(names))
#print(namesLists)
happinessValue = 0
for listOfNames in namesLists:
	happy = computeHappinessScore(listOfNames,inList)
	if happy > happinessValue:
		happinessValue = happy
print(happinessValue)

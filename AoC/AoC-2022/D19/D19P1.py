""" 
D19P1
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 3 ore and 7 clay. Each geode robot costs 4 ore and 11 obsidian.

"""

# fileName="input.txt"
fileName="input1.txt"

def readInList():
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip()
			inLine = inLine.replace('Blueprint ','')
			inLine = inLine.replace(': Each ore robot costs ',',')
			inLine = inLine.replace(' ore. Each clay robot costs ',',')
			inLine = inLine.replace(' ore. Each obsidian robot costs ',',')
			inLine = inLine.replace(' ore and ',',')
			inLine = inLine.replace(' clay. Each geode robot costs ',',')
			inLine = inLine.replace(' ore and ','')
			inLine = inLine.replace(' obsidian.','')
			newListStrs=inLine.split(',')
			newIntsList = []
			for i in newListStrs:
				newIntsList.append(int(i))
			inList.append(newIntsList)
	return inList
inList = readInList()
print(inList)

steps = 2
currentStep = 1
for blueprint in range(len(inList)):
	currentStep = 1
	currentOre = 0
	currentClay = 0
	currentObsidian = 0
	currentGeodes = 0
	currentOreRobots = 1
	currentClayRobots = 0
	currentObsidianRobots = 0
	currentGeodeRobots = 0
	print('inList[0]',inList[blueprint])
	blueprintNumber = inList[blueprint][0]
	oreRobotCost = inList[blueprint][1]
	clayRobotCost = inList[blueprint][2]
	obsidianRobotOreCost = inList[blueprint][3]
	obsidianRobotClayCost = inList[blueprint][4]
	geodeRobotOreCost = inList[blueprint][5]
	geodeRobotObsidianCost = inList[blueprint][6]
	print('Blueprint',blueprintNumber)
	print('Each ore robot costs',oreRobotCost,'ore')
	print('Each clay robot costs',clayRobotCost,'ore')
	print('Each obsidian robot costs',obsidianRobotOreCost,'ore and',obsidianRobotClayCost,'clay')
	print('Each geode robot costs',geodeRobotOreCost,'ore and',geodeRobotObsidianCost,'obsidian')
	while currentStep <= steps:
		print('currentStep',currentStep)
		# Can we build a Geode robot?
		if currentOre >= geodeRobotOreCost and geodeRobotObsidianCost >= currentObsidian:
			currentGeodeRobots += 1
			currentOre -= geodeRobotOreCost
			currentObsidian -= geodeRobotObsidianCost
		# Can we build an Obsidian robot?
		if currentOre >= obsidianRobotOreCost and currentClay > obsidianRobotClayCost:
			currentObsidianRobots += 1
			currentOre -= obsidianRobotOreCost
			currentClay -= obsidianRobotClayCost
		# Can we build a Clay Robot
		if currentOre >= clayRobotCost:
			currentClayRobots += 1
			currentOre -= clayRobotCost
		currentOre += 1
		currentStep += 1
	print('currentGeodes',currentGeodes)

	assert False
		



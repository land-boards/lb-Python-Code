""" 

2020 AoC Day 13 Part 1
1000109 too high

"""

import math

def readFileToListOfStrings(fileName):
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

inList = readFileToListOfStrings('input.txt')
bigNum = int(inList[0])
print(bigNum)
sched = inList[1].split(',')
print(sched)
reduxSched = []
for bus in sched:
	if bus != 'x':
		reduxSched.append(int(bus))
print(reduxSched)

currentTime = bigNum
noMatchAtTime = True
busNum = 0
while noMatchAtTime:
	for bus in reduxSched:
		#if float(int(currentTime/bus)) == (currentTime/bus):
		# print('fract',math.remainder(currentTime,bus))
		if math.remainder(currentTime,bus) == 0.0:
			noMatchAtTime = False
			busNum = bus
	currentTime += 1
currentTime-=1
print('time bus leaves',currentTime)
print('bus num',busNum)
deltaTime = currentTime-bigNum
print('delta time',deltaTime)
result = deltaTime * busNum
print('timestamp',result)


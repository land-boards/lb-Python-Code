# D20P1

import itertools

presentAtHouseCount = []
for elfNumber in itertools.count(1):
	#print('elfNumber',elfNumber)
	presentAtHouseCount.append(elfNumber*10)
	for elf in range(elfNumber-1,0,-1):
		#print('checking elf',elf,'against house number',elfNumber)
		if elfNumber % elf == 0:
			#print('elf',elf,'is modulo 0 at house',elfNumber)
			presentAtHouseCount[elfNumber-1] += elf * 10
			if presentAtHouseCount[elfNumber-1] >= 33100000:
				break
print(presentAtHouseCount)
print(house)

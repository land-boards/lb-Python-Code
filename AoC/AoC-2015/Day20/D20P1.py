# D20P1

import itertools

DEBUG_PRINT = True
DEBUG_PRINT = False
def debugPrint(thingToPrint):
	if DEBUG_PRINT:
		print(thingToPrint)

presentAtHouseCount = 0
maxCount = 0
for elfNumber in itertools.count(776000,10):
	#debugPrint('elfNumber' + str(elfNumber))
	presentAtHouseCount = elfNumber * 10
	for elf in range(elfNumber-1,0,-1):
		#debugPrint('checking elf' + str(elf) + 'against house number ' + str(elfNumber))
		if elfNumber % elf == 0:
			#debugPrint('elf'+ str(elf) +'is modulo 0 at house ' + str(elfNumber))
			presentAtHouseCount += elf * 10
	if presentAtHouseCount >= 33100000:
#	if presentAtHouseCount >= 130:
		break
	if presentAtHouseCount > maxCount:
		maxCount = presentAtHouseCount
	if (elfNumber % 100) == 0:
		print(elfNumber,maxCount)
		maxCount = 0
	
print(elfNumber,presentAtHouseCount)
# print(house)

import time
startTime = time.time()
loop1Val = 13233401
loop2Val = 6552760
# loop1Val = 5764801
# loop2Val = 17807724
modVal = 20201227
loopCount = 1
matchCount1 = 0
matchCount2 = 0
loopCount = 1
val = 7
currentVal = 1
found1 = False
found2 = False
while (not found1) or (not found2):
	#print('loopCount',loopCount,'currentVal',currentVal)
	currentVal = (val * currentVal) % modVal
	if currentVal == loop1Val:
		matchCount1 = loopCount
		found1 = True
		print('found ',loop1Val,' at loopCount',loopCount)
	elif currentVal == loop2Val:
		matchCount2 = loopCount
		found2 = True
		print('found ',loop2Val,' at loopCount',loopCount)
	loopCount += 1
print('matchCount1',matchCount1)
print('matchCount2',matchCount2)
#
val = loop2Val
currentVal = 1
loopCount = 1
while loopCount != matchCount1+1:
	currentVal = (val * currentVal) % modVal
	loopCount += 1
print('loopCount',loopCount,'currentVal',currentVal)
endTime = time.time()
print('time',endTime-startTime)

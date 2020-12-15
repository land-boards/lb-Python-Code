""" 

AoC 2020 D15 P1

"""

startingNumbers = [0,3,6]
#startingNumbers = [5,2,8,16,18,0,1]
#numberOfTurns = 30000000
numberOfTurns = 2020
turn = 0

nums = []

for num in startingNumbers:
	nums.append(num)
	turn += 1

delta1 = 0
delta2 = 0
while turn < numberOfTurns:
	if nums[-1] not in nums[0:-1]:
		nums.append(0)
		turn += 1
	else:
		foundOffset = 0
		lookingForLastNumber = nums[-1]
		whenSpoken = []
		for searchNum in range(turn):
			#print('checking',searchNum)
			if nums[searchNum] == lookingForLastNumber:
				delta2 = delta1
				delta1 = searchNum
		#print('whenSpoken',whenSpoken)
		nums.append(delta1-delta2)
		turn += 1
	#input('hit key')
print(nums)

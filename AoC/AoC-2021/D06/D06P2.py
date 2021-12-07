# D06P1.py
# 2021 Advent of Code
# Day 6
# Part 2

import time

# At start
startTime = time.time()

inList = [5,3,2,2,1,1,4,1,5,5,1,3,1,5,1,2,1,4,1,2,1,2,1,4,2,4,1,5,1,3,5,4,3,3,1,4,1,3,4,4,1,5,4,3,3,2,5,1,1,3,1,4,3,2,2,3,1,3,1,3,1,5,3,5,1,3,1,4,2,1,4,1,5,5,5,2,4,2,1,4,1,3,5,5,1,4,1,1,4,2,2,1,3,1,1,1,1,3,4,1,4,1,1,1,4,4,4,1,3,1,3,4,1,4,1,2,2,2,5,4,1,3,1,2,1,4,1,4,5,2,4,5,4,1,2,1,4,2,2,2,1,3,5,2,5,1,1,4,5,4,3,2,4,1,5,2,2,5,1,4,1,5,1,3,5,1,2,1,1,1,5,4,4,5,1,1,1,4,1,3,3,5,5,1,5,2,1,1,3,1,1,3,2,3,4,4,1,5,5,3,2,1,1,1,4,3,1,3,3,1,1,2,2,1,2,2,2,1,1,5,1,2,2,5,2,4,1,1,2,4,1,2,3,4,1,2,1,2,4,2,1,1,5,3,1,4,4,4,1,5,2,3,4,4,1,5,1,2,2,4,1,1,2,1,1,1,1,5,1,3,3,1,1,1,1,4,1,2,2,5,1,2,1,3,4,1,3,4,3,3,1,1,5,5,5,2,4,3,1,4]
inList1 = [3,4,3,1,2]
# 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
# 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
numberOfDays = 256

fishDayDict = {}

for day in range(9):
	fishDayDict[day] = 0

for fish in inList:
	fishDayDict[fish] += 1

for day in range(numberOfDays):
	newFish = fishDayDict[0]
	fishDayDict[0] = fishDayDict[1]
	fishDayDict[1] = fishDayDict[2]
	fishDayDict[2] = fishDayDict[3]
	fishDayDict[3] = fishDayDict[4]
	fishDayDict[4] = fishDayDict[5]
	fishDayDict[5] = fishDayDict[6]
	fishDayDict[6] = fishDayDict[7] + newFish
	fishDayDict[7] = fishDayDict[8]
	fishDayDict[8] = newFish

sum = 0
for day in range(9):
	sum += fishDayDict[day]#
print("sum",sum)
# At end
endTime = time.time()
print('time',endTime-startTime)

# 3183 too high
# 3258 is too high
# 5570 too high

import itertools

# def next_permutation(arr):
	# # Find non-increasing suffix
	# i = len(arr) - 1
	# while i > 0 and arr[i - 1] >= arr[i]:
		# i -= 1
	# if i <= 0:
		# return False
	
	# # Find successor to pivot
	# j = len(arr) - 1
	# while arr[j] <= arr[i - 1]:
		# j -= 1
	# arr[i - 1], arr[j] = arr[j], arr[i - 1]
	
	# # Reverse suffix
	# arr[i : ] = arr[len(arr) - 1 : i - 1 : -1]
	# return True

# inList = [50, 49, 47, 46, 44, 43, 42, 40, 40, 36, 32, 26, 24, 22, 21, 18, 18, 11, 10, 7]
# totalSize = 150
inList = [20,15,10,5,5]
totalSize = 25

testCount = 0
# print('inList',inList)
# inList.sort()
# print('inList',inList)
inList.reverse()
print('inList',inList)
print('len inList',len(inList))
for combo in itertools.permutations(inList):
	testSize = totalSize
	# print(inList)
	print(combo)
	for item in combo:
		#print(item,end=' ')
		testSize -= item
		if testSize == 0:
			testCount += 1
			print("hit",testCount)
			break
		if testSize < 0:
			break
	#print()
print('counts',testCount)

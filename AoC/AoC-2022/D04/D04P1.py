""" 
D04P1

"""


def isContained(nums):
	print(nums)
	if (nums[0] <= nums[2]) and (nums[1] >= nums[3]):
		print('contained')
		return True
	if (nums[0] >= nums[2]) and (nums[1] <= nums[3]):
		print('contained')
		return True
	return False

fileName = 'input.txt'
inCount = 0
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		if inLine != '':
			print(inLine)
			line1=inLine.split(',')
			#print(line1)
			np1=line1[0].split('-')
			np2=line1[1].split('-')
			newLine = []
			newLine.append(int(np1[0]))
			newLine.append(int(np1[1]))
			newLine.append(int(np2[0]))
			newLine.append(int(np2[1]))
			# print(newLine)
			if isContained(newLine):
				inCount += 1
print("Contained Count",inCount)
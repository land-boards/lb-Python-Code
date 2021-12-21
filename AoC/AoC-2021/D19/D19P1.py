# D19P1.py
# 2021 Advent of Code
# Day 19
# Part 1

import time

# At start
startTime = time.time()

def readFileToListOfStrings(fileName):
	"""
	"""
	inList = []
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inList.append(line.rstrip())
	return inList

def extractScannerVals(inList):
	scannersArray = []
	newScannerVals = []
	stateVal = 'scannerNum'
	for row in inList:
		if 'scanner' in row:
			newScannerVals = []
			stateVal = 'gotScannerNum'
			# print("New scanner")
		elif row == '':
			scannersArray.append(newScannerVals)
			stateVal = 'scannerNum'
		else:
			# print("row",row)
			scannerRow = row.split(',')
			# print("scannerRow",scannerRow)
			scalerRow = []
			for val in scannerRow:
				# print("val",val)
				scalerRow.append(int(val))
			newScannerVals.append(scalerRow)
			# print("newScannerVals",newScannerVals)
	scannersArray.append(newScannerVals)
	return scannersArray

inList = readFileToListOfStrings('input.txt')
scannersArray = extractScannerVals(inList)
# print("scannersArray",scannersArray)
for scanner in scannersArray:
	print("Scanner",scanner)

endTime = time.time()
print('time',endTime-startTime)

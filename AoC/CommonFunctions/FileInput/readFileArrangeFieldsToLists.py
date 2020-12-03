"""
ReadFileArrangeFieldsToLists

Input:

Output:


"""

def ReadFileArrangeFieldsToLists(listColumns, splitChar):
	readList = []
	with open('input.txt', 'r') as filehandle:  
		# Read in as a list of strings
		for line in filehandle:
			readList.append(line.rstrip())
	# split by the splitChar
	# line make into list
	inList = []
	for line in readList:
		splitInLine = line.split(splitChar)
		newLine = []
		for element in listColumns:
			newLine.append(splitInLine[element])
		inList.append(newLine)
	return inList

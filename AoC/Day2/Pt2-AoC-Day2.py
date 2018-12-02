# Pt2-AoCDay2.py
# 2018 Advent of Code
# Day 2
# Part 2

# define an empty list
boxIDs = []

accum = 0	# Accumulated sum

def dumpSame(string1,string2):
	#print 'Dump the same chars between strings'
	newString = ''
	charOffset = 0
	for char in string1:
		if char == string2[charOffset]:
			newString += char
		charOffset += 1
	return newString

def countDiffs(string1,string2):
	#print 'counting differences between strings'
	diffCount = 0
	charOffset = 0
	for char in string1:
		if char != string2[charOffset]:
			diffCount += 1
		charOffset += 1
	return diffCount
# open file and read the content into an accumulated sum
with open('input.txt', 'r') as filehandle:  
	for line in filehandle:
		boxIDs.append(line.strip('\n\r'))
#print boxIDs

string2Offset = 0
for string1 in boxIDs:
	string2Offset += 1
	for string2 in boxIDs[string2Offset:]:
		if countDiffs(string1,string2) == 1:
			print 'String1',string1
			print 'String2',string2
			print (dumpSame(string1,string2))
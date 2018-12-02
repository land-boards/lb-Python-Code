# Pt1-AoCDay2.py
# 2018 Advent of Code
# Day 2
# Part 1

# define an empty list
boxIDs = []

accum = 0	# Accumulated sum

def countN(theLineString,testCount):
	print 'looking for',testCount
	countOfNs = 0
	arrayOfPossibleChars = []
	i = 0
	while i < 26:
		arrayOfPossibleChars.append(0)
		i += 1
	for testChar in theLineString:
		#print 'testing character', testChar,
		#print 'offset is',ord(testChar)-ord('a')
		arrayOfPossibleChars[ord(testChar)-ord('a')] += 1
	#print 'array',arrayOfPossibleChars
	i = 0
	while i < 26:
		if arrayOfPossibleChars[i] == testCount:
			#print 'Found a',testChar
			return True
		i += 1
	return False

# open file and read the content into an accumulated sum
with open('input.txt', 'r') as filehandle:  
	for line in filehandle:
		boxIDs.append(line.strip('\n\r'))
#print boxIDs
count2 = 0
count3 = 0
for theLine in boxIDs:
	if countN(theLine,2):
		count2 += 1
	if countN(theLine,3):
		count3 += 1
print 'count of 2s',count2
print 'count of 3s',count3
print 'checksum',count2*count3

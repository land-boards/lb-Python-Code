# Pt2-AoCDay1.py
# 2018 Advent of Code
# Day 1
# Part 2

import time
print 'started', time.strftime('%X %x %Z')

# Read the input file into a list so it can be read over and over again
changes = []
print 'reading in list'
with open('input.txt', 'r') as filehandle:  
	for line in filehandle:
		changes.append(int(line[:-1]))
#print 'List of freq changes = ',changes

accumFreq = 0	# Accumulated frequency starts at 0
# define an empty list
freqsList = []
freqsList.append(accumFreq)		# Put first 0 into the list

print 'searching list'
highestAccum = 0
loopCount = 0
while loopCount < 1000:	# Loop through the list over and over
	print '+',	# Print a plus every time through the list
	for currentFreqChange in changes:
		accumFreq += currentFreqChange
		if accumFreq > highestAccum:
			highestAccum = accumFreq
	loopCount += 1
print 'highestAccum=',highestAccum

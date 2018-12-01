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
loopCount = 0
while 1:	# Loop through the list over and over
	print '+',	# Print a plus every time through the list
	for currentFreqChange in changes:
#		print 'Current frequency =', accumFreq,
#		print ', Input=', currentFreqChange,
		accumFreq += currentFreqChange
#		print ', Looking for value',accumFreq
		#print 'in the list', freqsList
		if accumFreq in freqsList:
			print '***Found first duplicated frequency***'
#			print 'list=',freqsList
			print 'Repeated frequency=', accumFreq
			print 'ended',time.strftime('%X %x %Z')
			exit(0)
		# add item to the list
		else:
			freqsList.append(accumFreq)
#print 'list[]=',freqsList
#print 'sorted list',sorted(freqsList)

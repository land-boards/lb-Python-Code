# Pt2-AoCDay1.py
# 2018 Advent of Code
# Day 1
# Part 2

import time
print 'started', time.strftime('%X %x %Z')

def readTextFileToList(fileName):
	"""readTextFileToList - read in file into list as integers
	"""
	freqChangesAsInts = []
	# open file and read the content into an accumulated sum
	#print 'Reading in file',time.strftime('%X %x %Z')
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			freqChangesAsInts.append(int(line.strip('\n\r')))
	return freqChangesAsInts

def findLoopPoint(changes):
	print 'Scanning for loop'
	currentFreqAccum = 0					# Accumulated frequency starts at 0
	freqsList = []							# define an empty list to hold all frequencies
	freqsList.append(currentFreqAccum)		# Put first 0 into the list
	while True:	# Loop through the list over and over
		print '+',	# Print a plus every time through the list
		for currentFreqChange in changes:
			currentFreqAccum += currentFreqChange
			if currentFreqAccum in freqsList:
				print '\nLength of Frequency list loop',len(freqsList)
				return(currentFreqAccum)
			freqsList.append(currentFreqAccum)	# add item to the list

freqChanges = readTextFileToList('input.txt')
#print 'List of freq freqChanges = ',freqChanges
accumFreq = findLoopPoint(freqChanges)

print 'Ended',time.strftime('%X %x %Z')
print '***Found first duplicated frequency***'
print 'Repeated frequency=', accumFreq

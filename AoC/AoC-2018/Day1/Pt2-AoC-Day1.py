# Pt2-AoCDay1.py
# 2018 Advent of Code
# Day 1
# Part 2
"""
--- Part Two ---
You notice that the device repeats the same frequency change list over and over. To calibrate the device, you need to find the first frequency it reaches twice.

For example, using the same list of changes above, the device would loop as follows:

Current frequency  0, change of +1; resulting frequency  1.
Current frequency  1, change of -2; resulting frequency -1.
Current frequency -1, change of +3; resulting frequency  2.
Current frequency  2, change of +1; resulting frequency  3.
(At this point, the device continues from the start of the list.)
Current frequency  3, change of +1; resulting frequency  4.
Current frequency  4, change of -2; resulting frequency  2, which has already been seen.
In this example, the first frequency reached twice is 2. Note that your device might need to repeat its list of frequency changes many times before a duplicate frequency is found, and that duplicates might be found while in the middle of processing the list.

Here are other examples:

+1, -1 first reaches 0 twice.
+3, +3, +4, -2, -4 first reaches 10 twice.
-6, +3, +8, +5, -6 first reaches 5 twice.
+7, +7, -2, -7, -4 first reaches 14 twice.
What is the first frequency your device reaches twice?

Your puzzle answer was 72889.

"""
from __future__ import print_function

import time

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
	print('Scanning for loop')
	currentFreqAccum = 0					# Accumulated frequency starts at 0
	freqsList = []							# define an empty list to hold all frequencies
	freqsList.append(currentFreqAccum)		# Put first 0 into the list
	while True:	# Loop through the list over and over
		print('+', end=' ')	# Print a plus every time through the list
		for currentFreqChange in changes:
			currentFreqAccum += currentFreqChange
			if currentFreqAccum in freqsList:
				print('\nLength of Frequency list loop',len(freqsList))
				return(currentFreqAccum)
			freqsList.append(currentFreqAccum)	# add item to the list

print('started', time.strftime('%X %x %Z'))

freqChanges = readTextFileToList('input.txt')

accumFreq = findLoopPoint(freqChanges)

print('Ended',time.strftime('%X %x %Z'))
print('***Found first duplicated frequency***')
print('Repeated frequency=', accumFreq)

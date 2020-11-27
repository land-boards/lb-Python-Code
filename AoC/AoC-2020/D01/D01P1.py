# Pt1-AoCDay1.py
# 2020 Advent of Code
# Day 1
# Part 1

"""
"""

accum = 0	# Accumulated sum

# open file and read the content into an accumulated sum
with open('AOC2019D01input.txt', 'r') as filehandle:  
	for lineIn in filehandle:
		currentPlace = int(int(lineIn.strip()) / 3)-2
		accum += currentPlace
print('sum =',accum)

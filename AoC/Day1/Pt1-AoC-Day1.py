# Pt1-AoCDay1.py
# 2018 Advent of Code
# Day 1
# Part 1

# define an empty list
#places = []

accum = 0	# Accumulated sum

# open file and read the content into an accumulated sum
with open('input.txt', 'r') as filehandle:  
	for line in filehandle:
		# remove linebreak which is the last character of the string
		currentPlace = int(line[:-1])
		accum += currentPlace

		# add item to the list
#		places.append(currentPlace)

#print places
print 'sum =',accum

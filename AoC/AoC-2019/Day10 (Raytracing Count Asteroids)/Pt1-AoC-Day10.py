# Pt1-AoCDay10.py
# 2019 Advent of Code
# Day 10
# Part 1
# https://adventofcode.com/2019/day/10

from __future__ import print_function
import numpy

"""
--- Day 10: Monitoring Station ---
You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here have an emergency: they're having trouble tracking all of the asteroids and can't be sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of space; they hand you a map of all of the asteroids in that region (your puzzle input).

The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller than they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids can be described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the top edge (so the top-left corner is 0,0 and the position immediately to its right is 1,0).

Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally. The best location is the asteroid that can detect the largest number of other asteroids.

For example, consider the following map:

.#..#
.....
#####
....#
...##
The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can detect 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its view of this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or fewer other asteroids. Here is the number of other asteroids a monitoring station on each asteroid could detect:

.7..7
.....
67775
....7
...87
Here is an asteroid (#) and some examples of the ways its line of sight might be blocked. If there were another asteroid at the location of a capital letter, the locations marked with the corresponding lowercase letter would be blocked and could not be detected:

#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c
Here are some larger examples:

Best is 5,8 with 33 other asteroids detected:

......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
Best is 1,2 with 35 other asteroids detected:

#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
Best is 6,3 with 41 other asteroids detected:

.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
Best is 11,13 with 210 other asteroids detected:

.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
Find the best location for a new monitoring station. How many other asteroids can be detected from that location?

274 is too gigh

"""

def readInFile(inFileName):
	inList = [line.rstrip('\n') for line in open(inFileName)]
	asteroidField = []
	for line in inList:
		newRow=[]
		for lineChar in line:
			newRow.append(lineChar)
		asteroidField.append(newRow)
	for row in asteroidField:
		print(row)
	columns = len(asteroidField[0])
	rows = len(asteroidField)
	print("Rows :",rows)
	print("Cols :",columns)
	asteroidLocations = []
	for row in range(rows):
		for column in range(columns):
			if asteroidField[row][column] == '#':
				asteroidLocations.append([column,row])
	return(asteroidLocations)

inFileName = "AOC2019D10input.txt"
asteroidLocations = readInFile(inFileName)
print("Asteroid count  =",len(asteroidLocations))
print("Asteroid Locations at at: ",asteroidLocations)

# Check pairs of asteroids one at a time and see if there are any other points which are in the way

def buildAnglesTable(currentAsteroid,asteroidLocations):
	anglesTable = []
	for compareAsteroid in asteroidLocations:
		newList = []
		if currentAsteroid != compareAsteroid:
			deltaYFloat = float(currentAsteroid[1]) - float(compareAsteroid[1])
			deltaXFloat = float(currentAsteroid[0]) - float(compareAsteroid[0])
			angle = numpy.arctan2(deltaXFloat,deltaYFloat)
			distance = (abs(currentAsteroid[1]) - abs(compareAsteroid[1])) + (abs(currentAsteroid[0]) - abs(compareAsteroid[0]))
			newList.append(compareAsteroid[0])
			newList.append(compareAsteroid[1])
			newList.append(angle)
			newList.append(distance)
			#print("Point/Angle,distance",newList)
			anglesTable.append(newList)
		# else:
			# print("Skipping self at :",compareAsteroid)
	return anglesTable

def stuffAngleTable(angleTable):
	newAngleTable = []
	for point in angleTable:
		if point[2] not in newAngleTable:
			newAngleTable.append(point[2])
	#print("Unique Angles count =",len(newAngleTable))
	return(newAngleTable)

maxAsteroids = 0
for currentAsteroid in asteroidLocations:
	print("For asteroid at :",currentAsteroid," ",end='')
	angleTable = buildAnglesTable(currentAsteroid,asteroidLocations)
	sortedAngleTable = sorted(stuffAngleTable(angleTable))
	print("currentAsteroid","count",len(sortedAngleTable))
	if len(sortedAngleTable) > maxAsteroids:
		maxAsteroids = len(sortedAngleTable)
	# for angle in sortedAngleTable:
		# print("\nasteroid angle",angle," ",end='')
		# for asteroidWithAngle in angleTable:
			# if asteroidWithAngle[2] == angle:
				# print(asteroidWithAngle[0:2],end='')
print("maxAsteroids",maxAsteroids)

# Pt1-AoCDay10.py
# 2019 Advent of Code
# Day 10
# Part 1
# https://adventofcode.com/2019/day/10

from __future__ import print_function
import numpy

"""
--- Part Two ---

Once you give them the coordinates, the Elves quickly deploy an Instant Monitoring Station to the location and discover the worst: there are simply too many asteroids.

The only solution is complete vaporization by giant laser.

Fortunately, in addition to an asteroid scanner, the new monitoring station also comes equipped with a giant rotating laser perfect for vaporizing asteroids. The laser starts by pointing up and always rotates clockwise, vaporizing any asteroid it hits.

If multiple asteroids are exactly in line with the station, the laser only has enough power to vaporize one of them before continuing its rotation. In other words, the same asteroids that can be detected can be vaporized, but if vaporizing one asteroid makes another one detectable, the newly-detected asteroid won't be vaporized until the laser has returned to the same position by rotating a full 360 degrees.

For example, consider the following map, where the asteroid with the new monitoring station (and laser) is marked X:

.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##

The first nine asteroids to get vaporized, in order, would be:

.#....###24...#..
##...##.13#67..9#
##...#...5.8####.
..#.....X...###..
..#.#.....#....##

Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7) won't have a chance to be vaporized until the next full rotation. The laser continues rotating; the next nine to be vaporized are:

.#....###.....#..
##...##...#.....#
##...#......1234.
..#.....X...5##..
..#.9.....8....76

The next nine to be vaporized are then:

.8....###.....#..
56...9#...#.....#
34...7...........
..2.....X....##..
..1..............

Finally, the laser completes its first full rotation (1 through 3), a second rotation (4 through 8), and vaporizes the last asteroid (9) partway through its third rotation:

......234.....6..
......1...5.....7
.................
........X....89..
.................

In the large example above (the one with the best monitoring station location at 11,13):

    The 1st asteroid to be vaporized is at 11,12.
    The 2nd asteroid to be vaporized is at 12,1.
    The 3rd asteroid to be vaporized is at 12,2.
    The 10th asteroid to be vaporized is at 12,8.
    The 20th asteroid to be vaporized is at 16,0.
    The 50th asteroid to be vaporized is at 16,9.
    The 100th asteroid to be vaporized is at 10,16.
    The 199th asteroid to be vaporized is at 9,6.
    The 200th asteroid to be vaporized is at 8,2.
    The 201st asteroid to be vaporized is at 10,9.
    The 299th and final asteroid to be vaporized is at 11,1.

The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which asteroid that will be; what do you get if you multiply its X coordinate by 100 and then add its Y coordinate? (For example, 8,2 becomes 802.)

121 is too low
1103 is too low
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

#inFileName = "TestCase2_1.txt"
inFileName = "AOC2019D10input.txt"#
#inFileName = "TrivialTestCase.txt"
print("Input data :",inFileName)
asteroidLocations = readInFile(inFileName)
print("Asteroid count  =",len(asteroidLocations))
print("Asteroid Locations at at: ",asteroidLocations)

def buildAnglesTable(currentAsteroid,asteroidLocations):
	anglesTable = []
	for compareAsteroid in asteroidLocations:
		newList = []
		if currentAsteroid != compareAsteroid:
			deltaYFloat = float(currentAsteroid[1] - compareAsteroid[1])
			deltaXFloat = float(currentAsteroid[0] - compareAsteroid[0])
			angle = (numpy.arctan2(deltaYFloat,deltaXFloat) * (180.0 / 3.1415926) - 90.0) % 360.0
			angle = round(angle,6)
			distance = (abs(currentAsteroid[1] - compareAsteroid[1])) + (abs(currentAsteroid[0] -compareAsteroid[0]))
			newList.append(compareAsteroid[0])
			newList.append(compareAsteroid[1])
			newList.append(angle)
			newList.append(distance)
			#print("Point/Angle,distance",newList)
			anglesTable.append(newList)
		# else:
			# print("Skipping self at :",compareAsteroid)
	return anglesTable

def stuffAngleTable(asteroidXYAngleDist):
	newAngleTable = []
	for point in asteroidXYAngleDist:
		if point[2] not in newAngleTable:
			newAngleTable.append(point[2])
	return(newAngleTable)

maxAsteroids = 0
bestLocation = []
for currentAsteroid in asteroidLocations:
	#print("For asteroid at :",currentAsteroid," ")
	asteroidXYAngleDist = buildAnglesTable(currentAsteroid,asteroidLocations)
	#print("asteroidXYAngleDist",asteroidXYAngleDist)
	sortedAngleTable = sorted(stuffAngleTable(asteroidXYAngleDist))
	#print("sortedAngleTable",sortedAngleTable)
	if len(sortedAngleTable) > maxAsteroids:
		maxAsteroids = len(sortedAngleTable)
		bestLocation = currentAsteroid[0:2]
print("Maximum number of Asteroids",maxAsteroids)
print("Best Location",bestLocation)
#print("Sorted angles table :",sortedAngleTable)
print("Number of unique angles :",len(sortedAngleTable))
asteroidXYAngleDist = buildAnglesTable(bestLocation,asteroidLocations)
#print("asteroidXYAngleDist",asteroidXYAngleDist)
sortedAngleTable = sorted(stuffAngleTable(asteroidXYAngleDist))
#print("sortedAngleTable",sortedAngleTable)
asteroidNum = 1
asteroid200 = []
for angle in sortedAngleTable:
	print("asteroide Number",asteroidNum,"check for anglesFromBase",angle," ",end="")
	for asteroid in asteroidXYAngleDist:
		#print("asteroid",asteroid)
		if asteroid[0:2] != bestLocation:
			if asteroid[2] == angle:
				print("asteroid",asteroid)
				if asteroidNum == 200:
					asteroid200 = asteroid
	asteroidNum = asteroidNum + 1
# print("200th angle",sortedAngleTable[199])
# for asteroid in asteroidXYAngleDist:
	# if asteroid[2] == sortedAngleTable[199]:
		# print(asteroid)
print("asteroid 200",asteroid200)
print("asteroid200",asteroid200[0]," ",asteroid200[1])

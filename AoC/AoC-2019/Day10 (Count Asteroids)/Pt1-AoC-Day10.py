# Pt1-AoCDay10.py
# 2019 Advent of Code
# Day 10
# Part 1

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
"""
from __future__ import print_function

# Look between all points and see if there is a point between the two points
# If there is no point between the two points can see each other

def isPointOnLineBetweenPoints(startXY, endXY, testXY):
	""" 
	startXY is the start point
	endXY is the end point
	testXY is the point to test to see if it is on the line
	"""
	equationOfALineDebug = True
	if equationOfALineDebug:
		print("Check if point is outside bounding box")
	if ((testXY[0] > startXY[0]) and (testXY[0] > endXY[0])):
		if equationOfALineDebug:
			print("Outside X to the right")
		return False
	elif ((testXY[0] < startXY[0]) and (testXY[0] < endXY[0])):
		if equationOfALineDebug:
			print("Outside X to the left")
		return False
	elif ((testXY[1] > startXY[1]) and (testXY[1] > endXY[1])):
		if equationOfALineDebug:
			print("Outside Y to the bottom")
		return False
	elif ((testXY[1] < startXY[1]) and (testXY[1] < endXY[1])):
		if equationOfALineDebug:
			print("Outside Y to the top")
		return False
	if equationOfALineDebug:
		print("Check if point is on horizontal line")
	if ((testXY[0] == startXY[0]) and (testXY[0] == endXY[0])):
		if equationOfALineDebug:
			print("Point is on horizontal line")
		return True
	if equationOfALineDebug:
		print("Check if point is on vertical line")
	if ((testXY[1] == startXY[1]) and (testXY[1] == endXY[1])):
		if equationOfALineDebug:
			print("Point is on vertical line")
		return True
	if startXYin[0] > startXYin:
		startXY[0] = startXYin[0]
		startXY[1] = startXYin[1]
		endXY[0] = endXYin[0]
		startXY[1] = startXYin[1]
		
		
	if equationOfALineDebug:
		print("Still maybe")
	return True
	
xy1=[1,1]
xy2=[3,3]
xyTest=[2,2]
print("Is test point on the line between the two points",isPointOnLineBetweenPoints(xy1,xy2,xyTest))
assert False,"Done"
inFileName = "TestCase1_1.txt"

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
print("Asteroid Locations at at: ", asteroidLocations)

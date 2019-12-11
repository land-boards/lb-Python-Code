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

274 is too gigh

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
	equationOfALineDebug = False
	if equationOfALineDebug:
		print("Original end points",startXY,endXY,"testing",testXY)
	if testXY == startXY:
		if equationOfALineDebug:
			print("Duplicate")
		return "duplicatePoint"
	if testXY == endXY:
		if equationOfALineDebug:
			print("Duplicate")
		return "duplicatePoint"
	if equationOfALineDebug:
		print("Check if point is outside bounding box")
	if ((testXY[0] > startXY[0]) and (testXY[0] > endXY[0])):
		if equationOfALineDebug:
			print("Outside X to the right")
		return "outsideBoundingBox"
	elif ((testXY[0] < startXY[0]) and (testXY[0] < endXY[0])):
		if equationOfALineDebug:
			print("Outside X to the left")
		return "outsideBoundingBox"
	elif ((testXY[1] > startXY[1]) and (testXY[1] > endXY[1])):
		if equationOfALineDebug:
			print("Outside Y to the bottom")
		return "outsideBoundingBox"
	elif ((testXY[1] < startXY[1]) and (testXY[1] < endXY[1])):
		if equationOfALineDebug:
			print("Outside Y to the top")
		return "outsideBoundingBox"
	if equationOfALineDebug:
		print("Check if point is on horizontal line")
	if ((testXY[0] == startXY[0]) and (testXY[0] == endXY[0])):
		if equationOfALineDebug:
			print("Point is on horizontal line")
		return "pointIsOnLine"
	if equationOfALineDebug:
		print("Check if point is on vertical line")
	if ((testXY[1] == startXY[1]) and (testXY[1] == endXY[1])):
		if equationOfALineDebug:
			print("Point is on vertical line")
		return "pointIsOnLine"
	if equationOfALineDebug:
		print("Move line and points to Quadrant I")
	startXYQ1 = startXY
	endXYQ1 = endXY
	testXYQ1 = testXY
	if equationOfALineDebug:
		print("Points in Quadrant I",startXYQ1,endXYQ1,testXYQ1)
		print("Ordering points to have start on the left")
	if startXYQ1[0] > endXYQ1[0]:
		startOrderedXY = endXYQ1
		endOrderedXY = startXYQ1
	else:
		startOrderedXY = startXYQ1
		endOrderedXY = endXYQ1
	if equationOfALineDebug:
		print("Ordered result",startOrderedXY,endOrderedXY,testXYQ1)
		print("Shift in Y to have y intercept = 0")
	shiftY = startOrderedXY[1]
	startZeroBasedXY 	= [startOrderedXY[0],startOrderedXY[1]-shiftY]
	endZeroBasedXY 		= [endOrderedXY[0],endOrderedXY[1]-shiftY]
	testZeroBasedXY 	= [testXYQ1[0],testXYQ1[1]-shiftY]
	if equationOfALineDebug:
		print("Shifted to x=0 points",startZeroBasedXY,endZeroBasedXY,testZeroBasedXY)
	deltaY = endZeroBasedXY[1]-startZeroBasedXY[1]
	deltaX = endZeroBasedXY[0]-startZeroBasedXY[0]
	if equationOfALineDebug:
		print("deltaX :",deltaX,"deltaY :",deltaY)
	testY = (10000*testZeroBasedXY[0] * deltaY) / deltaX
	if equationOfALineDebug:
		print("testY",testY)
	if testY == 10000*testZeroBasedXY[1]:
		if equationOfALineDebug:
			print("Point is on line")
		return "pointIsOnLine"
	else:
		if equationOfALineDebug:
			print("Point is not on line")
		return "pointNotOnLine"
	
def testCases():
	# Test cases for the line equation checker
	print("Test Case 01 (point on line) - ",end='')
	xy1=[1,1]
	xy2=[3,3]
	xyTest=[2,2]
	checkPoint = isPointOnLineBetweenPoints(xy1,xy2,xyTest)
	if checkPoint == "pointIsOnLine":
		print("Passed")
	else:
		print("Failed",checkPoint)

	print("Test Case 02 (point not on line) - ",end='')
	xy1=[1,1]
	xy2=[3,3]
	xyTest=[2,3]
	checkPoint = isPointOnLineBetweenPoints(xy1,xy2,xyTest)
	if checkPoint == "pointNotOnLine":
		print("Passed")
	else:
		print("Failed",checkPoint)

	print("Test Case 03 (Duplicate end point) - ",end='')
	xy1=[1,1]
	xy2=[3,3]
	xyTest=[1,1]
	checkPoint = isPointOnLineBetweenPoints(xy1,xy2,xyTest)
	if checkPoint == "duplicatePoint":
		print("Passed")
	else:
		print("Failed",checkPoint)

	print("Test Case 04 (Duplicate end point) - ",end='')
	xy1=[1,1]
	xy2=[3,3]
	xyTest=[3,3]
	checkPoint = isPointOnLineBetweenPoints(xy1,xy2,xyTest)
	if checkPoint == "duplicatePoint":
		print("Passed")
	else:
		print("Failed",checkPoint)

	print("Test Case 05 (outside bounding box) - ",end='')
	xy1=[1,1]
	xy2=[3,3]
	xyTest=[4,1]
	checkPoint = isPointOnLineBetweenPoints(xy1,xy2,xyTest)
	if checkPoint == "outsideBoundingBox":
		print("Passed")
	else:
		print("Failed",checkPoint)

	print("Test Case 06 (longer line) - ",end='')
	xy1=[0,0]
	xy2=[99,99]
	xyTest=[49,49]
	checkPoint = isPointOnLineBetweenPoints(xy1,xy2,xyTest)
	if checkPoint == "pointIsOnLine":
		print("Passed")
	else:
		print("Failed",checkPoint)

	print("Test Case 07 (point slightly off line) - ",end='')
	xy1=[0,0]
	xy2=[99,99]
	xyTest=[50,51]
	checkPoint = isPointOnLineBetweenPoints(xy1,xy2,xyTest)
	if checkPoint != "pointIsOnLine":
		print("Passed")
	else:
		print("Failed",checkPoint)

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

#testCases()
inFileName = "TestCase1_2.txt"
asteroidLocations = readInFile(inFileName)
print("Asteroid Locations at at: ", asteroidLocations,"\n")

# Check pairs of asteroids one at a time and see if there are any other points which are in the way

# for currentAsteroid in asteroidLocations:
# currentAsteroid = [3,4]
# maxAsteriodCount = 0

currentAsteroid = [5,8]
# compareAsteroid = [0,2]
# checkAsteroid = [1,2]
visibleAsteroids = 0
for compareAsteroid in asteroidLocations:
	foundBlockingAsteroid = False
	for checkAsteroid in asteroidLocations:
		rVal = isPointOnLineBetweenPoints(currentAsteroid,compareAsteroid,checkAsteroid)
		#print("Checking",currentAsteroid,"against",compareAsteroid,"for",checkAsteroid," ",rVal)
		if rVal == 'pointIsOnLine':
			foundBlockingAsteroid = True
	if not foundBlockingAsteroid:
		visibleAsteroids = visibleAsteroids + 1
		print("Didn't find blocking asteroid between",currentAsteroid,"and",compareAsteroid,"count",visibleAsteroids)
print("Found visible asteroid count :",visibleAsteroids)
assert False,"Done"

maxAsteriodCount = 0
for currentAsteroid in asteroidLocations:
	#print("\n*** Checking asteroid", currentAsteroid,"***")
	visibleAsteroids = 0
	for compareAsteroid in asteroidLocations:
		if currentAsteroid != compareAsteroid:
			#print("Checking asteroid", currentAsteroid,"against",compareAsteroid)
			foundBlockingAsteroid = False
			for checkAsteroid in asteroidLocations:
				if (checkAsteroid != currentAsteroid) and (checkAsteroid != compareAsteroid):
					rVal = isPointOnLineBetweenPoints(currentAsteroid,compareAsteroid,checkAsteroid)
					#print("Checking",currentAsteroid,"against",compareAsteroid,"for",checkAsteroid," ",rVal)
					if rVal == 'pointIsOnLine':
						foundBlockingAsteroid = True
				# else:
					# print("Duplicate(1) :",checkAsteroid,currentAsteroid,compareAsteroid)
			if not foundBlockingAsteroid:
				visibleAsteroids = visibleAsteroids + 1
				#print("Didn't find blocking asteroid between",currentAsteroid,"and",compareAsteroid,"count",visibleAsteroids)
			# else:
				# print("Blocking asteroid between",currentAsteroid,"and",compareAsteroid)
	print("Asteroid",currentAsteroid,"Count :",visibleAsteroids)
	if (visibleAsteroids > maxAsteriodCount):
		maxAsteriodCount = visibleAsteroids
		bestLoc = currentAsteroid
		#print("asteroids from",currentAsteroid,"count =",visibleAsteroids)
	# else:
		# print("Duplicate(2) :",currentAsteroid,compareAsteroid)		
print("Max asteroid count =",maxAsteriodCount,"at ",bestLoc)



































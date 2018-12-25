import numpy as np
import matplotlib.pyplot as plt

def plotScatterPoints(xyList):
	x = []
	y = []
	for point in xyList:
		x.append(point[0])
		y.append(point[1])

	plt.scatter(x,y)
	plt.show()

xyList = [[1,1],[3,2],[5,2]]
	
plotScatterPoints(xyList)

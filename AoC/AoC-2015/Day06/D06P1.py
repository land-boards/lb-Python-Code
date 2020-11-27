# 325000 is too low
# 382000 is too high
  
def readFileToList():
	inList = []
	with open('input.txt', 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)
	return inList

def performCmd(myarray,cmd,corner1,corner2):
	# print("performCmd: corner1",int(corner1[0]),int(corner1[1]))
	# print("corner2",int(corner2[0]),int(corner2[1]))
	for yVal in range(int(corner1[1]),int(corner2[1])+1):
		for xVal in range(int(corner1[0]),int(corner2[0])+1):
			if cmd == 'Toggle':
#				print("toggle loc",xVal,yVal)
				myarray[yVal][xVal] += 2
			elif cmd == 'TurnOn':
#				print("set loc to 1 =",xVal,yVal)
				myarray[yVal][xVal] += 1
			elif cmd == 'TurnOff':
#				print("set loc to 0 =",xVal,yVal)
				myarray[yVal][xVal] -= 1
			else:
				print("bad cmd",cmd)

def makeOneKSquareArray():
	lineArray = []
	theArray = []
	for y in range(1000):
		lineArray = []
		for x in range(1000):
			lineArray.append(0)
		theArray.append(lineArray)
	# print(theArray)
	return theArray

def countOns():
	lightsOnCount = 0
	for yVal in range(1000):
		for xVal in range(1000):
			if myarray[yVal][xVal] == 1:
				lightsOnCount += 1		
	print("count :",lightsOnCount)

inList = readFileToList()
# inList = ['turn on 0,0 through 3,3']
# inList = ['turn on 0,0 through 9,9','toggle 2,2 through 4,4']
print("Make array")
myarray = makeOneKSquareArray()
# ['turn', 'on', '185,412', 'through', '796,541']
# ['turn', 'off', '225,603', 'through', '483,920']
# ['toggle', '717,493', 'through', '930,875']

countOns()
for row in inList:
	cmdList=row.split(' ')
	print(cmdList)
	if cmdList[0]=='toggle':
		corner1=cmdList[1].split(',')
		corner2=cmdList[3].split(',')
		print("corner1",corner1)
		print("corner2",corner2)
		cmd='Toggle'
	else:
		corner1=cmdList[2].split(',')
		corner2=cmdList[4].split(',')
		# print("corner1 =",corner1)
		# print("corner2 =",corner2)
		if cmdList[1] == 'on':
			cmd = 'TurnOn'
		elif cmdList[1] == 'off':
			cmd = 'TurnOff'
		else:
			print("cmd opt bad")
	print(cmd," ", corner1, " ", corner2)
	performCmd(myarray,cmd,corner1,corner2)

# print(myarray[0][0:9])
# print(myarray[1][0:9])
# print(myarray[2][0:9])
# print(myarray[3][0:9])
# print(myarray[4][0:9])

lightsOnCount = 0
for yVal in range(1000):
	for xVal in range(1000):
		lightsOnCount += myarray[yVal][xVal]
			
print("count :",lightsOnCount)

""" 
D10P2

"""

# fileName = 'input1.txt'
fileName = 'input.txt'
# fileName = 'input2.txt'

instr = []
inList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		instr.append(inLine.split(' '))

# print('instr',instr)
clock = 0
traceBuffer = []
xReg = 1
step = 1
for line in instr:
	# print('line',line)
	if line[0] == 'noop':
		execTime = 1
	elif line[0] == 'addx':
		execTime = 2
	for clkCPU in range(execTime):
		traceBuffer.append(xReg)
		step += 1
	if line[0] == 'addx':
		xReg += int(line[1])
	# print('xReg',xReg)
# print('traceBuffer',traceBuffer)
# print(len(traceBuffer))
crtScreen = []
crtRow=['.']*40
tracePos = 0
screenXVals = []
for row in range(6):
	screenRow = []
	for col in range(40):
		screenRow.append(traceBuffer[tracePos]-1)
		tracePos += 1
	screenXVals.append(screenRow)
for row in screenXVals:
	print(row)
#Make blank screenXVals
for row in range(6):
	crtRow = []
	for col in range(40):
		crtRow.append('.')
	crtScreen.append(crtRow)
print('blank screen')
for col in range(6):
	for row in range(40):
		print(crtScreen[col][row],end='')
	print('')

pixelOn = False
for row in range(6):
	# print('screenXVals row',row,end=' ')
	for col in range(40):
		currentXRegVal = screenXVals[row][col]
		print('x y',row,col,'currentXRegVal',currentXRegVal,end = ' ')
		if col-1 <= currentXRegVal+1 <= col+1:
			crtScreen[row][col] = '#'
			print('#')
		else:
			print('.')
	# assert False,'stop'
	# print(crtScreen[row])
print
for row in range(6):
	for col in range(40):
		# print(crtScreen[row][col],end='')
		print(crtScreen[row][col],crtScreen[row][col],end='')
	print('')

""" 
D10P1

"""

fileName = 'input.txt'
# fileName = 'input1.txt'
# fileName = 'input2.txt'

instr = []
inList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		instr.append(inLine.split(' '))

print('instr',instr)
clock = 0
traceBuffer = []
xReg = 1
step = 1
for line in instr:
	print('line',line)
	if line[0] == 'noop':
		execTime = 1
	elif line[0] == 'addx':
		execTime = 2
	for clkCPU in range(execTime):
		traceBuffer.append([xReg,step*xReg])
		step += 1
	if line[0] == 'addx':
		xReg += int(line[1])
	print('xReg',xReg)
print('traceBuffer',traceBuffer)
for cycle in range(len(traceBuffer)):
	print(cycle+1,traceBuffer[cycle])
interestingCycles = [20,60,100,140,180,220]
sum = 0
for cycle in interestingCycles:
	print(traceBuffer[cycle-1])
	sum += traceBuffer[cycle-1][1]
print('sum',sum)


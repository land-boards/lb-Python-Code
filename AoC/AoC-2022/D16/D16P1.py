'''
D16P1.py


'''
import time

# At start
startTime = time.time()

def readInFile(fileName):
	inList=[]
	with open(fileName, 'r') as filehandle:  
		for line in filehandle:
			inLine = line.strip('\n')
			inList.append(inLine)

# fileName = 'input2.txt'
fileName = 'input.txt'
# fileName = 'input1.txt'
print(inList)

inList = readInFile(fileName)

# At end
print('time',time.time()-startTime)

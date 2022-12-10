""" 
D11P1

"""

fileName = 'input.txt'
# fileName = 'input1.txt'
# fileName = 'input2.txt'

inList=[]
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')

""" 
D06P1

"""

def compare4(c1,c2,c3,c4):
	if c1 == c2:
		return True
	if c1 == c3:
		return True
	if c1 == c4:
		return True
	if c2 == c3:
		return True
	if c2 == c4:
		return True
	if c3 == c4:
		return True
	return False

fileName = 'input.txt'
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		print(inLine)
gotResult = False
for offset in range(len(inLine)-3):
	c1 = inLine[offset]
	c2 = inLine[offset+1]
	c3 = inLine[offset+2]
	c4 = inLine[offset+3]
	if not compare4(c1,c2,c3,c4):
		if not gotResult:
			print(offset+4)
			gotResult = True
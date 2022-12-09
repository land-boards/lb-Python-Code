""" 
D07P1
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

1444864 is too high
"""

def addToCWD(dir):
	global cwd
	# print('addToCWD: ',end='')
	cwd += dir + '/'
	# print('*CWD=',cwd)
	
def goUpDir():
	global cwd
	# print('goUpDir: ',end='')
	endOff = len(cwd) - 2
	while cwd[endOff] != '/':
		endOff -= 1
	cwd = cwd[0:endOff] + '/'

cwd = ''

fileName = 'input.txt'
# fileName = 'input1.txt'

currDirSize = 0
dirDirectory = []
solvedPath = True
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip('\n')
		if inLine[0:4] == '$ cd':
			if cwd != '':
				dirDirectory.append([cwd,currDirSize,solvedPath])
			currDirSize = 0
			if inLine[2:4] == 'cd':
				if inLine[5:7] == '..':
					goUpDir()
				else:
					addToCWD(inLine[5:])
		elif inLine[0:2] == 'ls':
			currDirSize = 0
			solvedPath = True
		elif inLine[0:3] == 'dir':
			solvedPath = False
		elif '0' <= inLine[0] <= '9':
			fileLine = inLine.split()
			fileSize = int(fileLine[0])
			fileName = fileLine[1]
			currDirSize += fileSize
dirDirectory.append([cwd,currDirSize,True])
# print('Finished reading file')

newPath_Sizes = []
for testLine in dirDirectory:
	sum = 0
	for t2Line in dirDirectory:
		if testLine[0] in t2Line[0]:
			sum += t2Line[1]
	if [testLine[0],sum] not in newPath_Sizes:
		newPath_Sizes.append([testLine[0],sum])
# print('newPath_Sizes')
# print(newPath_Sizes)
hddSize = 70000000
usedSpace = newPath_Sizes[0][1]
unusedSpace = hddSize - usedSpace
print("hddSize",hddSize)
print("usedSpace",usedSpace)
print("unusedSpace",unusedSpace)
neededSpace = 30000000 - unusedSpace
print('neededSpace',neededSpace)
potentialFoldersList = []
smallest = 1000000000
for folder in newPath_Sizes:
	if (folder[1] > neededSpace) and (folder[1] < smallest):
		print('smallest so far',folder)
		smallest = folder[1]

	
import sys

def readFileToListOfStrings(fileName):
    """
    """
    inList = []
    with open(fileName, 'r') as filehandle:  
        for line in filehandle:
            inList.append(line.rstrip())
    return inList

inList = readFileToListOfStrings('D01_input-1.txt')
print(inList)
for row in inList:
    print(row)

position = 50
count = 0

# readFileToListOfStrings("D01_input-1.txt")

for line in inList:
    line = line.strip()
    if not line:
        continue
    direction = line[0]
    distance = int(line[1:])
    if direction == 'R':
        position = (position + distance) % 100
    elif direction == 'L':
        position = (position - distance) % 100
    if position == 0:
        count += 1

print(count)


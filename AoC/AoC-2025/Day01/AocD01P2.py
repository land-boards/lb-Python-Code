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
# print(inList)
# for row in inList:
    # print(row)

position = 50
total_zeros = 0

# readFileToListOfStrings("D01_input-1.txt")

for line in inList:
    line = line.strip()
    if not line:
        continue
    
    direction = line[0]
    try:
        steps = int(line[1:])
    except ValueError:
        continue  # skip invalid lines
    
    if direction == 'R':
        step = 1
    elif direction == 'L':
        step = -1
    else:
        continue  # invalid direction
    
    # Simulate each single click
    for _ in range(steps):
        position = (position + step) % 100
        if position == 0:
            total_zeros += 1

# The final position is already counted if it landed on 0 during the last step
print(total_zeros)



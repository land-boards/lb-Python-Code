""" 
D02P1
readFileOfStringsToListOfLists
Rock A defeats Scissors Z
Scissors C defeats Paper Y
Paper B defeats Rock X
A > X
B > Y
C > Z

A X = 1
A Y = 

"""

# Rock A defeats Scissors Z
# Scissors C defeats Paper Y
# Paper B defeats Rock X
# Win = 6
# Tie = 3
# Loss = 0
def calcScore(p1, p2):
	score = 0
	if p1=='A':			# p1 = rock
		if p2=='X':		# rock = rock tie
			score = 3 + 1
		elif p2=='Y':	# win paper vs rock
			score = 6 + 2
		elif p2=='Z':	# loss scissors vs rock
			score = 0 + 3
	if p1=='B':			# p1 = paper
		if p2=='X':		# loss paper vs rock
			score = 0 + 1
		elif p2=='Y':	# tie
			score = 3 + 2
		elif p2=='Z':	# win scissors vs paper
			score = 6 + 3
	if p1=='C':			# p1 = scissors
		if p2=='X':		# win rock vs scissors
			score = 6 + 1
		elif p2=='Y':	# loss paper vs scissor
			score = 0 + 2
		elif p2=='Z':		# tie
			score = 3 + 3
	return score

fileName="input.txt"
score = 0
total = 0
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		print(inLine,end=' ')
		p1 = inLine[0]
		p2 = inLine[2]
		score = calcScore(p1, p2)
		print(score)
		total += score
print('total',total)

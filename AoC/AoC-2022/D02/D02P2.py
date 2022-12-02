""" 
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
	print('players',p1,p2,end=' score ')
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

# Rock A defeats Scissors Z
# Scissors C defeats Paper Y
# Paper B defeats Rock X
def findP2(p1, wld):
	if wld == 'X':	# lose
		print("p2 loses")
		if p1 == 'A':	# rock defeats scisors
			p2 = 'Z'
		elif p1 == 'B':	# paper defears rock
			p2 = 'X'
		elif p1 == 'C':
			p2 = 'Y'
	elif wld == 'Y':	# draw
		print("p2 draws")
		if p1 == 'A':	# rock = rock
			p2 = 'X'
		elif p1 == 'B':	# paper = paper
			p2 = 'Y'
		elif p1 == 'C':	# scissors = scissors
			p2 = 'Z'
	elif wld == 'Z':	# win
		print("p2 wins")
		if p1 == 'A':	# rock loses to paper
			p2 = 'Y'
		elif p1 == 'B':	# paper loses to scissors
			p2 = 'Z'
		elif p1 == 'C':	# sicssors lose to rock
			p2 = 'X'
	return p2


fileName="input.txt"
score = 0
total = 0
with open(fileName, 'r') as filehandle:  
	for line in filehandle:
		inLine = line.strip()
		print(inLine,end=' ')
		p1 = inLine[0]
		wld = inLine[2]
		p2 = findP2(p1, wld)
		score = calcScore(p1, p2)
		print(score)
		total += score
print('total',total)

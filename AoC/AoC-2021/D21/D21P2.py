# D21P2.py
# 2021 Advent of Code
# Day 21
# Part 2

def rollDice(diceVal):
	diceVal += 1
	if diceVal > 3:
		diceVal = 1
	return diceVal

def rollDice3Times(diceLastRollValue):
	nextDiceRolls =[]
	diceLastRollValue = rollDice(diceLastRollValue)
	nextDiceRolls.append(diceLastRollValue)
	diceLastRollValue = rollDice(diceLastRollValue)
	nextDiceRolls.append(diceLastRollValue)
	diceLastRollValue = rollDice(diceLastRollValue)
	nextDiceRolls.append(diceLastRollValue)
	# print("nextDiceRolls",nextDiceRolls)
	return nextDiceRolls

def movePlayer(playerPosition,moves):
	# print("movePlayer playerPosition:",playerPosition)
	newPlayerPosition = playerPosition + sum(moves)
	while newPlayerPosition > 10:
		newPlayerPosition -= 10
	return newPlayerPosition

Player1CurrentPosition = 4
Player2CurrentPosition = 8
diceLastRollValue = 0
Player1Score = 0
Player2Score = 0
rollCount = 0
lowScore = 0
endScore = 21

while (Player1Score < endScore) and (Player2Score < endScore):
	# Run Player 1
	# print("\nPlayer 1",end = '')
	nextDiceRolls = rollDice3Times(diceLastRollValue)
	diceLastRollValue = nextDiceRolls[-1]
	# print(" rolls",nextDiceRolls,end=' ')
	Player1CurrentPosition = movePlayer(Player1CurrentPosition,nextDiceRolls)
	# print("and moves to space",Player1CurrentPosition,end='')
	Player1Score += Player1CurrentPosition
	# print(" for a total score",Player1Score)
	rollCount += 3
	if Player1Score < endScore:
		lowScore = Player1Score

	if Player1Score < endScore:
		# Run Player 2
		# print("Player 2",end = '')
		nextDiceRolls = rollDice3Times(diceLastRollValue)
		diceLastRollValue = nextDiceRolls[-1]
		# print(" rolls",nextDiceRolls,end=' ')
		Player2CurrentPosition = movePlayer(Player2CurrentPosition,nextDiceRolls)
		# print("and moves to space",Player2CurrentPosition,end='')
		Player2Score += Player2CurrentPosition
		# print(" for a total score",Player2Score)
		rollCount += 3
		if Player2Score < 1000:
			lowScore = Player2Score

print("lowScore",lowScore)
print("rollCount",rollCount)
print("product",lowScore*rollCount)

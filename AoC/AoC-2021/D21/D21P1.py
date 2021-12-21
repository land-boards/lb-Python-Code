Player1CurrentPosition = 4
Player2CurrentPosition = 8
diceLastRollValue = 0
Player1Score = 0
Player2Score = 0

def rollDice(diceVal):
	diceVal += 1
	if diceVal > 100:
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
	print("nextDiceRolls",nextDiceRolls)
	return nextDiceRolls

def movePlayer(playerPosition,moves):
	print("movePlayer playerPosition:",playerPosition)
	newPlayerPosition = playerPosition + sum(moves)
	if newPlayerPosition > 10:
		newPlayerPosition = (newPlayerPosition % 10) + 1
	print("movePlayer : newPlayerPosition",newPlayerPosition)
	return newPlayerPosition

while (Player1Score < 100) and (Player2Score < 100):
	# Run Player 1
	print("\nPlayer 1 - ",end = '')
	nextDiceRolls = rollDice3Times(diceLastRollValue)
	diceLastRollValue = nextDiceRolls[-1]
	print("Player 1 - diceLastRollValue",diceLastRollValue)
	Player1CurrentPosition = movePlayer(Player1CurrentPosition,nextDiceRolls)
	print("Player 1 - Current Position",Player1CurrentPosition)
	Player1Score += Player1CurrentPosition
	print("Player 1 - Score",Player1Score)

	# Run Player 2
	print("\nPlayer 2 -",end = '')
	nextDiceRolls = rollDice3Times(diceLastRollValue)
	diceLastRollValue = nextDiceRolls[-1]
	print("Player 2 - diceLastRollValue",diceLastRollValue)
	Player2CurrentPosition = movePlayer(Player2CurrentPosition,nextDiceRolls)
	print("Player 2 - Current Position",Player2CurrentPosition)
	Player2Score += Player2CurrentPosition
	print("Player 2 - Score",Player2Score)
	
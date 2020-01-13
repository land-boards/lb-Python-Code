def move(f,t):
	print("Move disc from {} to {}!".format(f,t))

def hanoi(numDiscs,fromPos,helperPos,toPos):
	if numDiscs == 0:
		pass
	else:
		hanoi(numDiscs-1,fromPos,toPos,helperPos)
		move(fromPos,toPos)
		hanoi(numDiscs-1,helperPos,fromPos,toPos)

hanoi(4,"A","B","C")
